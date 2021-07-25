import argparse
from . import gpxtofile


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
    parser.add_argument('-j',
                        '--json',
                        type=bool,
                        action='store_true',
                        default=False)
    args = parser.parse_args()
    gpxtofile(args.input_file, args.output_file, json=args.json)


if __name__ == '__main__':
    main()
