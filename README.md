DelphiPKA is a DelPhi-based C++ program, allowing to predict pKa's for ionizable groups in proteins, RNA and DNA.
Unique approach stems from:
    a) Use gaussian-based smooth function to mimic conformational changes associated with ionization changes.
    b) Calculate the electrostatic energy without defining molecular surface.

For questions and help, visit http://compbio.clemson.edu/forum/ or email to delphi@g.clemson.edu

User Manual can be found [here](http://compbio.clemson.edu/pka_webserver/assets/manual/DelPhiPKa_User_Manual.html)

If the use of DelPhiPKa results to a publication, please cite the following references:

*1.   Lin Wang, Lin Li, and Emil Alexov. "pKa predictions for proteins, RNAs and DNAs with the Gaussian dielectric function using DelPhiPKa." Proteins. (2015) Sep 26, doi: 10.1002/prot.24935*

*2.   Lin Wang, Min Zhang, and Emil Alexov. "DelPhiPKa Web Server: Predicting pKa of proteins, RNAs and DNAs." Bioinformatics. (2015) Oct 29, doi: 10.1093/bioinformatics/btv607*
## Building and running (branch nucleic-acids)

Needs a C++11 compiler with OpenMP, Open MPI (`mpic++`), GSL and the Boost headers (`boost/lexical_cast.hpp`, `boost/any.hpp`).
On Fedora: `sudo dnf install gcc-c++ openmpi-devel gsl-devel boost-devel`, then `export PATH=/usr/lib64/openmpi/bin:$PATH` and `make -j4`.

    ./delphiPKa run.prm                              # one process, one thread
    scripts/run_parallel.sh -n 4 run.prm               # 4 MPI ranks, each taking a share of the titratable sites (add -t 2 for OpenMP threads inside each solve)

`run_parallel.sh` pins every rank to its own cores (see its header for the options); results are identical for every split.
Do not pin `mpirun` itself, and on a machine with fast and slow cores start on the fast ones (`-f`).

The SOR solver's relaxation factor is now computed from the grid (it used to be fixed at 0.8 and left the solver
under-relaxed, so the pKa values stopped well short of convergence). Converged values differ from older output by up to
about 0.4-0.6 pKa units on nucleic acids and about 0.1 on proteins.

### Precision and speed options

The code is built in **single precision** by default (`delphi_real` = float; the authors' `SP` option, repaired). It halves the
memory traffic of the Poisson-Boltzmann solves and agrees with the double-precision build to the printed 0.01 pKa units on every
structure tested (1BNA, 1SDR, 1RNA, 6PTI, 1CRN, 3HDD). `make EXTRA=-DMX` builds double precision. In single precision a
per-iteration change below about 5e-5 cannot be reached, so `MAXC`/`MAXC0` are raised to at least 1e-4 (with a warning) and the
SOR loop stops after 20,000 iterations with a warning.

Two `run.prm` lines control the whole-molecule **base run**, which supplies the boundary values of the focusing runs and takes about
half of the time of a large system (the focusing runs stay at scales 2 and 4):

    Base grid scale (SCALE0)                : 1.0      # grid points per Angstrom of the base run (default 1.0)
    Convergence threshold, base run (MAXC0) : 0.01     # default: 10 x MAXC, i.e. 0.01 for the default MAXC = 0.001

The base run therefore converges to 10 x MAXC by default; set `MAXC0` equal to `MAXC` to get the old behaviour, and tightening `MAXC`
tightens the base run with it. Calibration against fully converged references (single precision, one core). 3HDD is a 1,800-atom
protein-DNA complex with 62 sites:

| SCALE0 | MAXC0 | 3HDD time | rms error | worst site |
|---|---|---|---|---|
| 1.0 | = MAXC (old behaviour) | 95.0 s | 0.003 | 0.01 |
| **1.0** | **10 x MAXC (default)** | **71.6 s** | **0.018** | **0.13** |
| 0.9 | 0.003 | 62.4 s | 0.035 | 0.19 |
| 0.9 | 0.01 | 55.5 s | 0.040 | 0.20 |
| 0.8 | = MAXC | 52.6 s | 0.037 | 0.17 |
| 0.8 | 0.01 | 44.7 s | 0.045 | 0.17 |

With the default, the smaller structures stay within the printed 0.01 of the converged answer (1BNA 0.000, 1SDR 0.004, 1RNA 0.003,
6PTI 0.003, 1CRN 0.005 rms).

The error is in pKa units against the converged answer; the few sites that carry it are DNA bases (3-5 of 62 sites above 0.05 for
SCALE0 0.9/0.8). Proteins are insensitive (6PTI: rms 0.004 at SCALE0 0.7, 0.006 at 0.5); nucleic acids are not (rms at SCALE0 0.9: 1BNA
0.006, 1RNA 0.011, 1SDR 0.033; at 0.7: 0.010, 0.096, 0.051; below 0.7 a DNA/RNA run degrades quickly). For comparison, the original
fixed relaxation factor left every pKa about 0.1-0.4 away from convergence. Set `MAXC0 = MAXC` when the last 0.01 matters.
