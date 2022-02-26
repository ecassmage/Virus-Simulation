import signal
import tkinter as tk
import time

import mainShared

import Classes.GUI as GUI


def switch(switchCode, queue):
    match switchCode.lower():
        case "quit soft":
            queue[0].put("Received")
            print("Window Closing")
            exit()


def deadFunc(queue, sig, frm):
    queue[0].put("QUIT Program")


def update(gui, queue):
    try:
        gui.update()
    except tk.TclError:
        queue[0].put("QUIT Program")
        switch(queue[1].get(), queue)


def flipQueue(queue):
    temp = queue[0]
    queue[0] = queue[1]
    queue[1] = temp


def setupHumansWithID(gui, queue):
    while True:
        obj = queue[1].get()
        if obj == "Complete 01":
            break
        queue[0].put(obj.drawSprite(gui.win))


# queue = [send, receive]
def main(queue):
    flipQueue(queue)
    signal.signal(signal.SIGINT, lambda sig, frm: deadFunc(queue, sig, frm))  # so as to avoid error reports when a crash is expected and wanted. ie signal interrupt

    gui = GUI.GUI()

    setupHumansWithID(gui, queue)
    queue[0].put("Check")
    queue[1].get()

    while True:
        startTimer = time.time()
        if not queue[1].empty():
            switch(queue[1].get(), queue)
        queue[0].put("newSet")
        gui.checkCoordinates(queue[1].get())
        update(gui, queue)
        endTimer = time.time()
        time.sleep(mainShared.collectTime(startTimer, endTimer, gui.stg['window']['hz'], "Window", gui.stg['debug'], queue))
    pass


if __name__ == '__main__':
    pass
