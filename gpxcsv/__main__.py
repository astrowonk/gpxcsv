import argparse
from . import gpxtocsv


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=str, help='input gpx file, may be .gpx or .gpx.gz')
    parser.add_argument('-o',
                        '--output-file',
                        type=str,
                        help='output csv file name, optional',
                        default=None)
    args = parser.parse_args()
    gpxtocsv(args.input_file, args.output_file)


if __name__ == '__main__':
    main()
