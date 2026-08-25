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

ny, nx = elevation_filled.shape

# --- Build a structured grid directly from the array ---
grid = pv.ImageData(dimensions=(nx, ny, 1), spacing=(90, 90, 1), origin=(0, 0, 0))
grid.point_data['elevation'] = elevation_filled.ravel(order='C')

# --- Warp into 3D relief ---
warped = grid.warp_by_scalar('elevation', factor=10)

# --- Plot ---
plotter = pv.Plotter(off_screen=True)

plotter.add_mesh(
    warped,
    scalars='elevation',
    cmap='viridis',
    show_scalar_bar=True,
    scalar_bar_args={
        'fmt': '%.0f',
        'title': 'Elevation (m)',
    }
)
plotter.show(
    screenshot='./images/bathymetry_pyvista.png',
    auto_close=True,
)
# plotter.show()

