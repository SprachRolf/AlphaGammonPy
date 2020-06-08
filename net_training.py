import pickle
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from pathlib import Path
from collections import OrderedDict
import cProfile

import board_analyzer as ba

"""
#file = open("boards_whitewins_redwins_300000_boards.p", "rb")
file = open("boards_whitewins_redwins_90000_boards.p", "rb")
X = pickle.load(file)
whiteWins = pickle.load(file)
redWins = pickle.load(file)

pWhiteWins = [whiteWins[i]/(whiteWins[i] + redWins[i]) for i in range(len(X))]
pRedWins =  [redWins[i]/(whiteWins[i] + redWins[i]) for i in range(len(X))]
y = [pWhiteWins[i] - pRedWins[i] for i in range(len(X))]
#print(y)
print(len(X), 'traing samples loaded.')

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

#regressor = MLPRegressor(solver='adam', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1, max_iter=1000000)
#regressor = MLPRegressor(solver='adam', alpha=1e-5, hidden_layer_sizes=(10, 4),activation="logistic", random_state=1, max_iter=1000000)
#regressor.fit(X_train, y_train)

regressor = MLPRegressor(solver='adam', alpha=1e-5, hidden_layer_sizes=(10, 4),activation="logistic", random_state=1, max_iter=1000000,)
regressor.partial_fit(X_train, y_train)
print(regressor.score(X_test, y_test))
regressor.partial_fit(X_train,y_train)
print(regressor.score(X_test, y_test))
regressor.partial_fit(X_train,y_train)
print(regressor.score(X_test, y_test))
regressor.partial_fit(X_train,y_train)
print(regressor.score(X_test, y_test))

pickle.dump(regressor,open("trained_net_online.p", "xb"))
"""

def generateUntrainedStarterNet():

    knownBoards = [[-2,0,0,0,0,5, 0,3,0,0,0,-5, 5,0,0,0,-3,0, -5,0,0,0,0,2,  0,0,0,0],
                [-2,0,0,0,0,5, 0,3,0,0,0,-5, 5,0,0,0,-3,0, -5,0,0,0,0,2,  0,0,0,0],
                [-2,0,0,0,0,5, 0,3,0,0,0,-5, 5,0,0,0,-3,0, -5,0,0,0,0,2,  0,0,0,0],
                [-2,0,0,0,0,5, 0,3,0,0,0,-5, 5,0,0,0,-3,0, -5,0,0,0,0,2,  0,0,0,0]
                ]

    X = knownBoards
    pWhiteWins = [1,1,1,1]
    pRedWins =  [1,1,1,1]
    y = [pWhiteWins[i] - pRedWins[i] for i in range(len(X))]

    #regressor = MLPRegressor(solver='adam', alpha=1e-5, hidden_layer_sizes=(10, 4),activation="logistic", random_state=1, max_iter=1000000,)

    # super simple net. Inputs directly to single output.
    #regressor = MLPRegressor(solver='adam', alpha=1e-5, hidden_layer_sizes=(), activation="logistic", random_state=1, max_iter=1000000,)

    # Trying to "mask" with the "rectified linear unit" (relu) activation function,
    # in order to only count "red" tokens.
    regressor = MLPRegressor(solver='adam', alpha=1e-5, hidden_layer_sizes=(56,2), activation="relu", random_state=1, max_iter=1000000,)
    regressor.partial_fit(X,y)

    pickle.dump(regressor, open("trained_net_white.p", "xb"))
    pickle.dump(regressor, open("trained_net_red.p", "xb"))

def trainFromAllTrainingBoards():
    pass
    # open training_batch_1_2020-0*
    # check for duplicate boards
    # do a single training run on all
    # test the net.

def trainFromLastTrainingBoards():
    dir = Path(".")
    print(type(Path(".")), Path("."))

    """
    boards = []
    probs = []
    knownBoards = 0
    knownFlippedBoards = 0
    newBoards = 0
    for datei in dir.rglob("training_batch_1_2020-06-06 12*"):
        print("loading ", datei.name)
        fileHandle = open(datei.name, "rb")
        fileBoards = pickle.load(fileHandle)
        y = pickle.load(fileHandle)
        fileHandle.close()
        print("loaded. Reading boards...")
        for board, prob in zip(fileBoards,y):
            flippedTokens = ba.BoardAnalyzer.flipBoard(board)
            knownBoardIndex = -1
            try:
                knownBoardIndex = boards.index(board)
                #print("k", end="")
                knownBoards +=1
            except:
                try:
                    knownBoardIndex = boards.index(flippedTokens)
                    #print("f", end="")
                    knownFlippedBoards +=1
                except:
                    #print("n", end="")
                    newBoards +=1
                    boards.append(board)
                    probs.append(prob)
        
    print("new boards:", newBoards, "known boards:", knownBoards, "known flipped Boards:", knownFlippedBoards)
    """
    boards = OrderedDict()

    for datei in dir.rglob("training_batch_1_2020-06-06 12*"):
        print("loading ", datei.name)
        fileHandle = open(datei.name, "rb")
        fileBoards = pickle.load(fileHandle)
        fileProbs = pickle.load(fileHandle)
        fileHandle.close()
        print("loaded. Reading boards...")
        for board, prob in zip(fileBoards,fileProbs):
            flippedTokens = ba.BoardAnalyzer.flipBoard(board)
            boards[tuple(board)] = prob
            # A few boards will be in there, where the flipped board is in too.

    X = tuple(boards.keys())
    y = tuple(boards.values())
    print(len(X), "Boards loaded, and", len(y), "winning probabilities.")
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
    print("Training net.")
    regressor = MLPRegressor(solver='adam', alpha=1e-5, hidden_layer_sizes=(56,2), activation="relu", random_state=1, max_iter=1000000,)
    regressor.partial_fit(X_train,y_train)
    print("Score:", regressor.score(X_test, y_test))

    print("Dumping net and training data to file")
    pickle.dump(regressor, open("trained_net_2020606_12uhr_training_data.p", "wb"))
    training_file = open("training_data_20200606_12uhr.p", "wb")
    pickle.dump(X, training_file)
    pickle.dump(y, training_file)

    pass

#generateUntrainedStarterNet()
trainFromLastTrainingBoards()
#cProfile.run('trainFromLastTrainingBoards()')
