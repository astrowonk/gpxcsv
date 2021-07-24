from lxml import etree
import csv
import gzip


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


def _process_trackpoint(trackpoint, update_dict={}):
    """Process a trackpoint element into a dictionary"""
    ext_dict = {}
    if trackpoint.find('extensions') is not None:
        for extension in trackpoint.find('extensions').getchildren():
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


def _process_track(trk):
    """process a trk element found in a gpx file"""
    non_trkseg_dict = {
        x.tag: x.text
        for x in
        [x for x in trk.getchildren() if x.tag not in ('trkseg', 'link')]
    }
    all_trackpoints = []
    for trkseg in trk.findall('trkseg'):
        seg_trackpoints = [
            _process_trackpoint(x, non_trkseg_dict)
            for x in trkseg.getchildren()
        ]
        all_trackpoints.extend(seg_trackpoints)
    return all_trackpoints


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


def _process_tree_tracks(root):
    """Input the lxml root, find all trks, and process them."""
    tracks = root.findall('trk')
    all_trackpoints = []
    for trk in tracks:
        all_trackpoints.extend(_process_track(trk))
    return all_trackpoints


def _list_to_csv(list_of_dicts, csv_file):
    """Process a list of dictionaries into a csv file"""
    header = {}
    for d in list_of_dicts:
        header = sorted(list(set(d.keys()).union(header)))
    with open(csv_file, 'w') as f:
        mywriter = csv.DictWriter(f,
                                  fieldnames=header,
                                  quoting=csv.QUOTE_MINIMAL)
        mywriter.writeheader()
        for row in list_of_dicts:
            mywriter.writerow(row)


def gpxtolist(gpxfile):
    """Convert a gpx file to a list of dictionaries"""
    root = _load_and_clean_gpx(gpxfile)
    all_trackpoints = _process_tree_tracks(root)
    return all_trackpoints


def gpxtocsv(gpxfile, csvfile=None):
    """Convert a gpx file to a csv file"""
    if csvfile is None:
        if gpxfile.endswith('gpx'):
            csvfile = gpxfile.replace('.gpx', '.csv')
        elif gpxfile.endswith('gpx.gz'):
            csvfile = gpxfile.replace('.gpx.gz', '.csv')
        else:
            csvfile = gpxfile + '.csv'

    _list_to_csv(gpxtolist(gpxfile), csvfile)
