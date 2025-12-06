This folder contains Excel files for analysis.

# Test 3: Geospatial Farm Polygon Analysis

## Project Overview
Analysis of cocoa farm polygons from Kobo Collect to verify geolocation accuracy, identify overlaps, and detect farms within forest areas.

## Dataset Information
- **Source**: Kobo Collect geospatial survey
- **Data Type**: Farm polygon coordinates (likely GeoJSON/Shapefile/CSV)
- **Contains**: Farmer names, polygon IDs, coordinates, area measurements

## Folder Structure
```
test-3-geospatial/
├── raw/                 # Original Kobo Collect data
├── cleaned/             # Processed and validated polygons
├── scripts/             # Geospatial analysis code
├── results/             # Maps, tables, reports
└── conditions/          # Analysis requirements
    └── requirements.md
```

## Analysis Requirements

### 1. Polygon Verification & Overlap Detection
Identify and categorize overlapping polygons:
- **< 10% overlap**: Minor boundary issues
- **11–25% overlap**: Moderate overlap requiring review
- **≥ 50% overlap**: Significant overlap requiring action

### 2. Overlap Treatment Strategy
Develop and apply methodology to handle overlaps:
- Prioritization rules (e.g., first registered, larger farm)
- Boundary adjustment methods
- Conflict resolution process
- Data quality flags

### 3. Forest Area Identification
Identify farm polygons within forest areas:
- Integrate forest-cover layer (e.g., Global Forest Watch, Hansen)
- Calculate intersection percentage
- Flag high-risk polygons
- Support deforestation monitoring

### 4. Tabular Output
Generate comprehensive table with:
- Farmer Name
- Polygon ID
- Polygon Area (hectares)
- Overlap Status (Yes/No, %)
- Forest Presence (Yes/No, %)
- Notes/Flags

### 5. Map Visualization
Create three maps:

**Map 1: All Farm Polygons**
- All polygons clearly displayed
- Labeled by Polygon ID
- Color-coded by status
- Legend with farmer names

**Map 2: Overlap Analysis**
- Highlight overlapping areas
- Color-coded by overlap percentage
- Visual indicators of conflict zones
- Clear boundary delineation

**Map 3: Forest Area Analysis**
- Forest layer overlay
- Polygons in forest areas highlighted
- Differentiate by forest type/protected status
- Risk categorization

## Key Questions to Answer
1. How many polygons have overlaps?
2. What is the total area affected by overlaps?
3. How many farms are located in forest areas?
4. What percentage of farm area is in protected forests?
5. Which farmers need boundary verification?

## Technical Approach

### Geospatial Tools
**Python Stack**:
- GeoPandas - spatial data manipulation
- Shapely - geometric operations
- Matplotlib/Folium - mapping
- Rasterio - raster data handling

**QGIS**:
- Open-source GIS software
- Visual analysis and quality control
- Map production

**R Stack**:
- sf package - spatial features
- leaflet - interactive maps
- ggplot2 - static maps

### Methodology
```python
# Overlap Detection
1. Load all polygons
2. Create spatial index
3. Check intersection for each pair
4. Calculate overlap percentage
5. Categorize and flag

# Forest Analysis
1. Load forest layer (GeoJSON/Shapefile)
2. Perform spatial join
3. Calculate intersection area
4. Flag polygons in forest
5. Generate risk scores
```

## Data Quality Checks
- [ ] Validate coordinate system (WGS84/UTM)
- [ ] Check for invalid geometries
- [ ] Verify polygon closure
- [ ] Remove duplicate coordinates
- [ ] Validate area calculations
- [ ] Check for self-intersections

## Deliverables
- ⬜ Cleaned polygon dataset (GeoJSON/Shapefile)
- ⬜ Overlap analysis table (CSV/Excel)
- ⬜ Forest intersection table (CSV/Excel)
- ⬜ Three visualization maps (PNG/PDF)
- ⬜ Methodology documentation
- ⬜ Data quality report
- ⬜ Recommendations for field teams

## Output Formats
- **Tables**: CSV, Excel
- **Maps**: PNG, PDF, Interactive HTML
- **Spatial Data**: GeoJSON, Shapefile
- **Reports**: PDF, Word

## Data Sources for Forest Layer
- [Global Forest Watch](https://www.globalforestwatch.org/)
- [Hansen Global Forest Change](https://glad.earthengine.app/view/global-forest-change)
- National forest cadastre databases
- Protected area boundaries (WDPA)

## Performance Metrics
- **Overlap Rate**: % of polygons with overlaps
- **Forest Encroachment**: % of area in forest
- **Data Quality Score**: Based on validation checks
- **Resolution Time**: Expected time to resolve conflicts

## Tools & Technologies
- **GIS Software**: QGIS, ArcGIS
- **Programming**: Python (GeoPandas), R (sf)
- **Visualization**: Folium, Leaflet, Mapbox
- **Data Format**: GeoJSON, Shapefile, KML

## Next Steps
1. Load and validate raw data
2. Set up geospatial environment
3. Run overlap detection algorithm
4. Integrate forest layer
5. Generate outputs and maps
6. Document findings and recommendations

## References
- See `conditions/requirements.md` for detailed specifications
- Kobo Collect documentation
- Geospatial analysis best practices
