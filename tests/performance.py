# compare performance of the different rags:
# ilastik-rag
# nifty-rag (plain)
# nifty-rag (wrapped)

import vigra
import nifty
import time

import sys

# hack in path to the ilastikrag
sys.path.append('../../ilastikrag')
import ilastikrag

# TODO hack in path to the wrapper

# TODO 2.5 D test

def performance_create_rag_3D():
    test_labels = vigra.readHDF5(
            '/home/consti/Work/data_neuro/nature_experiments/neuroproof_data/overseg_train.h5',
            'data')

    t_nifty = time.time()
    rag = nifty.graphs.

