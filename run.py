import signal
import os
import time
import urllib

from simplejson import dumps as to_json
from simplejson import loads as from_json

from web import start_gtk_thread
from web import launch_browser
from web import synchronous_gtk_message
from web import asynchronous_gtk_message
from web import kill_gtk_thread

import app

class Global(object):
    quit = False
    @classmethod
    def set_quit(cls, *args, **kwargs):
        cls.quit = True

def do_message(msg, web_send):
    if msg['message'] == 'Add Loan':
        app.add_loan(msg)
        web_send("message_recieved('populate home table', '%s')" % app.get_home_page_table())
    if msg['message'] == 'Get Loan':
        web_send("message_recieved('show loan info', '%s')" % app.get_loan(msg))
    if msg['message'] == 'Add Payment':
        app.add_payment(msg)
        web_send("message_recieved('show loan info', '%s')" % app.get_loan(msg))
        web_send("message_recieved('populate home table', '%s')" % app.get_home_page_table())
    if msg['message'] == 'Get Report':
        web_send("message_recieved('show report', '%s')" % app.generate_kiva_report())


def main():
    start_gtk_thread()

    # Create a proper file:// URL pointing to demo.xhtml:
    file = os.path.abspath('index.html')
    uri = 'file://' + urllib.pathname2url(file)
    browser, web_recv, web_send = \
        synchronous_gtk_message(launch_browser)(uri,
                                                quit_function=Global.set_quit)

    # Finally, here is our personalized main loop, 100% friendly
    # with "select" (although I am not using select here)!:
    last_second = time.time()
    uptime_seconds = 1
    clicks = 0
    time.sleep(1)
    web_send("message_recieved('populate home table', '%s')" % app.get_home_page_table())
    while not Global.quit:

        current_time = time.time()
        again = False
        msg = web_recv()
        if msg:
            msg = from_json(msg)
            do_message(msg, web_send)
            again = True

        if again: pass
        else:     time.sleep(0.1)


def my_quit_wrapper(fun):
    signal.signal(signal.SIGINT, Global.set_quit)
    def fun2(*args, **kwargs):
        try:
            x = fun(*args, **kwargs) # equivalent to "apply"
        finally:
            kill_gtk_thread()
            Global.set_quit()
        return x
    return fun2


if __name__ == '__main__': # <-- this line is optional
    my_quit_wrapper(main)()

