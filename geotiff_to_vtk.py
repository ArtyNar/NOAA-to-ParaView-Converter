import sys, os 
# Point to ParaView python libraries
sys.path.insert(0, r"C:\Program Files\ParaView 5.13.2\bin\Lib\site-packages")
os.add_dll_directory(r"C:\Program Files\ParaView 5.13.2\bin") 

from paraview.simple import * 
import tifffile
import numpy as np
import vtk
from vtk.util import numpy_support

# Read the file directly as a numpy array
elevation = tifffile.imread('./data/exportImage.tiff').astype(np.float64)
print("raw:", elevation.shape, elevation.min(), elevation.max())

# Data Processing  
nodata_mask = (elevation < -1e30) | (elevation > 1e30) # Find invalid values 
elevation[nodata_mask] = np.nan # Replace invalid values with NaN
print("cleaned:", elevation.shape, np.nanmin(elevation), np.nanmax(elevation))

# ParaView Visualization
# --- Step 1: Fill NaNs if any  
has_nan = np.any(np.isnan(elevation))
if has_nan:
    fill_value = np.nanmin(elevation)
    elevation = np.nan_to_num(elevation, nan=fill_value)

ny, nx = elevation.shape

# --- Build vtkImageData directly ---
image_data = vtk.vtkImageData()
image_data.SetDimensions(nx, ny, 1)
image_data.SetSpacing(90,90,1) # Comes from dataset cell size
image_data.SetOrigin(0, 0, 0)

values = elevation.ravel(order='C')  # Flattens row by row
vtk_array = numpy_support.numpy_to_vtk(values, deep=True)
vtk_array.SetName('Elevation')
image_data.GetPointData().SetScalars(vtk_array)

# --- Feed it into the ParaView pipeline ---
producer = TrivialProducer()
producer.GetClientSideObject().SetOutput(image_data)
producer.UpdatePipeline()

# --- Warp into 3D relief ---
warp = WarpByScalar(Input=producer)
warp.Scalars = ['POINTS', 'Elevation']
warp.ScaleFactor = 10

display = Show(warp)
ColorBy(display, ('POINTS', 'Elevation'))
display.SetScalarBarVisibility(GetActiveView(), True)
display.RescaleTransferFunctionToDataRange(True)

colorTF = GetColorTransferFunction('Elevation')
colorBar = GetScalarBar(colorTF, GetActiveView())

# Prettify the numeral formatting
colorBar.AutomaticLabelFormat = 0
colorBar.LabelFormat = '%.0f'
colorBar.RangeLabelFormat = '%.0f'

ResetCamera()
Render()
SaveScreenshot(r'.\images\bathymetry.png')
Interact()

# Save to vti
from vtkmodules.vtkIOXML import vtkXMLImageDataWriter

writer = vtkXMLImageDataWriter()
writer.SetFileName(r".\output\bathymetry.vti")
writer.SetInputConnection(producer.GetClientSideObject().GetOutputPort())  # or via servermanager
writer.Write()