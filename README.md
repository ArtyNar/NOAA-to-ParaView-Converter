# NOAA to ParaView Converter

Convert NOAA bathymetric elevation exports (GeoTIFF) into 3D relief visualizations.

Two independent converters are provided, both following the same pipeline: read an elevation raster, mask out NODATA values, build a structured grid from the elevation array, warp it into a 3D surface by elevation, and render it colored by depth/height.

- **[geotiff_to_vtk.py](geotiff_to_vtk.py)** — uses ParaView's Python API (`paraview.simple`), driving an actual ParaView render/export.
- **[geotiff_pyvista.py](geotiff_pyvista.py)** — uses [PyVista](https://pyvista.org/) instead, so it runs in a plain Python environment with no ParaView installation required.

![Bathymetry render](images/bathymetry.png)

> [!NOTE]
> Area of interest on the screenshot:
>
> West -125.33030416613947, South 45.568749228801046, East -124.61069967395203, North 45.860247378725035

## Requirements

- Python 3.10
- Python packages in [requirements.txt](requirements.txt): `numpy`, `tifffile`, `imagecodecs`, `pyvista`, `rasterio`, `typing_extensions`
- For [geotiff_to_vtk.py](geotiff_to_vtk.py) and the ParaView smoke test only: Windows with [ParaView](https://www.paraview.org/download/) installed (developed against 5.13.2), matching the venv's Python version

## Setup

1. Create a virtual environment:

   ```powershell
   py -3.10 -m venv pv-env
   ```

2. Activate it:

   ```powershell
   pv-env\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

4. If you're using [geotiff_to_vtk.py](geotiff_to_vtk.py) or the ParaView smoke test, point them at your local ParaView install. They start with:

   ```python
   sys.path.insert(0, r"C:\Program Files\ParaView 5.13.2\bin\Lib\site-packages")
   os.add_dll_directory(r"C:\Program Files\ParaView 5.13.2\bin")
   ```

   Update these paths if ParaView is installed elsewhere or at a different version.

## Usage

- **[geotiff_to_vtk.py](geotiff_to_vtk.py)** — reads `data/exportImage.tiff` with `tifffile`, cleans NODATA values, builds a `vtkImageData` grid, warps it into a 3D relief via ParaView's `WarpByScalar`, colors it by elevation, saves the render to `images/bathymetry.png`, and writes the grid to `output/bathymetry.vti`.

  ```powershell
  python geotiff_to_vtk.py
  ```

  Calls `Interact()` at the end, which opens an interactive ParaView render window — close it (or press `q`) to end the script.

- **[geotiff_pyvista.py](geotiff_pyvista.py)** — reads `data/exportImage.tiff` with `rasterio`, cleans NODATA values, builds a PyVista `ImageData` grid, warps it into a 3D relief, and opens an interactive PyVista render window colored by elevation, saving a screenshot to `bathymetry.png`.

  ```powershell
  python geotiff_pyvista.py
  ```

- **[tests/test_paraView.py](tests/test_paraView.py)** — minimal smoke test. Renders a cone in ParaView to confirm the venv can import `paraview.simple` and the DLL path is set up correctly, saving a screenshot to `images/screenshot.png`.

  ```powershell
  python tests/test_paraView.py
  ```

## Data

`data/exportImage.tiff` is expected to be a single-band elevation GeoTIFF exported from a NOAA bathymetry source (e.g. the [NOAA NCEI Bathymetric Data Viewer](https://www.ncei.noaa.gov/maps/bathymetry/)), with invalid/NODATA cells encoded as extreme sentinel values (for [geotiff_to_vtk.py](geotiff_to_vtk.py)) or via the raster's `nodata` metadata (for [geotiff_pyvista.py](geotiff_pyvista.py)). Swap in your own export at that path, or edit the path in the scripts.

## Project structure

```
data/exportImage.tiff      NOAA elevation GeoTIFF input
images/bathymetry.png      Rendered output from geotiff_to_vtk.py
images/screenshot.png      Rendered output from tests/test_paraView.py
output/bathymetry.vti      VTK image data export from geotiff_to_vtk.py
geotiff_to_vtk.py          TIFF -> VTK -> 3D relief converter (ParaView)
geotiff_pyvista.py         TIFF -> VTK -> 3D relief converter (PyVista)
tests/test_paraView.py     ParaView smoke test
requirements.txt           Python dependencies
```
