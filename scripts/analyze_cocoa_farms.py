"""
Cocoa Farm Geospatial Analysis Script
Analyzes Kobo Collect data for polygon overlaps and forest encroachment
Designed for GitHub Actions automation
"""

import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon, Point
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Patch
import numpy as np
import warnings
import os
import sys
from datetime import datetime
warnings.filterwarnings('ignore')

# =============================================================================
# CONFIGURATION - AUTO-DETECTS PATHS FOR GITHUB ACTIONS
# =============================================================================

# Check if running in GitHub Actions
IS_GITHUB_ACTIONS = os.getenv('GITHUB_ACTIONS') == 'true'

if IS_GITHUB_ACTIONS:
    # GitHub Actions paths
    BASE_PATH = 'excel-data/test-3-geospatial'
    RAW_PATH = os.path.join(BASE_PATH, 'raw')
    RESULTS_PATH = os.path.join(BASE_PATH, 'results')
    CLEANED_PATH = os.path.join(BASE_PATH, 'cleaned')
    
    # Get forest analysis setting from environment
    HAS_FOREST_DATA = os.getenv('FOREST_ANALYSIS', 'false').lower() == 'true'
    
    # Find the Excel file in raw folder
    raw_files = [f for f in os.listdir(RAW_PATH) if f.endswith(('.xlsx', '.xls'))]
    if not raw_files:
        print("❌ Error: No Excel file found in raw folder!")
        sys.exit(1)
    INPUT_FILE = os.path.join(RAW_PATH, raw_files[0])
    
    # Forest layer path (if exists)
    FOREST_LAYER = os.path.join(RAW_PATH, 'forest_cover.shp')
    if not os.path.exists(FOREST_LAYER):
        HAS_FOREST_DATA = False
else:
    # Local development paths
    INPUT_FILE = 'your_kobo_data.xlsx'
    RESULTS_PATH = 'results/'
    CLEANED_PATH = 'cleaned/'
    FOREST_LAYER = 'forest_cover.shp'
    HAS_FOREST_DATA = False

# Create output directories
os.makedirs(RESULTS_PATH, exist_ok=True)
os.makedirs(CLEANED_PATH, exist_ok=True)

# =============================================================================
# HELPER FUNCTION: PARSE GPS TRACE TO POLYGON
# =============================================================================

def parse_gps_trace_to_polygon(trace_string):
    """
    Parse GPS trace string to Shapely Polygon
    Format: "lat lon elevation accuracy;lat lon elevation accuracy;..."
    Example: "3.049306 98.242285 540.5 7.85;3.0491804 98.2420313 538.6 3.936;..."
    """
    try:
        if pd.isna(trace_string) or str(trace_string).strip() == '':
            return None
        
        # Split by semicolon to get individual points
        points = str(trace_string).split(';')
        
        # Parse each point (format: lat lon elevation accuracy)
        coordinates = []
        for point in points:
            parts = point.strip().split()
            if len(parts) >= 2:  # Need at least lat and lon
                lat = float(parts[0])
                lon = float(parts[1])
                # Note: Shapely uses (lon, lat) order, not (lat, lon)
                coordinates.append((lon, lat))
        
        # Need at least 3 points to make a polygon
        if len(coordinates) < 3:
            return None
        
        # Close the polygon if not already closed
        if coordinates[0] != coordinates[-1]:
            coordinates.append(coordinates[0])
        
        # Create polygon
        return Polygon(coordinates)
    
    except Exception as e:
        print(f"   ⚠ Error parsing GPS trace: {str(e)[:100]}")
        return None

# =============================================================================
# STEP 1: LOAD AND PREPARE DATA
# =============================================================================

print("="*70)
print("COCOA FARM GEOSPATIAL ANALYSIS")
print("="*70)
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Running in: {'GitHub Actions' if IS_GITHUB_ACTIONS else 'Local'}")
print("="*70)

print("\n[1/7] Loading data...")
print(f"   • Input file: {INPUT_FILE}")

# Load the Excel file
df = pd.read_excel(INPUT_FILE)

print(f"   ✓ Loaded {len(df)} records")

# Select essential columns
essential_cols = {
    'ID Petani': 'farmer_name',
    'ID Kebun': 'polygon_id',
    'Polygon Area': 'gps_trace',  # This contains the GPS trace!
    'Luas Lahan Kebun Kakao': 'area_ha',  # Actual area value
    '_Lokasi Kebun_latitude': 'latitude',
    '_Lokasi Kebun_longitude': 'longitude',
    '_Lokasi Kebun_precision': 'gps_precision'
}

