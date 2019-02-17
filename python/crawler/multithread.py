# -*- coding: utf-8 -*-

"""
Multi-threaded crawler
"""

import queue
import time
import threading


class MultiThreadingCrawler(object):
    def __init__(self):
        self.queue = queue.Queue()
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

    def run(self, max_threads):
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
