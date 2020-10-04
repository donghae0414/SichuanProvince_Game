from bangtal import *
import config

import random
import time

# Game Options
setGameOption(GameOption.INVENTORY_BUTTON, False)
setGameOption(GameOption.MESSAGE_BOX_BUTTON, False)

# Load Record Files
f = open(config.RecordFile, 'r')
for i in range(3):
    line = f.readline()
    config.record[i] = float(line)
f.close()


# Class
class StageButton(Object):
    def __init__(self, file, s):
        super().__init__(file)
        self.stage = s

    def onMouseAction(self, x, y, action):
        config.SuccessiveWrongCount = 0
        config.SuccessiveRightCount = 0
        config.CorrectNum = 0
        initClickedVars()
        config.StartTime = time.time()

        config.NowStage = self.stage
        config.NowState = config.State.NOCLICK
        
        gameScene.enter()

        deadLineTimer.set(config.deadLineTime[self.stage])
        createCards()
        answerShowTimer.set(config.AnswerShowTime)
        answerShowTimer.start()
        showTimer(answerShowTimer)

class Card(Object):
    def __init__(self, file, row, col):
        super().__init__(file)
        self.image = file
        self.row = row
        self.col = col
        self.isHide = False

    def locate(self, scene, x, y):
        super().locate(scene, x, y)

    def onMouseAction(self, x, y, action):
        global Cards, NowState, FirstClickedRow, FirstClickedCol, SecondClickedRow, SecondClickedCol
        
        if config.NowStage == config.State.CANNOTCLICK:
            return

        if (config.NowState == config.State.ONECLICK) and (config.FirstClickedRow == self.row) and (config.FirstClickedCol == self.col): # double Click Error
            print('wrong double click')
            return

        if config.NowState != config.State.TWOCLICK:
            self.setImage(self.image)

        if config.NowState == config.State.NOCLICK:
            config.NowState = config.State.ONECLICK
            config.FirstClickedRow = self.row
            config.FirstClickedCol = self.col

        elif config.NowState == config.State.ONECLICK:
            config.NowState = config.State.TWOCLICK
            config.SecondClickedRow = self.row
            config.SecondClickedCol = self.col
            
            if config.Cards[config.FirstClickedRow][config.FirstClickedCol].image == self.image:   # if it is answer
                print('answer')
                rightTimer.set(0.5)
                rightTimer.start()
            else:   # if it is wrong
                print('wrong')
                wrongTimer.set(0.5)
                wrongTimer.start()
    def hide(self):
        super().hide()
        self.isHide = True



# Timers
answerShowTimer = Timer(config.AnswerShowTime)
def answerShowTimer_onTimeout():
    for i in range(config.CardRow[config.NowStage]):
        for j in range(config.CardCol[config.NowStage]):
            config.Cards[i][j].setImage(config.CardBackImage)
    hideTimer()
    
    deadLineTimer.start()
    showTimer(deadLineTimer)
answerShowTimer.onTimeout = answerShowTimer_onTimeout

rightTimer = Timer(0.5)
def rightTimer_onTimeOut():
    config.SuccessiveRightCount += 1
    config.SuccessiveWrongCount = 0
    if config.SuccessiveRightCount == config.SuccessiveRightNum:
        config.SuccessiveRightCount = 0
        deadLineTimer.increase(3)

    config.NowState = config.State.NOCLICK
    config.Cards[config.FirstClickedRow][config.FirstClickedCol].hide()
    config.Cards[config.SecondClickedRow][config.SecondClickedCol].hide()
    initClickedVars()
    
    config.CorrectNum += 2
    if config.CorrectNum == config.CardRow[config.NowStage] * config.CardCol[config.NowStage]: # Game end

        ###
        ### 성공 시
        ###
        completeTime = format(time.time() - config.StartTime, ".2f")
        compare_record(float(completeTime))
        
        deadLineTimer.stop()
        hideTimer()
        endSceneTimer.start()
rightTimer.onTimeout = rightTimer_onTimeOut

