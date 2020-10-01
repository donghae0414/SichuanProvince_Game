from bangtal import *
import random
from enum import Enum

# Game Options
setGameOption(GameOption.INVENTORY_BUTTON, False)
setGameOption(GameOption.MESSAGE_BOX_BUTTON, False)


###
### Global Variables
###

# directories
CardBackImage = 'card.png'
class Directory(Enum):
    CHARACTER ='characters/'
    BUTTON = 'button/'


# variables
CharacterNum = 20
CharacterList = list(range(1, CharacterNum + 1))
CorrectNum = 0

CardRow = None
CardCol = None
Cards = []


class State(Enum):
    NOCLICK = 0
    ONECLICK = 1
    TWOCLICK = 2
NowState = State.NOCLICK
FirstClickedRow = None
FirstClickedCol = None
SecondClickedRow = None
SecondClickedCol = None

# Class

class Card(Object):
    def __init__(self, file, row, col):
        global CardImage
        super().__init__(file)
        self.image = file
        self.row = row
        self.col = col

    def locate(self, scene, x, y):
        super().locate(scene, x, y)

    def onMouseAction(self, x, y, action):
        global Cards, NowState, FirstClickedRow, FirstClickedCol, SecondClickedRow, SecondClickedCol
        
        if (NowState == State.ONECLICK) and (FirstClickedRow == self.row) and (FirstClickedCol == self.col): # double Click Error
            print('wrong double click')
            return

        if NowState != State.TWOCLICK:
            self.setImage(self.image)

        if NowState == State.NOCLICK:
            NowState = State.ONECLICK
            FirstClickedRow = self.row
            FirstClickedCol = self.col

        elif NowState == State.ONECLICK:
            NowState = State.TWOCLICK
            SecondClickedRow = self.row
            SecondClickedCol = self.col

            if Cards[FirstClickedRow][FirstClickedCol].image == self.image:   # if it is answer
                print('answer')
                rightTimer.set(1)
                rightTimer.start()
            else:   # if it is wrong
                print('wrong')
                wrongTimer.set(1)
                wrongTimer.start()


# Timers
AnswerShowTime = 2
answerShowTimer = Timer(AnswerShowTime)
def answerShowTimer_onTimeout():
    global Cards
    for i in range(CardRow):
        for j in range(CardCol):
            Cards[i][j].setImage(CardBackImage)
    hideTimer()
    
    deadlineTimer.start()
    showTimer(deadlineTimer)
answerShowTimer.onTimeout = answerShowTimer_onTimeout

rightTimer = Timer(0.5)
def rightTimer_onTimeOut():
    global Cards, NowState, CorrectNum

    NowState = State.NOCLICK
    Cards[FirstClickedRow][FirstClickedCol].hide()
    Cards[SecondClickedRow][SecondClickedCol].hide()
    initClickedVars()

    CorrectNum += 2
    if CorrectNum == CardRow * CardCol: # Game end
        showMessage('ㅊㅊ')
        hideTimer()
        endSceneTimer.start()
rightTimer.onTimeout = rightTimer_onTimeOut

wrongTimer = Timer(0.5)
def wrongTimer_onTimeout():
    global Cards, NowState

    NowState = State.NOCLICK
    Cards[FirstClickedRow][FirstClickedCol].setImage(CardBackImage)
    Cards[SecondClickedRow][SecondClickedCol].setImage(CardBackImage)
    initClickedVars()
wrongTimer.onTimeout = wrongTimer_onTimeout

deadlineTimer = Timer(200000)
def deadlineTimer_onTimeout():
    hideTimer()
    showMessage('ㅉㅉ')
    endSceneTimer.start()
deadlineTimer.onTimeout = deadlineTimer_onTimeout

endSceneTimer = Timer(1)
def endSceneTimer_onTimeout():
    endScene.enter()
endSceneTimer.onTimeout = endSceneTimer_onTimeout

###
### Start Scene
###
startScene = Scene('main', 'background.png')

def initClickedVars():
    global FirstClickedRow, FirstClickedCol, SecondClickedRow, SecondClickedCol
    FirstClickedRow, FirstClickedCol, SecondClickedRow, SecondClickedCol = None, None, None, None

startButton = Object(Directory.BUTTON.value + 'start.png')
startButton.locate(startScene, 600, 60)
startButton.show()
def startButton_onMouseAction(x, y, action):
    stageScene.enter()

startButton.onMouseAction = startButton_onMouseAction

###
### Stage Scene
###
stageScene = Scene('stage', 'background.png')

easyButton = Object(Directory.BUTTON.value + 'easy_button.png')
easyButton.locate(stageScene, 300, 60)
easyButton.setScale(0.5)
easyButton.show()
def easyButton_onMouseAction(x, y, action):
    global CardRow, CardCol
    initClickedVars()
    gameScene.enter()
    CardRow = 6
    CardCol = 4
    createCards()
    answerShowTimer.start()
    showTimer(answerShowTimer)

easyButton.onMouseAction = easyButton_onMouseAction

normalButton = Object(Directory.BUTTON.value + 'normal_button.png')
normalButton.locate(stageScene, 500, 60)
normalButton.setScale(0.5)
normalButton.show()


def createCards():
    global Cards

    # select Characters
    characterNum = int(CardRow * CardCol / 2)
    random.shuffle(CharacterList)
    CharacterArr = CharacterList[:characterNum]
    CharacterArr += CharacterArr
    random.shuffle(CharacterArr)
    print('Selected Characters :', CharacterArr)

    # shuffle map
    Cards = []

    map = []
    for i in range(CardRow):
        arr = []
        row = []
        for j in range(CardCol):
            arr.append((i, j))
            row.append(None)
        random.shuffle(arr)
        map.append(arr)
        Cards.append(row)
    random.shuffle(map)
    print('map :', map)
    
    # make Card Objects
    characterIdx = 0
    startRowPx = 100
    startColPx = 30
    scale = 0.3
    for i in range(CardRow):
        for j in range(CardCol):
            filename = int(CharacterArr[characterIdx])
            if filename < 10:
                filename = '0' + str(filename) + '.png'
            else:
                filename = str(filename) + '.png'
            Cards[map[i][j][0]][map[i][j][1]] = Card(Directory.CHARACTER.value + filename, map[i][j][0], map[i][j][1])
            Cards[map[i][j][0]][map[i][j][1]].locate(gameScene, startRowPx + i*int(380*scale) + 5, startColPx + j*int(502*scale) + 5)
            Cards[map[i][j][0]][map[i][j][1]].setScale(scale)
            Cards[map[i][j][0]][map[i][j][1]].show()
            characterIdx += 1

###
### Game Scene
###
gameScene = Scene('game', 'castle.png')

###
### end Scene
###
endScene = Scene('end', 'white_background.png')

# start Game
startGame(startScene)