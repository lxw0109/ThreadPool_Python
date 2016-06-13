#!/usr/bin/python2.7
# FileName: runDemo.py
# Author: lxw
# Date: 2016-02-23

from threadpool.threadpool import ThreadPool
import time

QUEUE_THREADS0 = 3
QUEUE_THREADS1 = 0.5

def echo(number):
    """
    Echo with the parameter "number".
    """
    time.sleep(QUEUE_THREADS0)
    print "In echo(): {0}".format(number)


def main():
    pool = ThreadPool(4)
    for number in range(20):
        pool.add_task(echo, number)
        time.sleep(QUEUE_THREADS1)
    pool.destroy()

    print "Main Thread Terminates."

if __name__ == '__main__':
    main()
else:
    print "Being imported as a module."
