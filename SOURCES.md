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

## Phase 0b: DOI leads (all DOIs below resolved on Crossref with matching title/journal/year)

Status key: [seen] = I read the passage that cites the number; [title only] = DOI/title verified, content not read.

### Model-compound pKa (isolated nucleosides/nucleotides): what to source the topology values from
Silva & Bussi, J Chem Inf Model 2025, 10.1021/acs.jcim.4c02185 (PMC12004511) [seen] states
A N1 pKa 3.5 and C N3 pKa 4.2, citing the four papers below, and calibrates on
experimental AMP/CMP and dinucleotide data. This is a secondary source; the
primary table must still be read before a value is adopted.
* Izatt, Christensen, Rytting, Chem Rev 1971, 71, 439, 10.1021/cr60273a002 [title only] (errata: 10.1021/cr60280a005)
* Christensen, Rytting, Izatt, Biochemistry 1970, 9, 4907, 10.1021/bi00827a012 [title only]
* Acharya et al., JACS 2004, 126, 2862, 10.1021/ja0386546 [title only]: model mononucleotide nucleobase pKa; DNA monomers vs RNA monomers
* Clauwaert & Stockx, Z Naturforsch B 1968, 10.1515/znb-1968-0105 [title only]
* Gonzalez-Olvera et al., Biophys Chem 2015, 10.1016/j.bpc.2015.07.001 and ChemBioChem 2018, 10.1002/cbic.201800310 [title only]: short oligonucleotides
* Jones et al., J Phys Chem A 2022, 10.1021/acs.jpca.1c10905 [title only]: modified-nucleobase pKa
* Zheng & Lafontant-Joseph, RSC Adv 2026, 16, 21397, 10.1039/d6ra02418a [abstract only]: 24,000+ digitized pKa entries; check for nucleosides/nucleotides

### Experimental pKa in nucleic-acid context (validation data)
* Acharya et al., JACS 2004, 126, 8674, 10.1021/ja048484c [title only]: sequence-context pKa perturbation in DNA (this is the Acharya/Chattopadhyaya paper, not Moody/Bevilacqua)
* Thaplyal & Bevilacqua, Methods Enzymol 2014, 10.1016/b978-0-12-801122-5.00009-x [abstract seen]: methods, not a value table
* Bevilacqua & Yajima, Curr Opin Chem Biol 2006, 10.1016/j.cbpa.2006.08.014 [title only]
* Legault & Pardi, JACS 1994, 116, 8390, 10.1021/ja00097a066 and JACS 1997, 10.1021/ja9640051 [title only]: source family for the NMR adenine pKa values in Wang 2015 Table 5 (PDB 1ldz)
* Acharya & Chattopadhyaya, Pure Appl Chem 2005, 10.1351/pac200577010291 [title only]

### Calculations to compare with (and force-field provenance)
* Tang, Alexov, Pyle, Honig, J Mol Biol 2007, 10.1016/j.jmb.2006.12.001 [title only]: PB pKa in RNA, the comparison in Wang 2015
* Goh, Knight, Brooks, JCTC 2012, 10.1021/ct2006314 and J Phys Chem Lett 2013, 10.1021/jz400078d [title only]: constant-pH MD for nucleic acids
* Silva & Bussi 2025 (above): AMBER chiOL3 + RESP charges for protonated A/C
* Barroso da Silva et al., J Chem Phys 2017, 10.1063/1.4972986; Pasquali et al., Interface Focus 2019, 10.1098/rsfs.2018.0066 [title only]: coarse-grained RNA titration
* Cornell et al. 1995, 10.1021/ja00124a002; Perez et al. 2007 (bsc0), 10.1529/biophysj.106.097782; Zgarbova et al. 2011 (OL3), 10.1021/ct200162x [title only]
* Aduri et al., JCTC 2007, 10.1021/ct600329w [title only]: AMBER parameters for modified RNA nucleosides
* Colominas, Luque, Orozco, JACS 1996, 10.1021/ja954293l [title only]: tautomerism/protonation of G and C

### Not found / still open
* Origin of the 3.80/4.35/4.10/4.40 model values in param/topology.
* Primary source for phosphate pKa in nucleotides (the report's Gorenstein hit, 10.1016/b978-0-08-091841-9.50023-0, is a 31P NMR compilation, [title only]).
* U/T/G model values (G N7 and N1, U/T N3) from a primary table.
