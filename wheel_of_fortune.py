from config import dictionaryloc
from config import turntextloc
from config import wheeltextloc
from config import maxrounds
from config import vowelcost
from config import roundstatusloc
from config import finalprize
from config import finalRoundTextLoc

import random
import time

players={0:{"roundtotal":0,"gametotal":0,"name":""},
         1:{"roundtotal":0,"gametotal":0,"name":""},
         2:{"roundtotal":0,"gametotal":0,"name":""},
        }

roundNum = 0
dictionary = []
turntext = ""
wheellist = []
roundWord = ""
blankWord = []
vowels = {"a", "e", "i", "o", "u"}
roundstatus = ""
finalroundtext = ""

def readDictionaryFile():
    global dictionary
    dictionaryfile = open(dictionaryloc,'r')
    dictionarystring = dictionaryfile.read()
    dictionaryfile.close()
    dictionary = dictionarystring.split('\n')

def readTurnTxtFile():
    global turntext   
    turntextfile = open(turntextloc,'r')
    turntext = turntextfile.read()
    turntextfile.close()

def readFinalRoundTxtFile():
    global finalroundtext   
    finalroundtextfile = open(finalRoundTextLoc)
    finalroundtext = finalroundtextfile.read()
    finalroundtextfile.close()

def readRoundStatusTxtFile():
    global roundstatus
    roundstatusfile = open(roundstatusloc)
    roundstatus = roundstatusfile.read()
    roundstatusfile.close()

def readWheelTxtFile():
    global wheellist
    wheellistfile = open(wheeltextloc)
    wheellist = wheellistfile.read()
    wheellistfile.close()
    
    wheellist = wheellist.split('\n')
    wheellist = list(wheellist)

def getPlayerInfo():
    global players
    player1 = players[0]
    player1['name'] = input('Player 1 name: ')
    players[0] = player1

    player2 = players[1]
    player2['name'] = input('Player 2 name: ')
    players[1] = player2

    player3 = players[2]
    player3['name'] = input('Player 3 name: ')
    players[2] = player3

def gameSetup():
    global turntext
    global dictionary

    readDictionaryFile()
    readTurnTxtFile()
    readWheelTxtFile()
    getPlayerInfo()
    readRoundStatusTxtFile()
    readFinalRoundTxtFile()

def getWord():
    global dictionary
    global roundWord
    global roundUnderscoreWord
    global blankWord

    roundWord = random.choice(dictionary)
    roundUnderscoreWord = []

    for a in roundWord:
        roundUnderscoreWord.append('_')

    blankWord = ''.join(roundUnderscoreWord)

    return roundWord, roundUnderscoreWord

def wofRoundSetup():
    global players
    global roundWord
    global blankWord

    player1 = players[0]
    player1['roundtotal'] = 0
    players[0] = player1

    player2 = players[1]
    player2['roundtotal'] = 0
    players[1] = player2

    player3 = players[2]
    player3['roundtotal'] = 0
    players[2] = player3

    playernums = [0,1,2]
    initPlayer = random.choice(playernums)

    getWord()

    return initPlayer

def spinWheel(playerNum):
    global wheellist
    global players
    global vowels
    global playerinfo
    global stillinTurn
    global wordcomplete

    print('\nThe wheel spins...')
    time.sleep(0.75)

    slot = random.choice(wheellist)

    if slot == 'BANKRUPT' or slot == 'Lose a Turn':
        print('\n' + slot)
    else:
        print('\n$' + slot)
    
    time.sleep(0.75)

    if slot == 'BANKRUPT':
        stillinTurn = False
        playerinfo['roundtotal'] = 0
        print('Sorry, your bank drops to 0 #Broke. NEXT!')
    elif slot == 'Lose a Turn':
        stillinTurn = False
        print('Sorry, you lose your turn. NEXT!')
    else:
        print('\nWord: ' + blankWord)
        letter = str(input('Guess a consonant: '))

        while len(letter) != 1:
            print('Guess ONE letter')
            letter = str(input('Guess a consonant: '))

        letter = letter.strip().lower()
        v_check = letter in vowels
        
        check = [a for a in range(len(blankWord)) if blankWord.startswith(letter, a)]

        while v_check == True or check != []:
            if v_check == True:
                print('Not a consonant, try again')
                letter = str(input('Guess a consonant: '))
                letter = letter.strip().lower()
                v_check = letter in vowels
                check = [a for a in range(len(blankWord)) if blankWord.startswith(letter, a)]
            elif check != []:
                print('Letter already guessed, try again')
                letter = str(input('Guess a consonant: '))
                letter = letter.strip().lower()
                v_check = letter in vowels
                check = [a for a in range(len(blankWord)) if blankWord.startswith(letter, a)]
        else:
            guessletter(letter, playerNum)

            if goodGuess == True:
                print('\nCorrect!')
                print('Word: ' + blankWord)
                time.sleep(0.5)
                playerinfo['roundtotal'] += int(slot) 
                stillinTurn = True
                print('\n$' + str(slot) + ' added to your bank')
                print('Total: $' + str(playerinfo['roundtotal']))
                time.sleep(0.5)

                if roundWord == blankWord:
                    wordcomplete = True
                else:
                    print('\n(S)pin the wheel, (b)uy a vowel, or (g)uess the word')
            else:
                print('\nIncorrect. NEXT!')
                time.sleep(0.5)
                stillinTurn = False
  
    return stillinTurn

