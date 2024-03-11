# -*- coding: UTF-8 -*-
####################################################
#--    similarity-score.py
#--
#--                                  ver. 20240304
#--                        written by Hiroki Otaki
####################################################
import os
import sys
import math
import time
import datetime
import numpy as np
import itertools
from decimal import Decimal, ROUND_HALF_UP


print ("****************************************************")
print ("*                                                  *")
print ("*             similarity-score.py                  *")
print ("*                                                  *")
print ("*                              version 20240304    *")
print ("*                              (c) Hiroki Otaki    *")
print ("*                                                  *")
print ("****************************************************")
print ("")
start_time = time.time()
start_date = datetime.datetime.now()
print("Submitted at:",start_date.strftime('%b. %d(%a) %Y %H:%M:%S'))
print()

print()
print("#------------------------")
print("    Read input files")
print("#------------------------")
print()

list_peakA = []
list_peakB = []

fileA=sys.argv[1]
fileB=sys.argv[2]

#-- alpha: Factor for weight of intensity compared to frequency
alpha=float(sys.argv[3])

#-- Nrank: Number of ranks to be output (from rank 1)
if ( len(sys.argv) == 4 ):
    Nrank = 10

elif ( len(sys.argv) == 5 ):
    Nrank = int(sys.argv[4])



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

#--
#-- Output of Files A & B
#--
print("Input file A: ", fileA)
print("  Frequency(cm-1)   Intensity")
for j in range(len(list_peakA)):
    print("{0:>14.6f}  {1:>14.8f}"\
    .format(list_peakA[j][0], list_peakA[j][1]))

print()

print("Input file B: ", fileB)
print("  Frequency(cm-1)   Intensity")
for j in range(len(list_peakB)):
    print("{0:>14.6f}  {1:>14.8f}"\
    .format(list_peakB[j][0], list_peakB[j][1]))
print()
#--
#-- Output of Files A & B END
#--

#--
#-- Assignment of Data
#--
print()
print("#---------------------------------")
print("    Assignment of input files")
print("#---------------------------------")
print()
print("The input file with more (less) peaks is assigned to Data 2 (Data 1)")

peakA = np.array(list_peakA)
peakB = np.array(list_peakB)

if (len(peakA) < len(peakB)):
    file_1 = fileA
    file_2 = fileB
    peak_1 = peakA
    peak_2 = peakB
    print("File A has been assigned to Data 1")
    print("File B has been assigned to Data 2")
    print()
else:
    file_1 = fileB
    file_2 = fileA
    peak_1 = peakB
    peak_2 = peakA
    print("File B has been assigned to Data 1")
    print("File A has been assigned to Data 2")
    print()


freq_1 = peak_1[:,0]
inten_1 = peak_1[:,1]
N1 = int(len(peak_1))

freq_2 = peak_2[:,0]
inten_2 = peak_2[:,1]
N2 = int(len(peak_2))

if ( N1 > N2 ):
    print("Error: N2 must be larger than (or equal to) N1")
    exit()


print("Data 1")
print("Input file: ", file_1)
print("    v1(cm-1)           I1")
for j in range(N1):
    print("{0:>14.6f}  {1:>14.8f}"\
    .format(freq_1[j], inten_1[j]))
print()

print("Data 2")
print("Input file: ", file_2)
print("    v2(cm-1)           I2")
for j in range(N2):
    print("{0:>14.6f}  {1:>14.8f}"\
    .format(freq_2[j], inten_2[j]))
print()

#--
#-- Assignment of Data END
#--

#--
#-- Normalization
#--
print()
print("#--------------------------------------")
print("    Normalization of peak intensity")
print("#--------------------------------------")
print()
max_inten = max(inten_1)
peak_1[:,1] = peak_1[:,1]/max_inten

max_inten = max(inten_2)
peak_2[:,1] = peak_2[:,1]/max_inten


