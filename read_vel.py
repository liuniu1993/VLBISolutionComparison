#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 10:55:55 2017

@author: Neo

Retrieve the estimates of velocities of global stations and the formal
uncertainties of these estimates from .vel file which is generated by
the program getpar.

   .vel file contains values estimates of velocities of global stations and the
formal uncertainties of these estimates. The list of the estimates is sorted in
alphabetic order of station names. Stations before and after episodic motions
are treated as different stations. Correlations between station positions and
velocities are also written.

   File contains lines of three types:

1) Comment. The first character is #. Header comment contain the full name of
   the spool file.

2) Cartesian components of the vector of station velocity. The first
   8 characters of this line are STA_GVX:

   Field   Format Units Meaning
   1-8     A8     --    record type identifier: STA_GVX:
   11-18   A8     --    station name.
   24-32   F9.2   mm/yr value of X-component of station velocity.
   37-44   F8.3   mm/yr formal uncertainty of X-component of station velocity.
   50-58   F9.2   mm/yr value of Y-component of station velocity.
   63-70   F8.3   mm/yr formal uncertainty of Y-component of station velocity.
   76-84   F9.2   mm/yr value of Z-component of station velocity.
   89-96   F8.3   mm/yr formal uncertainty of Z-component of station velocity.

3) Local topocentric components of the vector of station velocity: Up, East,
   North. The first 8 characters of this line are STA_GVU:

   Field   Format Units Meaning
   1-8     A8     --    record type identifier: STA_GVU:
   11-18   A8     --    station name.
   24-32   F9.2   mm/yr value of U-component of station velocity.
   37-44   F8.3   mm/yr formal uncertainty of U-component of station velocity.
   50-58   F9.2   mm/yr value of E-component of station velocity.
   63-70   F8.3   mm/yr formal uncertainty of E-component of station velocity.
   76-84   F9.2   mm/yr value of N-component of station velocity.
   89-96   F8.3   mm/yr formal uncertainty of N-component of station velocity.
"""

import numpy as np
import sys


# ------------------------------  FUNCTIONS  ---------------------------
def read_vel(dataflea):
    '''Retrieve the result from .lso file.

    Parameters
    ----------
    datafile : string
        name of data file

    Returns
    ----------
    staname : string
        name of station
    VX : array, float
        Velocity of X component, mm/yr
    VY : array, float
        Velocity of Y component, mm/yr
    VZ : array, float
        Velocity of Z component, mm/yr
    VX_err : array, float
        formal uncertainty of VX component, mm/yr
    VY_err : array, float
        formal uncertainty of VY component, mm/yr
    VZ_err : array, float
        formal uncertainty of VZ component, mm/yr
    VU : array, float
        Velocity of U component, mm/yr
    VE : array, float
        Velocity of E component, mm/yr
    VN : array, float
        Velocity of N component, mm/yr
    VU_err : array, float
        formal uncertainty of VU component, mm/yr
    VE_err : array, float
        formal uncertainty of VE component, mm/yr
    VN_err : array, float
        formal uncertainty of VN component, mm/yr
    '''

    # empty list for store data
    staname = []
    # XYZ
    VX = []
    VX_err = []
    VY = []
    VY_err = []
    VZ = []
    VZ_err = []
    # UEN
    VU = []
    VU_err = []
    VE = []
    VE_err = []
    VN = []
    VN_err = []

    for line in open(datafile, 'r'):
        if line[0] != '#':
            if line[:7] == 'STA_GVX':
                staname.append(line[10:18].rstrip())
                VX.append(float(line[23:32]))
                VX_err.append(float(line[36:44]))
                VY.append(float(line[49:58]))
                VY_err.append(float(line[62:70]))
                VZ.append(float(line[75:84]))
                VZ_err.append(float(line[88:96]))
            elif line[:7] == 'STA_GVU':
                VU.append(float(line[23:32]))
                VU_err.append(float(line[36:44]))
                VE.append(float(line[49:58]))
                VE_err.append(float(line[62:70]))
                VN.append(float(line[75:84]))
                VN_err.append(float(line[88:96]))
            else:
                print("Something must be wrong! Please check your file")
                exit()

    # List -> array, a rather stupid way.
    staname = np.array(staname)
    # XYZ
    VX = np.array(VX)
    VX_err = np.array(VX_err)
    VY = np.array(VY)
    VY_err = np.array(VY_err)
    VZ = np.array(VZ)
    VZ_err = np.array(VZ_err)
    # UEN
    VU = np.array(VU)
    VU_err = np.array(VU_err)
    VE = np.array(VE)
    VE_err = np.array(VE_err)
    VN = np.array(VN)
    VN_err = np.array(VN_err)

    return [staname, VX, VX_err, VY, VY_err, VZ, VZ_err,
            VU, VU_err, VE, VE_err, VN, VN_err]


# Retrieve estimates.
if len(sys.argv) == 1:
    datafile = 'result/test.vel'
else:
    datafile = sys.argv[1]
[staname, VX, VX_err, VY, VY_err, VZ, VZ_err,
 VU, VU_err, VE, VE_err, VN, VN_err] = read_vel(datafile)
print(staname[0],
      VX[0],
      VX_err[0],
      VY[0],
      VY_err[0],
      VZ[0],
      VZ_err[0],
      VU[0],
      VU_err[0],
      VE[0],
      VE_err[0],
      VN[0],
      VN_err[0])
# ------------------------------ END -----------------------------------
