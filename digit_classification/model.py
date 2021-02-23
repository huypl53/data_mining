#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : model.py
# Author            : phamlehuy53 <unknownsol98@gmail>
# Date              : 26.01.2021
# Last Modified Date: 02.02.2021
# Last Modified By  : phamlehuy53 <unknownsol98@gmail>

# %%
import os
import cv2
import numpy as np
import time
import glob
import sys
from kNN import kNNClassifier
if '__file__' in dir():
    CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
else:
    CURRENT_PATH = '.'

sys.path.insert(1, CURRENT_PATH)

from utils.io import read_csv
from extraction.weight import load_weights, update_weights
from dip.space import thresh_area
# %%
def get_itensity(matrix: np.ndarray, thresh:int = 1):
    return (matrix[matrix>thresh]).size
    # return np.sum(matrix)
def get_diff(arr_x: np.ndarray, arr_y: np.ndarray, indices=None):
    enh = 10000
    if indices:
        d = arr_x[indices]*enh - arr_y[indices]*enh
    else:
        d = arr_x*enh - arr_y*enh
    res = np.sqrt((np.sum(d**2)/d.size))
    return res
def calc_cells(image:np.ndarray,
               split_wid:int=60,
               split_hei:int=90,
               thresh:int=10):
    # sel_area = thresh_area(image, thresh=thresh, tg_size=50 )
    sel_area = thresh_area(image, thresh=thresh )
    if not sel_area.any():
        raise Exception('Threshed area is empty!')
    c_size = min(sel_area.shape[:2])/max(split_hei, split_wid)
    c_size = int(c_size) if c_size>1 else int(1/c_size)
    img = cv2.resize(sel_area, (c_size*split_wid, c_size*split_hei))
    # cv2.imshow('Calc', img)
    # c = cv2.waitKey(0)
    # cv2.destroyAllWindows()
    cells = []
    sum_intensity = img.size
    for i in range(split_hei):
        for j in range(split_wid):
            cells.append(get_itensity(img[i*c_size: (i+1)*c_size,
                                          j*c_size: (j+1)*c_size])/sum_intensity)
    return np.array(cells)
    
    pass


def log_cell(cells_list: [int], csv_path: str='./output.csv', mode:str='w'):
    assert mode in ['w', 'a']
    with open(csv_path, mode) as f:
        for cells in cells_list:
            cntxt = ','.join(np.array(cells, dtype=np.str)) + '\n'
            f.write(cntxt)


def path2cells(fpath):
    image = cv2.imread(fpath, cv2.IMREAD_GRAYSCALE)
    image = 255 - image
    try:
        cells = calc_cells(image,thresh=10)
        return cells
    except Exception as e:
        print(str(e))
        print("AT: ", fpath)

def simple_model():
# %%
    # Update weights
    # 
    # cset = [str(i) for i in range(10)]
    # for c in cset[:]:
    #     image_paths = glob.glob('./train/{}/*.*'.format(c))
    #     cells_list = [ path2cells(p) for p in image_paths ]
    #     log_cell(cells_list, csv_path='./weights/{}.csv'.format(c), )
    # 
    # # %%
    #     update_weights('./weights', read_csv)


    # for testing only
    # %%
    weight_list = load_weights('./weights')
    # %%
    n_test = 0
    n_true = 0
    for root_dir, sub_dir, files in os.walk('./test'):
        for i, f in enumerate(files):
            n_test += 1
            fpath = os.path.join(root_dir, f)
            image = cv2.imread(fpath, cv2.IMREAD_GRAYSCALE)
            image = 255 -image
            cells = calc_cells(image,thresh=10 )
            res = ( None, None )
            diff = 999999
            for w in weight_list:
                ind1 = w['weight'] > 0
                ind2 = cells > 0
                # indices = list(set(ind1).union(set(ind2)))
                d = get_diff(cells[ind2], w['weight'][ind2])
                # print(f"file {f} get diff {d} with {w[0]}")
                if d < diff:
                    res = (w['name'], diff)
                    diff = d
            cv2.imwrite(f"./prediction/{root_dir[-1]}_{i}_{res[0]}.png", image)
            if int(root_dir[-1].lower()) == int(res[0]):
                n_true += 1
    print(f"Accuracy: {n_true/n_test} on {n_test} images")
# %%

def kNN_model():
    # Init kNN's weights
    X, Y = [], []
    cset = [str(i) for i in range(10)]
    for c in cset[:]:
        image_paths = glob.glob('./train/{}/*.*'.format(c))
        # cells_list = [ path2cells(p) for p in image_paths ]
        for p in image_paths:
            x = path2cells(p)
            X.append(x)
            Y.append(int(c))

    X = np.array(X)
    Y = np.array(Y)
    # np.save('X.npy', X)
    # np.save('Y.npy', Y)
    model = kNNClassifier(1)
    model.fit(X, Y)
# %%

    # Test kNN model
    X_test = []
    Y_test = []
    for root_dir, sub_dir, files in os.walk('./test'):
        for i, f in enumerate(files):
            fpath = os.path.join(root_dir, f)
            image = cv2.imread(fpath, cv2.IMREAD_GRAYSCALE)
            image = 255 -image
            cells = calc_cells(image,thresh=10 )
            X_test.append(cells)
            Y_test.append(int(root_dir[-1].lower()))
    X_test = np.array(X_test)
    Y_test = np.array(Y_test)
    pred = model.predict(X_test)
    acc = np.sum( Y_test == pred ) / Y_test.shape[0]
    print(f"Accuracy: {acc} on {n_test} images")

if __name__ == "__main__":
    # simple_model()
    # kNN_model()
