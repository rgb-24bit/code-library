# -*- coding: utf-8 -*-

"""
Multi-process crawler
"""


import multiprocessing
import time
import threading

from mongoqueue import MongoQueue



class MultiThreadingCrawler(object):
    def __init__(self):
        self.queue = MongoQueue()
        self.gap = 1

    def producer(self):
        for i in range(100):
            self.queue.put(i)

    def consumer(self):
        while True:
            if not self.queue.empty():
                item = self.queue.get()
                print(item)
                self.queue.task_done()
            else:
                break

    def run(self, max_threads, *args, **kwargs):
        producer = threading.Thread(target=self.producer)
        producer.start()

        # Let the producer run for a while
        time.sleep(self.gap)

        threads = []
        while not self.queue.empty():
            for thread in threads:
                if not thread.is_alive():
                    threads.remove(thread)
            while len(threads) < max_threads and not self.queue.empty():
                thread = threading.Thread(target=self.consumer)
                thread.setDaemon(True)
                thread.start()
                threads.append(thread)
            # all threads have been processed
            # sleep temporarily so CPU can focus execution on other threads
            time.sleep(self.gap)
        # Waiting for all elements to be processed
        self.queue.join()

    def __call__(self, *args, **kwargs):
        self.run(*args, **kwargs)


def multiProcess(max_threads, **kwargs):
    num_cpus = multiprocessing.cpu_count()
    # pool = multiprocessing.Pool(processes=num_cpus)
    print('Starting {} processes'.format(num_cpus))
    processes = []
    for i in range(num_cpus):
        p = multiprocessing.Process(target=MultiThreadingCrawler(), args=[max_threads], kwargs=kwargs)
        # parsed = pool.apply_async(threaded_link_crawler, args, kwargs)
        p.start()
        processes.append(p)
    # wait for processes to complete
    for p in processes:
        p.join()
