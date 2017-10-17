#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Assignment 7. Pig Game"""

import random
import sys
import time
import argparse


class Player:
    def __init__(self, name, total=0):
        self.name = name
        self.total = total

    def newTotal(self, newPoint):
        self.total = self.total + newPoint

    def decision(self):
        roll = raw_input("Ready to roll? Enter 'r' to roll, 'h' to hold: ")
        return roll

class Dice:
    def __init__(self, roll=0, seed=0):
        self.roll =  roll
        self.seed = seed

    def newRoll(self, seed): 
        random.seed(seed)
        self.roll = random.randrange(1, 7)
        return self.roll

class GameCenter:
    def __init__(self, total=0):
        self.total = total

    def turnScore(self, newPoint):
        self.total = self.total + newPoint
        return self.total

    def totalScoreCheck(self, player, win_ponts):
        score = player.total + self.total
        if score >=  win_ponts:
            player.total = score
            print "%s congratulations! You win!!" % (player.name)
            print 'Your final score is ', player.total

    def turnSwitch(self, current_player,players):
        self.total = 0
        current_player = int(current_player)
        print 'Switching turns.'
        if current_player < len(players) :
            current_player +=1
        else:
            current_player = 1
        return current_player

    def statusMessage(self, player, new_roll):
        print "%s rolled %s. Score for this turn is %s and player's total score is %s" % \
        (player.name, new_roll, self.total, player.total )

    def welcomeMessage(self, player):
        print "Howdy %s, your current score is %s. Good luck!" % \
        (player.name,player.total)

    def gameStartOver(self):  
        num = raw_input("Enter number of players if would like to play again or any other key to exit. " )
        if num.isdigit() :
            return num
        else:
            self.gameOver()

    def gameOver(self):
        print "Game is over."    
        sys.exit()


def createPlayersDict(numPlayers):
    players = {}
    counter = 1

    while counter <= int(numPlayers) :
        player_name = 'player' + str(counter)
        players[counter] = Player(player_name)
        counter += 1

    return players


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--numPlayers", help='enter number players', type=str)
    args = parser.parse_args()

    if args.numPlayers:
        numPlayers = int(args.numPlayers)
        players = {}
        win_point = 100
        
        game_is_true = True 

        while game_is_true:
            seed = 0
            players.clear()
            players = createPlayersDict(numPlayers)
            dice = Dice(seed)
            game = GameCenter()
            current_player = 1
            game.total = 0
            game.welcomeMessage(players[current_player])

            while players[current_player].total < win_point :
                roll = players[current_player].decision()

                if roll == 'r':
                    new_roll = dice.newRoll(seed)

                    if new_roll == 1:
                        game.total = 0
                        print "Oh no! "
                        game.statusMessage(players[current_player],new_roll)
                        current_player = game.turnSwitch(current_player, players)
                        game.welcomeMessage(players[current_player])
                    else:
                        game.total = game.turnScore(new_roll)
                        game.statusMessage(players[current_player],new_roll)
                        game.totalScoreCheck(players[current_player], win_point)

                elif roll == 'h':
                    print players[current_player].name, " adds ", game.total, " points to his total of ", players[current_player].total
                    players[current_player].newTotal(game.total)
                    current_player = game.turnSwitch(current_player, players)
                    game.welcomeMessage(players[current_player])


                else:
                    print "enter r - to roll or h - to pass"

                seed = time.time()

        
            numPlayers = game.gameStartOver()



if __name__ == '__main__':
    main()
