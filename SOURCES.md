# Phase 0: source audit

Checked 2026-10-12 against Crossref and the NCBI PMC author manuscript.

## DOIs in deep-research-report.md

Only 3 of the 10 DOIs resolve to what the report says they are. Do not use the rest.

| DOI in report | Report says | Crossref says | Verdict |
|---|---|---|---|
| 10.5281/zenodo.7236452 | Zheng 2026 dataset | Zenodo id, not found on Crossref | unverified |
| 10.1039/JR9360001713 | Ogston 1936, J. Chem. Soc. | "Notes", J. Chem. Soc. 1936, authors incl. Ogston | author/year plausible, content unchecked |
| 10.1021/ja00902a036 | Harkins & Freiser 1958 | Pfitzner & Moffatt 1963, oxidation of alcohols | WRONG |
| 10.1021/ja01039a024 | Christensen 1966 | Carey & Tremper 1969, carbonium ion/silane | WRONG |
| 10.1021/bi00827a012 | Klee & Mudd 1967 | Christensen, Rytting, Izatt 1970, Biochemistry, "Thermodynamic pK, dH, dS, dCp for proton dissociation from several purines and their nucleosides" | real paper, wrong attribution in report; this is the usable source |
| 10.1021/bi00825a001 | Christensen 1970 | Sachdev & Fruton 1970, pepsin | WRONG |
| 10.1021/ja00958a019 | Izatt 1962 | Arnett & Mach 1966, acidity function | WRONG |
| 10.1021/ja00112a009 | Wallenfels & Sund 1957 | Pierre 1995, dicopper cryptand | WRONG |
| 10.1002/prot.24935 | (README) | Wang, Li, Alexov, Proteins 2015 | correct |
| 10.1093/bioinformatics/btv607 | (README) | Wang, Zhang, Alexov, Bioinformatics 2015 | correct |

Zheng & Lafontant-Joseph 2026 is real: 10.1039/d6ra02418a (RSC Adv.), preprint
10.26434/chemrxiv-2026-6khcw. Contents not yet inspected.

The report's own numbers (A 3.5, C 4.2, G 2.4/9.5, U 9.6, T 9.9, phosphate 1-1.5/6.5)
are NOT adopted. They are marked "consensus", "estimated" or "data not shown" and
their cited DOIs mostly fail. They need primary sources before any use.

## What the code ships with

* Model pKa, param/topology lines 691-694: A 3.80, C 4.35, DA 4.10, DC 4.40.
  No source in the repo, the README or the Proteins paper text. NOT yet sourced.
* Charges/radii: amber.crg/.siz say "created from amber98.prm, TINKER package".
  Upstream AMBER paper for the DNA charges not stated in the file.
  parseres.*: Sitkoff/Honig PARSE lineage per file headers.
* The Proteins 2015 paper (PMC4715546) says it extended the topology with
  protonated/unprotonated adenosine and cytidine; its only nucleic-acid
  validation is Table 5: adenosine in two NMR-studied RNAs (BPH, PDB 17ra;
  LDZ, PDB 1ldz). No cytidine or DNA validation. Abstract: "RNA and single
  stranded DNA".

## Verified leads (Crossref)

* Christensen, Rytting, Izatt, Biochemistry 1970, 10.1021/bi00827a012: thermodynamic pK of purines and nucleosides.
* Tang, Alexov, Pyle, Honig, J Mol Biol 2007, 10.1016/j.jmb.2006.12.001: pKa in RNA, cited by Wang 2015; the comparison data.
* Legault & Pardi, JACS 1994, 10.1021/ja00097a066: adenine protonation in RNA by 13C NMR.
* Legault & Pardi, JACS 1997, 10.1021/ja9640051: pKa shift in the lead-dependent ribozyme.
* Thaplyal & Bevilacqua, Methods Enzymol 2014, 10.1016/b978-0-12-801122-5.00009-x: measuring pKa in RNA and DNA.
* Cornell et al., JACS 1995, 10.1021/ja00124a002: AMBER ff94 (nucleic-acid charges candidate).
* Cheatham, Cieplak, Kollman, J Biomol Struct Dyn 1999, 10.1080/07391102.1999.10508297: modified Cornell field.
* Sitkoff, Sharp, Honig, J Phys Chem 1994, 10.1021/j100058a043: PARSE.

Still to find: source of the experimental BPH pKa values (Table 5), pyrimidine
(C, U, T) nucleoside pKa primary source, phosphate pKa primary source.
