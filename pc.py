import logging
import threading
import random
import concurrent.futures
import time

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-9s) %(message)s', )

if __name__ == '__main__':

    cv = threading.Condition()
    max = 10
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=max)

    finished = []


    def handler(ctr):
        logging.debug('entering %s' % ctr)
        seconds = random.randint(1, 10)
        time.sleep(seconds)
        logging.debug('slept %s!' % seconds)
        with cv:
            finished.append(ctr)
            if len(finished) == max:
                logging.debug('finished length=%s - notifying all' % len(finished))
                cv.notify_all()


    for i in range(0, max):
        executor.submit(lambda *args: handler(i))

    with cv:
        cv.wait()

    logging.debug('finished all threads!')
