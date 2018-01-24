#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 10:59:47 2017

@author: Neo

Retrieve the result from .eop file which is generated by
the program getpar.

.eop file contains estimates of X pole coordinate, Y pole coordinate, UT1-TAI
angle, UT1 rate and UT1 acceleration as well as their formal uncertainties.
Estimates are obtained using all observations of the specific session.
.eop file contains also database names and time-tags.

   File contains lines of two types:
1) Comment. The first character is #. Header comment contain the full name of
   the spool file.

2) Estimates.

   Field   Format Units     Meaning
   1-8     A8     --        record type identifier: EOP_LOC:
   11-20   A10    --        database name with leading dollar sign
   23-25   I3     --        database version number
   34-49   A16    calend    EOP time tag in Solve format: YYYY.MM.DD-hh:mm
                            Time scale is not defined. Adjustments are at TDB
                            time scale, a priori EOP are at unknown time scale.
   58-63   I6     --        number of observation used for getting these EOP
                            estimates.
   69-79   F11.4  mas       estimate of X-pole coordinate
   84-93   F10.2  muas      formal uncertainty of X-pole coordinate
   99-109  F11.4  mas       estimate of Y-pole coordinate
   114-123 F10.2  muas      formal uncertainty of Y-pole coordinate
   129-139 F11.4  msec      estimates of UT1-TAI
   144-153 F10.2  musec     formal uncertainty of UT1-TAI
   159-169 F11.4  mas/day   estimates of X pole rate
   174-183 F10.2  muas/day  formal uncertainties of X pole rate
   189-199 F11.4  msec/day  estimates of Y pole rate
   204-213 F10.2  msec/day  formal uncertainties of Y pole rate
   219-229 F11.4  msec/day  estimates of UT1-TAI rate
   234-243 F10.2  musec/day formal uncertainties of UT1-TAI rate
   249-259 F11.4  ms/day**2 estimates of UT1-TAI acceleration
   264-273 F10.2  ms/day**2 formal uncertainties of UT1-TAI acceleration

    If the specific parameter was not estimated in this experiment, the field
for its value and formal uncertainty is replaced by filler: $$$$$$. The filler
takes entire field.

