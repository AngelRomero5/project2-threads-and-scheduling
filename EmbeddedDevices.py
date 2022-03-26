# Created by Angel G. Romero Rosario on 9/22/21
# 801-18-2064

from threading import Thread
import random
import socket
import time 

# Range of sleep times
sleep_start, sleep_end = 1, 5

# Range of job times
job_start, job_end = 1, 100

# Limit of messages sent to the server side
message_limits = 50

# This thread sends messages with eDevice id and job time
class WorkerThread(Thread):
    
	# The constructor assign the internal id to the new thread.
	def __init__ (self, t_number):
			
		# This variable is used to assign an internal id to the thread.
		self.t_number = t_number
		Thread.__init__(self)

	def run(self):

		ctr = 0

		while ctr < message_limits:

			# Generate a random number for the sleep time and for the job_time 
			sleep_time = random.randint(sleep_start,sleep_end)
			job_time = random.randint(job_start, job_end)

			# Send message to the server side
			client_messenger(self.t_number, job_time)
			time.sleep(sleep_time)
			ctr += 1


# This function recieves the thread_id and job_time and send a 
# message with this info to the server side
def client_messenger(device_id, job_time):

	UDP_IP = "127.0.0.1"		# Ip Address
	UDP_PORT = 5005				# Port Address

	MESSAGE = bytes(str(device_id) + ":" + str(job_time), 'utf-8')
	
	sock = socket.socket(socket.AF_INET, 	# Internet
						socket.SOCK_DGRAM)  # UDP
	sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))


''' This is the main program '''

# Thread quantity
idealThreads = 6
thread = [0] * idealThreads

# Start the threads
for i in range(idealThreads):
	thread[i] = WorkerThread(i)
	thread[i].start()

# Wait for all the threads to do multithreading
for i in range(idealThreads):
	thread[i].join()