# Check which columns exist
available_cols = {k: v for k, v in essential_cols.items() if k in df.columns}
missing_cols = set(essential_cols.keys()) - set(available_cols.keys())

if missing_cols:
    print(f"   ⚠ Warning: Missing columns: {missing_cols}")

# Rename columns
df_clean = df[list(available_cols.keys())].copy()
df_clean.columns = list(available_cols.values())

# Remove rows with null GPS traces
df_clean = df_clean[df_clean['gps_trace'].notna()].copy()
print(f"   ✓ {len(df_clean)} records with GPS trace data")

# =============================================================================
# STEP 2: CREATE GEODATAFRAME FROM GPS TRACES
# =============================================================================

print("\n[2/7] Converting GPS traces to polygons...")

# Parse GPS traces into polygons
geometries = []
invalid_indices = []

for idx, trace in enumerate(df_clean['gps_trace']):
    geom = parse_gps_trace_to_polygon(trace)
    if geom is not None:
        geometries.append(geom)
    else:
        print(f"   ⚠ Invalid GPS trace at row {idx}")
        invalid_indices.append(idx)
        geometries.append(None)

df_clean['geometry'] = geometries

# Remove invalid geometries
if invalid_indices:
    df_clean = df_clean[df_clean['geometry'].notna()].copy()
    print(f"   ✓ Removed {len(invalid_indices)} invalid GPS traces")

# Create GeoDataFrame
gdf = gpd.GeoDataFrame(df_clean, geometry='geometry', crs='EPSG:4326')

# Calculate actual areas in hectares
gdf['calculated_area_ha'] = gdf.geometry.to_crs('EPSG:3857').area / 10000

print(f"   ✓ Created GeoDataFrame with {len(gdf)} valid polygons")
print(f"   ✓ Total area: {gdf['calculated_area_ha'].sum():.2f} hectares")

# Compare with reported area if available
if 'area_ha' in gdf.columns and gdf['area_ha'].notna().any():
    print(f"   ℹ Reported area (from Kobo): {gdf['area_ha'].sum():.2f} hectares")
    print(f"   ℹ Calculated area (from GPS): {gdf['calculated_area_ha'].sum():.2f} hectares")

# =============================================================================
# STEP 3: DETECT OVERLAPS
# =============================================================================

print("\n[3/7] Detecting polygon overlaps...")

overlaps = []
overlap_count = 0

# Create spatial index for faster processing
gdf_sindex = gdf.sindex

for idx1, row1 in gdf.iterrows():
    # Find potential intersecting polygons using spatial index
    possible_matches_idx = list(gdf_sindex.intersection(row1.geometry.bounds))
    possible_matches = gdf.iloc[possible_matches_idx]
    
    for idx2, row2 in possible_matches.iterrows():
        if idx1 < idx2:  # Avoid duplicate pairs and self-comparison
            if row1.geometry.intersects(row2.geometry):
                try:
                    intersection = row1.geometry.intersection(row2.geometry)
                    overlap_area_ha = gpd.GeoSeries([intersection], crs='EPSG:4326').to_crs('EPSG:3857').area[0] / 10000
                    
                    # Calculate overlap percentage (relative to smaller polygon)
                    area1 = row1['calculated_area_ha']
                    area2 = row2['calculated_area_ha']
                    smaller_area = min(area1, area2)
                    
                    if smaller_area > 0:
                        overlap_pct = (overlap_area_ha / smaller_area) * 100
                    else:
                        overlap_pct = 0
                    
                    # Categorize overlap
                    if overlap_pct < 10:
                        category = "< 10%"
                    elif overlap_pct < 25:
                        category = "11-25%"
                    elif overlap_pct < 50:
                        category = "26-49%"
                    else:
                        category = "≥ 50%"
                    
                    overlaps.append({
                        'polygon_1_id': row1['polygon_id'],
                        'polygon_1_farmer': row1['farmer_name'],
                        'polygon_1_area_ha': area1,
                        'polygon_2_id': row2['polygon_id'],
                        'polygon_2_farmer': row2['farmer_name'],
                        'polygon_2_area_ha': area2,
                        'overlap_area_ha': overlap_area_ha,
                        'overlap_percentage': overlap_pct,
                        'category': category,
                        'intersection_geom': intersection
                    })
                    overlap_count += 1
                    
                except Exception as e:
                    print(f"   ⚠ Error calculating overlap between {row1['polygon_id']} and {row2['polygon_id']}: {str(e)}")

