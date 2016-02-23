#!/usr/bin/python3
# FileName: runDemo.py
# Author: lxw
# Date: 2016-02-23

from threadpool.threadpool import ThreadPool
import time

def echo(number):
    """
    Echo with the parameter "number".
    """
    time.sleep(3)
    print("In echo(): {0}".format(number))


def main():
    """
    Test the implementation of ThreadPool.
    """
    pool = ThreadPool(4)
    for number in range(20):
        pool.add_task(echo, number)
    pool.destroy()


if __name__ == '__main__':
    main()
else:
    print("Being imported as a module.")
