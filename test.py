#!/usr/bin/python2.7
# FileName: test.py
# Author: lxw
# Date: 2016-02-23

from threadpool.threadpool import ThreadPool
import time

QUEUE_THREADS0 = 3
QUEUE_THREADS1 = 0.5

pool = ThreadPool(4)

def echo(number):
    """
    Echo with the parameter "number".
    """
    time.sleep(QUEUE_THREADS0)
    print "In echo(): {0}. in_queue.qsize: {1}".format(number, pool.get_in_queue_size())


def main():
    """
    Test the implementation of ThreadPool.
    """
    for number in range(20):
        pool.add_task(echo, number)
        time.sleep(QUEUE_THREADS1)
    pool.destroy()
    print "Main Thread Over"


if __name__ == '__main__':
    main()
else:
    print "Being imported as a module."
