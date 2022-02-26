import signal
import time

import mainShared
import Files.FileOpener
import Classes.Human


class LogicClass:
    def __init__(self):
        self.stg = Files.FileOpener.openStg()
        self.proximityLag = [0, self.stg['backEnd']['proximityLag']]
        pass


def switch(switchCode, queue):
    match switchCode.lower():
        case "quit soft":
            queue[0].put("Received")
            print("Logic Closing")
            exit()


def deadFunc(queue, sig, frm):
    queue[0].put("QUIT Program")


def flipQueue(queue):
    temp = queue[0]
    queue[0] = queue[1]
    queue[1] = temp


def startWindowRoutine(stg, queue):
    def WriteHumans():
        for _ in range(stg['human']['population']):
            newHuman = Classes.Human.Human()
            Classes.Human.addKey(masterHumanDictionary, newHuman)
            masterHumanList.append(newHuman)

    masterHumanDictionary = {}
    masterHumanList = []
    WriteHumans()
    for Human in masterHumanList:
        queue[0].put(Human)
        Human.setID(queue[1].get())
    queue[0].put("Complete 01")
    return masterHumanDictionary, masterHumanList


def routine(HumanList: list, HumanDict: dict, container: LogicClass, newDay: bool):
    for human in HumanList:
        human.routine(HumanDict, True if container.proximityLag[0] == container.proximityLag[1] else False, newDay)
    container.proximityLag[0] = container.proximityLag[0] + 1 if container.proximityLag[0] < container.proximityLag[1] else 0

    pass


# queue = [send, receive]
def main(queue):
    container = LogicClass()

    flipQueue(queue)
    signal.signal(signal.SIGINT, lambda sig, frm: deadFunc(queue, sig, frm))  # so as to avoid error reports when a crash is expected and wanted. ie signal interrupt
    HumanDict, HumanList = startWindowRoutine(container.stg, queue)

    queue[0].put("Check")
    queue[1].get()

    for number, human in enumerate(HumanList):
        if number == container.stg['human']['startingPopulationInfected']:
            break
        human.infect(guarantee=True)
    num = 0
    while True:

        if num >= container.stg['backEnd']['iterationRate']:
            num = 0
            newDay = True
        else:
            num += 1
            newDay = False

        startTimer = time.time()

        if not queue[1].empty():
            switch(queue[1].get(), queue)
        routine(HumanList, HumanDict, container, newDay)
        queue[0].put("newSet")
        queue[0].put(HumanList)

        endTimer = time.time()

        time.sleep(mainShared.collectTime(startTimer, endTimer, container.stg['backEnd']['iterationRate'], "Logic", container.stg['debug'], queue))


if __name__ == '__main__':
    pass
