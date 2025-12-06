# Test 3: Geospatial Analysis - Conditions

## Background
Geospatial dataset from Kobo Collect containing cocoa farm polygons.

## Dataset Information
- **Source**: Kobo Collect
- **Data Type**: Farm polygon coordinates
- **Format**: Geospatial data (likely GeoJSON/Shapefile)

## Analysis Requirements

### 1. Geolocation and Polygon Verification
Identify polygons that overlap with each other.

**Breakdown Required**:
- < 10% overlap
- 11–25% overlap
- ≥ 50% overlap

### 2. Treatment of Overlapping Polygons
**Tasks**:
- Explain approach to handle polygon overlaps
- Apply chosen methodology
- Document prioritization rules or cleaning methods

**Considerations**:
- Which polygon to keep?
- How to handle partial overlaps?
- Data quality implications

### 3. Forest Area Identification
**Tasks**:
- Identify polygons located within forest areas
- Integrate with forest-cover or land-use layer

**Data Sources** (examples):
- Global Forest Watch
- Hansen Global Forest Change
- Local forest cadastre data

### 4. Tabular Output
**Required Columns**:
- Farmer Name
- Polygon ID
- Polygon Area (hectares)
- Overlap Status (Yes/No, %)
- Forest Presence (Yes/No)
- Notes

**Example Format**:
```
| Farmer Name | Polygon ID | Area (ha) | Overlap % | In Forest |         Notes         |
|-------------|------------|-----------|-----------|-----------|-----------------------|
| John Doe    | POL_001    | 2.5       | 15%       | No        | Overlaps with POL_003 |
```

### 5. Map Visualization
**Required Maps**:

**Map 1: All Farm Polygons**
- All polygons clearly visible
- Labeled by Polygon ID
- Legend with farmer names

**Map 2: Overlap Highlights**
- Color-coded by overlap percentage
- Visual indication of overlapping areas
- Legend explaining categories

**Map 3: Forest Area Analysis**
- Polygons within forest areas highlighted
- Forest layer overlay
- Clear boundary delineation

## Tools Suggested
- Python: GeoPandas, Shapely, Matplotlib/Folium
- QGIS: Open-source GIS software
- R: sf, leaflet packages
- ArcGIS (if available)

## Deliverables
1. Cleaned polygon dataset
2. Overlap analysis table
3. Forest intersection analysis
4. Three visualization maps
5. Methodology documentation
6. Recommendations for data quality improvement
