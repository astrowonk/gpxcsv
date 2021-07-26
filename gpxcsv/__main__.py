import argparse
from . import GpxCSV


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file',
                        type=str,
                        help='input gpx file, may be .gpx or gzipped .gpx.gz')
    parser.add_argument(
        '-o',
        '--output-file',
        type=str,
        help=
        'output file name, optional. Name ending with .json will produce json instead of csv.',
        default=None)
    parser.add_argument('-j',
                        '--json',
                        action='store_true',
                        default=False,
                        help='Output a json file.')
    parser.add_argument('-v',
                        '--verbose',
                        action='store_true',
                        default=False,
                        help='Turn on verbose mode')

    args = parser.parse_args()
    VERBOSE = args.verbose

    GpxCSV(verbose=args.verbose).gpxtofile(args.input_file,
                                           args.output_file,
                                           json=args.json)


if __name__ == '__main__':
    main()
