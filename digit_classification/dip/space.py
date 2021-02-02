#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : space.py
# Author            : phamlehuy53 <unknownsol98@gmail>
# Date              : 02.02.2021
# Last Modified Date: 02.02.2021
# Last Modified By  : phamlehuy53 <unknownsol98@gmail>
import numpy as np
import cv2
def thresh_area(image: np.ndarray,
                thresh: np.uint8 = 20,
                max_pad: int=None
                ):
                # tg_size = 100):
    old_h, old_w = image.shape[:2]
    tg_size = min(image.shape[:2])
    image= cv2.resize(image, (tg_size, tg_size))
    h, w = tg_size, tg_size
    if not max_pad:
        max_pad = tg_size//30
    else:
        assert tg_size%max_pad==0
    xmin, ymin = 0, 0
    xmax, ymax = w, h
    while xmin<xmax:
        if np.max(image[:, xmin: xmin+max_pad, ...]) > thresh:
            break
        xmin+=max_pad
    while xmin<xmax:
        if np.max(image[:, xmax-max_pad: xmax , ...]) > thresh:
            break
        xmax-=max_pad
    # cv2.imshow('Progress', image)
    if xmax==xmin:
        if xmin==0:
            if np.max(image[:, xmin: xmin+max_pad, ...]) <= thresh:
                print('xmin')
                return np.array([])
            else:
                xmax += max_pad
        if xmax==w:
            if np.max(image[:, xmax-max_pad: xmax, ...]) <= thresh:
                print('xmax')
                return np.array([])
            else:
                xmin -= max_pad

    while ymin<ymax:
        if np.max(image[ ymin: ymin+max_pad, ...]) > thresh:
            break
        ymin+=max_pad
    
    while ymin<ymax:
        if np.max(image[ ymax-max_pad: ymax, ...]) > thresh:
            break
        ymax-=max_pad

    if ymax==ymin:
        if ymin==0:
            if np.max(image[ymin: ymin+max_pad, ...]) <= thresh:
                return np.array([])
            else:
                ymax += max_pad
        if ymax==h:
            if np.max(image[ymax-max_pad: ymax, ...]) <= thresh:
                return np.array([])
            else:
                ymin -= max_pad
        
    return image[ymin: ymax, xmin: xmax, ...]
