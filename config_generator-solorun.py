#!/usr/bin/env python3

import argparse
import json
from pathlib import Path

import shutil

PARSEC_LIST = ['streamcluster', 'canneal', 'swaptions', 'x264', 'ferret', 'bodytrack', 'blackscholes',
               'dedup', 'facesim', 'fluidanimate', 'freqmine', 'raytrace', 'vips']

RODINIA_LIST = ['nn', 'kmeans', 'cfd', 'particlefilter', 'bfs']
SPEC_LIST = ['lbm', 'libquantum', 'GemsFDTD', 'sphinx', 'gcc', 'zeusmp', 'sjeng']

WORKLOAD_LIST = RODINIA_LIST

JSON_WORKLOAD_TEMPLATE = {
    'num_of_threads': 16,
    'binding_cores': "16-31",
    'numa_nodes': "1",
    'cpu_freq': 2.1
}

JSON_TEMPLATE = {
    'workloads': [
    ],
    'launcher': {
        'hyper-threading': False,
        'stops_with_the_first': False,
        'post_scripts': [
            'avg_csv.py',
            'validate_perf.py'
        ]
    }
}


def main():
    parser = argparse.ArgumentParser(description='Config generator for benchmark_launcher. (solorun experiment)')
    parser.add_argument('dest_dir', metavar='DEST_DIR', type=str, default='.', nargs='?',
                        help='The directory path where the experiment directories will be created.')
    args = parser.parse_args()

    workspace = Path(args.dest_dir).absolute()
    for wl in WORKLOAD_LIST:
        JSON_WORKLOAD_TEMPLATE['name'] = wl

        JSON_TEMPLATE['workloads'] = [JSON_WORKLOAD_TEMPLATE]

        folder = workspace / str(wl)

        if folder.exists():
            shutil.rmtree(str(folder))

        folder.mkdir(parents=True)

        with open(str(folder / 'config.json'), mode='w') as fp:
            json.dump(JSON_TEMPLATE, fp, indent='\t')


if __name__ == '__main__':
    main()
