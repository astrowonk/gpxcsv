import glob
import argparse
from . import GpxCSV


def main():
    """Main function for command line utility"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'input_file',
        nargs='+',
        help=
        'input gpx file, may be .gpx or gzipped .gpx.gz. Can pass a wildcard like *.gpx'
    )
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
    parser.add_argument(
        '-s',
        '--silent',
        action='store_true',
        default=False,
        help='Turn off all printed output (except errors/asserts)')

    args = parser.parse_args()
    all_files = []
    for arg in args.input_file:
        all_files += glob.glob(arg)
    GpxCSV(verbose=args.verbose,
           silent=args.silent).gpxtofile(all_files,
                                         args.output_file,
                                         json=args.json)


if __name__ == '__main__':
    main()
