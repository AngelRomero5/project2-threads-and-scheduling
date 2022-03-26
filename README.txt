Created by Angel G. Romero Rosario on 9/22/2021

Project 2: Embedded Devices and a Central Compute Server

On this programs I use the following libraries:
    - threading
    - random
    - socket
    - time 

This program is divided into Embedded Devices and the Server:

    1) The eDevices will generate random numbers and then send a message
       using UDP to the Central Compute Server and "executes" a sleep time.
       The message contains the device id and the job-time. It is set to 
       a fixed number of messages it can send but the variable's value can
       change. The program also creates a fixed number of threads to do the 'jobs'.
    
    2) The Central Server will listen to the client side and will recieve messages
       containing the device id and the job time. This info is then saved to an 
       implemented queue class sorted using the job time. Another thread will extract
       the first pair of the queue and "execute" the job time and adds that time to 
       a table with all the devices id's and the total job time's in its respective device id.


EmbeddedDevices.py : 

    # This class recieves an id number. 
    # Creates a thread that works as an eDevice simulating a job.
    # The thread sends a message using a function that contains the device id 
    # and a job time asigned randomly.
    # It then executes a random sleep time between executions of the same thread.
        
        class WorkerThread(Thread) 

    # This function recieves the eDevice id and its respective job time.
    # This function uses UDP to send a message to the Central Compute Server.
    # The message contains the device_id and job_time 
        
        def client_messenger(device_id, job_time)

ComputeServer.py:

    # The following are variables that act as a mutual excusion and a semaphore 
    # respectivly

        mutex = Lock()
        available_spaces = Semaphore(0)

    # This class serves as an implementation of a queue 
    # It has a constructor, a enqueue() function, a dequeue() function
    # and a isEmpty() function 

        class SchedulerQueue()

            # This function inserts a pair of device id and job time in 
            # the ascending order using the job_time.
            # It uses the bubble sorting algorithm 
            def enqueue(self, device_id, job_time) 

            # Removes first item on the queue
            def dequeue(self)

            # Checks if queue is empty 
            def isEmpty(self)
    
    # This class acts as the thread that "listens" to the client side
    # This function recieves the queue object and it inserts at the end of the queue 
    # The eDevice id, and its respective job time
    # It uses a mutual exclusion variable that allows the thread to finish its job, 
    # before allowing other thread to run. 

        class ListenerThread(Thread)

    # This class works as the thread that recieves a queue object,
    # it extracts the first element on the queue and while there is
    # something on the queue, it "executes" the job time
    # After executing the job time, it sums that time to a variable associated 
    # with the eDevice id that performed that job time
    # This is later saved to a diccionary that works as a record table

        class ConsumerThread(Thread)


How to use the program:

    1) First, open a terminal and run the ComputeServer.py
    2) Second, open another terminal (or tab) and run the EmbeddedDevices.py
    3) This should display at the end the total job times of each eDevice
    4) There are commented prints through the program that can be used to check
       how the data is being pass from the client side to the Compute Server. 

    
People that helped me:

    Jasiel Rivera Trinidad
    Eliam Ruiz 

    







