#!/usr/bin/env python3

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#
# Tests for colorMaptoHTML_v1.0.py, colorMaptoHTML_v1.3.py, colorMaptoSLD.py, SLDtoColorMap.py
#

import sys
import unittest2 as unittest
import xmlrunner
from optparse import OptionParser
import subprocess
import os

COLORMAP_2_HTMLv10_PATH = "/usr/bin/colorMaptoHTML_v1.0.py"
COLORMAP_2_HTMLv13_PATH = "/usr/bin/colorMaptoHTML_v1.3.py"
COLORMAP_2_SLD_PATH = "/usr/bin/colorMaptoSLD.py"
SLD_2_COLORMAP_PATH = "/usr/bin/SLDtoColorMap.py"

class TestColormapHTMLSLD(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.testdata_path = os.path.join(os.getcwd(), 'colormap_html_sld_test_data/')
        self.expected_outputs_path = os.path.join(self.testdata_path, "expected_outputs")
    
    # Tests converting a colormap to HTML using colorMaptoHTML_v1.0.py
    def test_colorMaptoHTML_v1_0(self):
        cmd = ["python3", COLORMAP_2_HTMLv10_PATH, "-c", os.path.join(self.testdata_path, "ColorMap_v1.2_Sample.xml")]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        html_output, err = process.communicate()
        if err.decode('utf-8') != "":
            self.fail("ERROR in {0}:\n{1}".format(COLORMAP_2_HTMLv10_PATH, err.decode("utf-8")))
        else:
            with open(os.path.join(self.expected_outputs_path, "test_colorMaptoHTML_v1_0_expected.html")) as expected_html:
                expected_html_output = expected_html.read()
            fail_str = ("HTML generated by {0} does not match expected.\n" +
                        "The following HTML was generated instead:\n{1}").format(COLORMAP_2_HTMLv10_PATH,
                                                                                 html_output.decode("utf-8"))
            self.assertTrue(expected_html_output == html_output.decode("utf-8"), fail_str)

    # Tests converting a colormap to HTML using colorMaptoHTML_v1.3.py
    def test_colorMaptoHTML_v1_3(self):
        cmd = ["python3", COLORMAP_2_HTMLv13_PATH, "-c", os.path.join(self.testdata_path, "ColorMap_v1.2_Sample.xml")]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        html_output, err = process.communicate()
        if err.decode('utf-8') != "":
            self.fail("ERROR in {0}:\n{1}".format(COLORMAP_2_HTMLv13_PATH, err.decode("utf-8")))
        else:
            with open(os.path.join(self.expected_outputs_path, "test_colorMaptoHTML_v1_3_expected.html")) as expected_html:
                expected_html_output = expected_html.read()
            fail_str = ("HTML generated by {0} does not match expected.\n" +
                        "The following HTML was generated instead:\n{1}").format(COLORMAP_2_HTMLv13_PATH,
                                                                                 html_output.decode("utf-8"))
            self.assertTrue(expected_html_output == html_output.decode("utf-8"), fail_str)

    # Tests converting from a colormap to SLD using colorMaptoSLD.py using `-s 1.0.0`.
    # Uses AIRS_Precipitation_Day_v1.0.0.xml, which lacks a "No Data" colormap,
    # as the `-s 1.0.0` option does not support "No Data".
    def test_colorMaptoSLD_v1_0_0(self):
        cmd = ["python3", COLORMAP_2_SLD_PATH, "-c", os.path.join(self.testdata_path, "AIRS_Precipitation_Day_v1.0.0.xml"),
               "-l", "Precipitation", "-r", "RGBA", "-s", "1.0.0"]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        sld_output, err = process.communicate()
        if err.decode('utf-8') != "":
            self.fail("ERROR in {0}:\n{1}".format(COLORMAP_2_SLD_PATH, err.decode("utf-8")))
        else:
            with open(os.path.join(self.expected_outputs_path, "test_colorMaptoSLD_v1_0_0_expected.sld")) as expected_sld:
                expected_sld_output = expected_sld.read()
            fail_str = ("SLD generated by {0} does not match expected.\n" +
                        "The following SLD was generated instead:\n{1}").format(COLORMAP_2_SLD_PATH, sld_output.decode("utf-8"))
            self.assertTrue(expected_sld_output == sld_output.decode("utf-8"), fail_str)

    # Tests converting from a colormap to SLD using colorMaptoSLD.py using `-s 1.1.0`.
    # Uses AIRS_Surface_Skin_Temperature_Daily_Day.xml, which has the "No Data" colormap listed first
    def test_colorMaptoSLD_v1_1_0_no_data_first(self):
        cmd = ["python3", COLORMAP_2_SLD_PATH, "-c", os.path.join(self.testdata_path, "AIRS_Surface_Skin_Temperature_Daily_Day.xml"),
               "-l", "Time-Averaged.AIRS3STD_006_SurfSkinTemp_A", "-r", "RGB", "-s", "1.1.0"]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        sld_output, err = process.communicate()
        if err.decode('utf-8') != "":
            self.fail("ERROR in {0}:\n{1}".format(COLORMAP_2_SLD_PATH, err.decode("utf-8")))
        else:
            with open(os.path.join(self.testdata_path, "AIRS_Surface_Skin_Temperature_Daily_Day_SLD.xml")) as expected_sld:
                expected_sld_output = expected_sld.read()
            fail_str = ("SLD generated by {0} does not match expected.\n" +
                        "The following SLD was generated instead:\n{1}").format(COLORMAP_2_SLD_PATH, sld_output.decode("utf-8"))
            self.assertTrue(expected_sld_output == sld_output.decode("utf-8"), fail_str)
    
    # Tests converting from a colormap to SLD using colorMaptoSLD.py using `-s 1.1.0`.
    # Uses AIRS_Surface_Skin_Temperature_Daily_Day_nodata_last.xml, which has the "No Data" colormap listed last
    def test_colorMaptoSLD_v1_1_0_no_data_last(self):
        cmd = ["python3", COLORMAP_2_SLD_PATH, "-c", os.path.join(self.testdata_path, "AIRS_Surface_Skin_Temperature_Daily_Day_nodata_last.xml"),
               "-l", "Time-Averaged.AIRS3STD_006_SurfSkinTemp_A", "-r", "RGB", "-s", "1.1.0"]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        sld_output, err = process.communicate()
        if err.decode('utf-8') != "":
            self.fail("ERROR in {0}:\n{1}".format(COLORMAP_2_SLD_PATH, err.decode("utf-8")))
        else:
            with open(os.path.join(self.testdata_path, "AIRS_Surface_Skin_Temperature_Daily_Day_SLD.xml")) as expected_sld:
                expected_sld_output = expected_sld.read()
            fail_str = ("SLD generated by {0} does not match expected.\n" +
                        "The following SLD was generated instead:\n{1}").format(COLORMAP_2_SLD_PATH, sld_output.decode("utf-8"))
            self.assertTrue(expected_sld_output == sld_output.decode("utf-8"), fail_str)

    # Tests converting from a v1.0.0 SLD (airsnrt-precip.sld) to a colormap
    def test_SLDtoColorMap_v1_0_0(self):
        cmd = ["python3", SLD_2_COLORMAP_PATH, "-s", os.path.join(self.testdata_path, "airsnrt-precip.sld"),
               "-l", "AIRS_Precipitation_A", "-r", "RGBA", "-u", "mm"]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        colormap_output, err = process.communicate()
        if err.decode('utf-8') != "":
            self.fail("ERROR in {0}:\n{1}".format(SLD_2_COLORMAP_PATH, err.decode("utf-8")))
        else:
            with open(os.path.join(self.expected_outputs_path, "test_SLDtoColorMap_v1_0_0_expected.xml")) as expected_sld:
                expected_colormap_output = expected_sld.read()
            fail_str = ("colormap generated by {0} does not match expected.\n" +
                        "The following colormap was generated instead:\n{1}").format(SLD_2_COLORMAP_PATH,
                                                                                     colormap_output.decode("utf-8"))
            self.assertTrue(expected_colormap_output == colormap_output.decode("utf-8"), fail_str)
        
    # Tests converting from a v1.0.0 SLD (airsnrt-precip.sld) to a colormap
    # Uses the `--offset` option with 10 as an argument, as well as the `--factor` option with 1.5 as an argument.
    def test_SLDtoColorMap_v1_0_0_offset_factor(self):
        cmd = ["python3", SLD_2_COLORMAP_PATH, "-s", os.path.join(self.testdata_path, "airsnrt-precip.sld"),
               "-l", "AIRS_Precipitation_A", "-r", "RGBA", "-u", "mm", "-o", "10", "-f", "1.5"]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        colormap_output, err = process.communicate()
        if err.decode('utf-8') != "":
            self.fail("ERROR in {0}:\n{1}".format(SLD_2_COLORMAP_PATH, err.decode("utf-8")))
        else:
            with open(os.path.join(self.expected_outputs_path, "test_SLDtoColorMap_v1_0_0_offset_factor_expected.xml")) as expected_sld:
                expected_colormap_output = expected_sld.read()
            fail_str = ("colormap generated by {0} does not match expected.\n" +
                        "The following colormap was generated instead:\n{1}").format(SLD_2_COLORMAP_PATH,
                                                                                     colormap_output.decode("utf-8"))
            self.assertTrue(expected_colormap_output == colormap_output.decode("utf-8"), fail_str)
    
    # Tests converting from a v1.0.0 SLD (airsnrt-precip.sld) to a colormap
    # Uses the `--precision` option with 3f as an argument
    def test_SLDtoColorMap_v1_0_0_precision(self):
        cmd = ["python3", SLD_2_COLORMAP_PATH, "-s", os.path.join(self.testdata_path, "airsnrt-precip.sld"),
               "-l", "AIRS_Precipitation_A", "-r", "RGBA", "-u", "mm", "-p", "3f"]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        colormap_output, err = process.communicate()
        if err.decode('utf-8') != "":
            self.fail("ERROR in {0}:\n{1}".format(SLD_2_COLORMAP_PATH, err.decode("utf-8")))
        else:
            with open(os.path.join(self.expected_outputs_path, "test_SLDtoColorMap_v1_0_0_precision_expected.xml")) as expected_sld:
                expected_colormap_output = expected_sld.read()
            fail_str = ("colormap generated by {0} does not match expected.\n" +
                        "The following colormap was generated instead:\n{1}").format(SLD_2_COLORMAP_PATH,
                                                                                     colormap_output.decode("utf-8"))
            self.assertTrue(expected_colormap_output == colormap_output.decode("utf-8"), fail_str)
    
    # Tests converting from a v1.1.0 SLD (AIRS_Surface_Skin_Temperature_Daily_Day_SLD.xml) to a colormap
    def test_SLDtoColorMap_v1_1_0(self):
        cmd = ["python3", SLD_2_COLORMAP_PATH, "-s", os.path.join(self.testdata_path, "AIRS_Surface_Skin_Temperature_Daily_Day_SLD.xml"),
               "-l", "Time-Averaged.AIRS3STD_006_SurfSkinTemp_A", "-u", "K", "-r", "RGB"]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        colormap_output, err = process.communicate()
        if err.decode('utf-8') != "":
            self.fail("ERROR in {0}:\n{1}".format(SLD_2_COLORMAP_PATH, err.decode("utf-8")))
        else:
            with open(os.path.join(self.expected_outputs_path, "test_SLDtoColorMap_v1_1_0_expected.xml")) as expected_sld:
                expected_colormap_output = expected_sld.read()
            fail_str = ("colormap generated by {0} does not match expected.\n" +
                        "The following colormap was generated instead:\n{1}").format(SLD_2_COLORMAP_PATH,
                                                                                     colormap_output.decode("utf-8"))
                                                                                                                            
            self.assertTrue(expected_colormap_output == colormap_output.decode("utf-8"), fail_str)

    # Tests converting from a v1.1.0 SLD (AIRS_Surface_Skin_Temperature_Daily_Day_SLD.xml) to a colormap
    # Uses the `--offset` option with 10 as an argument, as well as the `--factor` option with 1.5 as an argument.
    def test_SLDtoColorMap_v1_1_0_offset_factor(self):
        cmd = ["python3", SLD_2_COLORMAP_PATH, "-s", os.path.join(self.testdata_path, "AIRS_Surface_Skin_Temperature_Daily_Day_SLD.xml"),
               "-l", "Time-Averaged.AIRS3STD_006_SurfSkinTemp_A", "-u", "K", "-r", "RGB", "-o", "10", "-f", "1.5"]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        colormap_output, err = process.communicate()
        if err.decode('utf-8') != "":
            self.fail("ERROR in {0}:\n{1}".format(SLD_2_COLORMAP_PATH, err.decode("utf-8")))
        else:
            with open(os.path.join(self.expected_outputs_path, "test_SLDtoColorMap_v1_1_0_offset_factor_expected.xml")) as expected_sld:
                expected_colormap_output = expected_sld.read()
            fail_str = ("colormap generated by {0} does not match expected.\n" +
                        "The following colormap was generated instead:\n{1}").format(SLD_2_COLORMAP_PATH,
                                                                                     colormap_output.decode("utf-8"))
                                                                                                                            
            self.assertTrue(expected_colormap_output == colormap_output.decode("utf-8"), fail_str)

    # Tests converting from a v1.1.0 SLD (AIRS_Surface_Skin_Temperature_Daily_Day_SLD.xml) to a colormap
    # Uses the `--precision` option with "3f" as an argument
    def test_SLDtoColorMap_v1_1_0_precision(self):
        cmd = ["python3", SLD_2_COLORMAP_PATH, "-s", os.path.join(self.testdata_path, "AIRS_Surface_Skin_Temperature_Daily_Day_SLD.xml"),
               "-l", "Time-Averaged.AIRS3STD_006_SurfSkinTemp_A", "-u", "K", "-r", "RGB", "-p", "3f"]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        colormap_output, err = process.communicate()
        if err.decode('utf-8') != "":
            self.fail("ERROR in {0}:\n{1}".format(SLD_2_COLORMAP_PATH, err.decode("utf-8")))
        else:
            with open(os.path.join(self.expected_outputs_path, "test_SLDtoColorMap_v1_1_0_precision_expected.xml")) as expected_sld:
                expected_colormap_output = expected_sld.read()
            fail_str = ("colormap generated by {0} does not match expected.\n" +
                        "The following colormap was generated instead:\n{1}").format(SLD_2_COLORMAP_PATH,
                                                                                     colormap_output.decode("utf-8"))
                                                                                                                            
            self.assertTrue(expected_colormap_output == colormap_output.decode("utf-8"), fail_str)
    
    # Tests converting from a v1.1.0 SLD (AIRS_Surface_Skin_Temperature_Daily_Day_SLD.xml) to a colormap
    # Uses the `--densify` option with "r5" as an argument
    def test_SLDtoColorMap_v1_1_0_densify_r(self):
        cmd = ["python3", SLD_2_COLORMAP_PATH, "-s", os.path.join(self.testdata_path, "AIRS_Surface_Skin_Temperature_Daily_Day_SLD.xml"),
               "-l", "Time-Averaged.AIRS3STD_006_SurfSkinTemp_A", "-u", "K", "-r", "RGB", "-d", "r5"]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        colormap_output, err = process.communicate()
        if err.decode('utf-8') != "":
            self.fail("ERROR in {0}:\n{1}".format(SLD_2_COLORMAP_PATH, err.decode("utf-8")))
        else:
            with open(os.path.join(self.expected_outputs_path, "test_SLDtoColorMap_v1_1_0_densify_r_expected.xml")) as expected_sld:
                expected_colormap_output = expected_sld.read()
            fail_str = ("colormap generated by {0} does not match expected.\n" +
                        "The following colormap was generated instead:\n{1}").format(SLD_2_COLORMAP_PATH,
                                                                                     colormap_output.decode("utf-8"))
                                                                                                                            
            self.assertTrue(expected_colormap_output == colormap_output.decode("utf-8"), fail_str)

if __name__ == '__main__':
    # Parse options before running tests
    parser = OptionParser()
    parser.add_option(
        '-o',
        '--output',
        action='store',
        type='string',
        dest='outfile',
        default='test_colormap_html_sld_results.xml',
        help='Specify XML output file (default is test_colormap_html_sld_results.xml')
    parser.add_option(
        '-s',
        '--start_server',
        action='store_true',
        dest='start_server',
        help='Load test configuration into Apache and quit (for debugging)')
    (options, args) = parser.parse_args()

    # --start_server option runs the test Apache setup, then quits.
    if options.start_server:
        TestColormapHTMLSLD.setUpClass()
        sys.exit(
            'Apache has been loaded with the test configuration. No tests run.'
        )

    # Have to delete the arguments as they confuse unittest
    del sys.argv[1:]

    with open(options.outfile, 'wb') as f:
        print('\nStoring test results in "{0}"'.format(options.outfile))
        unittest.main(testRunner=xmlrunner.XMLTestRunner(output=f))
