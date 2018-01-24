#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 10:57:02 2017

@author: Neo

Retrieve the estimates of right ascension and declination of global
sources, their formal uncertainties, and correlations between right
ascension and declination of the same source of from .sou file which
is generated by the program getpar.


   .sou file contains estimates of right ascension and declination of
global sources, as well as formal their uncertainties and correlations between
right ascension and declination of the same source.

   File contains lines of two types:
1) Comment. The first character is #. Header comment contain the full name of
   the spool file.

2) Estimates.

   Field   Format Units  Meaning
   1-8     A8     --     record type identifier: SOU_GCO:
   11-18   A8     --     IVS source name.
   25-26   I2     hours  right ascension. hours part
   27-27   A1     --     separator "_"
   28-29   I2     min.   right ascension. minutes part
   30-30   A1     --     separator "_"
   31-41   F11.8  sec.   right ascension. seconds part
   46-55   F10.4  mas    formal error of right ascension
   62-64   I3     deg.   declination. degrees part.
   65-65   A1     --     separator "_"
   66-67   I2     arcmin declination. arcminutes part.
   68-68   A1     --     separator "_"
   69-78   F10.7  arcsec declination. arcseconds part.
   83-92   F10.4  mas    formal uncertainty of declination
   99-104  F6.4   d/l    correlation between the estimates of right ascension
                         and declination.
   116-122 I7     --     the number of observations of this source used in
                         solution.
   133-139 I7     --     total number of observations of this source.
   151-155 I5     --     the number of sessions of this source used in
                         solution.
   166-170 I5     --     total number of sessions with this source.
   182-191 A10    --     the date of the first session with this source used
                         in solution. format: yyyy.mm.dd (as integer numbers)
   203-212 A10    --     the date of the last session with this source used
                         in solution. format: yyyy.mm.dd (as integer numbers)

"""

import numpy as np
import sys
from pos_conv import RA_conv, DC_conv
from time_conv import date2year

# ------------------------------  FUNCTIONS  ---------------------------1


def read_sou(datafile):
    '''Retrieve the result from .sou file.

    Parameters
    ----------
    datafile : string
        name of data file

    Returns
    ----------
    sou : array, string
        IVS source name
    RA : array, float
        Right ascension, as
    RA_err : array, float
        formal uncertainty of RA, mas
    DC : array, float
        Declination, as
    DC_err : array, float
        formal uncertainty of DC, mas
    Cor : array, float
        correlation between RA and DC
    ObsUsed : array, int
        Number of used observations of this source
    ObsTot : array, int
        Total number of observations of this source
    SesUsed : array, int
        Number of used sessions for this source
    SesTot : array, int
        Total number of sessions for this source
    DateBeg : array, float
        Epoch of the first observation
    DateEnd : array, float
        Epoch of the last observation
    '''

    sou = np.genfromtxt(datafile, dtype=str, usecols=(1,), unpack=True)
    RA, RA_err, DC, DC_err, cor = np.genfromtxt(
        datafile, usecols=np.arange(3, 12, 2),
        converters={3: RA_conv, 7: DC_conv},
        missing_values='*'*8,
        filling_values=0.,
        unpack=True)

    ObsUsed, ObsTot, SesUsed, SesTot = np.genfromtxt(
        datafile, usecols=np.arange(13, 20, 2), dtype=int, unpack=True)

    # empty list for store data
    DateBeg, DateEnd = [], []

    for line in open(datafile, 'r'):
        if line[0] != '#':
            DateBeg.append(date2year(line[181:191]))
            DateEnd.append(date2year(line[202:212]))

    DateBeg = np.array(DateBeg)
    DateEnd = np.array(DateEnd)

    return [sou, RA, RA_err, DC, DC_err, cor,
            ObsUsed, ObsTot, SesUsed, SesTot, DateBeg, DateEnd]


def read_sou_pos(datafile):
    '''Retrieve position information from .sou file.

    Parameters
    ----------
    datafile : string
        name of data file

    Returns
    ----------
    sou : array, string
        IVS source name
    RA : array, float
        Right ascension, as
    RA_err : array, float
        formal uncertainty of RA, mas
    DC : array, float
        Declination, as
    DC_err : array, float
        formal uncertainty of DC, mas
    Cor : array, float
        correlation between RA and DC
    '''

    [sou, RA, RA_err, DC, DC_err, cor,
     ObsUsed, ObsTot, SesUsed, SesTot, DateBeg, DateEnd] = read_sou(datafile)

    return [sou, RA, RA_err, DC, DC_err, cor]


# # Retrieve estimates.
# if len(sys.argv) == 1:
#     datafile = 'result/test.sou'
# else:
#     datafile = sys.argv[1]
# [sou, RA, RA_err, DC, DC_err, cor,
#  ObsUsed, ObsTot, SesUsed, SesTot, DateBeg, DateEnd] = read_sou(datafile)
# print(sou[0], RA[0], RA_err[0], DC[0], DC_err[0], cor[0],
#       ObsUsed[0], ObsTot[0], SesUsed[0], SesTot[0],
#       DateBeg[0], DateEnd[0])
# ------------------------------ END -----------------------------------