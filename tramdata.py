import json
import csv
import sys
from haversine import haversine, Unit


STOP_FILE = './data/tramstops.json'
LINE_FILE = './data/tramlines.txt'

TRAM_FILE = './tramnetwork.json'


def build_tram_stops(jsonobject):
    stop_dict = {}
    with open(jsonobject, 'r', encoding="utf-8") as infile:
        data = json.load(infile)
        for stop in data:
            pos_dict = {}
            pos_dict["lat"] = data[stop]['position'][0]
            pos_dict["lon"] = data[stop]['position'][1]
            stop_dict[stop] = pos_dict
    return stop_dict
                

def build_tram_lines(lines):
    with open(lines, encoding="utf-8") as infile:
        rows = csv.reader(infile, delimiter="\t")
        time_dict, line_dict = {}, {}
        tram_line, pre_name, pre_time = "", "", 0
        for row in rows:
            if row == []:
               pre_name, pre_time = "", 0
            else:
                txt_list = row[0].split()
                if len(txt_list) == 1:
                    n = 0
                    if txt_list[0][n + 1].isdigit():
                        tram_line = txt_list[0][:2]
                    else:
                        tram_line = txt_list[0][0]
                    line_dict.setdefault(tram_line, [])
                else:
                    cur_name = " ".join(txt_list[:-1])              #sorted()
                    time = int(txt_list[-1][-2:])
                    line_dict[tram_line].append(cur_name)
                    sort1, sort2 = sorted((cur_name, pre_name))
                    if sort1 in time_dict:
                        time_dict[sort1][sort2] = time - pre_time
                    else:
                        time_dict.setdefault(sort1, {sort2: time - pre_time})
                    pre_name = cur_name
                    pre_time = time
    return line_dict, time_dict
        

def build_tram_network(stopfile, linefile):
    data = {"stops": build_tram_stops(stopfile), "lines": build_tram_lines(linefile)[0], "times":build_tram_lines(linefile)[1]}
    with open(TRAM_FILE, "w", encoding="utf-8") as outfile:
        json.dump(data, outfile, indent=2, ensure_ascii=False)


def lines_via_stop(linedict, stop):
    list = []
    for tram_lines in linedict:
        if stop in linedict[tram_lines]:
            list.append(tram_lines)
    return list


def lines_between_stops(linedict, stop1, stop2):
    list = []
    for tram_lines in linedict:
        if stop1 in linedict[tram_lines] and stop2 in linedict[tram_lines]:
            list.append(tram_lines)
    return list


def time_between_stops(linedict, timedict, line, stop1, stop2):
    if stop1 in linedict[line] and stop2 in linedict[line]:
        if linedict[line].index(stop2) < linedict[line].index(stop1):
            stop1, stop2 = stop2, stop1
        stop1_index = linedict[line].index(stop1)
        current_stop = linedict[line][stop1_index]
        next_stop = linedict[line][stop1_index + 1]
        time = 0
        while current_stop != stop2:
            if current_stop in timedict and next_stop in timedict[current_stop]:
                time += timedict[current_stop][next_stop]
            else:
                time += timedict[next_stop][current_stop]
            current_stop = next_stop
            if len(linedict[line]) > linedict[line].index(next_stop) + 1:
                next_stop = linedict[line][linedict[line].index(next_stop) + 1]
        return time
    else:
        print("The stops does not exist in the line given")


def distance_between_stops(stopdict, stop1, stop2):
    stop1_cord = (float(stopdict[stop1]["lat"]), float(stopdict[stop1]["lon"]))
    stop2_cord = (float(stopdict[stop2]["lat"]), float(stopdict[stop2]["lon"]))
    return haversine(stop1_cord, stop2_cord)
    

def dialogue(tramfile):
    with open(tramfile, "r", encoding="utf-8") as outfile:
        data = json.load(outfile)
    while True:
        query = input("Vafan vill du? ")
        if query == "quit":
            break
        print(answer_query(data, query))
        #return answer_query(data, query)


def answer_query(tramdict, query):
    q_split = query.split()
    try:
        if q_split[0] == "via":
            stop = " ".join(q_split[1:])
            return lines_via_stop(tramdict["lines"], stop)

        elif q_split[0] == "between":
            and_index = q_split.index("and")
            stop1 = " ".join(q_split[1:and_index])
            stop2 = " ".join(q_split[and_index + 1:])
            return lines_between_stops(tramdict["lines"], stop1, stop2) 

        elif q_split[0] == "time":
            to_index = q_split.index("to")
            line = q_split[2]
            stop1 = " ".join(q_split[4:to_index])
            stop2 = " ".join(q_split[to_index + 1:])
            return time_between_stops(tramdict["lines"], tramdict["times"], line, stop1, stop2)

        elif q_split[0] == "distance":
            to_index = q_split.index("to")
            stop1 = " ".join(q_split[2:to_index])
            stop2 = " ".join(q_split[to_index + 1:])
            return distance_between_stops(tramdict["stops"], stop1, stop2)
        
        else:
            return print("sorry, try again")
    except:
        return print("unknown arguments")

if __name__ == '__main__':
    if sys.argv[1:] == ['init']:
        build_tram_network(STOP_FILE, LINE_FILE)
    else:
        dialogue(TRAM_FILE)	


#build_tram_network(STOP_FILE, LINE_FILE)
