#!/usr/bin/env python
#
# This script runs the benchmarks described in the benchmarks.xml file.
# The output of these benchmarks is concatenated into a single html file
# (benchmark_result.html).
#

import os
import sys
import getopt
import xml.dom.minidom

top = """\
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html>
<head>
  <title>Benchmark suite result</title>
</head>

<body>
<u><h1>Benchmark suite result</h1></u>
<br/>
"""

bottom = """
</body>
</html>
"""

def configure_environment():
    os.putenv('DISPLAY',':0.0')

def get_benchmark_html_template(name, description, command, result):
    text = "<h3><i>" + name + "</i></h3> \
        <hr/><table> \
        <tr><td><i><u>Description:</u></i></td><td>" + description + "</td></tr> \
        <tr><td><i><u>Command:</u></i></td><td>" + command + " </td></tr> \
        </table> \
        <br/> \
        <u><i>Result:</u></i> \
        <p>" + result + "</p> \
        <br/>"
    return text

def get_benchmark_nodes(benchmarks_node):
    benchmark_nodes = []
    for node in benchmarks_node.childNodes:
        if node.nodeType == node.ELEMENT_NODE and node.localName == "benchmark":
            benchmark_nodes.append(node)
    return benchmark_nodes

def get_text_node(nodes):
    text = ""
    for node in nodes:
        if node.nodeType == node.TEXT_NODE:
            text = text + node.data
    return text

def run_benchmarks(benchmark_nodes):
    result_html = top
    for benchmark_node in benchmark_nodes:
        name = ""
        description = ""
        command = ""
        result = ""

        for node in benchmark_node.childNodes:
            if node.nodeType == node.ELEMENT_NODE and \
               node.localName == "name":
                name = get_text_node(node.childNodes)
            if node.nodeType == node.ELEMENT_NODE and \
               node.localName == "description":
                description = get_text_node(node.childNodes)
            if node.nodeType == node.ELEMENT_NODE and \
               node.localName == "command":
                command = get_text_node(node.childNodes)
                print "run benchmark: " + name + " - " + command + " ..."
                p = os.popen(command);
                result = p.read().replace("\n","<br/>")
                p.close()
        result_html += get_benchmark_html_template(name, description, command, result)

    result_html += bottom
    return result_html

def usage():
    print "Benchmark runner\n"
    print "benchmark_runner.py: [-h] [-c benchmarks.xml] ..."
    print ""
    print " -h : help"
    print " -c : benchmarks configuration file in xml format (defaults benchmarks.xml)"
    print ""

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:", ["help config="])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)

    configure_environment()

    benchmarks = "benchmarks.xml"
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        if o == "-c":
            benchmarks = a

    doc = xml.dom.minidom.parse(benchmarks)
    benchmarks_node = doc.childNodes[0]
    benchmark_nodes = get_benchmark_nodes(benchmarks_node)
    result_html = run_benchmarks(benchmark_nodes)

    fp = open("benchmarks_result.html", "w")
    fp.write(result_html)
    fp.close()

if __name__ == "__main__":
    main()
