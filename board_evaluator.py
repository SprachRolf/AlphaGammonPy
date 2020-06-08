import pickle
import datetime
import game
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
#
#  rate a board with scikit-learn.neural_net
#
#
class HitBoardEvaluator:
    def __init__(self, color):
        if color == game.Game.white:
            self.regressor = pickle.load(open("trained_net_white_500_runs_10_4_hidden_nodes.p", "rb"))
        else:
            self.regressor = pickle.load(open("trained_net_red_500_runs_10_4_hidden_nodes.p", "rb"))

        """
        file = open("boards_n_values_35mb.p", "rb")
        X = pickle.load(file)
        y = pickle.load(file)

        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

        #print(len(X), len(y), X[0], y[0])

        for i in range(len(y)):
            print(X[i])
        for i in range(len(y)):
            val = (( (int) (y[i]*100))/100 )
            print(val)

        print(len(X))
        """

        #self.regressor = MLPRegressor(solver='adam', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1, max_iter=1000)
        #print("Training the net.")
        #self.regressor.fit(X_train, y_train)
        #print("Training finished. Score on test set:", self.regressor.score(X_test, y_test))

    def getBoardRating(self, tokens):
        return self.regressor.predict([tokens])

class WinningColorBoardEvaluator:
    def __init__(self):
        self.regressor = pickle.load(open("trained_net_305000_logistic.p", "rb"))


    def getBoardRating(self, tokens):
        return self.regressor.predict([tokens])


class OnlineBoardEvaluator:
    def __init__(self, netFilename):
        try:
            print("Trying to load neural net:", netFilename +".p")
            self.regressor = pickle.load(open(netFilename +".p", "rb"))
            print("Loading was successful.")
        except:
            print("Creating new neural net.")
            self.regressor = MLPRegressor(solver='adam', alpha=1e-5, activation="logistic", random_state=1, max_iter=1000000,)

        self.filenameBase = netFilename

        self.updates = 0
        self.saveEveryXth = 1


    def getBoardRating(self, tokens):
        return self.regressor.predict([tokens])

    def learnBatch(self, boards, whiteWins, redWins):
        X = boards
        pWhiteWins = [whiteWins[i]/(whiteWins[i] + redWins[i]) for i in range(len(X))]
        pRedWins =  [redWins[i]/(whiteWins[i] + redWins[i]) for i in range(len(X))]
        y = [pWhiteWins[i] - pRedWins[i] for i in range(len(X))]

        #X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
        #self.regressor.fit(X_train, y_train)
        #print("net score:", self.regressor.score(X_test, y_test))


        self.regressor.partial_fit(X,y)
        self.updates +=1
        if (self.updates >= self.saveEveryXth):
            print("Saving net.")
            dateString = str(datetime.datetime.now())
            pickle.dump(self.regressor, open(self.filenameBase +"_"+ dateString +".p", "xb"))
            pickle.dump(self.regressor, open(self.filenameBase +".p", "wb"))
            self.updates = 0
            print("saving a sample batch.")
            batchFile = open("training_batch_"+ str(self.saveEveryXth) +"_"+ dateString + "_"+ str(len(boards))  +".p", "xb")
            pickle.dump(X, batchFile)
            pickle.dump(y, batchFile)
            pickle.dump(whiteWins, batchFile)
            pickle.dump(redWins, batchFile)
            batchFile.close()

            """
            fig, axes = plt.subplots(8, 8)
            # use global min / max to ensure all weights are shown on the same scale
            vmin, vmax = self.regressor.coefs_[1].min(), self.regressor.coefs_[0].max()
            for coef, ax in zip(self.regressor.coefs_[1].T, axes.ravel()):
                ax.matshow(coef.reshape(28,1), cmap=plt.cm.gray, vmin=.5 * vmin,
                        vmax=.5 * vmax)
                ax.set_xticks(())
                ax.set_yticks(())

            #plt.show()
            plt.savefig("graph_"+ dateString +".png")
            plt.close()
            """


