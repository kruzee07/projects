import ee

# Authenticate and initialize Earth Engine
ee.Authenticate()
ee.Initialize(project='my-first-project')
print(ee.String('Hello from the Earth Engine servers!').getInfo())

# Define the center and buffer
center = ee.Geometry.Point([75.7, 31.4])
buffer = center.buffer(10000)  # Buffer of 10 km

# Calculate and print buffer area in square kilometers
buffer_area_sq_km = buffer.area().divide(1e6).getInfo()
print('Buffer Area (sq km):', buffer_area_sq_km)

# Function to get and print mean values
def get_mean_value(image_collection, band_name, start_date, end_date, buffer, scale=30):
    image_collection_filtered = image_collection \
        .select(band_name) \
        .filterDate(start_date, end_date) \
        .filterBounds(buffer)
    mean_value = image_collection_filtered.mean().reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=buffer,
        scale=scale
    ).get(band_name).getInfo()
    return mean_value

# 1. Air Quality (Sentinel-5P CH4)
air_quality_mean = get_mean_value(
    ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_CH4'),
    'CH4_column_volume_mixing_ratio_dry_air',
    '2019-01-01',
    '2019-12-31',
    buffer
)
print('Air Quality (CH4) Mean (ppbv):', air_quality_mean)

# 2. NO2 Concentration (Sentinel-5P)
no2_mean = get_mean_value(
    ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_NO2'),
    'tropospheric_NO2_column_number_density',
    '2019-01-01',
    '2019-12-31',
    buffer
)
print('NO2 Mean (mol/m²):', no2_mean)

# 3. Land Use (MODIS Land Cover)
land_cover_mode = ee.ImageCollection('MODIS/006/MCD12Q1') \
    .select('LC_Type1') \
    .filterDate('2019-01-01', '2019-12-31') \
    .filterBounds(buffer) \
    .mode() \
    .reduceRegion(
        reducer=ee.Reducer.mode(),
        geometry=buffer,
        scale=30
    ).get('LC_Type1').getInfo()
print('Land Cover Mode:', land_cover_mode)

# 4. Water Quality (Landsat 8 Surface Reflectance)
water_quality_median = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR') \
    .select(['B2', 'B3', 'B4']) \
    .filterDate('2019-01-01', '2019-12-31') \
    .filterBounds(buffer) \
    .median() \
    .reduceRegion(
        reducer=ee.Reducer.median(),
        geometry=buffer,
        scale=30
    ).getInfo()
print('Water Quality Median B2 (Reflectance):', water_quality_median.get('B2'))
print('Water Quality Median B3 (Reflectance):', water_quality_median.get('B3'))
print('Water Quality Median B4 (Reflectance):', water_quality_median.get('B4'))

# 5. Air Temperature (MODIS Surface Temperature Day)
air_temp_mean = get_mean_value(
    ee.ImageCollection('MODIS/006/MOD11A1'),
    'LST_Day_1km',
    '2019-01-01',
    '2019-12-31',
    buffer
)
print('Air Temperature (Day) Mean (K*100):', air_temp_mean)

# 6. Surface Temperature (MODIS Surface Temperature Night)
surface_temp_mean = get_mean_value(
    ee.ImageCollection('MODIS/006/MOD11A1'),
    'LST_Night_1km',
    '2019-01-01',
    '2019-12-31',
    buffer
)
print('Surface Temperature (Night) Mean (K*100):', surface_temp_mean)

# 7. NDVI (MODIS)
ndvi_mean = get_mean_value(
    ee.ImageCollection('MODIS/006/MOD13A1'),
    'NDVI',
    '2019-01-01',
    '2019-12-31',
    buffer
)
print('NDVI Mean:', ndvi_mean)

# 8. Precipitation (CHIRPS)
precipitation_sum = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY') \
    .select('precipitation') \
    .filterDate('2019-01-01', '2019-12-31') \
    .filterBounds(buffer) \
    .sum() \
    .reduceRegion(
        reducer=ee.Reducer.sum(),
        geometry=buffer,
        scale=30
    ).get('precipitation').getInfo()
print('Total Precipitation (mm):', precipitation_sum)