print(f"   ✓ Found {overlap_count} overlapping polygon pairs")

# Create overlap summary
if overlaps:
    overlap_df = pd.DataFrame(overlaps)
    print("\n   Overlap Breakdown:")
    for cat in ["< 10%", "11-25%", "26-49%", "≥ 50%"]:
        count = len(overlap_df[overlap_df['category'] == cat])
        if count > 0:
            print(f"      • {cat}: {count} cases")
else:
    overlap_df = pd.DataFrame()
    print("   ✓ No overlaps detected!")

# Add overlap flags to main dataframe
gdf['has_overlap'] = False
gdf['overlap_notes'] = 'No overlap'

if not overlap_df.empty:
    overlap_polygons = set(overlap_df['polygon_1_id'].tolist() + overlap_df['polygon_2_id'].tolist())
    gdf.loc[gdf['polygon_id'].isin(overlap_polygons), 'has_overlap'] = True
    
    # Add detailed overlap notes
    for idx, row in gdf.iterrows():
        if row['has_overlap']:
            overlaps_with = overlap_df[
                (overlap_df['polygon_1_id'] == row['polygon_id']) | 
                (overlap_df['polygon_2_id'] == row['polygon_id'])
            ]
            notes = []
            for _, ovl in overlaps_with.iterrows():
                other_id = ovl['polygon_2_id'] if ovl['polygon_1_id'] == row['polygon_id'] else ovl['polygon_1_id']
                notes.append(f"{ovl['category']} with {other_id}")
            gdf.at[idx, 'overlap_notes'] = "; ".join(notes)

# =============================================================================
# STEP 4: APPLY OVERLAP TREATMENT (CLEANING)
# =============================================================================

print("\n[4/7] Applying overlap treatment...")

# Create a cleaned version of the data
gdf_cleaned = gdf.copy()

# Treatment approach: Prioritize by GPS precision (lower is better)
# For overlapping polygons, keep the one with better GPS precision
if not overlap_df.empty and 'gps_precision' in gdf.columns:
    polygons_to_remove = set()
    
    for _, ovl in overlap_df.iterrows():
        if ovl['overlap_percentage'] >= 50:  # Only clean significant overlaps
            poly1_id = ovl['polygon_1_id']
            poly2_id = ovl['polygon_2_id']
            
            poly1_precision = gdf[gdf['polygon_id'] == poly1_id]['gps_precision'].values[0]
            poly2_precision = gdf[gdf['polygon_id'] == poly2_id]['gps_precision'].values[0]
            
            # Remove polygon with worse GPS precision (higher value)
            if pd.notna(poly1_precision) and pd.notna(poly2_precision):
                if poly1_precision > poly2_precision:
                    polygons_to_remove.add(poly1_id)
                    print(f"   • Removing {poly1_id} (worse GPS precision: {poly1_precision}m vs {poly2_precision}m)")
                else:
                    polygons_to_remove.add(poly2_id)
                    print(f"   • Removing {poly2_id} (worse GPS precision: {poly2_precision}m vs {poly1_precision}m)")
    
    # Apply removal
    if polygons_to_remove:
        gdf_cleaned = gdf_cleaned[~gdf_cleaned['polygon_id'].isin(polygons_to_remove)].copy()
        print(f"   ✓ Removed {len(polygons_to_remove)} polygons with significant overlaps")
    else:
        print("   ✓ No significant overlaps (≥50%) requiring removal")
else:
    print("   • No overlap treatment applied (no significant overlaps or GPS precision data)")

print(f"   • Original: {len(gdf)} polygons")
print(f"   • Cleaned: {len(gdf_cleaned)} polygons")

# =============================================================================
# STEP 5: FOREST AREA ANALYSIS (OPTIONAL)
# =============================================================================

print("\n[5/7] Analyzing forest areas...")

