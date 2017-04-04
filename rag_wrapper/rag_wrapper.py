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
        assert accumulator_set="default"
        return ["edge_standard", "node_standard", "edge_geometry", "node_geometry"]

    # TODO on filters
    # TODO do we need to define the accumulator set at all
    # only very basic features for now and not possible to choose
    def compute_features(self, value_img, feature_names, edge_group=None, accumulator_set="default"):
        assert accumulator_set == "default" # only one type of accumulators for now
        assert not self.flat_supperpixels, "Not Implemented"
        features = []

        # get edge and node features from image
        min_, max_ = value_img.min(), value_img.max()
        edge_f, node_f = nifty.graph.rag.accumulateStandartFeatures( self._rag, value_img, min_, max_, numberOfThreads = self._n_threads)

        features.append(edge_f)

        # node features to edge_features
        # TODO more combinations than this
        uv_ids = self._rag.uvIds()
        node_to_edge_f = np.abs( node_f[uv_ids[:,0]] - node_f[uv_ids[:,1]] )[:,None]
        features.append(node_to_edge_f)

        geo_f = nifty.graph.rag.accumulateGeometricEdgeFeatures(self._rag)
        feaures.append(geo_f)

        return np.nan_to_num( np.concatenate(features, axis = 1) )


    # TODO implement
    def edge_decisions_from_groundtruth(self, groundtruth_vol, asdict=False):
        pass


    # TODO implement if needed
    def naive_segmentation_from_edge_decisions(self, edge_decisions, out=None ):
        pass

    # TODO will need to change the syntax for serializations
    # actually not that much !, we can just write the deserialized graph to the h5py_group

    def serialize_hdf5(self, h5py_group, store_labels=False, compression='lzf', compression_opts=None):
        if self.flat_supperpixels:
            assert False, "Not implemented yet" # this is a bit more tricky to deserialze, but I have done that in nifty py bindings already
        else:
            h5py_group.create_dataset( 'rag', rag.serialize() )

        # label_img metadata
        labels_dset = h5py_group.create_dataset('label_img',
                                                shape=self._label_img.shape,
                                                dtype=self._label_img.dtype,
                                                compression=compression,
                                                compression_opts=compression_opts)
        labels_dset.attrs['valid_data'] = False

        # label_img contents
        if store_labels:
            # Copy and compress.
            labels_dset[:] = self._label_img
            labels_dset.attrs['valid_data'] = True



    # TODO implement
    def deserialize_hdf5(cls, h5py_group, label_img=None):
        pass