def compare_record(completeTime):
    msg = ""
    if config.NowStage == config.Stage.EASY:
        if config.record[0] > completeTime:
            config.record[0] = completeTime
            msg = 'Easy 기록 갱신! ' + str(float(completeTime)) + ' 초!'
        else:
            msg = '이번 기록 : ' + str(float(completeTime)) + ' 초!\n' + 'Easy 최고 기록 : ' + str(config.record[0]) + ' 초'
    elif config.NowStage == config.Stage.NORMAL:
        if config.record[1] > completeTime:
            config.record[1] = completeTime
            msg = 'Normal 기록 갱신! ' + str(float(completeTime)) + ' 초!'
        else:
            msg = '이번 기록 : ' + str(float(completeTime)) + ' 초!\n' + 'Normal 최고 기록 : ' + str(config.record[1]) + ' 초'
    elif config.NowStage == config.Stage.HARD:
        if config.record[2] > completeTime:
            config.record[2] = completeTime
            msg = 'Hard 기록 갱신! ' + str(float(completeTime)) + ' 초!'
        else:
            msg = '이번 기록 : ' + str(float(completeTime)) + ' 초!\n' + 'Hard 최고 기록 : ' + str(config.record[2]) + ' 초'
    else:
        print('compare_record stage error')

    f = open(config.RecordFile, 'w')
    for i in range(3):
        f.write(str(config.record[i]) + "\n")
    f.close

    showMessage(msg)

wrongTimer = Timer(0.5)
def wrongTimer_onTimeout():
    
    config.SuccessiveRightCount = 0
    config.SuccessiveWrongCount += 1
    if config.SuccessiveWrongCount == config.SuccessiveWrongNum:
        item_eye.show()

    config.NowState = config.State.NOCLICK
    config.Cards[config.FirstClickedRow][config.FirstClickedCol].setImage(config.CardBackImage)
    config.Cards[config.SecondClickedRow][config.SecondClickedCol].setImage(config.CardBackImage)
    initClickedVars()
wrongTimer.onTimeout = wrongTimer_onTimeout

deadLineTimer = Timer(60)
def deadLineTimer_onTimeout():
    hideTimer()

    ###
    ### 실패 시
    ###

    showMessage('실패!')
    endSceneTimer.start()
deadLineTimer.onTimeout = deadLineTimer_onTimeout

endSceneTimer = Timer(0.5)
def endSceneTimer_onTimeout():
    endScene.enter()
endSceneTimer.onTimeout = endSceneTimer_onTimeout



###
### Start Scene
###
startScene = Scene('main', config.Directory.BACKGROUND.value + 'castle.png')

def initClickedVars():
    config.FirstClickedRow, config.FirstClickedCol, config.SecondClickedRow, config.SecondClickedCol = None, None, None, None

startButton = Object(config.Directory.BUTTON.value + 'start_button.png')
startButton.locate(startScene, 526, 120)
startButton.setScale(0.5)
startButton.show()
def startButton_onMouseAction(x, y, action):
    stageScene.enter()
    curtainTimer.start()
startButton.onMouseAction = startButton_onMouseAction


###
### Stage Scene
###
stageScene = Scene('stage', config.Directory.BACKGROUND.value + 'castle.png')

curtainLeft = Object(config.Directory.BACKGROUND.value + 'curtain_left.png')
curtainLeft.x = -267
curtainLeft.locate(stageScene, curtainLeft.x, 0)
curtainLeft.show()

curtainRight = Object(config.Directory.BACKGROUND.value + 'curtain_right.png')
curtainRight.x = 1280
curtainRight.locate(stageScene, curtainRight.x, 0)
curtainRight.show()

curtainTop = Object(config.Directory.BACKGROUND.value + 'curtain_top.png')
curtainTop.y = 720
curtainTop.locate(stageScene, 0, curtainTop.y)
curtainTop.show()

curtainTimer = Timer(0.01)
def curtainTimer_onTimeout():
    curtainLeft.x += 10
    curtainLeft.locate(stageScene, curtainLeft.x, 0)
    curtainRight.x -= 10
    curtainRight.locate(stageScene, curtainRight.x, 0)
    curtainTop.y -= 5
    curtainTop.locate(stageScene, 0, curtainTop.y)

    if curtainLeft.x < 0:
        curtainTimer.set(0.01)
        curtainTimer.start()
    else:
        curtainLeft.locate(stageScene, 0, 0)
        curtainRight.locate(stageScene, 1280 - 292, 0)
        curtainTop.locate(stageScene, 0, 720 - 133)
        curtainTimer.stop()
curtainTimer.onTimeout = curtainTimer_onTimeout

