from multiprocessing import Process
import time

def sleep(duration):
    time.sleep(duration)

    print('a')

def test():
    print(__name__)

def wait_for_process():
    if not __name__ in ('test'):
        return
    proc = Process(target = sleep, args = (10,))
    proc.start()
    proc.join(timeout=0)
    while proc.is_alive():
        print('running')
        time.sleep(1.0)