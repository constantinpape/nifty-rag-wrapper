import nifty
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

        if isinstance(label_img, str) and label_img == '__will_deserialize__':
            return

        # TODO deal with vigra and axistags
        assert label_img.ndim == 3

        # TODO assert that label img is consecutive / use ilastik->opRelabelConsecutive before calling this

        self._n_threads = n_threads

        # TODO this seems unnecessary and eating up quite some memory for larger data
        self._label_img = label_img

        if flat_supperpixels:
            # TODO check correct axis order
            self._flat_superpixels = True
            self._rag = nifty.graph.rag.gridRagStacked2D(self._label_img, self._n_threads)
        else:
            self._flat_superpixels = False
            self._rag = nifty.graph.rag.gridRag(self._label_img, self.n_threads)



    @property
    def label_img(self):
        return self._label_img

    @property
    def flat_supperpixels(self):
        return self._flat_superpixels

    # TODO is there a function in nifty rag already ?
    @property
    def sp_ids(self):
        pass
        #return self._rag.

    @property
    def num_sp(self):
        return self._rag.numberOfNodes()

    # we assume a consecutive segmentation starting at 0 here.
    @property
    def max_sp(self):
        return self._rag.numberOfNodes() - 1

    @property
    def num_edges(self):
        return self._rag.numberOfEdges()

    @property
    def edge_ids(self):
        return self._rag.uvIds()

    # TODO implement if needed in ilastik
    @property
    def flat_edge_label_img(self):
        raise NotImplementedError("flat_edge_label_img not implemented for wrapper.")

    # dict of pandas dataframe -> not implemented
    @property
    def unique_edge_tables(self):
        raise NotImplementedError("flat_edge_label_img not implemented for wrapper.")

    # pandas dataframe -> not implemented
    @property
    def dense_edge_tables(self):
        raise NotImplementedError("flat_edge_label_img not implemented for wrapper.")

    # TODO implement
    def supported_features(self, accumulator_set="default"):
        pass

    # TODO implement
    def compute_features(self, value_img, feature_names, edge_group=None, accumulator_set="default"):
        pass

    # TODO implement
    def edge_decisions_from_groundtruth(self, groundtruth_vol, asdict=False):
        pass

    # TODO implement if needed
    def naive_segmentation_from_edge_decisions(self, edge_decisions, out=None ):
        pass

    # TODO will need to change the syntax for serializations

    # TODO implement
    def serialize_hdf5(self, h5py_group, store_labels=False, compression='lzf', compression_opts=None):
        pass

    # TODO implement
    def deserialize_hdf5(cls, h5py_group, label_img=None):
        pass
