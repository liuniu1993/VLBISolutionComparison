#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name: list_crossmatch.py
"""
Created on Fri Apr 27 00:24:29 2018

@author: Neo(liuniu@smail.nju.edu.cn)
"""

import numpy as np


# -----------------------------  FUNCTIONS -----------------------------
def list_crossmatch(X1, X2):
    '''Corssmatch between two list.

    Parameters
    ----------
    X1 : array_like
        first dataset, shape(N1, D)
    X2 : array_like
        second dataset, shape(N2, D)

    Returns
    -------
    '''

    # =======
    # Add some codes here to eliminate duplicate elemnets
    # =======

    com_list = []
    index1 = []
    index2 = []

    for i, x1 in enumerate(X1):
        indarr = np.where(X2 == x1)[0]

        if indarr:
            com_list.append(x1)
            index1.append(i)
            j = indarr[0]
            index2.append(j)
        # else:

    com_list = np.asarray(com_list, dtype=str)
    index1 = np.asarray(index1, dtype=str)
    index2 = np.asarray(index2, dtype=str)

    return com_list, index1, index2

# --------------------------------- END --------------------------------