if HAS_FOREST_DATA:
    try:
        print(f"   • Loading forest layer: {FOREST_LAYER}")
        forest_gdf = gpd.read_file(FOREST_LAYER)
        
        # Ensure same CRS
        if forest_gdf.crs != gdf.crs:
            forest_gdf = forest_gdf.to_crs(gdf.crs)
        
        # Spatial join to find farms in forest
        for dataset, name in [(gdf, 'original'), (gdf_cleaned, 'cleaned')]:
            dataset['in_forest'] = False
            dataset['forest_overlap_pct'] = 0.0
            dataset['forest_notes'] = 'Not in forest area'
            
            for idx, farm in dataset.iterrows():
                forest_intersects = forest_gdf[forest_gdf.intersects(farm.geometry)]
                
                if len(forest_intersects) > 0:
                    forest_intersection = farm.geometry.intersection(forest_gdf.unary_union)
                    if not forest_intersection.is_empty:
                        forest_area_ha = gpd.GeoSeries([forest_intersection], crs='EPSG:4326').to_crs('EPSG:3857').area[0] / 10000
                        forest_pct = (forest_area_ha / farm['calculated_area_ha']) * 100
                        
                        dataset.at[idx, 'in_forest'] = True
                        dataset.at[idx, 'forest_overlap_pct'] = forest_pct
                        dataset.at[idx, 'forest_notes'] = f"{forest_pct:.1f}% in forest area ({forest_area_ha:.2f} ha)"
        
        forest_count = gdf['in_forest'].sum()
        forest_count_cleaned = gdf_cleaned['in_forest'].sum()
        print(f"   ✓ Found {forest_count} farms in forest areas (original)")
        print(f"   ✓ Found {forest_count_cleaned} farms in forest areas (cleaned)")
        
    except Exception as e:
        print(f"   ⚠ Error loading forest data: {str(e)}")
        print("   • Continuing without forest analysis")
        HAS_FOREST_DATA = False

if not HAS_FOREST_DATA:
    print("   • Skipping forest analysis (no forest layer provided)")
    for dataset in [gdf, gdf_cleaned]:
        dataset['in_forest'] = False
        dataset['forest_overlap_pct'] = 0.0
        dataset['forest_notes'] = 'Forest data not available'

# =============================================================================
# STEP 6: CREATE OUTPUT TABLES
# =============================================================================

print("\n[6/7] Creating output tables...")

# Main output table - ORIGINAL DATA
output_table = pd.DataFrame({
    'Farmer Name': gdf['farmer_name'],
    'Polygon ID': gdf['polygon_id'],
    'Area (ha)': gdf['calculated_area_ha'].round(2),
    'Overlap Status': gdf['overlap_notes'],
    'Forest Status': gdf['forest_notes']
})

# Cleaned data table
output_table_cleaned = pd.DataFrame({
    'Farmer Name': gdf_cleaned['farmer_name'],
    'Polygon ID': gdf_cleaned['polygon_id'],
    'Area (ha)': gdf_cleaned['calculated_area_ha'].round(2),
    'Forest Status': gdf_cleaned['forest_notes']
})

# Save RESULTS (analysis outputs)
results_file = os.path.join(RESULTS_PATH, f'cocoa_farm_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx')

with pd.ExcelWriter(results_file, engine='openpyxl') as writer:
    output_table.to_excel(writer, sheet_name='Farm Summary', index=False)
    
    if not overlap_df.empty:
        overlap_export = overlap_df[[
            'polygon_1_id', 'polygon_1_farmer', 'polygon_1_area_ha',
            'polygon_2_id', 'polygon_2_farmer', 'polygon_2_area_ha',
            'overlap_area_ha', 'overlap_percentage', 'category'
        ]].copy()
        overlap_export.columns = [
            'Polygon 1 ID', 'Farmer 1', 'Area 1 (ha)',
            'Polygon 2 ID', 'Farmer 2', 'Area 2 (ha)',
            'Overlap Area (ha)', 'Overlap %', 'Category'
        ]
        overlap_export = overlap_export.round(2)
        overlap_export.to_excel(writer, sheet_name='Overlaps Detail', index=False)
    
    # Summary statistics
    summary = pd.DataFrame({
        'Metric': [
            'Total Farms (Original)',
            'Total Farms (Cleaned)',
            'Total Area Original (ha)',
            'Total Area Cleaned (ha)',
            'Farms with Overlaps',
            'Overlap Cases',
            'Farms Removed',
            'Farms in Forest (Original)',
            'Farms in Forest (Cleaned)',
            'Average Farm Size (ha)'
        ],
        'Value': [
            len(gdf),
            len(gdf_cleaned),
            round(gdf['calculated_area_ha'].sum(), 2) if len(gdf) > 0 else 0,
            round(gdf_cleaned['calculated_area_ha'].sum(), 2) if len(gdf_cleaned) > 0 else 0,
            int(gdf['has_overlap'].sum()) if len(gdf) > 0 else 0,
            len(overlap_df),
            len(gdf) - len(gdf_cleaned),
            int(gdf['in_forest'].sum()) if len(gdf) > 0 else 0,
            int(gdf_cleaned['in_forest'].sum()) if len(gdf_cleaned) > 0 else 0,
            round(gdf['calculated_area_ha'].mean(), 2) if len(gdf) > 0 else 0
        ]
    })
    summary.to_excel(writer, sheet_name='Summary Statistics', index=False)

