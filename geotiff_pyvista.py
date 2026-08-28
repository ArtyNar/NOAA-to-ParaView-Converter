import rasterio
import numpy as np
import pyvista as pv

with rasterio.open('./data/exportImage.tiff') as src:
    elevation = src.read(1).astype(np.float64)
    nodata = src.nodata
    transform = src.transform

print("transform:", transform)
print("x resolution:", transform.a)
print("y resolution:", transform.e)
print("origin x:", transform.c)
print("origin y:", transform.f)
print("raw:", elevation.shape, elevation.min(), elevation.max(), "nodata:", nodata)

if nodata is not None:
    elevation[elevation == nodata] = np.nan

fill_value = np.nanmin(elevation)
elevation_filled = np.nan_to_num(elevation, nan=fill_value)

ny, nx = elevation.shape
mesh = pv.ImageData(dimensions=(nx, ny, 1), spacing=(90, 90, 1), origin=(0, 0, 0))
mesh.point_data['Elevation'] = elevation_filled.ravel(order='C')

warped = mesh.warp_by_scalar('Elevation', factor=5) 
surf = warped.extract_surface().triangulate() # Necessary for decimate_pro
# surf = surf.decimate_pro(.5)  # Performance lever

surf.plot(
    cmap='gist_earth',
    scalar_bar_args={'fmt': '%.0f', 'title': 'Elevation (m)'}
)
