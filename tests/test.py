import threading

def b(num=None, dispatch=None):
    print('num', num)
    print('kwargs', dispatch)

threading.Thread(target=b, kwargs={'dispatch': 123}).start()