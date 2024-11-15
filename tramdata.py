import json
import csv

def build_tram_stops(jsonobject):
    stop_dict = {}
    with open(jsonobject, 'r') as infile:
        data = json.load(infile)
        for stop in data:
            pos_dict = {}
            pos_dict["lat"] = data[stop]['position'][0]
            pos_dict["lon"] = data[stop]['position'][1]
            stop_dict[stop] = pos_dict
    return stop_dict
                

def build_tram_lines(lines):
    with open(lines) as infile:
        rows = csv.reader(infile, delimiter="\t")
        time_dict, line_dict = {}, {}
        tram_line, stop_name, stop_time = 1, "", 0
        for row in rows:
            if row == []:
               tram_line += 1
               stop_name, stop_time = "", 0
            else:
                txt_list = row[0].split()
                if len(txt_list) == 1:
                    line_dict.setdefault(str(tram_line), [])
                else:
                    if len(txt_list) == 3:
                        name = txt_list[0] + " " + txt_list[1]
                    elif len(txt_list) == 4:
                        name = txt_list[0] + " " + txt_list[1] + " " + txt_list[2]
                    else:
                        name = txt_list[0]
                    time = int(txt_list[-1][-2:])
                    line_dict[str(tram_line)].append(name)
                    if stop_name in time_dict:
                        time_dict[stop_name][name] = time - stop_time
                    else:
                        time_dict.setdefault(name, {})
                    stop_name = name
                    stop_time = time
    return line_dict, time_dict
        
