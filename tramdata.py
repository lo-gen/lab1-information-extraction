import json
import csv

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
        tram_line, stop_name, stop_time = "", "", 0
        for row in rows:
            if row == []:
               stop_name, stop_time = "", 0
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
                    if len(txt_list) == 3:
                        name = txt_list[0] + " " + txt_list[1]
                    elif len(txt_list) == 4:
                        name = txt_list[0] + " " + txt_list[1] + " " + txt_list[2]
                    else:
                        name = txt_list[0]
                    time = int(txt_list[-1][-2:])
                    line_dict[tram_line].append(name)
                    if stop_name in time_dict:
                        time_dict[stop_name][name] = time - stop_time
                    else:
                        time_dict.setdefault(stop_name, {name: time - stop_time})
                    stop_name = name
                    stop_time = time
    return line_dict, time_dict
        

def build_tram_network(stopfile, linefile):
    data = {"stops": build_tram_stops(stopfile), "lines": build_tram_lines(linefile)[0], "times":build_tram_lines(linefile)[1]}
    with open("tramnetwork.json", "w", encoding="utf-8") as outfile:
        json.dump(data, outfile, indent=2, ensure_ascii=False)


def lines_via_stop(linedict, stop):
    for tram_lines in linedict:
        if stop in linedict[tram_lines]:
            print(tram_lines)

def lines_between_stops(linedict, stop1, stop2):
    for tram_lines in linedict:
        if stop1 in linedict[tram_lines] and stop2 in linedict[tram_lines]:
            print(tram_lines)

def time_between_stops(linedict, timedict, line, stop1, stop2):
    if stop1 in linedict[line] and stop2 in linedict[line]:
        if linedict[line].index(stop2) < linedict[line].index(stop1):
            stop1, stop2 = stop2, stop1
        stop1_index, stop2_index = linedict[line].index(stop1), linedict[line].index(stop2)
        current_stop = linedict[line][stop1_index]
        next_stop = linedict[line][stop1_index + 1]
        time = 0
        while current_stop != stop2:
            print(current_stop)
            if current_stop in timedict and timedict[current_stop] != {}:
                time += timedict[current_stop][next_stop]
            else:
                time += timedict[next_stop][current_stop]
            current_stop = next_stop
            if len(linedict[line]) > linedict[line].index(next_stop) + 1:
                next_stop = linedict[line][linedict[line].index(next_stop) + 1]
        print(time)


            

            
    else:
        print("The stops does not exist in the line given")




#lines_via_stop(build_tram_lines("tramlines.txt")[0], "Opaltorget")

#lines_between_stops(build_tram_lines("tramlines.txt")[0], "Chalmers","Marklandsgatan")

time_between_stops(build_tram_lines("tramlines.txt")[0], build_tram_lines("tramlines.txt")[1], "6", "Aprilgatan", "Varmfrontsgatan")

build_tram_network("tramstops.json", "tramlines.txt")

#print(build_tram_stops("tramstops.json"))

#print(build_tram_lines("tramlines.txt"))


#print(build_tram_stops("tramstops.json"))

    #data = {: row for row in rows} 

#print(data)