print()
print("Normalized Data 1")
print("Filename: ", file_1)
print("N1 (Number of peaks): ", N1)
print(" ID       v1      I1(normalized)")
print("        (cm-1)     (arb.unit)")
for j in range(len(freq_1)):
    print("{0:>3}     {1:>6.2f}     {2:>7.4f}"\
        .format(j, freq_1[j], inten_1[j]))


print()
print("Normalized Data 2")
print("Filename: ", file_2)
print("N2 (Number of peaks): ", N2)
print(" ID       v2      I2(normalized)")
print("        (cm-1)     (arb.unit)")
for j in range(len(freq_2)):
    print("{0:>3}     {1:>6.2f}     {2:>7.4f}"\
        .format(j, freq_2[j], inten_2[j]))

print()

#--
#-- Normalization END
#--

#-- list of assigned frequency (N1 elements)
freq_data2_selected = []

#-- list of assigned peak (Freq & Intensity, N1*2 elements)
peak_data2_selected = []

#-- [id, shift=ave(delta), S2, rankS2]
list_score2 = []

#-- [id, S2, rankS2, S1, rankS1]
list_scores = []


list_1 = np.array(list(range(N1)))
list_2 = np.array(list(range(N2)))

# print("")
# print("#-- List_1")
# print(list_1)
# print("")
# print("#-- List_2")
# print(list_2)
# print("")



list_selected_data2 = list(itertools.combinations(list_2,N1))
list_not_selected_data2 = []

Ncombi = len(list_selected_data2)

for j in range(Ncombi):
    list_not_selected_data2.append(tuple([ k for k in range(N2) if k not in list_selected_data2[j] ]))


#--
#-- Setting of maxrank
#--
if ( Nrank == 0 ):
    maxrank = Ncombi

elif ( len(sys.argv) == 4 ):
    maxrank = Nrank

else:
    maxrank = min(Nrank, Ncombi)


print()
print("#-------------------------")
print("    Output information")
print("#-------------------------")
print()
print("Ncombi (number of combinations to select peaks for assignment): ", Ncombi)
print("Nrank (0: All): ", Nrank)
print("==> Results from rank 1 to {0} will be output".format(maxrank))
print()


#--
#-- Calculation of S2 for each peak assignment
#--
print()
print("#-------------------------")
print("    Calculation of S2")
print("#-------------------------")
print()

for j in range(Ncombi):

    freq_data2_selected.append(np.array([ peak_2[k][0] for k in list_selected_data2[j] ]))
    peak_data2_selected.append(np.array([ peak_2[k] for k in list_selected_data2[j] ]))

    print("combination No: ", j)
    print("ID list of selected peaks in Data 2: ", list_selected_data2[j])
    # print("frequency of selected peaks in data2: ", freq_data2_selected[j])
    # print("frequency of data1: ", freq_1)

    deltafreq = freq_data2_selected[j] - freq_1
    deltafreq2 = (freq_data2_selected[j] - freq_1)**2
    # print("deltafreq: ", deltafreq)
    # print("deltafreq2: ", deltafreq2)

    ave_deltafreq = np.sum(deltafreq) / float(N1)
    ave_deltafreq2 = np.sum((deltafreq)**2) / float(N1)
    min_delta2 = N1 * (ave_deltafreq2 - ave_deltafreq**2)
    score2 = math.sqrt(ave_deltafreq2 - ave_deltafreq**2)

    # print("ave_deltafreq: ", ave_deltafreq)
    # print("ave_deltafreq2: ", ave_deltafreq2)
    print("S2(cm-1): {0:.1f}".format(score2))
    print()

    #-- index for combination No, shift, S2
    list_score2.append([j, ave_deltafreq, score2])

print()
print("#-----------------------------")
print("    Calculation of S2 Done")
print("#-----------------------------")
print()

#--
#-- Sort with S2
#--
list_score2.sort(key=lambda x:x[2])

#--
#-- Get minimum of S2
#-- and append relative value of S2 to list_score2
#--
minS2 = list_score2[0][2]
for j in range(len(list_score2)):
    list_score2[j].append(list_score2[j][2] - minS2)

