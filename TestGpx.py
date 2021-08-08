import unittest
from gpxcsv import GpxCSV, gpxtofile, gpxtolist
import os


class TestGpx(unittest.TestCase):
    """Unit test the class"""
    def test_gpx_to_file(self):
        """Test the gpx to file"""
        g = GpxCSV()
        g.gpxtofile(['myfile.gpx'], output_name='myfile_test.csv')
        self.assertTrue(os.path.exists('myfile_test.csv'))
        g = GpxCSV(verbose=True)

        ### need to mock patch sys.stdout to check printing outputs

        g.gpxtofile(['myfile.gpx'], output_name='myfile_test.csv')

    def test_gpx_to_list(self):
        """Test the gpx to list"""
        g = GpxCSV()
        theList = g.gpxtolist('myfile.gpx')
        self.assertAlmostEqual(theList[0]['ele'], 51.820438)
