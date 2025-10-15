# 🧬 Supporting Materials for Manuscript  
**Global diversity mapping of hydrothermal vent viruses: Virus–host interactions pervade deep-sea "oases of life"**

---

## 📖 Overview

This repository contains scripts, configurations, and auxiliary resources supporting the analyses presented in the manuscript:

> **Global diversity mapping of hydrothermal vent viruses: Virus–host interactions pervade deep-sea "oases of life"**

The workflows described here cover viral and microbial genome assembly, quality control, viral prediction, host association, phylogenetic analysis, diversity assessment, and functional annotation.

---

## 📂 Data Availability

- **GOHVGD — Global Ocean Hydrothermal Vent Virus Genome Database**  
  [OEZ00021625 (BioSino)](https://www.biosino.org/node/analysis/detail/OEZ00021625)

- **GOHMGD — Global Ocean Hydrothermal Vent Microbial Genome Database**  
  [OEZ00021644 (BioSino)](https://www.biosino.org/node/analysis/detail/OEZ00021644)

---

## 💻 Code Availability and Workflow Summary

### 1. **[Contig assembly and binning](https://github.com/Cris-du/RDPS/commit/2213e09b262300cd71d74adf8c1417d0b164a55b)**
Metagenomic reads were assembled into contigs and contig ≥ 1 kb were binned into MAG (metagenomic assembly genome).  
Microbial prediction, quality control and microbial taxonomic classification were performed for all bins.

### 2. **Viral prediction and vOTU clustering**
Viral sequences prediction from contig ≥3 kb, and quality-checked following the pipeline described in the manuscript.  
Representative viral genomes were clustered at the species level (**vOTUs**) based on **Average Nucleotide Identity (ANI)**.

### 3. **Viral gene prediction and protein clustering**
Viral coding sequences were predicted and clustered into protein families for downstream comparative and functional analyses.

### 4. **Viral taxonomic assignment**
Viral genomes were grouped into genera-level and family-level based on **Average Amino Acid Identity (AAI)**, with taxonomic assignment according to the **International Committee on Taxonomy of Viruses (ICTV)** framework.

### 5. **Uniqueness and cross-Dataset Comparison of GOHVGD**
The uniqueness and sharedness of GOHVGD at **vOTU**, **genus**, **family**, and **protein-clusters (PCs)** levels was evaluated against surface-ocean virus datasets: **Global Ocean Virome 2 (GOV2.0)** and previously published hydrothermal virus datasets (Cheng et al,. 2022, Langwig et al,. 2025). 

### 6. **Virus–Host infective relationship prediction**
Viral–host infective relationship were inferred through:
- **CRISPR-Spacer sequence matches**
- **Whole-genome sequence matches**  
between GOHVGD and GOHMGD genomes.

### 7. **Phylogenetic Analysis**
Perform phylogenetic analysis on the hallmark proteins of **Caudoviricetes** of GOHVGD and genome of GOHMGD.

### 8. **Viral and Microbial Abundance caculation**
Normalized abundance of GOHVGD vOTUs and GOHMGD genomes was caculated across all samples for:
- **Macrodiversity (α-, β-diversity)**
- **Microdiversity (nucleotide diversity, pN/pS ratio)**
- **Functional system diversity**

### 9. **Defense and Anti-Defense System Analysis**
Identification and diversity profiling of:
- **Host antiviral defense systems** (e.g., CRISPR, RM, TA, Abi)
- **Viral anti-defense systems**

### 10. **Auxiliary Metabolic Gene (AMG) Analysis**
Detection and classification of viral **AMGs**; diversity and environmental distribution analyses.

### 11. **Functional Annotation and Genome Collinearity**
Functional annotation of viral proteins and synteny comparison among ubiquitous viral genomes.

### 12. **Physiological Prediction of GOHMGD Members**
Prediction of microbial physiological traits:
- **Optimal growth temperature (OGT)**
- **Minimum doubling time (MDT)**

### 13. **Viral Macro- and Micro-Diversity Analyses**
Computation of **α- and β-diversity indices**, **nucleotide diversity**, and **selection metrics (pN/pS)** across environmental groups.

---

## 🧩 Repository Structure

