#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : weight.py
# Author            : phamlehuy53 <unknownsol98@gmail>
# Date              : 02.02.2021
# Last Modified Date: 02.02.2021
# Last Modified By  : phamlehuy53 <unknownsol98@gmail>
import os
import numpy as np
import sys
# from ..utils.io import read_csv

# if '__file__' in dir():
#     CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
# else:
#     CURRENT_PATH = '.'
# sys.path.insert(1, os.path.join(CURRENT_PATH, '../'))
# 
# from utils.io import read_csv
def load_weights(dir_in: str):
    """
    Return list of [<class_name, weights>]
    """
    wfiles = os.listdir(dir_in)
    wfiles = list(filter( lambda x: '.npy' in x, wfiles))
    res = []
    for f in wfiles:
        fpath = os.path.join(dir_in, f)
        W = np.load(fpath, allow_pickle=True).item()
        # print(W)
        if 'count' in W and W['count'] > 0:
            res.append(W)
            pass
        else:
            print(f"Warning: Weight file {f} is empty!")
    if res:
        return np.array(res,dtype=np.object)
    else:
        print(f"Nothing is loaded!")
        return np.array([])

def update_weights(dir_in: str, read_csv_fn: None):
    classes = os.listdir(dir_in)
    classes = list(filter( lambda x: '.csv' in x, classes))
    if not classes:
        print(f"Warning: No csv files found!")
        return
    for cl in classes:
        bname = os.path.splitext(cl)[0]
        wp = os.path.join( dir_in, bname + '.npy')
        cl_path = os.path.join(dir_in, cl)
        if os.stat(cl_path).st_size == 0:
            print(f"File {cl_path} is empty!")
            continue
        if os.path.isfile(wp) and os.stat(wp).size > 10:
            W = np.load(wp, allow_pickle=True)
        else:
            W = {'name': bname,
                    'count': 0,
                    'weight': 0}

        csv_cont = read_csv_fn(cl_path)
        # reduced_csv = np.sum(csv_cont==0, axis=0)
        # csv_cont[:, reduced_csv>0.9*len(csv_cont)] = 0
        W['weight'] = W['weight']*W['count'] + np.sum(csv_cont, axis=0)
        W['count'] = W['count'] + len(csv_cont)
        W['weight'] = W['weight']/W['count']
        open(cl_path, 'w').close()
        np.save(wp, W)
    print(f"Save weights done!")
