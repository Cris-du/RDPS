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

### 1. **Contig Assembly and Binning**
Metagenomic reads were assembled into contigs and contig ≥ 1 kb were binned into MAG (metagenomic assembly genome).  
Microbial prediction, quality control and microbial taxonomic classification were performed for all bins.

### 2. **Viral Prediction and vOTU Clustering**
Viral sequences prediction from contig ≥3 kb, and quality-checked following the pipeline described in the manuscript.  
Representative viral genomes were clustered at the species level (**vOTUs**) based on **Average Nucleotide Identity (ANI)**.

### 3. **Viral Gene Prediction and Protein Clustering**
Viral coding sequences were predicted and clustered into protein families for downstream comparative and functional analyses.

### 4. **Viral Taxonomic Assignment**
Viral genomes were grouped into genera and families using **Average Amino Acid Identity (AAI)**, with taxonomic assignment according to the **ICTV** framework.

### 5. **Uniqueness and Cross-Dataset Comparison of GOHVGD**
The uniqueness and sharedness of GOHVGD was evaluated against surface-ocean virus datasets (**GOV2.0**) and previously published hydrothermal virus datasets (2022, 2025).  
Comparisons were made at **vOTU**, **genus**, **family**, and **protein-cluster** levels.

### 6. **Virus–Host Interaction Prediction**
Viral–host links were inferred through:
- **CRISPR spacer matches**
- **Whole-genome nucleotide similarity**  
between GOHVGD vOTUs and GOHMGD genomes.

### 7. **Phylogenetic Analysis**
Phylogenies of **Caudoviricetes** hallmark proteins and GOHMGD representatives were reconstructed to infer evolutionary relationships.

### 8. **Viral and Microbial Abundance Estimation**
Normalized abundance of GOHVGD vOTUs and GOHMGD genomes was computed across samples for:
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
- **Growth rate** (via codon usage models)

### 13. **Viral Macro- and Micro-Diversity Analyses**
Computation of **α- and β-diversity indices**, **nucleotide diversity**, and **selection metrics (pN/pS)** across environmental groups.

---

## 🧩 Repository Structure

