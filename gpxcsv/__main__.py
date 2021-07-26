import argparse
from . import GpxCSV


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file',
                        type=str,
                        help='input gpx file, may be .gpx or .gpx.gz')
    parser.add_argument('-o',
                        '--output-file',
                        type=str,
                        help='output file name, optional',
                        default=None)
    parser.add_argument('-j', '--json', action='store_true', default=False)
    parser.add_argument('-v', '--verbose', action='store_true', default=False)

    args = parser.parse_args()
    VERBOSE = args.verbose

    GpxCSV(verbose=args.verbose).gpxtofile(args.input_file,
                                           args.output_file,
                                           json=args.json)


if __name__ == '__main__':
    main()
