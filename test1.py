import sys, os 

sys.path.append(r"C:\Program Files\ParaView 5.13.2\bin\Lib\site-packages") 
os.add_dll_directory(r"C:\Program Files\ParaView 5.13.2\bin") 

from paraview.simple import * 

Cone()
SetProperties(Resolution=3)
Show()
Render()

SaveScreenshot(r".\images\screenshot.png")
Interact()

