import argparse
import json
from pathlib import Path

import copy
import shutil

PARSEC_LIST = ['streamcluster', 'canneal', 'swaptions', 'x264', 'ferret', 'bodytrack', 'blackscholes',
               'dedup', 'facesim', 'fluidanimate', 'freqmine', 'raytrace', 'vips']
RODINIA_LIST = ['nn', 'kmeans', 'cfd', 'particlefilter', 'bfs']
SPEC_LIST = ['lbm', 'libquantum', 'GemsFDTD', 'sphinx', 'gcc', 'zeusmp', 'sjeng']

WORKLOAD_LIST = [
    'blackscholes',
    'bodytrack',
    'canneal',
    'ferret',
    'kmeans',
    'particlefilter',
    'streamcluster',
    'swaptions'
]

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
    parser = argparse.ArgumentParser(description='Config generator for benchmark_launcher. (2-collocated experiment)')
    parser.add_argument('dest_dir', metavar='DEST_DIR', type=str, default='.', nargs='?',
                        help='The directory path where the experiment directories will be created.')
    args = parser.parse_args()

    workspace = Path(args.dest_dir)
    for idx, wl in enumerate(WORKLOAD_LIST):
        wl_config = copy.deepcopy(JSON_WORKLOAD_TEMPLATE)
        wl_config['name'] = wl

        for wl2 in WORKLOAD_LIST[idx:]:
            wl_config2 = copy.deepcopy(JSON_WORKLOAD_TEMPLATE)
            wl_config2['name'] = wl2

            config = copy.deepcopy(JSON_TEMPLATE)

            config['workloads'].append(wl_config)
            config['workloads'].append(wl_config2)

            folder = workspace / f'{wl}-{wl2}'

            if folder.exists():
                shutil.rmtree(str(folder))

            folder.mkdir(parents=True)

            with open(str(folder / 'config.json'), mode='w') as fp:
                json.dump(config, fp, indent='\t')


if __name__ == '__main__':
    main()
