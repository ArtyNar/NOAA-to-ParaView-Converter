import rasterio
import numpy as np
import pyvista as pv

with rasterio.open('./data/exportImage.tiff') as src:
    elevation = src.read(1).astype(np.float64)
    nodata = src.nodata
    transform = src.transform
    print("CRS:", src.crs)
    print("Size:", src.width, src.height)
    print("Bands:", src.count)
    print("dtype:", src.dtypes)
    print("nodata:", src.nodata)
    print("bounds:", src.bounds)
    print("transform:", src.transform)

    for i in range(1, src.count + 1):
        data = src.read(i)
        print(
            f"Band {i}:",
            "min =", data.min(),
            "max =", data.max(),
            "unique =", np.unique(data)[:20]
        )
