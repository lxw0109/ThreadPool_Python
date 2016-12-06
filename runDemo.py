#!/usr/bin/python2.7
# FileName: runDemo.py
# Author: lxw
# Date: 2016-02-23

from threadpool.threadpool import ThreadPool
import time

EXACT4THREADS0 = 2
EXACT4THREADS1 = 0.5

#In this situation, more than 2 threads are in the queue during the process of running.
QUEUE_THREADS0 = 3
QUEUE_THREADS1 = 0.5

def echo(number):
    """
    Echo with the parameter "number".
    """
    #time.sleep(EXACT4THREADS0)
    time.sleep(QUEUE_THREADS0)
    #print("In echo(): {0}".format(number))
    print "In echo(): {0}".format(number)


def main():
    """
    Test the implementation of ThreadPool.
    """
    pool = ThreadPool(4)
    for number in range(20):
        pool.add_task(echo, number)
        #time.sleep(EXACT4THREADS1)
        time.sleep(QUEUE_THREADS1)
    pool.destroy()
    #QUEUE_THREADS0 & QUEUE_THREADS1 can prove that daemon thread "TERMINATES" with main thread.
    print "Main Thread Terminates."


if __name__ == '__main__':
    main()
else:
    #print("Being imported as a module.")
    print "Being imported as a module."

