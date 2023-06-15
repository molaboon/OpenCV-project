import random

class Obj():
    def __init__(self, pos, eatFolder, nonEatFolder, currentObj, isEatable) :
        self.pos = pos
        self.eat = eatFolder
        self.noneat = nonEatFolder
        self.currentObj = currentObj
        self.speed = 10
        self.isEatable = isEatable

    def fallDown(self, score):
        self.pos[1] += self.speed+((score//10)*5)

        if self.pos[1] > 570:
            self.resetObject()
    
    def resetObject(self):
        self.pos[0] = random.randint(100, 1180)
        self.pos[1] = 0
        randNo = random.randint(0, 2)  # change the ratio of eatables/ non-eatables
        if randNo == 0:
            self.currentObj = self.eat[random.randint(0, len(self.eat)-1)]
            self.isEatable = True
        else:
            self.currentObj = self.noneat[random.randint(0, len(self.noneat)-1)]
            self.isEatable = False



