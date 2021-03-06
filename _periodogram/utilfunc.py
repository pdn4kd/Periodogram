#!/usr/bin/env python3
# This file contains a few utilities used throughout the program.

import copy
from _periodogram.constants import *


# This takes in a matrix, and returns the transpose.
# Note: assumes rectangular matrix
def transpose(matrix):
    n = []
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if j == len(n):
                n.append([matrix[i][j]])
            else:
                n[j].append(matrix[i][j])
    return n


# Returns an array of length num, filled with copies
# of the inlist array.
def makeArrOfCopies(inlist, num):
    bigArr = [[]] * num
    for k in inlist:
        for i in range(len(bigArr)):
            bigArr[i].append(k)
    return bigArr


# Returns a single copy of the input arr.
# Switched over to deepcopy, because
# python internals are generally more
# efficient. Just hoping.
def makeCopy(arr):
    return copy.deepcopy(arr)


# Returns a single copy of the input arr.
# Now unused, replaced with copy.deepcopy.
def makeCopy_OLD(arr):
    newArr = []
    for k in arr:
        newArr.append(k)
    return newArr


# Finds the indices to split the period array at
# for multiprocessing. Hopefully, should lump the
# fractional bits onto the last array.
def getSplitNums(nsamp, nproc):
    n = nsamp / nproc
    k = math.floor(n)
    startArr, endArr, myNsamp = [], [], nsamp
    while myNsamp >= k:
        startArr.append(math.floor(nsamp - myNsamp))
        myNsamp -= n
        endArr.append(math.floor(nsamp - myNsamp))
    return startArr, endArr


# Turns a 2d array into a 1d array, by appending
# elements in order.
def merge_arrs(arr2d):
    newArr = []
    for l in arr2d:
        for e in l:
            newArr.append(e)
    return newArr


# Sorts an array's columns according to the values in
# one of the columns, specified by sortIdx. Each row
# will stick together, but the row order will change.
def sortColumns(arr2d, sortIdx):
    # Check that the sortIdx is valid
    if sortIdx >= DATA_FIELD_TYPE.DATA_N_TYPES:
        raise ValueError('Inappropriate value:\nsortIdx is greater than maximum value!')

    # Make a temporary array for sorting
    sortArr = []
    for i in range(len(arr2d[sortIdx])):
        # first element of each element in sortArr is the value, the
        # second is its initial index, to keep track of where each element
        # went.
        sortArr.append([arr2d[sortIdx][i], i])

    # Sort sortArr. This will sort by the first element (the value),
    # and only use the second element (the index) as a tie-breaker,
    # which is fine for our purposes
    sortArr.sort()

    # Now make all of the elements of the columns in arr2d rearrange
    # themselves to match the order of sortArr
    for i in range(len(arr2d)):
        # make a temporary column variable
        col = []
        for k in sortArr:
            # fill it with the elements in the right order
            col.append(arr2d[i][k[1]])
        # and set it
        arr2d[i] = col

    # Return the now-sorted array
    return arr2d


# New version of mod function, once I remembered
# that python has a builtin
def mod(n, m):
    return n % m


# Finds the smallest nonnegative
# number that is a multiple of m away from n.
# Recursive, for fun.
def mod_OLD(n, m):
    if m <= 0:
        raise ValueError("Inappropriate value: m must be positive!")
    if 0 <= n < m:
        return n
    if n < 0:
        return mod(n + m, m)
    else:
        return mod(n - m, m)


# estimateProcessingTime()
# Function to estimate the time required to execute the command with
# the input values of nsamp, ndata, nbins, and qmax.
# The relative time spent in the different loops of BLS is empirically
# estimated. For really reliable estimates, might do linear regression.
def estimateProcessingTime(nsamp, ndata, args, qmax, algo):
    if algo == "bls":
        if args.nbins == DEFAULT_NBINS:
            if ndata <= 500:
                args.nbins = 50
            elif ndata <= 20000:
                args.nbins = int(ndata / 10)
            else:
                args.nbins = 2000
        scaledNsamp = BLS_T0 * nsamp
        timeEst = (scaledNsamp * (ndata + (2.096 * args.nbins) + ((qmax * args.nbins) * (-2.6 + 0.38 * args.nbins))))
    elif algo == "ls":
        timeEst = ((LS_T0 * nsamp) * ndata)
    elif algo == "plav":
        timeEst = (((PLAV_T0 * nsamp) * ndata) * math.log2(ndata))
    else:
        raise ValueError("PeriodogramType: invalid value " + algo)
    if timeEst == 0:
        # this must have been a non-fatal error: note it
        timeEst = -1
    else:
        # Scale the timeEst based on SCALING_FUNC()
        timeEst *= SCALING_FUNC(args.nproc)
    return timeEst