config.StageButtons.append(StageButton(config.Directory.BUTTON.value + 'easy_button.png', config.Stage.EASY))
config.StageButtons.append(StageButton(config.Directory.BUTTON.value + 'normal_button.png', config.Stage.NORMAL))
config.StageButtons.append(StageButton(config.Directory.BUTTON.value + 'hard_button.png', config.Stage.HARD))
for i in range(len(config.StageButtons)):
    config.StageButtons[i].locate(stageScene, 211 + 300*i, 120)
    config.StageButtons[i].setScale(0.5)
    config.StageButtons[i].show()

def createCards():
    # select Characters
    characterNum = int(config.CardRow[config.NowStage] * config.CardCol[config.NowStage] / 2)
    random.shuffle(config.CharacterList)
    CharacterArr = config.CharacterList[:characterNum]
    CharacterArr += CharacterArr
    random.shuffle(CharacterArr)
    print('Selected Characters :', CharacterArr)

    # shuffle map
    config.Cards = []
    map = []
    for i in range(config.CardRow[config.NowStage]):
        arr = []
        row = []
        for j in range(config.CardCol[config.NowStage]):
            arr.append((i, j))
            row.append(None)
        random.shuffle(arr)
        map.append(arr)
        config.Cards.append(row)
    random.shuffle(map)
    print('map :', map)
    
    # make Card Objects
    characterIdx = 0
    scale = 0.3
    for i in range(config.CardRow[config.NowStage]):
        for j in range(config.CardCol[config.NowStage]):
            filename = int(CharacterArr[characterIdx])
            if filename < 10:
                filename = '0' + str(filename) + '.png'
            else:
                filename = str(filename) + '.png'
            config.Cards[map[i][j][0]][map[i][j][1]] = Card(config.Directory.CHARACTER.value + filename, map[i][j][0], map[i][j][1])
            config.Cards[map[i][j][0]][map[i][j][1]].locate(gameScene, config.startRowPx[config.NowStage] + i*int(380*scale) + 5, config.startColPx[config.NowStage] + j*int(502*scale) + 5)
            config.Cards[map[i][j][0]][map[i][j][1]].setScale(scale)
            config.Cards[map[i][j][0]][map[i][j][1]].show()
            characterIdx += 1

###
### Game Scene
###
gameScene = Scene('game', config.Directory.BACKGROUND.value + 'castle.png')

item_eye = Object(config.Directory.ITEM.value + 'eye.png')
item_eye.locate(gameScene, 5, 600)
item_eye.setScale(0.8)

def item_eye_onMouseAction(x, y, action):
    config.SuccessiveWrongCount = 0
    config.NowState = config.State.CANNOTCLICK

    item_eye.hide()
    for i in range(config.CardRow[config.NowStage]):
        for j in range(config.CardCol[config.NowStage]):
            if not config.Cards[i][j].isHide:
                config.Cards[i][j].setImage(config.Cards[i][j].image)
    item_eye_timer.set(2)
    item_eye_timer.start()
item_eye.onMouseAction = item_eye_onMouseAction

item_eye_timer = Timer(2)
def item_eye_timer_onTimeout():
    config.NowState = config.State.NOCLICK
    for i in range(config.CardRow[config.NowStage]):
        for j in range(config.CardCol[config.NowStage]):
            if not config.Cards[i][j].isHide:
                config.Cards[i][j].setImage(config.Directory.CARD.value + 'card.png')
item_eye_timer.onTimeout = item_eye_timer_onTimeout


###
### end Scene
###
endScene = Scene('end', config.Directory.BACKGROUND.value + 'castle.png')
def endScene_onEnter():
    for i in range(config.CardRow[config.NowStage]):
        for j in range(config.CardCol[config.NowStage]):
            config.Cards[i][j].hide()
    
endScene.onEnter = endScene_onEnter


restartButton = Object(config.Directory.BUTTON.value + 'restart_button.png')
restartButton.locate(endScene, 280, 200)
restartButton.setScale(0.5)
restartButton.show()
def restartButton_onMouseAction(x, y, action):
    stageScene.enter()
    curtainTimer.start()
restartButton.onMouseAction = restartButton_onMouseAction

exitButton = Object(config.Directory.BUTTON.value + 'exit_button.png')
exitButton.locate(endScene, 763, 200)
exitButton.setScale(0.5)
exitButton.show()
def exitButton_onMouseAction(x, y, action):
    endGame()
exitButton.onMouseAction = exitButton_onMouseAction

# start Game
startGame(startScene)