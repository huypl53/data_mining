# %%
import numpy as np
import os


# %%
class kNNClassifier(object):
    def __init__(self, k):
        assert k > 0
        super( kNNClassifier, self).__init__()
        self._X = None
        self._Y = None
        self.k = k

    def fit(self, X, Y):
        assert len(X) == len(Y)
        self._X = X
        self._Y = Y

    def predict(self, X):
        assert X.shape[1:] == self._X.shape[1:]
        pred = []
        for x in X:
            indices = np.argsort( np.linalg.norm(self._X - x, axis=1), axis=0)[:self.k]

            # TODO: implement weights for neighbors
            cls_, freq = np.unique(self._Y[indices], return_counts=True)
            pred.append( cls_[np.argmax(freq)] )
        return pred
