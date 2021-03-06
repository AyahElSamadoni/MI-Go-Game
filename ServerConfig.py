import json
import numpy as np
from game import Game
from Stones import Turn
import asyncio

def server_config(GameConfig,FileName=None,mode=1,GuiObject=None):
    if(FileName is None):
        GameConfig = GameConfig
    else:
        with open(FileName, 'r') as f:
            GameConfig = json.load(f)
    #print("1")
    #print(GameConfig)
    # TODO DO we need reamining time of anything at the initalization state(begining of the game from a certain stage)
    GameState = GameConfig["initialState"]
    moveLogJsonArr = GameConfig["moveLog"]

    wloc = list(zip(*np.where((np.array(GameState["board"])) == "W")))
    bloc = list(zip(*np.where((np.array(GameState["board"])) == "B")))
    bCaptured = GameState["players"]["W"]["prisoners"]
    wCaptured = GameState["players"]["B"]["prisoners"]

    gameArgs = {"wloc": wloc, "bloc": bloc,
                "wCapturedStones": wCaptured,
                "bCapturedStones": bCaptured}

    # TODO  Check for any misplaced argument and if initialization of any argument can affect other class members
    """
    instance of backend game supposed to be only one instance
    """
    if mode == 1:
        backEndGame = Game(**gameArgs)
    else:
        backEndGame = Game(**gameArgs,GuiObject=GuiObject, mode=mode)

    turn = Turn.black if GameState["turn"] == "B" else Turn.white
    #print("1.1")
    #print(turn)
    """
    logically speaking Yahia should not send resign move at the beginning
    """
    """
        Taking the move log and adding stones till we reach final state to begin with
    """
    for move in moveLogJsonArr:

        if move["move"]["type"] == "place":
            print("location", (move["move"]["point"]["row"], move["move"]["point"]["column"]), turn)
            x = backEndGame.play(
                (move["move"]["point"]["row"], move["move"]["point"]["column"], turn))
            # gameBoard = backEndGame.getBoard()
            # print(gameBoard)
            if (not x):
                print("Error in location", (move["move"]["point"]["row"], move["move"]["point"]["column"]), turn)
                backEndGame.Drawboard()
                # input('Press any key ...')
        elif (move["move"]["type"] == "pass"):
            backEndGame.play(1, turn)
        elif (move["move"]["type"] == "resign"):
            # TODO handle resign at game config(illogical)
            print("Error in parsing JSON FILE AT GAME INIT CONFIG")
        else:
            # TODO handle error at game config
            pass
            print("Error in parsing JSON FILE AT GAME INIT CONFIG")
        turn = 1 - turn
        # backEndGame.Drawboard()
        # input('Press any key ...')

    # score, TerrBoard = backEndGame.getScoreAndTerrBoard()
    # print(score)
    """"
    NOW instance backEnd stage is initialized with the data parsed
    """
    #print("2")
    return backEndGame
