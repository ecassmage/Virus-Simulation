import time
import random
import copy


class Coord:
    def __init__(self, c):
        self.coord = c


def proximityCheck(selfCmp, coordCmp, proximityVar=10):
    return (coordCmp[0] - selfCmp[0]) ** 2 + (coordCmp[1] - selfCmp[1]) ** 2 < proximityVar**2


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


def getCoord():
    return [random.randrange(1000), random.randrange(1000)]
    pass


if __name__ == "__main__":
    D = {}
    L = []
    CoordList = []
    CoordList2 = copy.copy(CoordList)

    for i in range(1000):
        C = Coord(getCoord())
        C2 = Coord(getCoord())
        CoordList.append(C)
        CoordList2.append(C2)
        addKey(D, C2)

    StartOverAll = time.time()
    for _ in range(10):
        Start = time.time()
        for _ in range(60):
            for coord in CoordList:
                if random.randrange(100) > 0:
                    continue

                coord.coord = [coord.coord[0] + 1, coord.coord[1] + 1]

                for otherCoord in CoordList:
                    proximityCheck(coord.coord, otherCoord.coord)
        End = time.time()
        print(f"List Only Time = {End - Start}")
    EndOverAll = time.time()
    print(f"List Only TimeOverAll = {EndOverAll - StartOverAll}\n")

    time.sleep(0.5)
    StartOverAll = time.time()
    for _ in range(10):
        Start = time.time()
        for __ in range(60):
            for coord in CoordList2:
                if random.randrange(100) > 5:
                    continue
                removeKey(D, coord)
                coord.coord = [coord.coord[0]+1, coord.coord[1]+1]
                for x in range(coord.coord[0]-10, coord.coord[1]+10):
                    if x in D:
                        for coordinate in D[x]:
                            proximityCheck(coord.coord, coordinate.coord)
                addKey(D, coord)
        End = time.time()
        print(f"List To Dictionary Time = {End - Start}")
    EndOverAll = time.time()
    print(f"List To Dictionary Time Over All = {EndOverAll - StartOverAll}\n")

