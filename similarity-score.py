# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++
#--    similarity-score.py
#--
#--                  written by Hiroki Otaki
#+++++++++++++++++++++++++++++++++++++++++++++++

import os
import sys
import math
import numpy as np
import itertools

list_peakA = []
list_peakB = []

fileA=sys.argv[1]
fileB=sys.argv[2]

#-- factor for weight of intensity compared to frequency
alpha=float(sys.argv[3])

fA = open(fileA, "r")
fB = open(fileB, "r")

#--
#-- Read Data A
#--
data = fA.readlines()
Nlines = len(data)
cnt = 0

for j in range(Nlines):
    if ( data[j][0] == "#" or data[j][0] == "@" ): 
        continue

    if ( data[j].find("TER") >= 0 or data[j].find("END") >= 0 ): 
        break

    cnt = cnt + 1
    wvn = float(data[j].split()[0])
    inten = float(data[j].split()[1])

    list_peakA.append([wvn, inten])

#-- Sort with frequency
list_peakA.sort(key=lambda x:x[0], reverse=True)

#--
#-- Read Data A END
#--


#--
#-- Read Data B
#--
data = fB.readlines()
Nlines = len(data)
cnt = 0

for j in range(Nlines):
    if ( data[j][0] == "#" or data[j][0] == "@" ): 
        continue

    if ( data[j].find("TER") >= 0 or data[j].find("END") >= 0 ): 
        break

    cnt = cnt + 1
    wvn = float(data[j].split()[0])
    inten = float(data[j].split()[1])

    list_peakB.append([wvn, inten])

#-- Sort with frequency
list_peakB.sort(key=lambda x:x[0], reverse=True)

#--
#-- Read Data B END
#--

print("#--")
print("#-- Data A: ", fileA)
print("#--")
for j in range(len(list_peakA)):
    print(list_peakA[j][0], list_peakA[j][1])

print("")
print("#--")
print("#-- Data B: ", fileB)
print("#--")
for j in range(len(list_peakB)):
    print(list_peakB[j][0], list_peakB[j][1])


peakA = np.array(list_peakA)
peakB = np.array(list_peakB)


if (len(peakA) < len(peakB)):
    file_1 = fileA
    file_2 = fileB
    peak_1 = peakA
    peak_2 = peakB
else:
    file_1 = fileB
    file_2 = fileA
    peak_1 = peakB
    peak_2 = peakA


freq_1 = peak_1[:,0]
inten_1 = peak_1[:,1]

freq_2 = peak_2[:,0]
inten_2 = peak_2[:,1]

#--
#-- Normalization
#--
max_inten = max(inten_1)
peak_1[:,1] = peak_1[:,1]/max_inten

max_inten = max(inten_2)
peak_2[:,1] = peak_2[:,1]/max_inten
#--
#-- Normalization END
#--

print("")
print("#-- File 1")
print(file_1)
print("#-- File 2")
print(file_2)

print("")
print("#-- Check of normalized data")
print("#-- Data 1")
print(freq_1)
print(inten_1)
print("")
print("#-- Data 2")
print(freq_2)
print(inten_2)


#-- list of assigned frequency (N1 elements)
freq_data2_selected = []

#-- list of assigned peak (Freq & Intensity, N1*2 elements)
peak_data2_selected = []

#-- [id, shift=ave(delta), score2, rankS2]
list_score2 = []

#-- [id, score2, rankS2, score1, rankS1]
list_scores = []


N1 = int(len(peak_1))
N2 = int(len(peak_2))

print("")
print("#-- N1 (number of peaks of data 1): ", N1)
print("#-- N2 (number of peaks of data 2): ", N2)
if ( N1 > N2 ):
    print("Error: N2 must be larger than (or equal to) N1 !!")
    exit()

print("")

list_1 = np.array(list(range(N1)))
list_2 = np.array(list(range(N2)))

print("#-- List_1")
print(list_1)
print("")
print("#-- List_2")
print(list_2)
print("")


list_selected_data2 = list(itertools.combinations(list_2,N1))

Ncombi = len(list_selected_data2)
print("#-- Ncombi (number of combinations to select peaks for assignment): ", Ncombi)
print("")


#--
#-- calc score2 for each peak assignment
#--
for j in range(Ncombi):

    freq_data2_selected.append(np.array([ peak_2[k][0] for k in list_selected_data2[j] ]))
    peak_data2_selected.append(np.array([ peak_2[k] for k in list_selected_data2[j] ]))

    print("list_selected_data2: ", list_selected_data2[j])
    print("freq_data2_selected: ", freq_data2_selected[j])
    print("freq_1: ", freq_1)

    deltafreq = freq_data2_selected[j] - freq_1
    deltafreq2 = (freq_data2_selected[j] - freq_1)**2
    print("deltafreq: ", deltafreq)
    print("deltafreq2: ", deltafreq2)

    ave_deltafreq = np.sum(deltafreq) / float(N1)
    ave_deltafreq2 = np.sum((deltafreq)**2) / float(N1)
    min_delta2 = N1 * (ave_deltafreq2 - ave_deltafreq**2)
    score2 = math.sqrt(ave_deltafreq2 - ave_deltafreq**2)

    print("ave_deltafreq: ", ave_deltafreq)
    print("ave_deltafreq2: ", ave_deltafreq2)
    print("score2: ", score2)
    print()

    #-- index for combination, shift, score1
    list_score2.append([j,ave_deltafreq,score2])


