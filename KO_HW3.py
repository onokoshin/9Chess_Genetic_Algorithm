"""
KOSHIN ONO

NxN Queen Problem
This program contains genetic algorithm to solve NxN Queen problem.
For genetic algorithm, this program includes
    - Chromesome - represented by boards filled with queens on each column and row
    - Crossover function
    - Mutation function
    - Fitness function

"""


import random

"""
INSTRUCTION

    The board is set to 4 x 4 as default. If you want to try 8x8 or 16x16, simply change the
    size of the board by modifying the board size below.

"""
SIZE = 4
POPULATION = 50
MAXFIT = SIZE*(SIZE-1)/2
MAXIETERATION = 100000
FIND = False
MUTPROB = 50

class nxnQueens:
    def __init__(self):

        self.totalAverageFitScore = 0 #To store total avg fitness score here
        self.avgFitScore = []   #calculate average fit score
        self.isMaxFit = False   #to indicate whether it's the max fit or not
        self.goal = 0
        self.iterationNum = 0       #to indicate which iteration/generation we are in
        self.currBoards = []

        #populate initial 50 sets of populations by using startPopulation function
        self.startPopulate()

    def startPopulate(self):

        for i in range(POPULATION):
            b = Board(MAXFIT, SIZE)
            self.currBoards.append(b)

    def getAvg(self):
        numTotal = 0

        for i in range(len(self.currBoards)):
            numTotal += self.currBoards[i].fitScore

        self.avgFitScore.append(numTotal/len(self.currBoards))


    def checkFind(self):
        global FIND
        for i in range(len(self.currBoards)):
            if self.currBoards[i].fitScore == MAXFIT:
                FIND = True
                self.goal = self.currBoards[i].new

    def loop_func(self):
        while FIND is False:
            self.getAvg()  # to get average fitness score of 1 generation
            self.checkFind()  # to check whether we have discovered the goal state or not


            if FIND is True:
                print(self.iterationNum, MAXIETERATION)
                print("Goal state has been found")
                print(self.goal)
                break
            elif self.iterationNum == MAXIETERATION:
                print("maximum point reached", MAXIETERATION)
                break
            else:

                #Chromesome are now sorted based on fitscore in desc order
                sortedList = selectionSort(self.currBoards)

                #first parent is the fittest and second parent is random to avoid local maxima
                oneParent = sortedList[0]
                rand = random.randint(0, POPULATION-1)
                twoParent = sortedList[rand]

                #reproduce function
                child1, child2 = reproduce(oneParent, twoParent)

                #if the probability random num is less than or equal to 1, mutation occur
                mutationProb = random.randint(0, 100)

                if(mutationProb) <= MUTPROB:
                    child1 = mutation(child1)
                    child2 = mutation(child2)

                del sortedList[POPULATION - 1]
                sortedList.append(child1)
                del sortedList[POPULATION - 2]
                sortedList.append(child2)

                self.currBoards = sortedList
                print(self.avgFitScore[self.iterationNum])
                self.iterationNum += 1

def selectionSort(alist):
   for fillslot in range(len(alist)-1,0,-1):
       positionOfMax=0
       for location in range(1,fillslot+1):
           if alist[location].fitScore < alist[positionOfMax].fitScore:
               positionOfMax = location

       temp = alist[fillslot]
       alist[fillslot] = alist[positionOfMax]
       alist[positionOfMax] = temp

   return alist

def reproduce(popOne, popTwo):
    global SIZE
    child1 = Board(MAXFIT, SIZE)
    child2 = Board(MAXFIT, SIZE)


    rand = random.randint(0, SIZE - 1)
    left = SIZE - rand


    set1 = []
    set2 = []

    for i in range(0, left):
        set1.append(popOne.new[i])
        set2.append(popTwo.new[i])

    for i in range(left, SIZE):
        set2.append(popOne.new[i])
        set1.append(popTwo.new[i])

    child1.new = set1
    child1.fitScore = child1.getFitnessScore()

    child2.new = set2
    child2.fitScore = child2.getFitnessScore()

    return child1, child2

def mutation(child):

    randIndex = random.randint(0, SIZE-1)
    randNum = random.randint(0, SIZE-1)

    child.new[randIndex] = randNum
    child.fitScore = child.getFitnessScore()

    return child


class Board:
    def __init__(self, maxFitness, boardSize, new=None):
        self.maxFit = maxFitness
        self.bdSize = boardSize;
        self.fitScore = 0
        self.new = list(range(self.bdSize))

        if new==None:
            self.initBoard()
        else:
            self.new = new
        self.getFitness()


    def initBoard(self):
        for i in range(self.bdSize):
            self.new[i] = random.randint(0, self.bdSize-1)



    def getFitness(self):
        self.fitScore = self.maxFit
        for i in range(0, self.bdSize):
            for j in range(0, self.bdSize):
                if (i != j):
                    if (self.new[i] == self.new[j]):
                        self.fitScore -= 1
                    if (abs(self.new[i] - self.new[j]) == abs(i-j)):
                        self.fitScore -= 1


    def getFitnessScore(self):
        self.getFitness()
        return self.fitScore

def main():
    #calls the nxnQUeens object
    obj = nxnQueens()

    # the loop function runs until either find the fitness goal or max iteration
    obj.loop_func()

if __name__ == '__main__':

    #run the program by calling nxnQueens class
    main()
