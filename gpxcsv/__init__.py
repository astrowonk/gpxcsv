from lxml import etree
import csv
import gzip
import json


def _strip_ns_prefix(tree):
    """strip the namespace prefixes from all elements in a tree"""
    #thank you to https://stackoverflow.com/questions/30232031/how-can-i-strip-namespaces-out-of-an-lxml-tree
    query = "descendant-or-self::*[namespace-uri()!='']"
    for element in tree.xpath(query):
        element.tag = etree.QName(element).localname
    return tree


def _try_to_float(s):
    """convert string to float or leave as string"""
    try:
        return float(s)
    except ValueError:
        return s


def _load_and_clean_gpx(gpx_file):
    """load a gpx file, clean up the name space, return the root of the lxml tree."""
    if gpx_file.endswith('.gz'):
        with gzip.open(gpx_file, 'rb') as f:
            tree = etree.parse(f)
    else:
        with open(gpx_file, 'rb') as f:
            tree = etree.parse(f)
    tree = _strip_ns_prefix(tree)
    etree.cleanup_namespaces(tree)
    return tree.getroot()


def make_new_file_name(gpxfile, suffix):
    """Make a new file name based on the old file name using the suffix"""
    suffix = '.' + suffix
    if gpxfile.endswith('gpx'):
        output = gpxfile.replace('.gpx', suffix)
    elif gpxfile.endswith('gpx.gz'):
        output = gpxfile.replace('.gpx.gz', suffix)
    else:
        output = gpxfile + suffix
    return output


class GpxCSV():
    """A class to convert a gpx file to a csv file"""
    verbose = None
    silent = None

    def __init__(self, verbose=False, silent=False) -> None:
        self.verbose = verbose
        self.silent = silent

    @staticmethod
    def _process_trackpoint(trackpoint, update_dict={}):
        """Process a trackpoint element into a dictionary"""
        ext_dict = {}
        if trackpoint.find('extensions') is not None:
            for extension in list(trackpoint.find('extensions')):
                ext_dict.update({
                    x.tag: _try_to_float(x.text)
                    for x in extension.getchildren()
                })
        child_dict = {
            x.tag: _try_to_float(x.text)
            for x in trackpoint.getchildren() if x.tag != 'extensions'
        }

        final_dict = {
            'lat': _try_to_float(trackpoint.attrib['lat']),
            'lon': _try_to_float(trackpoint.attrib['lon']),
        }
        final_dict.update(ext_dict)
        final_dict.update(update_dict)
        final_dict.update(child_dict)
        return final_dict

    def _check_verbose_print(self, msg, force=False):
        """print a message if verbose is enabled and not silent"""
        if not self.silent and self.verbose or (force and not self.silent):
            print(msg)

    def _process_track(self, trk):
        """process a trk element found in a gpx file"""
        non_trkseg_dict = {
            x.tag: x.text
            for x in [x for x in list(trk) if x.tag not in ('trkseg', 'link')]
        }
        self._check_verbose_print(
            f'Processing trk with tag info {non_trkseg_dict}')

        all_trackpoints = []
        all_tracksegments = trk.findall('trkseg')
        num_segments = len(all_tracksegments)
        if num_segments > 1:
            self._check_verbose_print(f'Found {num_segments} track segments')
        for n, trkseg in enumerate(all_tracksegments):
            if num_segments > 1:
                non_trkseg_dict.update({'trkseg': n + 1})
            temp_trackpoints = trkseg.findall('trkpt')

            self._check_verbose_print(
                f'{len(temp_trackpoints)} trackpoints found in segment {n+1}')
            seg_trackpoints = [
                self._process_trackpoint(x, non_trkseg_dict)
                for x in trkseg.findall('trkpt')
            ]
            all_trackpoints.extend(seg_trackpoints)
        return all_trackpoints

    def _process_tree_tracks(self, root):
        """Input the lxml root, find all trks, and process them."""
        tracks = root.findall('trk')
        self._check_verbose_print(f'Found {len(tracks)} tracks')
        all_trackpoints = []
        for trk in tracks:
            all_trackpoints.extend(self._process_track(trk))
        return all_trackpoints

    def _list_to_json(self, list_of_dicts, json_file):
        """Process a list of dictionaries into a json file"""
        if not list_of_dicts:
            print(
                "No valid data to convert to json. Please examine the gpx file directly."
            )
            return
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(list_of_dicts, f, ensure_ascii=False, indent=4)
        self._check_verbose_print(
            f"JSON written to {json_file} with {len(list_of_dicts)} records.",
            True)

    def _list_to_csv(self, list_of_dicts, csv_file):
        """Process a list of dictionaries into a csv file"""
        if not list_of_dicts:
            print(
                "No valid data to convert to csv. Please examine the gpx file directly."
            )
            return
        header = {}
        for d in list_of_dicts:
            header = list(set(d.keys()).union(header))
        header.sort()
        with open(csv_file, 'w') as f:
            mywriter = csv.DictWriter(f,
                                      fieldnames=header,
                                      quoting=csv.QUOTE_MINIMAL)
            mywriter.writeheader()
            for row in list_of_dicts:
                mywriter.writerow(row)
        self._check_verbose_print(
            f"CSV {csv_file} written to {csv_file} with {len(list_of_dicts)} rows",
            force=True)
        if self.verbose:
            #leaving this in an if statement because of the column formatting for now
            print(f'gpx file converted to {csv_file} with columns:')
            for col in header:
                print(f"  {col}")

    def gpxtolist(self, gpxfile):
        """Convert a gpx file to a list of dictionaries"""
        root = _load_and_clean_gpx(gpxfile)
        all_trackpoints = self._process_tree_tracks(root)
        return all_trackpoints

    def _gpxtofile(self, gpxfile, output_name=None, json=False):
        """Convert a gpx file to a csv or json file"""
        assert gpxfile.endswith('.gpx') or gpxfile.endswith(
            '.gpx.gz'), 'File must be gpx or gpx.gz'
        #this logic feels like it could be cleaner
        if json or (output_name is not None and output_name.endswith('.json')):
            if not output_name:
                output_name = make_new_file_name(gpxfile, 'json')
            self._list_to_json(self.gpxtolist(gpxfile), output_name)

            return
        if not output_name:
            output_name = make_new_file_name(gpxfile, 'csv')
        self._list_to_csv(self.gpxtolist(gpxfile), output_name)

    def gpxtofile(self, gpxfile, output_name=None, json=False):
        """Convert a gpx file to a csv or json file"""
        self._check_verbose_print(f"Converting: {gpxfile}")
        if len(gpxfile) > 1:
            assert not output_name, "Can't use wildcard and an output name."
        for file in gpxfile:
            if file:
                self._gpxtofile(file, output_name, json)


def gpxtolist(gpxfile, verbose=False):
    """wrapper for GpxCSV.gpxtolist"""
    return GpxCSV(verbose=verbose).gpxtolist(gpxfile)


def gpxtofile(
    *args,
    verbose=False,
    **kwargs,
):
    """Wrapper for GpxCSV.gpxtofile"""
    GpxCSV(verbose=verbose).gpxtofile(*args, **kwargs)
