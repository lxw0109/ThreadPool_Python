#coding: utf-8
# ThreadPool is a simple thread pool
#
# Copyright (C) 2012 Yummy Bian <yummy.bian#gmail.com>
#
# under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ThreadPool is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.";
#

import sys
import Queue
#import queue
import threading

"""
The Queue module implements multi-producer, multi-consumer queues. It is especially useful
in threaded programming when information must be exchanged safely between multiple threads.
The Queue class in this module implements all the required locking semantics.
"""

#KEY: Queue.get() and Queue.put() block until resource(an item/a slot) is available.

class Worker(threading.Thread):
    """
    Routines for work thread.
    """
    def __init__(self, in_queue, out_queue, err_queue):
        """
        Initialize and launch a work thread,
        in_queue contains tasks waiting for to be processed,
        out_queue contains the return value of the task in it,
        err_queue stores error info when processing the task.
        """
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.in_queue = in_queue    #4-tuple: (command, callback, args, kwds)
        self.out_queue = out_queue  #2-tuple or 3-tuple, etc. Determined by the type of return value of callback.
        self.err_queue = err_queue  #2-tuple
        #Start the thread once it is created.
        self.start()

    def run(self):
        # NOTE：这里的run()不是直接执行需要完成的工作，而是从in_queue中获取一个task，然后执行这个task
        while 1:
            # Processing tasks in the in_queue until command is "stop".
            # Similar to 360 interview: "args" and "kwds" can be assigned correctly.
            command, callback, args, kwds = self.in_queue.get() #blocked on in_queue.get() if no task in in_queue
            if command == "stop":
                break

            try:
                if command != "process":
                    raise ValueError("Unknown command %r" % command)
            except:
                self.report_error()
            else:
                self.out_queue.put(callback(*args, **kwds)) #blocked on out_queue.put() if no slot in out_queue

    def dismiss(self):
        command = "stop"
        self.in_queue.put((command, None, None, None))

    def report_error(self):
        """'''
        We "report" errors by adding error information to err_queue.
        """
        self.err_queue.put(sys.exc_info()[:2])


class ThreadPool():
    """
    Manage thread pool.
    """
    MAX_THREADS = 32

    def __init__(self, num_threads, buffer_size=0):
        """
        Spawn num_threads threads in the thread pool, and initialize three queues.
        """
        # buffer_size = 0 indicates buffer is unlimited.
        num_threads = ThreadPool.MAX_THREADS \
            if num_threads > ThreadPool.MAX_THREADS \
            else num_threads
        self.in_queue = Queue.Queue(buffer_size)    # Queue.Queue(maxsize=0)  If maxsize is less than or equal to zero, the queue size is infinite.
        self.out_queue = Queue.Queue(buffer_size)
        self.err_queue = Queue.Queue(buffer_size)

        self.workers = {}
        for i in range(num_threads):
            worker = Worker(self.in_queue, self.out_queue, self.err_queue)
            self.workers[i] = worker

    def add_task(self, callback, *args, **kwds):
        command = 'process'
        self.in_queue.put((command, callback, args, kwds))  #NOTE: here not *args, **kwds.  Why?

    def get_task(self):
        return self.out_queue.get()

    def get_in_queue_size(self):
        return self.in_queue.qsize()

    def _get_results(self, queue):
        """
        Generator to yield one after another of all items currently in the queue, without any waiting
        """
        try:
            while 1:
                yield queue.get_nowait()
        except Queue.Empty:
            raise StopIteration

    def show_results(self):
        for result in self._get_results(self.out_queue):
            print("Result: {0}".format(result))

    def show_errors(self):
        for etyp, err in self._get_results(self.err_queue):
            print('Error: {0} {1}'.format(etyp, err))

    def destroy(self):
        #order is important: firstly, request all threads to stop.
        for i in self.workers:
            self.workers[i].dismiss()

        #then, wait for each of them to terminate:
        for i in self.workers:
            self.workers[i].join()
            
        # clean up the workers from now-unused thread objects
        del self.workers