print(f"   ✓ Results saved to: {results_file}")

# Save CLEANED DATA (processed GeoDataFrame)
cleaned_file = os.path.join(CLEANED_PATH, f'cleaned_cocoa_farms_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx')

with pd.ExcelWriter(cleaned_file, engine='openpyxl') as writer:
    output_table_cleaned.to_excel(writer, sheet_name='Cleaned Farms', index=False)

# Also save as shapefile for GIS use
cleaned_shapefile = os.path.join(CLEANED_PATH, f'cleaned_cocoa_farms_{datetime.now().strftime("%Y%m%d_%H%M%S")}.shp')
gdf_cleaned_export = gdf_cleaned[['polygon_id', 'farmer_name', 'calculated_area_ha', 'geometry']].copy()
gdf_cleaned_export.to_file(cleaned_shapefile)

print(f"   ✓ Cleaned data saved to: {cleaned_file}")
print(f"   ✓ Shapefile saved to: {cleaned_shapefile}")

# =============================================================================
# STEP 7: CREATE MAPS
# =============================================================================

print("\n[7/7] Generating maps...")

# Map 1: All farms with IDs
fig, ax = plt.subplots(1, 1, figsize=(15, 12))

gdf.plot(ax=ax, facecolor='lightblue', edgecolor='darkblue', linewidth=1, alpha=0.6)

# Add polygon ID labels
for idx, row in gdf.iterrows():
    centroid = row.geometry.centroid
    ax.annotate(text=str(row['polygon_id']), 
                xy=(centroid.x, centroid.y),
                ha='center', fontsize=7, weight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))

ax.set_title('All Cocoa Farm Polygons', fontsize=16, weight='bold')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
plt.grid(True, alpha=0.3)
plt.tight_layout()
map1_path = os.path.join(RESULTS_PATH, 'map_1_all_farms.png')
plt.savefig(map1_path, dpi=300, bbox_inches='tight')
print(f"   ✓ Saved: map_1_all_farms.png")
plt.close()

# Map 2: Overlaps highlighted
if not overlap_df.empty:
    fig, ax = plt.subplots(1, 1, figsize=(15, 12))
    
    # Plot all farms in light color
    gdf[~gdf['has_overlap']].plot(ax=ax, facecolor='lightgray', edgecolor='gray', linewidth=0.5, alpha=0.5)
    
    # Plot overlapping farms in different colors
    gdf[gdf['has_overlap']].plot(ax=ax, facecolor='orange', edgecolor='red', linewidth=1.5, alpha=0.6)
    
    # Plot overlap intersections
    overlap_gdf = gpd.GeoDataFrame(overlap_df, geometry='intersection_geom', crs='EPSG:4326')
    overlap_gdf.plot(ax=ax, facecolor='red', alpha=0.8, edgecolor='darkred', linewidth=2)
    
    # Add labels for overlapping farms
    for idx, row in gdf[gdf['has_overlap']].iterrows():
        centroid = row.geometry.centroid
        ax.annotate(text=str(row['polygon_id']), 
                    xy=(centroid.x, centroid.y),
                    ha='center', fontsize=8, weight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.9))
    
    # Legend
    legend_elements = [
        Patch(facecolor='lightgray', edgecolor='gray', label='No Overlap'),
        Patch(facecolor='orange', edgecolor='red', label='Has Overlap'),
        Patch(facecolor='red', edgecolor='darkred', label='Overlap Area')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=10)
    
    ax.set_title('Farm Polygons - Overlaps Highlighted', fontsize=16, weight='bold')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    map2_path = os.path.join(RESULTS_PATH, 'map_2_overlaps.png')
    plt.savefig(map2_path, dpi=300, bbox_inches='tight')
    print(f"   ✓ Saved: map_2_overlaps.png")
    plt.close()

