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

    # Dummy values for pressure calculations
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

        # Add first 10 values for average pressure at 0 height    
        if i < 11*128:
            av.append(pressure[0])

        # Set min pressure
        if pressure[0] < min:
            min = pressure [0]

        else:
            pass
                   
        # Increment file pointer
        i += 128

        
    print('Minimum value of pressure is ', min/100, ' mBar')

    # Calculate average ground pressure
    ave = sum(av)/len(av)

    # Set necessary constants
    rho = 1.225
    g = 9.81

    # Calculate height from pressure (assume air density constant)
    h = abs(ave-min)/(g*rho)
    print('The maximum height reached is {0:.2f}'.format(h) + ' m')
