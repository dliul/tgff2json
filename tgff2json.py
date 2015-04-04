#!/usr/bin/python

__author__ = "Di Liu"
__description__ = "Parse a tgff graph and convert it to a json format"

import re
import sys
import os.path
import argparse
import json
import string


class task:
    """ Class task represents one task in task graph.
        It is comprised of the following properties:
        taskID     an unique task id
        prec        all precedent tasks
    """
    def __init__(self):
        taskID = 0

class graph:
    """ This class represents the graph read from the input
        file.
    """
    def __init__(self):
        task_num = 0
        tasks = []
        edges = []


def parse(filename, output):
    
    g = graph()
    data = {}
    data['tasks'] = []
    data['edges'] = []
    with open(filename,"r") as f:
        while True:
            line = f.readline()
            if not line:
                break
            sl = line.split()
            if sl and sl[0] == "@HYPERPERIOD":
                hp = {'hyperperiod':sl[1]}
                data.update(hp)
            elif sl and sl[0] == "PERIOD":
                p = {'period':sl[1]}
                data.update(p)
            elif sl and sl[0] == "TASK":
                task = {'taskID':sl[1],'type': sl[-1]}
                data['tasks'].append(task)   
            elif sl and sl[0] == "ARC":
                edge = {'edgeID':sl[1],'from':sl[3],'to':sl[5],'type':sl[-1]}
                data['edges'].append(edge)
        data.update({'task cnt':len(data['tasks'])})
        data.update({'edge cnt':len(data['edges'])})
    r = open(output, 'w')    
    json.dump(data,r,indent=4)   
    r.close()


def main():
    """ Main method in tgff2paser.
    """
    parser = argparse.ArgumentParser(description=__description__, epilog= "Author: %s" 
            % __author__)
    parser.add_argument("tgff", help="The path to the tgff graph")
    parser.add_argument("-o", default="output.json", help=
            "The name of the output file. (Default name: filename.json)")
    args = parser.parse_args()
   
    if not os.path.exists(args.tgff):
        sys.stderr.write("Error! the provided path does not exist! \n")
        sys.exit(-1)

    filename = args.o
    fn, fe = os.path.splitext(args.tgff)
    output = fn + ".json"
    
    if fe == '.tgff':
        print "Parse tgff %s and convert it to a json file" % args.tgff
        parse(args.tgff,output)
    else:
        print "Parse %s and convert it to a json file" % args.tgff





if __name__ == '__main__':
    main()


