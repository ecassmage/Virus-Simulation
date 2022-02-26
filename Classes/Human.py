import random
import math

import Files.FileOpener as FileOpener
try:
    import Virus
except ModuleNotFoundError:
    import Classes.Virus as Virus


class Human:
    def __init__(self):
        self.stg = FileOpener.openStg()

        self.infected = False
        self.update = True
        self.immune = False
        self.virus = None
        self.ageOfInfection = 0

        self.size = self.stg['human']['size'] // 2
        self.speed = self.stg['human']['speed']

        self.coord = getStartingPosition([self.stg['window']['width'], self.stg['window']['height']], self.size)
        self.pathing = [0, 0, [0, 0]]  # [Ratio, Current Point in Ratio, [unit vector x, unit vector y]]
        self.path = []  # a two-point x-y indicating the position this human will be traversing for the foreseeable future.

        self.color = self.stg['human']['color']  # red if infected
        self.Name = []  # To know who is dying on a personal level
        self.id = -1  # -1 means not set yet.

    def routine(self, HumanDict: dict, proximity: bool, newDay: bool):
        if newDay:
            self.increaseVirusAge()
        self.unInfectHuman()
        if not self.immune:
            self.choosePath(HumanDict)
            if proximity:
                self.proximity(HumanDict)

    def infect(self, virus=None, guarantee=False):
        if virus is None:
            virus = Virus.Virus()

        if virus.infectHuman() or guarantee:
            self.infected = True
            self.virus = virus
            self.color = self.stg['virus']['color']

    def increaseVirusAge(self):

        if self.infected:
            self.ageOfInfection += 1

    def unInfectHuman(self):
        def unInfect():
            self.infected = False
            self.color = self.stg['virus']['colorRecovered']
            self.ageOfInfection = 0
            self.immune = True
            self.update = False

        if self.ageOfInfection > self.stg['virus']['earliestRecovery']:
            if self.ageOfInfection > self.stg['virus']['latestRecovery']:
                unInfect()
            elif (100 * (1 / (1 + math.exp(-1 * ((self.ageOfInfection - (self.stg['virus']['latestRecovery'] - self.stg['virus']['earliestRecovery'])) / (self.stg['virus']['latestRecovery'] / 5)))))) / self.stg['backEnd']['iterationRate'] >= random.randrange(100):
                unInfect()

    def setID(self, registerID):
        self.id = registerID
        pass

    def setName(self):
        pass

    def drawSprite(self, tkinterWindow):
        return tkinterWindow.create_oval(self.coord[0] - self.size, self.coord[1] - self.size, self.coord[0] + self.size, self.coord[1] + self.size, fill=self.color)

    def checkProximity(self, other, proximityCheck):
        return (other[0] - self.coord[0]) ** 2 + (other[1] - self.coord[1]) ** 2 <= proximityCheck ** 2

    def proximity(self, HumanDictionary):
        if not self.infected:
            return

        for x in range(self.coord[0] - self.size - self.virus.proximity, self.coord[0] + self.size + self.virus.proximity):
            if x in HumanDictionary:
                for human in HumanDictionary[x]:
                    if human.immune or self == human:
                        continue
                    if self.checkProximity(human.coord, self.virus.proximity+self.size):
                        human.infect(self.virus)

    def choosePath(self, dictionary):
        if len(self.path) == 0 or self.checkProximity(self.path, 2 * self.speed):
            x = random.randrange(1 + self.size, self.stg['window']['width'] - self.size - 1)
            y = random.randrange(1 + self.size, self.stg['window']['height'] - self.size - 1)
            self.path = [x, y]
            self.calculatePath()
        self.move(dictionary)

    def calculatePath(self):
        try:
            self.pathing[0] = abs((self.path[1] - self.coord[1]) / (self.path[0] - self.coord[0]))
        except ZeroDivisionError:
            self.pathing[0] = 0

        self.pathing[2][0] = 1 * self.speed if self.path[0] - self.coord[0] > 0 else -1 * self.speed
        self.pathing[2][1] = 1 * self.speed if self.path[1] - self.coord[1] > 0 else -1 * self.speed

    def move(self, dictionary):
        def horizontalMovement():
            self.coord[0] += self.pathing[2][0]

        def verticalMovement():
            self.coord[1] += self.pathing[2][1]

        removeKey(dictionary, self)

        if self.path[0] == self.coord[0]:
            verticalMovement()
        elif self.path[1] == self.coord[1]:
            horizontalMovement()
        else:
            if self.pathing[1] < self.speed:
                self.pathing[1] += self.pathing[0]
                horizontalMovement()
            else:
                self.pathing[1] -= self.speed
                verticalMovement()

        addKey(dictionary, self)


def removeKey(dictionary, removeThis):
    if len(dictionary[removeThis.coord[0]]) == 1:
        del[dictionary[removeThis.coord[0]]]
    else:
        dictionary[removeThis.coord[0]].pop(dictionary[removeThis.coord[0]].index(removeThis))


def addKey(dictionary, addThis):
    if addThis.coord[0] in dictionary:
        dictionary[addThis.coord[0]].append(addThis)
    else:
        dictionary.update({addThis.coord[0]: [addThis]})


def getStartingPosition(Boundary, size):
    return [random.randrange(1 + size, Boundary[0] - size - 1), random.randrange(1 + size, Boundary[1] - size - 1)]


if __name__ == '__main__':
    human1 = Human()
    human2 = Human()
    human3 = Human()

    human1.virus = Virus.Virus()

    human1.coord = [100, 78]
    human2.coord = [93, 76]
    human3.coord = [98, 77]
    dic = {human1.coord[0]: [human1], human2.coord[0]: [human2], human3.coord[0]: [human3]}
    print(human1.proximity(dic))  # should return False if proximity is 10 and True if proximity is 100
    print(human1.proximity(dic))  # should return True if proximity is 10 and True if proximity is 100

    human1.choosePath(dic)
    print(f"{human1.coord} {human1.path} {human1.pathing}")
    for i in range(10000):
        human1.choosePath(dic)
        if human1.checkProximity(human1.path, 5):
            print(f"{human1.coord} {human1.path} {human1.pathing}")

    print("HumanCls.py Test Run")
    pass