def guessletter(letter, playerNum): 
    global players
    global blankWord
    global roundUnderscoreWord
    global goodGuess
    global playerinfo

    check = [a for a in range(len(roundWord)) if roundWord.startswith(letter, a)]

    for a in check:
        roundUnderscoreWord[a] = letter

    if check == []:
        goodGuess = False
    else:
        goodGuess = True
        blankWord = ''.join(roundUnderscoreWord)

    return goodGuess

def buyVowel(playerNum):
    global players
    global vowels
    global playerinfo
    global stillinTurn
    global wordcomplete

    print('\nWord: ' + blankWord)
    print('\nBank amount: $' + str(playerinfo['roundtotal']))
    letter = str(input('Select a vowel: '))
    letter = letter.strip().lower()
    v_check = letter in vowels

    while v_check == False:
        print('Not a vowel, try again')
        letter = str(input('Select a vowel: '))
        letter = letter.strip().lower()
        v_check = letter in vowels
    else:
        playerinfo['roundtotal'] -= vowelcost
        guessletter(letter, playerNum)
        time.sleep(0.5)
        print('\nBank amount: $' + str(playerinfo['roundtotal']))
        print('\nWord: ' + blankWord)
        print('\n(S)pin the wheel, (b)uy a vowel, or (g)uess the word')

    if blankWord == roundWord:
        wordcomplete = True

    return goodGuess      

def guessWord(playerNum):
    global players
    global blankWord
    global roundWord
    global wordcomplete

    print('\nWord: ' + blankWord)

    guess = str(input('Guess the word: '))
    guess = guess.lower()

    if guess == roundWord:
        blankWord = roundWord
        print('\nCorrect!')
        print('Word: ' + blankWord)
        wordcomplete = True
    else:
        print('\nIncorrect. NEXT!')

    return False

def wofTurn(playerNum):  
    global roundWord
    global blankWord
    global turntext
    global players
    global stillinTurn
    global playerinfo
    global wordcomplete

    playerinfo = players[playerNum]

    print('\n' + str(playerinfo['name']) + '\'s turn')
    print('————————————————————————————')
    time.sleep(0.5)
    print('(S)pin the wheel, (b)uy a vowel, or (g)uess the word')

    stillinTurn = True

    while stillinTurn == True:
        if wordcomplete == True:
            break
        else:
            choice = input('Select: ')
            
            if(choice.strip().upper() == "S"):
                stillinTurn = spinWheel(playerNum)
            elif(choice.strip().upper() == "B"):
                if playerinfo['roundtotal'] >= vowelcost:
                    stillinTurn = buyVowel(playerNum)
                else:
                    print('You do not have enough to buy a vowel')
            elif(choice.upper() == "G"):
                stillinTurn = guessWord(playerNum)
            else:
                print("Not a correct option")      

def wofRound():
    global players
    global roundWord
    global blankWord
    global roundstatus
    global roundcount
    global wordcomplete

    print('\nRound ' + str(roundcount))
    print('============================\n')
    time.sleep(0.5)

    initPlayer = wofRoundSetup()

    print('Word: ' + str(blankWord))
    time.sleep(0.75)

    turncounter = 3
    wordcomplete = False

    while wordcomplete == False:
        wofTurn((turncounter + initPlayer) % 3)
        time.sleep(0.75)
        turncounter += 1
    else:
        print('\n' + str(playerinfo['name']) + ' wins!')
        playerinfo['gametotal'] += playerinfo['roundtotal']
        print('\nRound total: $' + str(playerinfo['roundtotal']))
        print('Game total: $' + str(playerinfo['gametotal']) + '\n')