#--
#-- Append rankS2 (starts from 1)
#--
for j in range(len(list_score2)):
    list_score2[j].append(j+1)

#--
#-- Output of peak assignment and scores
#--
print()
print("#---------------------------")
print("       Result (S2)")
print("#---------------------------")
print()
# for j in range(len(list_score2)):
for j in range(maxrank):

    idx = list_score2[j][0]
    shift = list_score2[j][1]
    score2 = list_score2[j][2]
    rel_score2 = list_score2[j][3]
    rankS2 = list_score2[j][4]

    print("#  rankS2: {0}".format(rankS2))
    print("#  S2(cm-1): {0:.1f}".format(score2))
    print("#  DeltaS2(cm-1): {0:.1f}".format(rel_score2))
    print("#  combination No: {0}".format(idx))
    print("#  ID list of selected peaks in Data 2: ", list_selected_data2[idx])
    print("#  ID list of NOT selected peaks in Data 2: ", list_not_selected_data2[idx])
    print("#")

    freq_1_out = [ float(Decimal(str(freq_1[k])).quantize(Decimal('0.01'), ROUND_HALF_UP)) for k in range(N1) ]
    freq_2_out = freq_data2_selected[idx].tolist()

    for k in range(len(list_not_selected_data2[idx])):
        freq_1_out.append("----")
        freq_2_out.append(freq_2[ list_not_selected_data2[idx][k] ])

    if ( len(freq_2_out) != N2 ):
        print("Error: freq_2_out is not equal to N2")
        exit()

    freq_out=[]

    for k in range(N2):
        freq_out.append([freq_1_out[k],freq_2_out[k]])

    freq_out.sort(key=lambda x:x[1], reverse=True)

    print("#   v1(cm-1)  v2(cm-1)")
    for k in range(N2):
        if ( type(freq_out[k][0]) == str ):
            print("#  {0:^8}  {1:>8.2f}  *"\
                .format(freq_out[k][0], freq_out[k][1]))
        else:
            print("#  {0:>8.2f}  {1:>8.2f}"\
                .format(freq_out[k][0], freq_out[k][1]))

    print("#")
    print("#                      (* ... discarded in the assignment)")
    print("#")
    print()


#--
#-- Calculation of S1
#--
print()
print("#-------------------------")
print("    Calculation of S1")
print("#-------------------------")
print()

for j in range(len(list_score2)):

    idx = list_score2[j][0]
    shift = list_score2[j][1]
    score2 = list_score2[j][2]
    rel_score2 = list_score2[j][3]
    rankS2 = list_score2[j][4]

    print("combination No: {0}".format(idx))
    print("ID list of selected peaks in Data 2: ", list_selected_data2[idx])
    # print("freq1: ", freq_1)
    # print("freq2: ", peak_data2_selected[idx][:,0])
    # print("inten1: ", inten_1)
    # print("inten2: ", peak_data2_selected[idx][:,1])

    deltafreq = peak_data2_selected[idx][:,0] - freq_1
    deltainten = peak_data2_selected[idx][:,1] - inten_1

    score1 = math.sqrt((np.sum(deltafreq**2) + (alpha**2) * np.sum(deltainten**2)) / float(N1))

    print("S1(cm-1): {0:.1f}".format(score1))
    print()

    #-- Calc. mean absolute deviation
    mad = np.average(np.abs(deltafreq))

    #-- index, S2, rel_S2, rankS2, S1, mad
    list_scores.append([idx, score2, rel_score2, rankS2, score1, mad])

print()
print("#-----------------------------")
print("    Calculation of S1 Done")
print("#-----------------------------")
print()

#--
#-- Sort with S1
#--
list_scores.sort(key=lambda x:x[4])

#--
#-- Append rankS1 (starts from 1)
#--
for j in range(Ncombi):
    list_scores[j].append(j+1)