# Map 3: Forest areas (if available)
if HAS_FOREST_DATA and gdf['in_forest'].sum() > 0:
    fig, ax = plt.subplots(1, 1, figsize=(15, 12))
    
    # Plot forest layer first
    forest_gdf.plot(ax=ax, facecolor='darkgreen', alpha=0.3, edgecolor='green', linewidth=0.5)
    
    # Plot farms not in forest
    gdf[~gdf['in_forest']].plot(ax=ax, facecolor='lightblue', edgecolor='blue', linewidth=1, alpha=0.6)
    
    # Plot farms in forest
    gdf[gdf['in_forest']].plot(ax=ax, facecolor='red', edgecolor='darkred', linewidth=1.5, alpha=0.7)
    
    # Add labels for farms in forest
    for idx, row in gdf[gdf['in_forest']].iterrows():
        centroid = row.geometry.centroid
        ax.annotate(text=str(row['polygon_id']), 
                    xy=(centroid.x, centroid.y),
                    ha='center', fontsize=8, weight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.9))
    
    # Legend
    legend_elements = [
        Patch(facecolor='darkgreen', alpha=0.3, label='Forest Area'),
        Patch(facecolor='lightblue', edgecolor='blue', label='Farm (Not in Forest)'),
        Patch(facecolor='red', edgecolor='darkred', label='Farm (In Forest)')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=10)
    
    ax.set_title('Farm Polygons - Forest Areas Highlighted', fontsize=16, weight='bold')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    map3_path = os.path.join(RESULTS_PATH, 'map_3_forest_areas.png')
    plt.savefig(map3_path, dpi=300, bbox_inches='tight')
    print(f"   ✓ Saved: map_3_forest_areas.png")
    plt.close()

# Map 4: Cleaned data (before/after comparison)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

# Before (with overlaps)
gdf.plot(ax=ax1, facecolor='lightblue', edgecolor='darkblue', linewidth=1, alpha=0.6)
if not overlap_df.empty:
    gdf[gdf['has_overlap']].plot(ax=ax1, facecolor='orange', edgecolor='red', linewidth=1.5, alpha=0.7)
ax1.set_title(f'Before Cleaning ({len(gdf)} farms)', fontsize=14, weight='bold')
ax1.set_xlabel('Longitude')
ax1.set_ylabel('Latitude')
ax1.grid(True, alpha=0.3)

# After (cleaned)
gdf_cleaned.plot(ax=ax2, facecolor='lightgreen', edgecolor='darkgreen', linewidth=1, alpha=0.6)
ax2.set_title(f'After Cleaning ({len(gdf_cleaned)} farms)', fontsize=14, weight='bold')
ax2.set_xlabel('Longitude')
ax2.set_ylabel('Latitude')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
map4_path = os.path.join(RESULTS_PATH, 'map_4_before_after_cleaning.png')
plt.savefig(map4_path, dpi=300, bbox_inches='tight')
print(f"   ✓ Saved: map_4_before_after_cleaning.png")
plt.close()

# =============================================================================
# FINAL SUMMARY
# =============================================================================

print("\n" + "="*70)
print("ANALYSIS COMPLETE!")
print("="*70)
print(f"\n📊 SUMMARY:")
print(f"   • Total farms analyzed: {len(gdf)}")
print(f"   • Total farms after cleaning: {len(gdf_cleaned)}")
print(f"   • Farms removed: {len(gdf) - len(gdf_cleaned)}")
print(f"   • Total area (original): {gdf['calculated_area_ha'].sum():.2f} ha")
print(f"   • Total area (cleaned): {gdf_cleaned['calculated_area_ha'].sum():.2f} ha")
print(f"   • Farms with overlaps: {gdf['has_overlap'].sum()}")
print(f"   • Overlap cases: {len(overlap_df)}")
if HAS_FOREST_DATA:
    print(f"   • Farms in forest (original): {gdf['in_forest'].sum()}")
    print(f"   • Farms in forest (cleaned): {gdf_cleaned['in_forest'].sum()}")
print(f"\n📁 OUTPUT LOCATIONS:")
print(f"   • Results: {RESULTS_PATH}/")
print(f"   • Cleaned data: {CLEANED_PATH}/")
print("\n" + "="*70)
