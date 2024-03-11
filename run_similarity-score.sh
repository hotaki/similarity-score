#!/bin/bash
file1=data_spectrum1.dat
file2=data_spectrum2.dat
basename_out=score_result_alpha

#-- alpha: Factor for weight of intensity with respect to frequency
alpha=50

#-- Nrank: Number of ranks to be output (from rank 1)
#-- Default (empty): 10
#-- All: 0
Nrank=0


output=$basename_out$alpha.out

python3 similarity-score.py $file1 $file2 $alpha $Nrank > $output


