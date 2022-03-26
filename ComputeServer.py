# Created by Angel G. Romero Rosario on 9/22/21
# 801-18-2064

from threading import Thread, Lock, Semaphore
import socket
import time

message_limits = 20  # How many messages the server can receive
mutex = Lock()       # Create a mutual exclusion variable 

available_spaces = Semaphore(0)  # This semaphore will allow to block a thread so it doesn't poll for messages

# This class will act as the scheduler queue
class SchedulerQueue():

    # Constructor
    def __init__(self):

        self.__init__
        self.myqueue = []

    # Function to add an element to the queue
    def enqueu(self, device_id, job_time):

        # Append pair into the queue
        self.myqueue.append([device_id, job_time])

        # Implementation of a bubble sort algorithm
        for x in range(len(self.myqueue)):
            is_sorted = True
            for y in range(len(self.myqueue) - x - 1):
                if self.myqueue[y][1] > self.myqueue[y+1][1]:

                    # Swap elements
                    self.myqueue[y], self.myqueue[y+1] = self.myqueue[y+1], self.myqueue[y]

                    is_sorted = False

            if is_sorted:
                break

        
    # Function to extract first element from the queue
    def dequeue(self):
        if self.isEmpty():
            return(-1)      # If the queue is empty, it will return -1
        else:
            return self.myqueue.pop(0)

    # This function returns True if is empty
    def isEmpty(self):
        if len(self.myqueue) == 0:
            return True
        else:
            return False


# This thread will listen to the client side and will save the jobs to a queue
class ListenerThread(Thread):

    def __init__ (self, tQueue : SchedulerQueue):
        Thread.__init__(self)
        self.tQueue = tQueue

    def run(self):
        #  IP Address and port number
        UDP_IP = "127.0.0.1" 
        UDP_PORT = 5005

        sock = socket.socket(socket.AF_INET, # Internet
                            socket.SOCK_DGRAM) # UDP
        sock.bind((UDP_IP, UDP_PORT))

        global message_limits
        ctr = 0
        
        while ctr < message_limits:

            available_spaces.release()  # Semaphore

            mutex.acquire()             # Access to critical region is now blocked for other threads

            data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            data_pair = str(data)            # Convert from byte to string

            dthread = int(data_pair[2]) # Thread
            dtime = int(data_pair[4])   # Jobtime

            # Save the info into the queue
            self.tQueue.enqueu(dthread, dtime) 
            ctr+=1

            print(data_pair)

            mutex.release()     # Access to critical region is now unlocked for other threads


# This class works as the thread that recieves a queue object,
# it extracts the first element on the queue and while there is
# something on the queue, it "executes" the job time
# After executing the job time, it sums that time to a variable associated 
# with the eDevice id that performed that job time
# This is later saved to a diccionary that works as a record table
class ConsumerThread(Thread):

    def __init__(self, tQueue : SchedulerQueue, table : dict):
        Thread.__init__(self)
        self.tQueue = tQueue
        self.table = table

    def run(self):

        ctr = 0         # Counter variable
        while ctr < message_limits:

            available_spaces.acquire()

            # print("Entre al consumer con: "+ )

            mutex.acquire()     # Access to critical region is now blocked for other threads

            # Create a pair of the times for each job per thread
            pair = self.tQueue.dequeue()

            # If the thread is in record, sum the job time
            if pair[0] in self.table.keys():
                new_job_time = pair[1] + self.table[pair[0]]

                self.table[pair[0]] = new_job_time
                # Simulate the job
                time.sleep(pair[1])
            # Else: create the space for it
            else:
                self.table[pair[0]] = pair[1]
                # Simulate the job, sleep for that moment
                time.sleep(pair[1])

            mutex.release()     # Access to critical region is now unlocked for other threads 
            ctr += 1

# Main program here
def main():
    ''' This is the main program '''
    
    thread_queue = SchedulerQueue()         # Thread Queue will save thread id and job time
    table = {}                              # This table contains the embedded devices' id and it total job time

    LThread = ListenerThread(thread_queue)  # Create Thread object
    LThread.start()                         # Start Thread object
    LThread.join()                          # Wait for other threads

    CThread = ConsumerThread(thread_queue, table) 
    CThread.start()
    CThread.join()

    for key, value in table.items():
        print("\n Device " + str(key) + " consumed " + str(value) + " seconds of CPU time")

# Main function to start program 
main()