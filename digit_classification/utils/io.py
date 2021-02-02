#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : io.py
# Author            : phamlehuy53 <unknownsol98@gmail>
# Date              : 02.02.2021
# Last Modified Date: 02.02.2021
# Last Modified By  : phamlehuy53 <unknownsol98@gmail>

import os
import numpy as np
def read_csv(fpath):
    res = []
    if os.stat(fpath).st_size == 0:
        pass
    else:
        with open(fpath, 'r') as fread:
            content = fread.read().strip().split('\n')
            for line in content:
                res.append(line.split(','))
    return np.array(res, dtype=np.float)
