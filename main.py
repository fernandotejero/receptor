#################################################
# LoRa receiver
#
# Jorge Navarro-Ortiz (jorgenavarro@ugr.es), 2021
#################################################

DEBUG=False

from network import LoRa
import socket
import machine
import time

import os
import cv2

print('\n(c) Fernando Tejero Rodriguez\n')

# initialise LoRa in LORA mode
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
# more params can also be given, like frequency, tx power and spreading factor
lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868, frequency=868100000, tx_power=3, bandwidth=LoRa.BW_500KHZ, sf=7, preamble=8, coding_rate=LoRa.CODING_4_5)

# create a raw LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# Change frequency, spreading factor, coding rate... at any time
lora.frequency(868100000)
lora.sf(7)
lora.coding_rate(LoRa.CODING_4_5)

print('LoRa initialized!')

packets_per_measurement=100
i=0
while True:
    i=i+1
    # send some data
#    s.setblocking(True)
#    s.send('Hello')

    # get any data received...
    s.setblocking(True)
    message = s.recv(256)

    salida = "C:\Users\ferna\OneDrive\Escritorio\imagenes"
    
    os.makedirs(salida)
    print("Directorio creado: ", salida)

    cv2.imwrite(output_images_path + "/image" + str(count) + ".jpg", image)

    if DEBUG:
        print('[' + str(i) + '] Message sent: ' + str(message))
        print('[' + str(i) + '] LoRa stats: ' + str(lora.stats()))

    if i==1:
        time_start=time.ticks_us()

    if i%packets_per_measurement == 0:
        time_end=time.ticks_us()
        time_diff=time.ticks_diff(time_end,time_start)
        print('[' + str(i) + '] Received ' + str(packets_per_measurement) + ' packets of ' + str(len(message)) + ' bytes in ' + str(time_diff/1e6) + " seconds")
        throughput=packets_per_measurement*8*len(message)*1e6/time_diff
        print('[' + str(i) + '] Throughput ' + str(throughput) + ' bps')
        time_start=time_end

    # wait a random amount of time
#    time.sleep(machine.rng() & 0x0F)
