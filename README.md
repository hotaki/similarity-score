# similarity-score.py

A script for peak assignment of IR spectra using similarity scores.


## Files

- README.md: This file

- similarity-score.py: Script for peak assignment using similarity scores

- run_similarity-score.sh: Script to run similarity-score.py

- data_spectrum1.dat: Sample input file 1

- data_spectrum2.dat: Sample input file 2


## Usage

- In data file, a set of peak position (i.e., frequency) and height (i.e., intensity) should be written in one row. The first column is the frequency and the second column is the intensity. 

- In similarity-score.py, 
	- The data are sorted in decreasing order of frequency. 

	- Intensities are normalized so that the maximum value is equal to one.
	
	- The inputfile with more (less) peaks is automatically assigned to data2 (data1) (i.e., the order of inputfiles 1 & 2 does not affect the result).


- The line which begins with "#" or "@" will be ignored (can be used for coment liens).

- A weight parameter "alpha" should be specified.

- To run similarity-score.py, type (see also run_similarity-score.sh)

```bash
$ python3 similarity-score.py [inputfile1] [inputfile2] [alpha] > [outputfile]
```


