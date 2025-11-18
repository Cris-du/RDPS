#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

def generate_bed_from_fna(fna_filename, bed_filename):
    with open(fna_filename, 'r') as fna, open(bed_filename, 'w') as bed:
        contig_name = ''
        contig_length = 0
        for line in fna:
            line = line.strip()
            if line.startswith('>'):
                if contig_name:
                    bed.write('{}\t0\t{}\n'.format(contig_name, contig_length))
                contig_name = line[1:].split()[0]
                contig_length = 0
            else:
                contig_length += len(line)
        if contig_name:
            bed.write('{}\t0\t{}\n'.format(contig_name, contig_length))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate_bed_from_fna.py <input_fasta/fa/fna_file> <output_bed_file>")
        sys.exit(1)
    
    fna_filename = sys.argv[1]
    bed_filename = sys.argv[2]
    generate_bed_from_fna(fna_filename, bed_filename)
