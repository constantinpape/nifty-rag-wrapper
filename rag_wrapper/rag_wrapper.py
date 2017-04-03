import nifty
# TODO do we really need all the pandas stuff ?
import pandas as pd
import numpy as np

# the class that wraps the nifty rag
class Rag(object):
    """
    Region Adjacency Graph
    TODO docu
    """

    # TODO default n-threads ?
    def __init__(self, label_img, flat_supperpixels = False, n_threads = -1):
        """
        Parameters
        """
        # TODO if label img is a vigra array with axistags, we need to remove them and
        # make sure that the img is not transosed (not sure if this is correct right now)
        if hasattr(label_img, 'axistags'):
            # TODO make sure that we only have xyz axistags
            label_view = label_img.view(np.ndarray) # FIXME beware of axis transposing!
        else:
            label_view = label_img.view()

        # TODO safe correctly (we don't want to save the view, but also not the axis-tag mess)
        self._label_img = label_img

        self._n_threads = n_threads

        if flat_supperpixels:
            assert label_img.ndim == 3
            # TODO check correct axis order
            self._flat_superpixels = True
            self._rag = nifty.graph.rag.gridRagStacked2D(labels, self._n_threads)
        else:
            self._flat_superpixels = False
            self._rag = nifty.graph.rag.gridRag(labels, self.n_threads)




    @property
    def label_img(self):
        return self._label_img

    @property
    def flat_supperpixels(self):
        return self._flat_superpixels

    def num


