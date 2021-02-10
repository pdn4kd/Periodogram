#!/usr/bin/env python3
# John Berberian
# This file contains constants and defaults internal to
# the program.

import math

# These are the scaling factors for estimating how long it
# will take the program to run. They were derived on a
# cluster running at 2.8 GHz.
# Adjust as needed (or just to taste).
BLS_T0 = 1.39e-6
LS_T0 = 1.964e-6
PLAV_T0 = 7.878398e-7
# This is a function for estimating how time scales
# with more threads.
SCALING_FUNC = lambda x: 1 / math.sqrt(x)

# These are some default values for CLI argument parsing.
DEFAULT_HDU = UNSET_VALUE
DEFAULT_CONSTRAINT = UNSET_VALUE
DEFAULT_MAXPERIOD = UNSET_VALUE
DEFAULT_MINPERIOD = UNSET_VALUE
DEFAULT_PSTEP = "exp"
DEFAULT_OVERSAMPLE = 1
DEFAULT_SUBSTEP = 0.10
DEFAULT_DFREQ = UNSET_VALUE
DEFAULT_NOUT = 500
DEFAULT_SMOOTH = 0.06
DEFAULT_NPHASED = 50
DEFAULT_SIG_THRESH = 1.0
DEFAULT_POW_NUM = UNSET_VALUE
DEFAULT_POW_MEAN = UNSET_VALUE
DEFAULT_POW_SD = UNSET_VALUE
DEFAULT_ALGO = "bls"
DEFAULT_NBINS = -32768
DEFAULT_QMIN = 0.05
DEFAULT_QMAX = 0.10
DEFAULT_DELIMITER = ','
DEFAULT_NPROC = mp.cpu_count()

MIN_NDATA = 2

# These are constants. They must be set to these values
# to ensure that the program is able to run properly.
# Change them at your own risk.
UNSET_VALUE = -32768
MAXSTR = 32768
TINY_NUM = 0.0000001
UNSET_MEAN = -1e7
