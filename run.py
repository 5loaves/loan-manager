import signal
import os
import time
import urllib

from json import dumps as to_json
from json import loads as from_json

#from web import start_gtk_thread
#from web import launch_browser
#from web import synchronous_gtk_message
#from web import asynchronous_gtk_message
#from web import kill_gtk_thread

import websocket
import app

socket = None
global_msg = None
class Global(object):
    quit = False
    @classmethod
    def set_quit(cls, *args, **kwargs):
        cls.quit = True


def do_message(msg, web_send):
    print msg
    if msg['message'] == 'Add Loan':
        app.add_loan(msg)
        web_send('["populate home table", %s]' % app.get_home_page_table())
    if msg['message'] == 'Get Loan':
        print 'getting loan'
        web_send('["show loan info", %s]' % app.get_loan(msg))
    if msg['message'] == 'Add Payment':
        app.add_payment(msg)
        web_send('["show loan info", %s]' % app.get_loan(msg))
        web_send('["populate home table", %s]' % app.get_home_page_table())
    if msg['message'] == 'Get Report':
        web_send('["show report", %s]' % app.generate_kiva_report())


def web_send(msg):
    global socket
    print 'sending'
    socket.send(msg)

def web_recv(ws, msg):
    print 'got msg', msg
    if 'connected' in msg:
        web_send('["populate home table", %s]' % app.get_home_page_table())
    msg = from_json(msg)
    do_message(msg, web_send)

def main():
#    global httpd
#    start_gtk_thread()
    
    # Create a proper file:// URL pointing to demo.xhtml:
#    file = os.path.abspath('index.html')
#    uri = 'file://' + urllib.pathname2url(file)
#    browser, web_recv, web_send = \
#        synchronous_gtk_message(launch_browser)(uri,
 #                                               quit_function=Global.set_quit)

    global socket
    socket = websocket.WebSocketApp('ws://localhost:5522', on_message=web_recv)
    socket.run_forever()
    # Finally, here is our personalized main loop, 100% friendly
    # with "select" (although I am not using select here)!:
    # last_second = time.time()
    # uptime_seconds = 1
    # clicks = 0
    # time.sleep(1)
    # while not Global.quit:

    #     current_time = time.time()
    #     again = False
    #     msg = web_recv()
    #     if msg:
    #         msg = from_json(msg)
    #         do_message(msg, web_send)
    #         again = True

    #         if again: pass
    #     else:     time.sleep(0.1)


def my_quit_wrapper(fun):
    global httpd
    signal.signal(signal.SIGINT, Global.set_quit)
    def fun2(*args, **kwargs):
        try:
            x = fun(*args, **kwargs) # equivalent to "apply"
        finally:
#            kill_gtk_thread()
            #server.close()
            Global.set_quit()
        return x
    return fun2


if __name__ == '__main__': # <-- this line is optional
    my_quit_wrapper(main)()
