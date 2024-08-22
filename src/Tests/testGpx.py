import unittest
from gpxcsv import GpxCSV, gpxtofile, gpxtolist
import os
from glob import glob
from io import StringIO


class TestGpx(unittest.TestCase):
    """Unit test the class"""

    @classmethod
    def setUpClass(cls) -> None:
        """set up test files"""
        os.chdir('src/Tests')

    def test_gpx_to_file(self):
        """Test the gpx to file"""
        for file in glob('*.csv') + glob('*.json'):
            os.remove(file)
        # test with output name
        GpxCSV().gpxtofile(['myfile.gpx'], output_name='myfile_test.csv')
        self.assertTrue(os.path.exists('myfile_test.csv'))

        # test without output name
        GpxCSV(verbose=True).gpxtofile(['myfile.gpx'])
        self.assertTrue(os.path.exists('myfile.csv'))

        # will need to mock patch sys.stdout to check printing outputs

    def testStringIo(self):
        """Load file to StringIo and pass StringIo object to gpxtolist"""

        with open('myfile.gpx', 'r') as f:
            strio = StringIO(f.read())
        theList = GpxCSV().gpxtolist(strio)
        self.assertTrue(theList[0]['ele'] == 50.003891)

    def test_gpx_to_list(self):
        """Test the gpx to list"""
        g = GpxCSV()
        theList = g.gpxtolist('myfile.gpx')
        self.assertAlmostEqual(theList[0]['ele'], 50.003891)

    def test_multi_segment(self):
        """test multi segment support"""
        try:
            os.remove('myfile_multseg.csv')
        except FileNotFoundError:
            pass
        GpxCSV().gpxtofile(['myfile_multseg.gpx.gz'])
        self.assertTrue(os.path.exists('myfile_multseg.csv'))

    def test_convert_json(self):
        """test json conversion"""
        GpxCSV().gpxtofile(['myfile.gpx'], json=True)
        self.assertTrue(os.path.exists('myfile.json'))
        GpxCSV().gpxtofile(['myfile.gpx'], json=True, output_name='myfile.json')

    def test_empty_list(self):
        GpxCSV().gpxtofile([None])  # why do I handle this scenario?
        self.assertIsNone(GpxCSV()._list_to_csv([], 'out.csv'))
        self.assertIsNone(GpxCSV()._list_to_json([], 'out.json'))

    def test_invalid_filename(self):
        self.assertCountEqual(GpxCSV().gpxtolist('myfile.json'), [])

    def test_glob_and_output_name(self):
        self.assertRaises(
            AssertionError,
            GpxCSV().gpxtofile,
            ['myfile.gpx', 'bogus_basin.gpx'],
            output_name='out.csv',
        )

    def test_wrappers(self):
        for file in glob('*.csv') + glob('*.json'):
            os.remove(file)
        gpxtofile('myfile.gpx')
        self.assertTrue(os.path.exists('myfile.csv'))
        out = gpxtolist('myfile.gpx')
        self.assertAlmostEqual(out[0]['ele'], 50.003891)

    def test_odd_extension(self):
        g = GpxCSV()
        theList = g.gpxtolist('non_trackpoint_extension.gpx')
        self.assertEqual(theList[0]['speed'], 0.484723)
        self.assertEqual(theList[0]['hAcc'], 1.486173)

    def test_trk_extension(self):
        g = GpxCSV()
        theList = g.gpxtolist('Lannion_Plestin_parcours24.4RE.gpx')
        self.assertEqual(theList[0]['DisplayColor'], 'Black')
        self.assertAlmostEqual(theList[0]['ele'], 1.1)
