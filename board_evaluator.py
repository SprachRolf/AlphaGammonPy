import game
import pickle
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split

#
#  rate a board with scikit-learn.neural_net
#
#
class BoardEvaluator:
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