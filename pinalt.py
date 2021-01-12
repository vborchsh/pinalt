#! /usr/bin/env python

import sys
import csv
import os

# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
def pins_extraction(filename, exclude_nets):
    content = ''
    VERSION = '0.0.2'

    content = content + '\n\t# pinalt(ium) generator version: %s\n\n' % VERSION

    netlist = []
    qsflist = []
    xdclist = []

    # File reading
    with open(filename, "r") as pf:
        reader = csv.reader(pf, delimiter=',')
        next(reader) # Skip Altium header
        next(reader) # Skip empty string-separator
        next(reader) # Skip headers
        for row in reader:
            pinname = row[0]
            netname = row[1]
            netname = netname.lower()
            if pinname and netname:
                    netlist.append(netname)
                    qsflist.append([netname, pinname])
                    xdclist.append([netname, pinname])

    netcontent = content
    qsfcontent = content
    xdccontent = content

    netlist.sort()
    qsflist.sort()
    xdclist.sort()

    for qsf in qsflist:
        net = qsf[0]
        pin = qsf[1]
        if net in exclude_nets:
            pass
        else:
            qsfcontent = qsfcontent + 'set_location_assignment PIN_%s -to %s\n' % (pin, net)

    for xdc in xdclist:
        net = xdc[0]
        pin = xdc[1]
        if net in exclude_nets:
            pass
        else:
            xdccontent = xdccontent + 'set_property PACKAGE_PIN %s [get_ports {%s}]\n' % (pin, net)
			
    for net in netlist:
        if net in exclude_nets:
            pass
        else:
            netcontent = netcontent + '%s\n' % (net)

    # Get pure filename
    os_filename = os.path.basename(filename)
    index_of_dot = os_filename.index('.')
    pure_filename = os_filename[:index_of_dot]

    # Saving to files
    fdwt = open((pure_filename + '.qsf'), "w")
    fdwt.write(qsfcontent)
    fdwt.close()

    fdwt = open((pure_filename + '.xdc'), "w")
    fdwt.write(xdccontent)
    fdwt.close()

    fdwt = open((pure_filename + 'net.txt'), "w")
    fdwt.write(netcontent)
    fdwt.close()

# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
def error (msg):
    print(msg, file=sys.stderr)
    print("\nCorrect format is :\n\npinalt.py <pinmap csv file> <ignoring nets>", file=sys.stderr)
    sys.exit(100)

# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    nargs = len(sys.argv) - 1

    exclude_nets = []

    if nargs < 1:
        error("ERROR: %d arguments less then 1;" % nargs)
    else:
        for net in sys.argv[2:]:
            exclude_nets.append(net.lower());
        try:
            pins_extraction(sys.argv[1], exclude_nets)
        except IOError:
            error("ERROR: Invalid netfilename;")