"""

import numpy as np
from time import strptime, mktime
import matplotlib.pyplot as plt


# ------------------------------  FUNCTIONS  ---------------------------
def time_trans(timestr):
    ts = mktime(strptime(str(timestr, 'utf-8'),
                         "%Y.%m.%d-%H:%M"))
    return ts / 365.25 / 86400 + 1970.0
    # return ts / 86400 + 1970.0 + 1.0 / 24


def read_eop(datafile):
    '''Retrieve the result from .eop file.

    Parameters
    ----------
    datafile : string
        name of data file

    Returns
    ----------
    dbname : array, string
       database name with leading dollar sign
    tag : array, float
        EOP time flag, year
    obsnum : array, int
        number of observations used
    X : array, float
        X-pole coordinate, mas
    X_err : array, float
        formal uncertainty of X, mas
    Y : array, float
        Y-pole coordinate, mas
    Y_err : array, float
        formal uncertainty of Y, mas
    U : array, float
        UT1 - TAI, msec
    U_err : array, float
        formal uncertainty of U, msec
    XR : array, float
        X-pole coordinate rate, mas/day
    XR_err : array. float
        formal uncertainty of XR, mas/day
    YR : array, float, mas/day
        Y-pole coordinate rate, mas/day
    YR_err : array. float
        formal uncertainty of YR, mas/day
    UR : array, float
        UT1 - TAI rate, msec/day
    UR_err : array. float
        formal uncertainty of UR, msec/day
    '''

    dbname = np.genfromtxt(datafile, dtype=str, usecols=(1,))
    tag = np.genfromtxt(datafile, usecols=(4,), converters={4: time_trans})
    obsnum = np.genfromtxt(datafile, dtype=int, usecols=(6,))
    X, X_err, Y, Y_err, U, U_err = np.genfromtxt(datafile,
                                                 usecols=np.arange(8, 20, 2),
                                                 missing_values='*'*8,
                                                 filling_values=0.,
                                                 unpack=True)
    XR, XR_err, YR, YR_err, UR, UR_err = np.genfromtxt(
        datafile, usecols=np.arange(20, 32, 2), unpack=True)
    # uas -> mas or usec -> msec
    X_err, Y_err, U_err = X_err / 1000.0, Y_err / 1000.0, U_err / 1000.0
    # uas/day -> mas/day or usec/day -> msec/day
    XR_err, YR_err, UR_err = XR_err / 1000, YR_err / 1000, UR_err / 1000

    return [dbname, tag, obsnum, X, X_err, Y, Y_err, U, U_err,
            XR, XR_err, YR, YR_err, UR, UR_err]


def read_eops(datafile):
    '''Retrieve from the result from .eops data.

    Data columns are listed as follow:

      Columns  Units   Meaning
         1     days    Modified Julian date
         2     arcsec  X pole coordinate
         3     arcsec  Y pole coordinate
         4     sec     UT1-TAI
         5     mas     Celestial pole offset dX wrt IAU 2006
         6     mas     Celestial pole offset dY wrt IAU 2006
         7     arcsec  Formal uncertainty of X pole coordinate
         8     arcsec  Formal uncertainty of Y pole coordinate
         9     sec     Formal uncertainty of UT1-TAI
        10     mas     Formal uncertainty of celestial pole offset dX
        11     mas     Formal uncertainty of celestial pole offset dY
        12     --      10-character database identifier
        13     --      Correlation between X and Y
        14     --      Correlation between X and UT1-TAI
        15     --      Correlation between Y and UT1-TAI
        16     --      Correlation between dX and dY
        17     --      Number of used observations in the session
        18     --      6-character session identifier
        19     hours   Session duration
        20     asc/day X pole coordinate rate
        21     asc/day Y pole coordinate rate
        22     ms      Excess of length of day
        23             Field not used
        24             Field not used
        25     asc/day Formal uncertainty of X pole coordinate rate
        26     asc/day Formal uncertainty of Y pole coordinate rate
        27     ms      Formal uncertainty of excess of length of day
        28             Field not used
        29             Field not used
        30     ps      Postfit rms delay
        31     --      Array structure

# Note: Some EOP were not estimated for some sessions. They are however left in this
# file for sake of completeness. They can be identified by their sigma set
# to zero.

    Parameters
    ----------
    datafile : string
        name of data file

    Returns
    ----------
    mjd : array, float
        time lag, modified Julian date
    Xp : array, float
        X-pole coordinate, mas
    Xperr : array, float
        formal uncertainty of X, mas
    Yp : array, float
        Y-pole coordinate, mas
    Yperr : array, float
        formal uncertainty of Y, mas
    U : array, float
        UT1 - TAI, msec
    Uerr : array, float
        formal uncertainty of U, msec
    dX : array, float
        X coordinate of nutation offset, mas
    dXerr : array. float
        formal uncertainty of XR, mas
    dY : array, float, mas
        Y coordinate of Nutation offset, mas
    dYerr : array. float
        formal uncertainty of dY, mas
    '''

    mjd, Xp, Yp, U, dX, dY = np.genfromtxt(datafile,
                                           usecols=range(6),
                                           unpack=True)

    Xperr, Yperr, Uerr, dXerr, dYerr = np.genfromtxt(datafile,
                                                     usecols=range(6, 11, 1),
                                                     unpack=True)
    # as -> mas or sec -> msec
    Xp, Yp, Up = Xp * 1000.0, Yp * 1000.0, Up * 1000.0
    Xperr, Yperr, Uerr = Xperr * 1000.0, Yperr * 1000.0, Uerr * 1000.0

    Xperr = np.where(Xperr == 0, 1.e6, Xperr)
    Yperr = np.where(Yperr == 0, 1.e6, Yperr)
    Uerr = np.where(Uerr == 0, 1.e6, Uerr)
    dXerr = np.where(perr == 0, 1.e6, dXerr)
    dYerr = np.where(dYerr == 0, 1.e6, dYperr)

    return [mjd, Xp, Xperr, Yp, Yperr, U, Uerr,
            dX, dXerr, dY, dYerr]


# # Retrieve estimates.
# [dbname, tag, obsnum, X, X_err, Y, Y_err, U, U_err,
#  XR, XR_err, YR, YR_err, UR, UR_err] = read_eop('result/test.eop')

# print(tag[0])
# # Plot it.
# fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, sharex=True)
# ax0.errorbar(tag, X, yerr=X_err, fmt='.')
# ax0.set_title("X-pole (mas)")
# ax0.set_ylim([-500, 500])
# ax1.errorbar(tag, Y, yerr=Y_err, fmt='.')
# ax1.set_title("Y-pole (mas)")
# ax1.set_ylim([-200, 800])
# ax2.errorbar(tag, U, yerr=U_err, fmt='.')
# ax2.set_title("UT1-TAI (ms)")
# plt.savefig("figures/eop1.eps")
# plt.show()

# ------------------------------ END -----------------------------------
