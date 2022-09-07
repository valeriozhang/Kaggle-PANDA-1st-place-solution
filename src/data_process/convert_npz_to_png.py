import glob
from PIL import Image
import numpy as np

for file in glob.glob("./input/train_256_36/*.npz"):
    npz_arr = np.load(file)["arr_0"]
    im = Image.fromarray(npz_arr)
    im.save("{}".format(file.replace(".npz",".png")))
    # break