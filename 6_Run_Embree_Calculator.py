import sys
sys.path.append('./RECOTOOLS/')
# import project_metadata
from core import system_run, survey_metadata, run_collection
import datalibrary
import processor
import systems.pelisystem
import pandas as pd
from pandas_tools import *
import matplotlib.pyplot as plt
from scipy import interpolate
import scipy
from core import system_run, survey_metadata, run_collection

from mugrass.units import *
from mugrass.voxelframe_meshgrid import *
from mugrass.pixel_collection import *
from mugrass.linear_solver import *

import sys
from mugrass.embree_helper import *



voxel_col = voxelframe_meshgrid(pickle_path="voxel_dataframe_masked.vxl")
pixel_col = pixel_collection(pickle_path="pixel_dataframe.pxl")
coo = embree_matrix(voxel_col, pixel_col)

#scipy.sparse.save_npz(f"test_weights_cowburn", coo)

crs=scipy.sparse.csr_matrix(coo)
ccs=scipy.sparse.csc_matrix(coo)

scipy.sparse.save_npz(f"weights_masked_crs", crs)

scipy.sparse.save_npz(f"weights_masked_ccs", ccs)