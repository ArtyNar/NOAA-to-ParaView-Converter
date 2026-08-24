import sys, os 

sys.path.append(r"C:\Program Files\ParaView 5.13.2\bin\Lib\site-packages") 
os.add_dll_directory(r"C:\Program Files\ParaView 5.13.2\bin") 

from paraview.simple import * 
import tifffile
import numpy as np
import vtk
from vtk.util import numpy_support

# Read the file directly as a numpy array
elevation = tifffile.imread('./data/exportImage.tiff').astype(np.float64)
print("raw:", elevation.shape, elevation.min(), elevation.max())

nodata_mask = (elevation < -1e30) | (elevation > 1e30) # Find invalid values 
elevation[nodata_mask] = np.nan # Replace invalid values with NaN
print("cleaned:", elevation.shape, np.nanmin(elevation), np.nanmax(elevation))

# ParaView portion
fill_value = np.nanmin(elevation)
elevation_filled = np.nan_to_num(elevation, nan=fill_value)

ny, nx = elevation_filled.shape

# --- Build vtkImageData directly (no text embedding, no NaN issue) ---
image_data = vtk.vtkImageData()
image_data.SetDimensions(nx, ny, 1)
image_data.SetSpacing(1, 1, 1)
image_data.SetOrigin(0, 0, 0)

values = elevation_filled.ravel(order='C')  # x-fastest, matches SetDimensions(nx, ny, 1)
vtk_array = numpy_support.numpy_to_vtk(values, deep=True)
vtk_array.SetName('elevation')
image_data.GetPointData().SetScalars(vtk_array)

# --- Feed it into the ParaView pipeline ---
producer = TrivialProducer()
producer.GetClientSideObject().SetOutput(image_data)
producer.UpdatePipeline()

# --- Warp into 3D relief ---
warp = WarpByScalar(Input=producer)
warp.Scalars = ['POINTS', 'elevation']
warp.ScaleFactor = 0.05

display = Show(warp)
ColorBy(display, ('POINTS', 'elevation'))
display.SetScalarBarVisibility(GetActiveView(), True)
display.RescaleTransferFunctionToDataRange(True)

ResetCamera()
Render()
SaveScreenshot(r'.\images\bathymetry.png')
Interact()

# from vtkmodules.vtkIOXML import vtkXMLImageDataWriter

# writer = vtkXMLImageDataWriter()
# writer.SetFileName('bathymetry.vti')
# writer.SetInputConnection(flow.GetClientSideObject().GetOutputPort())  # or via servermanager
# writer.Write()