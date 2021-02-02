#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : spliting.py
# Author            : phamlehuy53 <unknownsol98@gmail>
# Date              : 26.01.2021
# Last Modified Date: 02.02.2021
# Last Modified By  : phamlehuy53 <unknownsol98@gmail>
# %%
import os
import sys
from glob import glob
import json
from joblib import Parallel, delayed
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

def read_dir_file(in_dir: str, exts=['.txt']):
    """
    Read all files in <exts>
    Return <basename, text>
    """
    for ext in exts:
        file_list = glob(in_dir+'/*{}'.format(ext))
        for f in file_list:
            with open(f, 'r') as fread:
                content = fread.read()
                yield (os.path.basename(f), content)

def parse(input_dir, output_dir,):
    def write(f, text):
        outpath = os.path.join(output_dir, f)
        word_dict = split(text, sep=' ')
        with open(os.path.splitext(outpath)[0]+'.json', 'w') as fwrite:
            json.dump(word_dict, fwrite, indent=2)
            # fwrite.write(json.dumps(word_dict, indent=2))
    # for f, text in read_dir_file(input_dir):
        # write(f, text)

    _ = Parallel(n_jobs=4, prefer='threads')(delayed(write)(f,text) for f, text in read_dir_file(input_dir))

# %%
if __name__ == "__main__":
    """
    args: input_dir output_dir
    """
    args = sys.argv[1:3]
    # in_str = '  Him im   go su    !  '
    # print(split(in_str))
    input_dir, output_dir = args[0], args[1]
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
        print(f"Warning: {output_dir} not exist! The new one is created")
    parse(input_dir, output_dir)
    pass
