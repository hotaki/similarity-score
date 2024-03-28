![](https://img.shields.io/badge/Python-v3.x-green)
[![](https://img.shields.io/badge/DOI-10.1039/D4CP00064A-blue)](https://doi.org/10.1039/D4CP00064A)

# similarity-score.py

A python script for peak assignment of IR spectra using similarity scores.


## Author

- Hiroki OTAKI, Graduate School of Biomedical Sciences, Nagasaki University, Japan


## Files

- README.md: This file

- similarity-score.py: Script for peak assignment using similarity scores

- run_similarity-score.sh: Sample script to run similarity-score.py

- data_spectrum1.dat: Sample input file 1

- data_spectrum2.dat: Sample input file 2


## Usage

- In data file, a set of peak position (i.e., frequency) and height (i.e., intensity) should be written in one row. The first column is the frequency and the second column is the intensity. 

- In similarity-score.py, 
	- The data are sorted in decreasing order of frequency. 

	- Intensities are normalized so that the maximum value is equal to one.
	
	- The input file with more (less) peaks is automatically assigned to data2 (data1) (i.e., the order of input files 1 & 2 for submitting this script does not affect the result).

- The line which begins with "#" or "@" will be ignored (can be used for comment lines).

- A weight parameter "alpha" should be specified. For definition of alpha, see reference.

- The number of ranks (Nrank) for output can be specified (if empty, Nrank is set to 10). When Nrank is set to zero, all results will be output.

- To run similarity-score.py, type (see also run_similarity-score.sh)

```bash
$ python3 similarity-score.py [input file1] [input file2] [alpha] [Nrank] > [output file]
```


## Tips (may be useful for pasting into Excel)

- Get table of similarity scores (including rank, S1, S2, MAD) from output file

```bash
$ cat [output file] | grep -e '^#[!]' > scores.dat
```

- Get results of peak assignment from output file

```bash
$ cat [output file] | grep -e '^#[$]' > assignment.dat
```

- Get both of the above

```bash
$ cat [output file] | grep -e '^#[!$]' > result.dat
```


## Citation

Please cite:

- H. Otaki, S.-I. Ishiuchi, M. Fujii, Y. Sugita, and K. Yagi, **Similarity scores of vibrational spectra reveal the atomistic structure of pentapeptides in multiple basins.** *Physical Chemistry Chemical Physics* 2024, 26 (13), 9906-9914. DOI: [10.1039/D4CP00064A](https://doi.org/10.1039/D4CP00064A)

