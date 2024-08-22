import glob
import argparse
import sys
from . import GpxCSV


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


def main():
    """Main function for command line utility"""
    parser = MyParser()
    parser.add_argument(
        'input_file',
        nargs='+',
        help='input gpx file, may be .gpx or gzipped .gpx.gz. Can pass a wildcard like *.gpx',
    )
    parser.add_argument(
        '-o',
        '--output-file',
        type=str,
        help='output file name, optional. Name ending with .json will produce json instead of csv.',
        default=None,
    )
    parser.add_argument(
        '-j', '--json', action='store_true', default=False, help='Output a json file.'
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true', default=False, help='Turn on verbose mode'
    )
    parser.add_argument(
        '-s',
        '--silent',
        action='store_true',
        default=False,
        help='Turn off all printed output (except errors/asserts)',
    )

    parser.add_argument(
        '-r',
        '--raise-errors',
        action='store_true',
        default=False,
        help='Stop processing / Assert if encountering a non .gpx file',
    )

    args = parser.parse_args()
    all_files = []
    for arg in args.input_file:
        all_files += glob.glob(arg)
    assert all_files, 'File or files not found'
    if args.raise_errors:
        error = 'errors'
    else:
        error = 'ignore'
    GpxCSV(verbose=args.verbose, silent=args.silent, errors=error).gpxtofile(
        all_files, args.output_file, json=args.json
    )


if __name__ == '__main__':
    main()
