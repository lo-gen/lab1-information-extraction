import unittest
from tramdata import *

STOP_FILE = './data/tramstops.json'
LINE_FILE = './data/tramlines.txt'
TRAM_FILE = './tramnetwork.json'

class TestTramData(unittest.TestCase):

    def setUp(self):
        with open(TRAM_FILE) as trams:
            tramdict = json.loads(trams.read())
            self.stopdict = tramdict['stops']
            self.linedict = tramdict['lines']
            self.timedict = tramdict["times"]

    def test_stops_exist(self):
        stopset = {stop for line in self.linedict for stop in self.linedict[line]}
        for stop in stopset:
            self.assertIn(stop, self.stopdict, msg = stop + ' not in stopdict')

    def test_lines_in_linedict(self):
        with open(LINE_FILE, encoding="utf-8") as infile:
            rows = csv.reader(infile, delimiter="\t")
            list_of_lines = []
            tram_line = ""
            for row in rows:
                if row != []:
                    txt_list = row[0].split()
                    if len(txt_list) == 1:
                        n = 0
                        if txt_list[0][n + 1].isdigit():
                            tram_line = txt_list[0][:2]
                        else:
                            tram_line = txt_list[0][0]
                        list_of_lines.append(tram_line)
        real_list_of_lines = []
        for line in self.linedict:
            real_list_of_lines.append(line)
        self.assertEqual(list_of_lines, real_list_of_lines, msg = "All lines are not in the linedict")

    def test_stops_in_tramline(self):
        pass

    def test_distance(self):
        for stop1 in self.stopdict:
            for stop2 in self.stopdict:
                self.assertTrue(20 > distance_between_stops(self.stopdict, stop1, stop2),
                                msg = "Distance longer then 20km between " + stop1 + " and " + stop2
                                )

    def test_time(self):
        for line in self.linedict:
            for stop1 in self.linedict[line]:
                for stop2 in self.linedict[line]:  
                    self.assertEqual(time_between_stops(self.linedict, self.timedict, line, stop1, stop2), 
                                    time_between_stops(self.linedict, self.timedict, line, stop2, stop1), 
                                    msg = "Time not equal for " + stop1 + "-" + stop2 + " and " + stop2 + "-" + stop1
                                    )

if __name__ == '__main__':
    unittest.main()

