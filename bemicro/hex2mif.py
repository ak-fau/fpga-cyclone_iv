#!/usr/bin/env python2

WIDTH = 8
MIN_ADDR = 0
MAX_ADDR = 0xFFFF + 1
GAP_FILL = 0xFF

import sys
from numbers import Number
from intelhex import IntelHex

def mif_header(data_width = WIDTH,
               minaddr = MIN_ADDR,
               maxaddr = MAX_ADDR,
               addr_radix = "HEX",
               data_radix = "HEX"):
    s  = """-- DO NOT EDIT!
-- This file is autogenerated with hex2mif.py script
--
"""
    s += "DEPTH = %d;\n" % (maxaddr - minaddr)
    s += "WIDTH = %d;\n" % data_width
    s += "ADDRESS_RADIX = %s;\n" % addr_radix
    s += "DATA_RADIX = %s;\n" % data_radix
    return s

def mif_data(data = {},
             minaddr = MIN_ADDR,
             maxaddr = MAX_ADDR,
             gap_fill = GAP_FILL):
    s = "CONTENT\n"
    s += "BEGIN\n"
    s += "[%x..%x] : %x;\n" %(minaddr, maxaddr-1, gap_fill)
    for k in data.keys():
        if isinstance(k, Number):
            s += "%x : %x;\n" %(k, data[k])
    s += "END;\n"
    return s

if __name__ == '__main__':
    ih = IntelHex()
    ih.fromfile(sys.stdin, format='hex')
    data = ih.todict()

    for a in range(0, 4096, 4):
        if data.has_key(a):
            d = data[a] + (data[a+1] << 8) + (data[a+2] << 16) + (data[a+3] << 24)
            del data[a], data[a+1], data[a+2], data[a+3]
            data[a] = d

    print mif_header(32, 0, 4096)
    print mif_data(data, 0, 4096, 0x00000013)