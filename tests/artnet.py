"""Modified version of the example from cpvalente on GitHub used to set an 8 channel head patched at address 1 to change from red, to green, to blue."""

from stupidArtnet import StupidArtnet
import time
import random

# THESE ARE MOST LIKELY THE VALUES YOU WILL BE NEEDING
target_ip = '192.168.56.1'		# typically in 2.x or 10.x range
universe = 0 										# see docs
packet_size = 100								# it is not necessary to send whole universe

# CREATING A STUPID ARTNET OBJECT
# SETUP NEEDS A FEW ELEMENTS
# TARGET_IP   = DEFAULT 127.0.0.1
# UNIVERSE    = DEFAULT 0
# PACKET_SIZE = DEFAULT 512
# FRAME_RATE  = DEFAULT 30
# ISBROADCAST = DEFAULT FALSE
a = StupidArtnet(target_ip, universe, packet_size, 30, True, True)

# MORE ADVANCED CAN BE SET WITH SETTERS IF NEEDED
# NET         = DEFAULT 0
# SUBNET      = DEFAULT 0



# CHECK INIT
print(a)

# YOU CAN CREATE YOUR OWN BYTE ARRAY OF PACKET_SIZE
packet = bytearray(packet_size)		# create packet for Artnet
for i in range(packet_size):			# fill packet with sequential values
    packet[i] = (i % 256)

# ... AND SET IT TO STUPID ARTNET
a.set(packet)						# only on changes

# ALL PACKETS ARE SAVED IN THE CLASS, YOU CAN CHANGE SINGLE VALUES
		# set channel 1 to 255
# a.clear()
# a.start()
# a.set_single_value(1, 255)	
# for i in range(4):
#     print("Setting channel %d to 255" % (i + 2))
#     a.set_single_value(i + 2, 255)		# set first 4 channels to 255
#     if (i > 0):
#         a.set_single_value(i+1, 0)		# set previous 4 channels to 0
#     time.sleep(1)

a.clear()
a.start()
a.set_single_value(1, 255)
a.set_single_value(2, 255)
a.set_single_value(3, 255)
a.set_single_value(4, 255)
a.set_single_value(5, 255)
a.set_single_value(6, 255)
time.sleep(5)

# Do a rainbow effect
while True:    
    a.clear()
    a.start()
    a.set_single_value(1, 255)
    for i in range(255):
        a.set_single_value(2, i)
        time.sleep(0.01)
    for i in range(255):
        a.set_single_value(3, i)
        time.sleep(0.01)
    for i in range(255):
        a.set_single_value(2, 255 - i)
        time.sleep(0.01)
    for i in range(255):
        a.set_single_value(4, i)
        time.sleep(0.01)
    for i in range(255):
        a.set_single_value(3, 255 - i)
        time.sleep(0.01)