print()
print("#---------------------------")
print("      Result (S1 & S2)")
print("#---------------------------")
print()

print("#$")
print("#$ Data 1: ", file_1)
print("#$ Data 2: ", file_2)
print("#$")
print()

# for j in range(Ncombi):
for j in range(maxrank):
    idx = list_scores[j][0]
    print("#$-------------------------------------------------------------------------")
    print("#  rankS1: {0}".format(list_scores[j][6]))
    print("#  S1(cm-1): {0:.2f}".format(list_scores[j][4]))
    print("#  combination No: {0}".format(list_scores[j][0]))
    print("#  rankS2: {0}".format(list_scores[j][3]))
    print("#  S2(cm-1): {0:.2f}".format(list_scores[j][1]))
    print("#  DeltaS2(cm-1): {0:.2f}".format(list_scores[j][2]))
    print("#  MAD(cm-1): {0:.2f}".format(list_scores[j][5]))
    print("#  ID list of selected peaks in Data 2: ", list_selected_data2[idx])
    print("#  ID list of NOT selected peaks in Data 2: ", list_not_selected_data2[idx])


    print("#!")
    print("#! rankS1    S1   rankS2    S2      DeltaS2    MAD")
    print("#!         (cm-1)         (cm-1)    (cm-1)    (cm-1)")
    print("#!  {0:>3}  {1:>8.2f}  {2:>3}  {3:>8.2f}  {4:>8.2f}  {5:>8.2f}"\
        .format(list_scores[j][6], list_scores[j][4], list_scores[j][3], list_scores[j][1], list_scores[j][2], list_scores[j][5]))
    print("#$")
    print("#$ rankS1: {0}".format(list_scores[j][6]))
    print("#$     v1        v2       dv(v2-v1)     I1         I2")
    print("#$   (cm-1)    (cm-1)      (cm-1)    (arb.unit) (arb.unit)")

    dv = peak_data2_selected[idx][:,0] - freq_1

    freq_1_out = [ float(Decimal(str(freq_1[k])).quantize(Decimal('0.01'), ROUND_HALF_UP)) for k in range(N1) ]
    inten_1_out = [ float(Decimal(str(inten_1[k])).quantize(Decimal('0.001'), ROUND_HALF_UP)) for k in range(N1) ]
    freq_2_out = freq_data2_selected[idx].tolist()
    inten_2_out = peak_data2_selected[idx][:,1].tolist()
    dv_out = [ float(Decimal(str(dv[k])).quantize(Decimal('0.01'), ROUND_HALF_UP)) for k in range(N1) ]

    for k in range(len(list_not_selected_data2[idx])):
        freq_1_out.append("----")
        inten_1_out.append("----")
        freq_2_out.append(freq_2[ list_not_selected_data2[idx][k] ])
        inten_2_out.append(inten_2[ list_not_selected_data2[idx][k] ])
        dv_out.append("----")

    if ( len(freq_2_out) != N2 ):
        print("Error: freq_2_out is not equal to N2")
        exit()

    data_out=[]

    for k in range(N2):
        data_out.append([freq_1_out[k],freq_2_out[k],dv_out[k],inten_1_out[k],inten_2_out[k]])

    data_out.sort(key=lambda x:x[1], reverse=True)

    for k in range(N2):
        if ( type(data_out[k][0]) == str ):
            print("#$  {0:^8}  {1:>8.2f}    {2:>7}    {3:>7}    {4:>7.3f}  *"\
                .format(data_out[k][0], data_out[k][1], data_out[k][2], data_out[k][3], data_out[k][4]))
        else:
            print("#$  {0:>8.2f}  {1:>8.2f}    {2:>7.2f}    {3:>7.3f}    {4:>7.3f}"\
                .format(data_out[k][0], data_out[k][1], data_out[k][2], data_out[k][3], data_out[k][4]))

    print("#$")
    print("#$                       (* ... discarded in the assignment)")
    print("#$")
    print()


