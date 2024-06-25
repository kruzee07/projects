import ee
ee.Authenticate()
ee.Initialize(project='my-first-project')
print(ee.String('Hello from the Earth Engine servers!').getInfo())