def wofFinalRound():
    global roundWord
    global blankWord
    global finalroundtext

    rstlne = {'r','s','t','l','n','e'}

    player1 = players[0]
    player2 = players[1]
    player3 = players[2]

    if player1['gametotal'] > player2['gametotal'] and player1['gametotal'] > player3['gametotal']:
        winplayernum = 0
    elif player2['gametotal'] > player1['gametotal'] and player2['gametotal'] > player3['gametotal']:
        winplayernum = 1
    elif player3['gametotal'] > player1['gametotal'] and player3['gametotal'] > player2['gametotal']:
        winplayernum = 2

    winplayer = players[winplayernum]

    print('\nFinal Round')
    print('============================\n')
    print('Final round player is ' + str(winplayer['name']))
    getWord()
    print('\nWord: ' + str(blankWord))
    time.sleep(0.75)
    print('\nFirst, we will reveal R-S-T-L-N-E letters')
    time.sleep(0.5)

    for a in rstlne:
        guessletter(a ,winplayer)

    print('\nWord: ' + str(blankWord))

    print('\nNow, choose 3 consonants and 1 vowel')
    
    guessedletters = []

    for a in range(3):
        letter = str(input('Guess a consonant: '))
        
        while len(letter) != 1:
            print('Guess ONE letter')
            letter = str(input('Guess a consonant: '))

        check = letter in rstlne
        vcheck = letter in vowels
        gcheck = letter in guessedletters

        while check == True or vcheck == True or gcheck == True:
            if check == True:
                print('Letter already revealed, try again')
                letter = str(input('Guess a consonant: '))
                check = letter in rstlne
                vcheck = letter in vowels
                gcheck = letter in guessedletters
            elif vcheck == True:
                print('Not a consonant, try again')
                letter = str(input('Guess a consonant: '))
                check = letter in rstlne
                vcheck = letter in vowels
                gcheck = letter in guessedletters
            elif gcheck == True:
                print('Letter already guessed, try again')
                letter = str(input('Guess a consonant: '))
                check = letter in rstlne
                vcheck = letter in vowels
                gcheck = letter in guessedletters
        else:
            guessedletters.append(letter)
    
    letter = str(input('Guess a vowel: '))
    vcheck = letter in vowels
    
    while vcheck == False:
        print('Not a vowel, try again')
        letter = str(input('Guess a vowel: '))
        vcheck = letter in vowels
    else:
        guessedletters.append(letter)

    print('\nLet\'s check...')
    time.sleep(0.75)

    for a in guessedletters:
        guessletter(a, winplayer)

    if blankWord == roundWord:
        print('\nWord: ' + roundWord)
        time.sleep(0.5)
        print('\nCongratulations! You guessed correctly!')
        time.sleep(0.5)
        print('\nYou win $' + str(finalprize) + '!')
        winplayer['gametotal'] += finalprize
    else:
        print('\nWord: ' + str(blankWord))
        time.sleep(0.75)

        print('\nNow, try to guess the word')
        finalguess = str(input('Make a guess: '))
        finalguess = finalguess.lower()
        print('\n...')
        time.sleep(0.75)

        if finalguess == roundWord:
            print('\nCongratulations! You guessed correctly!')
            time.sleep(0.5)
            print('\nYou win $' + str(finalprize) + '!')
            winplayer['gametotal'] += finalprize
        else:
            print('\nSorry, unfortunately you guessed wrong.')
            print('\nThe word is:' + str(roundWord))

    print('\nYour total winnings are: $' + str(winplayer['gametotal']))

def main():
    global roundcount

    roundcount = 1

    print('\nWelcome to Wheel of Fortune!')
    print('============================\n')
    gameSetup()

    for i in range(0,maxrounds):
        if i in [0,1]:
            wofRound()
            roundcount += 1
            time.sleep(0.75)

            player1 = players[0]
            player2 = players[1]
            player3 = players[2]

            print('Round totals:\n')
            print(str(player1['name']) + ': $' + str(player1['gametotal']))
            print(str(player2['name']) + ': $' + str(player2['gametotal']))
            print(str(player3['name']) + ': $' + str(player3['gametotal']))
        else:
            wofFinalRound()

if __name__ == "__main__":
    main()
