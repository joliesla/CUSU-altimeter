#!/usr/bin/env python3

import sys
import struct


# Useage
if len(sys.argv) != 2:
    print("Usage: {} <log_00011.bin>".format(sys.argv[0]))
    sys.exit(1)


# Message Type Definitions
MESSAGE_PRESSURE = 1        
        
# Open log file
with open(sys.argv[1], 'rb') as log:

    # Read File
    log.read();

    # File pointer
    i = 0
    num_bytes = log.tell()
    min = 100000000
    av = []
    
    # Loop until EOF
    while i in range(num_bytes):
        
        # Seek to next log
        log.seek(i)
        
        # Read Metadata
        header = log.read(5)    
        
        # Get Message Metadata
        meta_data = struct.unpack('<BI', header)
        log_type = meta_data[0]
        systick = meta_data[1]
        systick /= 10000.0

            
        
        # Read Raw Pressure 
        if (log_type == MESSAGE_PRESSURE):
                       
            payload = log.read(4)
            pressure = struct.unpack('<I', payload)
            print("Time = ", systick, "s", "    Pressure = ", pressure[0]/100.0, "mBar")
        if i < 11*128:
            av.append(pressure[0])


        if pressure[0] < min:
            min = pressure [0]

        else:
            pass
                   
        # Increment file pointer
        i += 128
    print('Minimum value of pressure is ', min/100, ' mBar')
    ave = sum(av)/len(av)
    min = 97772
    rho = 1.225
    g = 9.81
    h = abs(ave-min)/(g*rho)
    print('The maximum height reached is {0:.2f}'.format(h) + ' m')
