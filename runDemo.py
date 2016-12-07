#!/usr/bin/python2.7
#coding: utf-8
# FileName: runDemo.py
# Author: lxw
# Date: 2016-02-23

#NOTE: when using threadpool, the threadpool.destroy() is ESSENTIAL to revoke.

from threadpool.threadpool import ThreadPool
import time
import logging

EXACT4THREADS0 = 2
EXACT4THREADS1 = 0.5
#EXACT4THREADS1 = 0.2

#In this situation, more than 2 threads are in the queue during the process of running.
QUEUE_THREADS0 = 3
QUEUE_THREADS1 = 0.5

logging.basicConfig(level=logging.DEBUG,  
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s',  
                    datefmt='%a, %d %b %Y %H:%M:%S',  
                    filename="./runDemo.log",#'/home/lxw/IT/program/github/ThreadPool_Python/runDemo.log',  
                    filemode='w')  

def echo(number):
    """
    Echo with the parameter "number".
    """
    time.sleep(EXACT4THREADS0)
    #time.sleep(QUEUE_THREADS0)
    logging.debug("In echo(): {0}".format(number))


def main():
    """
    Test the implementation of ThreadPool.
    """
    try:
        pool = ThreadPool(4)
        for number in range(20):
            pool.add_task(echo, number)
            time.sleep(EXACT4THREADS1)
            #time.sleep(QUEUE_THREADS1)
        #QUEUE_THREADS0 & QUEUE_THREADS1 can prove that daemon thread "TERMINATES" with main thread.(self.setDaemon(True) && WITHOUT pool.destroy())
        pool.destroy() 
        #1. 只要有pool.detroy()不管是否设置self.setDaemon(True)，都可以保证程序正常退出，因为有destroy()中的dismiss()和join()让程序正常退出 
        #2. 如果没有pool.detroy():
        ##1).不设置self.setDaemon(True)，程序无法退出[Worker.run()里面的while 1会一直执行下去，程序不结束. 即使有exit(0)，程序也不会结束]
        ##2).设置self.setDaemon(True)，程序退出[没有执行完的工作也不继续执行了]
        logging.debug("Main Thread Terminates before exit(0).")
        exit(0)
        logging.debug("Main Thread Terminates after exit(0).")
    except Exception as e:
        logging.error(e)
    else:
        logging.debug("OK")


if __name__ == '__main__':
    main()
else:
    #print("Being imported as a module.")
    print "Being imported as a module."

