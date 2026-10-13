#!/usr/bin/env python3

# SPDX-License-Identifier: LGPL-3.0-or-later

# Modified on branch nucleic-acids by noshou: new launcher; 
# Linux, macOS and Windows, standard library only.

"""Run delphiPKa on several MPI ranks that each take a share of the titratable sites.

    python scripts/run_parallel.py [-n RANKS] [-t THREADS] [-f FIRST_CORE] [-x BINARY] [--dry-run] run.prm

    -n  MPI ranks                                                   (default 4, never more than the cores / THREADS)
    -t  OpenMP threads inside each rank's Poisson-Boltzmann solves  (default 1)
    -f  first core to use; rank r gets cores FIRST + r*T .. FIRST + r*T + T-1   (default 0)
    -x  the delphiPKa binary                                        (default ./delphiPKa, delphiPKa.exe on Windows)

The launcher finds mpiexec or mpirun (Open MPI, MPICH, Intel MPI and Microsoft MPI are recognised), 
hands the settings to the ranks in environment variables and starts them. The ranks pin themselves 
to their cores (see src/delphiPKa/cpu_pin.h): Linux and Windows honour it, macOS has no hard thread 
affinity and ignores it. On a machine with fast and slow cores give -f the first fast core (cores 

Without this script the same thing is, on any platform with an MPI launcher:
    DELPHI_FIRST_CORE=0 DELPHI_THREADS=1 mpiexec -n 4 ./delphiPKa run.prm
"""
import argparse
import os
import shutil
import subprocess
import sys


def find_launcher():
    for name in ("mpiexec", "mpirun"):
        path = shutil.which(name)
        if path:
            return path
    return None


def flavour(launcher):
    """Which MPI is it? Decides how environment variables are handed to the ranks."""
    try:
        text = subprocess.run(  
                    [launcher, "--version"], 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.STDOUT,
                    universal_newlines=True, 
                    timeout=20
                ).stdout.lower()
    except Exception:
        return "unknown"
    if "open mpi" in text or "prrte" in text or "open-mpi" in text:
        return "openmpi"
    if "microsoft mpi" in text or "ms-mpi" in text:
        return "msmpi"
    if "hydra" in text or "mpich" in text or "intel" in text:
        return "hydra"
    return "unknown"


def main():
    ap = argparse.ArgumentParser(description="Run delphiPKa on several MPI ranks.", add_help=True)
    ap.add_argument("-n", type=int, default=4, help="MPI ranks (default 4)")
    ap.add_argument("-t", type=int, default=1, help="OpenMP threads per rank (default 1)")
    ap.add_argument("-f", type=int, default=0, help="first core to use (default 0)")
    ap.add_argument("-x", default=None, help="the delphiPKa binary")
    ap.add_argument("--dry-run", action="store_true", help="print the command and stop")
    ap.add_argument("prm", help="the run.prm file")
    a = ap.parse_args()

    binary = a.x or os.path.join(".", "delphiPKa.exe" if os.name == "nt" else "delphiPKa")
    if not os.path.exists(binary):
        sys.exit("cannot find %s (build it with make, or give the path with -x)" % binary)
    if not os.path.exists(a.prm):
        sys.exit("cannot find %s" % a.prm)
    launcher = find_launcher()
    if not launcher:
        sys.exit("no mpiexec/mpirun on the PATH: install an MPI (Open MPI, MPICH, Intel MPI or Microsoft MPI)")

    threads = max(1, a.t)
    ranks = max(1, min(a.n, max(1, (os.cpu_count() or 1) // threads)))
    if ranks != a.n:
        print("note: %d ranks x %d threads do not fit in %d cores, using %d ranks" % (
                a.n, 
                threads, 
                os.cpu_count() or 1, 
                ranks)
            )

    settings = {
                    "DELPHI_FIRST_CORE": str(a.f), 
                    "DELPHI_THREADS": str(threads), 
                    "OMP_NUM_THREADS": str(threads)
                }
    kind = flavour(launcher)
    cmd = [launcher]
    if kind == "openmpi":
        cmd += ["--bind-to", "none"] + sum([["-x", k] for k in settings], [])
        cmd += ["-np", str(ranks)]
    elif kind == "msmpi":
        cmd += ["-n", str(ranks)] + sum([["-env", k, v] for k, v in settings.items()], [])
    elif kind == "hydra":
        cmd += ["-n", str(ranks)] + sum([["-genv", k, v] for k, v in settings.items()], [])
    else:
        cmd += ["-n", str(ranks)] # unknown MPI: the ranks inherit this process' environment
    cmd += [binary, a.prm]

    env = dict(os.environ)
    env.update(settings)
    print(" ".join(cmd))
    if a.dry_run:
        return 0
    return subprocess.call(cmd, env=env)

if __name__ == "__main__":
    sys.exit(main())
