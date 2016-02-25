Software Demands:
============
Python 2.7 +

Thread pool
============
This is a simple thread pool for python(using queue module).

Install:
============
```Shell
python setup.py install
```

Usage:
============

- Firstly, you should define a callback to deal with your task.

```Python
def do_work(*args, **kwds):
    # do something
```       
- Then, you can create a thread pool to schedule your tasks.
    
```Python
    from threadpool import ThreadPool
    # Create thread pool with nums threads
    pool = ThreadPool(nums)
    # Add a task into pool
    pool.add_task(do_work, args, kwds)
    # Join and destroy all threads
    pool.destroy()
```

Demo:
============
```Shell
./runDemo.py
```


[Overview on Wikipedia](https://en.wikipedia.org/wiki/Thread_pool):
============

Reasons for using a thread pool, rather than the obvious alternative of spawning one thread per task, are to prevent the time and memory overhead inherent in thread creation, and to avoid running out of resources such as open files or network connections (of which operating systems allocate a limited number to running programs).</br>
A sample thread pool (green boxes) with waiting tasks (blue) and completed tasks (yellow) is shown in the following picture.</br>
![Thread Pool](http://7xr6bp.com1.z0.glb.clouddn.com/Thread_pool.png)

线程池的引用范围：
============

1. 需要大量的线程来完成任务，且完成任务的时间比较短。</br>
WEB服务器完成网页请求这样的任务，使用线程池技术是非常合适的。因为单个任务小，而任务数量巨大，你可以想象一个热门网站的点击次数。</br>
但对于长时间的任务，比如一个Telnet连接请求，线程池的优点就不明显了。因为Telnet会话时间比线程的创建时间大多了。</br>
2. 对性能要求苛刻的应用，比如要求服务器迅速响应客户请求。</br>
3. 接受突发性的大量请求，但不至于使服务器因此产生大量线程的应用。突发性大量客户请求，在没有线程池情况下，将产生大量线程，虽然理论上大部分操作系统线程数目最大值不是问题，短时间内产生大量线程可能使内存到达极限，并出现"OutOfMemory"的错误。</br>
4. 可以明确的限定“允许同时运行的线程的最大数目”。</br>

NOTE:
============
Forked from [yummybian/ThreadPool](https://github.com/yummybian/ThreadPool.git).</br>
