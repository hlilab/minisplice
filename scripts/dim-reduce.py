#!/usr/bin/env python3

# generated by DeepSeek-R1

import argparse
import sys
import gzip
import numpy as np
from sklearn.decomposition import PCA
from umap import UMAP

def main():
    parser = argparse.ArgumentParser(description='Dimensionality reduction with PCA or UMAP.')
    parser.add_argument('--method', choices=['pca', 'umap'], required=True,
                        help='Dimensionality reduction method: pca or umap')
    parser.add_argument('--input', type=str, required=True,
                        help='Input data file (TAB-delimited, optionally gzipped)')
    parser.add_argument('--output', type=str,
                        help='Output file (optional, stdout by default)')
    parser.add_argument('--n_components', type=int, default=2,
                        help='Number of output dimensions (default: 2)')
    
    # UMAP-specific parameters
    parser.add_argument('--n_neighbors', type=int, default=15,
                        help='UMAP: number of neighbors (default: 15)')
    parser.add_argument('--min_dist', type=float, default=0.1,
                        help='UMAP: minimum distance (default: 0.1)')
    
    # PCA-specific parameters
    parser.add_argument('--whiten', action='store_true',
                        help='PCA: apply whitening to output components')
    
    args = parser.parse_args()

    # Handle gzipped input
    if args.input.endswith('.gz'):
        opener = gzip.open
        mode = 'rt'
    else:
        opener = open
        mode = 'r'

    # Read input data
    labels = []
    features = []
    with opener(args.input, mode) as f:
        for line in f:
            parts = line.strip().split('\t')
            labels.append(parts[0])
            features.append([float(x) for x in parts[1:]])
    
    feature_array = np.array(features)

    # Apply selected dimensionality reduction
    if args.method == 'pca':
        reducer = PCA(n_components=args.n_components, whiten=args.whiten)
        result = reducer.fit_transform(feature_array)
        col_prefix = 'PC'
    elif args.method == 'umap':
        reducer = UMAP(
            n_components=args.n_components,
            n_neighbors=args.n_neighbors,
            min_dist=args.min_dist
        )
        result = reducer.fit_transform(feature_array)
        col_prefix = 'UMAP'
    
    # Generate output lines
    output_lines = []
    for label, coords in zip(labels, result):
        coord_str = "\t".join([f"{x:.6f}" for x in coords])
        output_lines.append(f"{label}\t{coord_str}\n")

    # Write output
    if args.output:
        with open(args.output, 'w') as f:
            f.writelines(output_lines)
    else:
        sys.stdout.writelines(output_lines)

if __name__ == '__main__':
    main()
