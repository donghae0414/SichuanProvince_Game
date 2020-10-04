from enum import Enum
import sys
###
### Global Variables
###

# directories
class Directory(Enum):
    CARD = 'card/'
    BACKGROUND = 'background/'
    CHARACTER = 'characters/'
    BUTTON = 'button/'
    ITEM = 'item/'
CardBackImage = Directory.CARD.value + 'card.png'

# Stage
class Stage(Enum):
    EASY = 0
    NORMAL = 1
    HARD = 2
NowStage = None

# State
class State(Enum):
    NOCLICK = 0
    ONECLICK = 1
    TWOCLICK = 2
    CANNOTCLICK = 3
NowState = State.NOCLICK

# item variables
SuccessiveWrongNum = 4
SuccessiveWrongCount = 0

SuccessiveRightNum = 2
SuccessiveRightCount = 0

# map variables
Cards = []
StageButtons = []
CharacterNum = 20
CharacterList = list(range(1, CharacterNum + 1))
CorrectNum = 0

CardRow = {
    Stage.EASY : 4,
    Stage.NORMAL : 6,
    Stage.HARD : 10}
CardCol = {
    Stage.EASY : 3,
    Stage.NORMAL : 4,
    Stage.HARD : 4}

startRowPx = {
    Stage.EASY : 412,
    Stage.NORMAL : 298,
    Stage.HARD : 70}
startColPx = {
    Stage.EASY : 134,
    Stage.NORMAL : 59,
    Stage.HARD : 59}

# click variables
FirstClickedRow = None
FirstClickedCol = None
SecondClickedRow = None
SecondClickedCol = None


# Records
RecordFile = 'record.txt'
record = [sys.maxsize, sys.maxsize, sys.maxsize]

# Game Time
StartTime = None
AnswerShowTime = 2
deadLineTime = {
    Stage.EASY : 30,
    Stage.NORMAL : 60,
    Stage.HARD : 60}