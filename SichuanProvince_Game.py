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
    BACKGROUND = 'background/'
    CHARACTER = 'characters/'
    BUTTON = 'button/'


# variables
CharacterNum = 20
CharacterList = list(range(1, CharacterNum + 1))
CorrectNum = 0

class Difficulty(Enum):
    EASY = 0,
    NORMAL = 1,
    HARD = 2
NowStage = None

CardRow = {
    Difficulty.EASY : 4,
    Difficulty.NORMAL : 6,
    Difficulty.HARD : 10}
CardCol = {
    Difficulty.EASY : 3,
    Difficulty.NORMAL : 4,
    Difficulty.HARD : 4}
Cards = []

startRowPx = {
    Difficulty.EASY : 412,
    Difficulty.NORMAL : 298,
    Difficulty.HARD : 70}
startColPx = {
    Difficulty.EASY : 134,
    Difficulty.NORMAL : 59,
    Difficulty.HARD : 59}

deadLineTime = {
    Difficulty.EASY : 30,
    Difficulty.NORMAL : 30,
    Difficulty.HARD : 60}

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
Stages = []
class Stage(Object):
    def __init__(self, file, s):
        super().__init__(file)
        self.difficulty = s

    def onMouseAction(self, x, y, action):
        global NowStage
        initClickedVars()

        gameScene.enter()

        NowStage = self.difficulty
    
        deadLineTimer.set(deadLineTime[self.difficulty])
        createCards()
        answerShowTimer.start()
        showTimer(answerShowTimer)

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
    for i in range(CardRow[NowStage]):
        for j in range(CardCol[NowStage]):
            Cards[i][j].setImage(CardBackImage)
    hideTimer()
    
    deadLineTimer.start()
    showTimer(deadLineTimer)
answerShowTimer.onTimeout = answerShowTimer_onTimeout

rightTimer = Timer(0.5)
def rightTimer_onTimeOut():
    global Cards, NowState, CorrectNum

    NowState = State.NOCLICK
    Cards[FirstClickedRow][FirstClickedCol].hide()
    Cards[SecondClickedRow][SecondClickedCol].hide()
    initClickedVars()

    CorrectNum += 2
    if CorrectNum == CardRow[NowStage] * CardCol[NowStage]: # Game end
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

deadLineTimer = Timer(60)
def deadLineTimer_onTimeout():
    hideTimer()
    showMessage('ㅉㅉ')
    endSceneTimer.start()
deadLineTimer.onTimeout = deadLineTimer_onTimeout

endSceneTimer = Timer(1)
def endSceneTimer_onTimeout():
    endScene.enter()
endSceneTimer.onTimeout = endSceneTimer_onTimeout



###
### Start Scene
###
startScene = Scene('main', Directory.BACKGROUND.value + 'castle.png')

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
stageScene = Scene('stage', Directory.BACKGROUND.value + 'castle.png')
curtain = Object(Directory.BACKGROUND.value + 'curtain.png')
curtain.locate(stageScene, 0, 0)
curtain.show()

Stages.append(Stage(Directory.BUTTON.value + 'easy_button.png', Difficulty.EASY))
Stages.append(Stage(Directory.BUTTON.value + 'normal_button.png', Difficulty.NORMAL))
Stages.append(Stage(Directory.BUTTON.value + 'hard_button.png', Difficulty.HARD))
for i in range(len(Stages)):
    Stages[i].locate(stageScene, 211 + 300*i, 120)
    Stages[i].setScale(0.5)
    Stages[i].show()

def createCards():
    global Cards

    # select Characters
    characterNum = int(CardRow[NowStage] * CardCol[NowStage] / 2)
    random.shuffle(CharacterList)
    CharacterArr = CharacterList[:characterNum]
    CharacterArr += CharacterArr
    random.shuffle(CharacterArr)
    print('Selected Characters :', CharacterArr)

    # shuffle map
    Cards = []

    map = []
    for i in range(CardRow[NowStage]):
        arr = []
        row = []
        for j in range(CardCol[NowStage]):
            arr.append((i, j))
            row.append(None)
        random.shuffle(arr)
        map.append(arr)
        Cards.append(row)
    random.shuffle(map)
    print('map :', map)
    
    # make Card Objects
    characterIdx = 0

    scale = 0.3
    for i in range(CardRow[NowStage]):
        for j in range(CardCol[NowStage]):
            filename = int(CharacterArr[characterIdx])
            if filename < 10:
                filename = '0' + str(filename) + '.png'
            else:
                filename = str(filename) + '.png'
            Cards[map[i][j][0]][map[i][j][1]] = Card(Directory.CHARACTER.value + filename, map[i][j][0], map[i][j][1])
            Cards[map[i][j][0]][map[i][j][1]].locate(gameScene, startRowPx[NowStage] + i*int(380*scale) + 5, startColPx[NowStage] + j*int(502*scale) + 5)
            Cards[map[i][j][0]][map[i][j][1]].setScale(scale)
            Cards[map[i][j][0]][map[i][j][1]].show()
            characterIdx += 1


###
### Game Scene
###
gameScene = Scene('game', Directory.BACKGROUND.value + 'castle.png')


###
### end Scene
###
endScene = Scene('end', Directory.BACKGROUND.value + 'castle.png')


# start Game
startGame(startScene)