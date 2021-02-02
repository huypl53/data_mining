#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : spliting.py
# Author            : phamlehuy53 <unknownsol98@gmail>
# Date              : 26.01.2021
# Last Modified Date: 26.01.2021
# Last Modified By  : phamlehuy53 <unknownsol98@gmail>
# %%
import os
import sys

# %%
def split(in_str: str, sep: str = ' '):
    k = 0
    cc = ' '
    ddict = {}
    def put(word):
        if word not in ddict:
            ddict[word] = 1
        else:
            ddict[word] += 1
    i = 0
    len_str = len(in_str)
    while i < len_str:
        if in_str[i]!=sep:
            if cc == sep:
                k = i
        else:
            if cc != sep:
                word = in_str[k: i]
                put(word)
            else:
                pass
        cc = in_str[i]
        i+=1
    if in_str[-1] != sep:
        put(in_str[k:])
    return ddict

# %%
if __name__ == "__main__":
    in_str = '  Him im   go su    !  '
    print(split(in_str))
    pass
