# compare performance of the different rags:
# ilastik-rag
# nifty-rag (plain)
# nifty-rag (wrapped)

import numpy as np
import vigra
import nifty
import time

import sys

# hack in path to the ilastikrag
sys.path.append('../../ilastikrag')
import ilastikrag

# TODO hack in path to the wrapper

# TODO 2.5 D test

def performance_create_rag_3D(labels):
    test_labels = vigra.readHDF5(
            '/home/consti/Work/data_neuro/nature_experiments/neuroproof_data/overseg_train.h5',
            'data')

    #t_nifty = time.time()
    #rag_nifty = nifty.graph.rag.gridRag(labels) # using all threads
    #print "Computed nifty rag in %f s" % (time.time() - t_nifty)

    # need to transform this to a vigra array for ilrag....
    print type(labels)
    labels = vigra.Volume(labels, dtype = np.uint32)
    t_ilrag = time.time()
    print labels.dtype
    rag_il = ilastikrag.Rag(labels)
    print "Computing ilastikrag in %f s" % (time.time() - t_ilrag)

    #assert rag_il.max_sp + 1 == rag_nifty.numberOfNodes, "%i, %i" % (rag_il.max_sp + 1, rag_nifty.numberOfNodes)
    #assert rag_il.num_edges == rag_nifty.numberOfEdges, "%i, %i" (rag_il.num_edges, rag_nifty.numberOfEdges)

    print rag_il.supported_features()



if __name__ == '__main__':
    labels = vigra.readHDF5(
            '/home/consti/Work/data_neuro/nature_experiments/neuroproof_data/overseg_train.h5',
            'data').astype('uint32')
    assert isinstance(labels, np.ndarray)
    performance_create_rag_3D(labels)
