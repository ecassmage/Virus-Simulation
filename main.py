from multiprocessing import Process, Queue
import time
import signal

import Files.FileOpener
import Classes.Human
import Logic
import Window
import InformationManager
import mainShared


class Container:
    def __init__(self):
        self.stg = Files.FileOpener.openStg()
        self.main_Window = [Queue(), Queue()]
        self.main_Logic = [Queue(), Queue()]

        self.Info = InformationManager.InfoMgr()

        self.masterHumanList = []
        self.masterHumanDictionary = {}

        self.BackUp = []

    def WriteHumans(self):
        for _ in range(self.stg['human']['population']):
            newHuman = Classes.Human.Human()
            Classes.Human.addKey(self.masterHumanDictionary, newHuman)
            self.masterHumanList.append(newHuman)
        pass


def switchWindow(switch, extraInfo=None):
    match switch.lower():
        case "quit program":
            sigint(0, 0, extraInfo)

        case "quit soft":
            extraInfo.main_Window[0].put(switch)

        case "newset":
            if len(extraInfo.BackUp) != 0:
                extraInfo.main_Window[0].put(extraInfo.BackUp)
                extraInfo.BackUp = []
            else:
                extraInfo.main_Window[0].put("N/A")

        case "print":
            print(extraInfo.main_Window[1].get())


def switchLogic(switch, extraInfo=None):
    match switch.lower():
        case "quit program":
            sigint(0, 0, extraInfo)

        case "quit soft":
            extraInfo.main_Logic[0].put(switch)

        case "newset":
            extraInfo.BackUp = extraInfo.main_Logic[1].get()
            timeStart = time.time()
            if not extraInfo.Info.countUpHumans(extraInfo.BackUp, extraInfo.stg['window']['stipple']):
                sigint(0, 0, extraInfo)
            timeEnd = time.time()
            mainShared.collectTime(timeStart, timeEnd, 120, "Main")

        case "print":
            print(extraInfo.main_Logic[1].get())

    pass


def startWindowRoutine(container):
    for Human in container.masterHumanList:
        container.main_Window[0].put(Human)
        Human.setID(container.main_Window[1].get())
    container.main_Window[0].put("Complete 01")


def startLogicRoutine(container):
    while True:
        obj = container.main_Logic[1].get()
        if obj == "Complete 01":
            container.main_Window[0].put(obj)
            break
        container.main_Window[0].put(obj)
        container.main_Logic[0].put(container.main_Window[1].get())


def sigint(sig, frm, container):
    switchLogic("QUIT SOFT", container)
    switchWindow("QUIT SOFT", container)

    container.main_Window[1].get()
    container.main_Logic[1].get()

    time.sleep(0.1)

    container.main_Window[0].close()
    container.main_Window[1].close()
    container.main_Logic[0].close()
    container.main_Logic[1].close()
    print("Main Closing")
    container.Info.Graph.tk.mainloop()
    exit()


def test(TK):
    pass


# queue = [send, receive]
def main():
    container = Container()

    LogicProcess = Process(target=Logic.main, args=(container.main_Logic,))
    WindowProcess = Process(target=Window.main, args=(container.main_Window,))

    # container.WriteHumans()
    # print(container.masterHumanDictionary)
    # print(container.masterHumanList)
    WindowProcess.start()
    LogicProcess.start()

    signal.signal(signal.SIGINT, lambda sig, frm: sigint(sig, frm, container))  # so as to avoid error reports when a crash is expected and wanted. ie signal interrupt

    # startWindowRoutine(container)
    startLogicRoutine(container)

    container.main_Window[1].get()         # These Checks are just to align the 3 processes together
    container.main_Logic[1] .get()         # These Checks are just to align the 3 processes together
    container.main_Window[0].put("Check")  # These Checks are just to align the 3 processes together
    container.main_Logic[0] .put("Check")  # These Checks are just to align the 3 processes together
    print("Done")
    # container.Info.Graph.tk.mainloop()
    while True:
        if not container.main_Window[1].empty():
            switchWindow(container.main_Window[1].get(), container)
            # Do this if window sent something over.
            pass

        if not container.main_Logic[1].empty():
            switchLogic(container.main_Logic[1].get(), container)
            # Do this if logic sent something over.
            pass


if __name__ == '__main__':
    main()
    pass
