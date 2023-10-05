#!/bin/bash
alpha=50
file1=data_spectrum1.dat
file2=data_spectrum2.dat
basename_out=score_result_alpha

output=$basename_out$alpha.out

python3 similarity-score.py $file1 $file2 $alpha > $output


