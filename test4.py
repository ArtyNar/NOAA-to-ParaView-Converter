import sys, os

sys.path.insert(0, r"C:\Program Files\ParaView 5.13.2\bin\Lib\site-packages")
os.add_dll_directory(r"C:\Program Files\ParaView 5.13.2\bin")

from paraview.simple import *

reader = OpenDataFile('./data/exportImage.tiff')
reader.UpdatePipeline()

# List all point-data array names and their value ranges
for i in range(reader.PointData.GetNumberOfArrays()):
    arr = reader.PointData.GetArray(i)
    print(arr.GetName(), arr.GetRange())

# --- Warp into 3D relief directly using the reader's own array ---
warp = WarpByScalar(Input=reader)
warp.Scalars = ['POINTS', 'Tiff Scalars']   # note the space - array name as printed
warp.ScaleFactor = 0.05

display = Show(warp)
ColorBy(display, ('POINTS', 'Tiff Scalars'))
display.SetScalarBarVisibility(GetActiveView(), True)
display.RescaleTransferFunctionToDataRange(True)

ResetCamera()
Render()
SaveScreenshot(r'.\images\bathymetry.png')
Interact()