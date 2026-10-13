#!/bin/bash
# SPDX-License-Identifier: LGPL-3.0-or-later
# Modified on branch nucleic-acids by noshou: new launcher (MPI ranks over sites, OpenMP threads inside each solve).
#
# usage: scripts/run_parallel.sh [-n RANKS] [-t THREADS] [-f FIRST_CORE] [-x BINARY] run.prm
#
#   -n  MPI ranks, each takes a share of the titratable sites     (default 4)
#   -t  OpenMP threads inside each rank's Poisson-Boltzmann solves (default 1)
#   -f  first core to use; rank r gets cores FIRST+r*T .. FIRST+r*T+T-1   (default 0)
#   -x  the delphiPKa binary                                       (default ./delphiPKa)
#
# Every rank is pinned to its own cores. Pin the ranks, never mpirun itself: a pinned mpirun busy-waits on the
# solver's core and halves its speed. On a machine with fast and slow cores give -f the first fast core
# (e.g. -f 4 on an Apple M2 under Linux, whose cores 4-7 are the performance cores); RANKS*THREADS should not
# exceed the number of fast cores. Ranks are the robust choice: they synchronise only once, at the end. Threads
# add little on large grids (10-30 %) and stall whenever one pinned thread is descheduled, since they synchronise
# twice per SOR iteration. The results are identical for every RANKS/THREADS split.
# Needs mpirun and taskset (Linux); on other systems run  OMP_NUM_THREADS=T mpirun -np R ./delphiPKa run.prm
set -e
ranks=4; threads=1; first=0; bin=./delphiPKa
while getopts "n:t:f:x:" o; do
    case $o in
        n) ranks=$OPTARG ;; t) threads=$OPTARG ;; f) first=$OPTARG ;; x) bin=$OPTARG ;;
        *) sed -n 4,9p "$0" | sed 's/^# \{0,1\}//'; exit 2 ;;
    esac
done
shift $((OPTIND - 1))
[ $# -eq 1 ] || { echo "usage: $0 [-n RANKS] [-t THREADS] [-f FIRST_CORE] [-x BINARY] run.prm" >&2; exit 2; }
command -v taskset > /dev/null || { echo "taskset not found: run  OMP_NUM_THREADS=$threads mpirun -np $ranks $bin $1" >&2; exit 1; }
export OMP_NUM_THREADS=$threads FIRST_CORE=$first RANK_THREADS=$threads
exec mpirun --bind-to none -np "$ranks" bash -c \
    'a=$((FIRST_CORE + OMPI_COMM_WORLD_RANK * RANK_THREADS)); exec taskset -c $a-$((a + RANK_THREADS - 1)) "$@"' _ "$bin" "$1"