#--
#-- sort with score2
#--
list_score2.sort(key=lambda x:x[2])

#--
#-- get minimum of score2
#-- and append relative value of score2
#--
minS2 = list_score2[0][2]
for j in range(len(list_score2)):
    list_score2[j].append(list_score2[j][2] - minS2)

#--
#-- append rankS2 (starts from 1)
#--
for j in range(len(list_score2)):
    list_score2[j].append(j+1)

#--
#-- output of peak assignment and scores
#--
print()
print("#---------------------------")
print("       Result (Score2)")
print("#---------------------------")
print()
for j in range(len(list_score2)):

    idx = list_score2[j][0]
    shift = list_score2[j][1]
    score2 = list_score2[j][2]
    rel_score2 = list_score2[j][3]
    rankS2 = list_score2[j][4]
    print("rankS2: ", rankS2, ": ", list_score2[j])
    print("list_selected_data1: ", list_selected_data2[idx])
    print("freq1: ", freq_1)
    print("freq2: ", freq_data2_selected[idx])
    print()


#--
#-- calc score for assignment with peak position and intensity
#--
print()
print("#--------------------------------------------------------------")
print("  Calc score for assignment with peak position and intensity")
print("#--------------------------------------------------------------")
print()

for j in range(len(list_score2)):

    idx = list_score2[j][0]
    shift = list_score2[j][1]
    score2 = list_score2[j][2]
    rel_score2 = list_score2[j][3]
    rankS2 = list_score2[j][4]
    print("list_selected_data2: ", list_selected_data2[idx])
    print("freq_1: ", freq_1)
    print("freq_2-1: ", freq_data2_selected[idx])
    print("freq_2-2: ", peak_data2_selected[idx][:,0])
    print("inten_1: ", inten_1)
    print("inten_2: ", peak_data2_selected[idx][:,1])
    print()

    deltafreq = peak_data2_selected[idx][:,0] - freq_1
    deltainten = peak_data2_selected[idx][:,1] - inten_1

    score1 = math.sqrt((np.sum(deltafreq**2) + (alpha**2) * np.sum(deltainten**2)) / float(N1))

    #-- Calc. mean absolute deviation
    mad = np.average(np.abs(deltafreq))

    #-- index, score2, rel_score2, rankS2, score1, mad
    list_scores.append([idx, score2, rel_score2, rankS2, score1, mad])


#--
#-- Sort with score1
#--
list_scores.sort(key=lambda x:x[4])

#--
#-- append rankS1 (starts from 1)
#--
for j in range(Ncombi):
    list_scores[j].append(j+1)


print()
print("#---------------------------")
print("       Result (Final)")
print("#---------------------------")
print()

# for j in range(10):
for j in range(Ncombi):
    idx = list_scores[j][0]
    print("# rankS1: {0}".format(list_scores[j][6]))
    print("# score1: {0:.3f}".format(list_scores[j][4]))
    print("# index: {0}".format(list_scores[j][0]))
    print("# rankS2: {0}".format(list_scores[j][3]))
    print("# score2: {0:.3f}".format(list_scores[j][1]))
    print("# score2(relative): {0:.3f}".format(list_scores[j][2]))
    print("# MAD(cm-1): {0:.2f}".format(list_scores[j][5]))
    print("# list_selected_data2: ", list_selected_data2[idx])


    print("#")
    print("#! rankS1    score1    rankS2    score2    score2(relative)    MAD(cm-1)")
    print("#!    {0}      {1:.3f}      {2}      {3:.3f}       {4:.3f}           {5:.2f}"\
        .format(list_scores[j][6], list_scores[j][4], list_scores[j][3], list_scores[j][1], list_scores[j][2], list_scores[j][5]))
    print("#")
    print("#$   freq1          freq2        delta_freq       inten1          inten2")
    print("#$   (cm-1)         (cm-1)         (cm-1)       (arb.unit)      (arb.unit)")
    for k in range(len(freq_1)):
        delta = freq_1[k] - peak_data2_selected[idx][k,0]
        print("#$   {0:>8.2f}    {1:>8.2f}    {2:>7.2f}    {3:>7.3f}    {4:>7.3f}"\
            .format(freq_1[k], peak_data2_selected[idx][k,0], delta, inten_1[k], peak_data2_selected[idx][k][1]))
    print()


