import random

import Files.FileOpener


class Virus:
    def __init__(self):
        # Mutations Will go here...
        temp = Files.FileOpener.openStg()['virus']
        self.proximity = temp['proximity']
        self.infectivity = temp['infectivity']

        self.randomUpperBound = None

        self.getRandomUpperBound()
        pass

    def getRandomUpperBound(self):
        temp = str(self.infectivity).split(".")
        while int(temp[0]) < 100:
            temp[0] = str(int(temp[0]) * 10)  # why the warning python, why.
        total = 0
        for num in temp:
            total += len(num)
        self.randomUpperBound = [10 ** (total-1), 0]
        if len(temp) == 2:
            self.randomUpperBound[1] = len(temp[1])

    def infectHuman(self):
        return self.infectivity >= random.randrange(self.randomUpperBound[0]) / (10 ** self.randomUpperBound[1])

    # Maybe the virus will begin to mutate. OOOH spooky.


if __name__ == '__main__':
    v = Virus()
    pass
