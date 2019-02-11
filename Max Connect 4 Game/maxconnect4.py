#!/usr/bin/env python

# Written by Chris Conly based on C++
# code provided by Vassilis Athitsos
# Written to be Python 2.4 compatible for omega

import sys
import time
import MaxConnect4Game as maxconnect



class MinmaxDecision:

    def __init__(self):
        initialGameboard = maxconnect.MaxConnect4Game()
        depth_limit=0

    def setInitState(self,inFile,gameMode,nextPlayer):
        self.initialGameboard = maxconnect.MaxConnect4Game()
        self.initialGameboard.setBoardFromFile(inFile,gameMode,nextPlayer)
        self.initialGameboard.printGameBoard()
        return self.initialGameboard

    def minimaxDecision(self, initialGameboard):
        score = 0
        move = -1
        start = time.time()
        matrix = self.candidate(initialGameboard)
        v = float('-inf')
        for k in matrix.iterkeys():
            temp = self.minVal(matrix[k], alpha=-100000, beta=100000, depth=1)
            if temp >= v:
                v = temp
                move = k
        end = time.time()
        time_for_decision= end-start
        #time_taken=  time.strftime("%M:%S:%m:%ms'", time.gmtime(time_for_decision))
        print 'Time for decision :', time_for_decision
        isvalid, demo = initialGameboard.playPiece(move)
        return demo, move, v



    def maxVal(self,currentGameboard, alpha, beta, depth):
        v = float('-inf')
        cnt = currentGameboard.checkPieceCount()
        if cnt == 42:
            util = currentGameboard.utility()
            return util
        elif depth == self.depth_limit:
            score = currentGameboard.evaluation()
            return score
        else:
            depth = depth + 1
            matrix = self.candidate(currentGameboard)
            for k in matrix.iterkeys():
                board = matrix[k]
                temp = self.minVal(board, alpha, beta, depth)
                if temp >= v:
                    v = temp
                    move = k
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v

    def minVal(self, currentGameboard, alpha, beta, depth):
        v = float('inf')
        cnt = currentGameboard.checkPieceCount()
        if cnt == 42:
            util = currentGameboard.utility()
            return util
        if depth == self.depth_limit:
            score = currentGameboard.evaluation()
            return score
        else:
            depth = depth + 1
            matrix = self.candidate(currentGameboard)
            for k in matrix.iterkeys():
                board = matrix[k]
                temp = self.maxVal(board, alpha, beta, depth)
                if temp <= v:
                    v = temp
                    move = k
                if v <= alpha:
                    return  v
                beta = min(beta, v)
            return v


    def candidate(self, gameboard):
        matrix = {}
        columns_available = gameboard.numberofpossibleColumns()
        for i in range(len(columns_available)):
            move = columns_available.pop()
            isValid, newGameboard = gameboard.playPiece(move)
            matrix[move] = newGameboard
        return matrix



def finalverdict(score1, score2, nextPlayer):
    if score1>score2:
        #if nextPlayer=='computer-next':
        #    print('Human wins')
        #elif nextPlayer=='human-next':
        #    print('Computer wins')
        print('Player1 wins')
        print'WINNING SCORE',score1
    elif score1<score2:

        #if nextPlayer=='computer-next':
        #    print('Computer wins')
        #elif nextPlayer=='human-next':
        #    print('Human wins')
        print('Player2 wins')
        print 'WINNING SCORE:',score2
    elif score1==score2:
        print('It is a tie')

def main(argv):
    #v = float('-inf')
    mm = MinmaxDecision()
    nextPlayer = ''
    #inFile = ''
    #outFile = ''
    gameMode = argv[1]

    if gameMode == 'interactive':
        inFile = argv[2]
        nextPlayer = argv[3]
        #initnextplayer=nextPlayer
        #player = p.Player()
        mm.depth_limit = int(argv[4])
        initstate = mm.setInitState(inFile,gameMode,nextPlayer)
        while True:
            count = initstate.checkPieceCount()
            if count == 42 and nextPlayer=='computer-next':
                initstate.countScore()
                print 'Computer Score: ', initstate.player1score
                print 'Player Score:', initstate.player2score
                initstate.printGameBoard()
                print('Board is full')
                break
            elif count==42 and nextPlayer=='human-next':
                initstate.countScore()
                #print 'Computers Score: ', initstate.player1score
                #print 'Player score:', initstate.player2score
                initstate.printGameBoard()
                print('Board is full')
                break

            if nextPlayer == 'computer-next':
                initstate, move, score = mm.minimaxDecision(initstate)
                initstate.countScore()
                print 'Computer Score: ', initstate.player2score
                print 'Player Score:', initstate.player1score
                initstate.printBoardToFile('computer.txt')
                nextPlayer = 'human-next'

            elif nextPlayer == 'human-next':
                initstate.countScore()
                initstate.printGameBoard()
                print 'Computer Score:', initstate.player2score
                print 'Player Score: ', initstate.player1score
                print "Enter column between 1-7:"
                human_move = int(raw_input())
                while human_move<1 or human_move>7:
                    print "Enter column between 1-7:"
                    human_move = int(raw_input())
                isValid, initstate = initstate.playPiece(human_move-1)
                while not isValid:
                    print "Enter column between 1-7:"
                    human_move = int(raw_input())
                    isValid, initstate = initstate.playPiece(human_move-1)
                initstate.printBoardToFile('human.txt')
                nextPlayer = 'computer-next'




    elif gameMode == 'one-move':
        inFile = argv[2]
        outFile = argv[3]
        #player = p.Player()
        mm.depth_limit = int(argv[4])
        initstate = mm.setInitState(inFile,gameMode,nextPlayer)
        temp, move, score = mm.minimaxDecision(initstate)
        print 'Move : Column', move+1
        print 'Score:', score
        print 'GameBoard after column',move+1,'move:'
        temp.printGameBoard()
        temp.printBoardToFile(outFile)

    if gameMode=='interactive':
        score1 = initstate.player1score
        print('Final Verdict:')
        print(score1)
        score2 = initstate.player2score
        print(score2)
        finalverdict(score1, score2, nextPlayer)

    elif gameMode=='one-move':
        print('computer move recorded!')






if __name__ == '__main__':
    print('MAXCONNECT 4 GAME')
    main(sys.argv)
