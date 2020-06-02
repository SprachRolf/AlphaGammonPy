import pickle
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split


file = open("boards_whitewins_redwins_pre_logistic_305000_boards.p", "rb")
X = pickle.load(file)
whiteWins = pickle.load(file)
redWins = pickle.load(file)

pWhiteWins = [whiteWins[i]/(whiteWins[i] + redWins[i]) for i in range(len(X))]
pRedWins =  [redWins[i]/(whiteWins[i] + redWins[i]) for i in range(len(X))]
y = [pWhiteWins[i] - pRedWins[i] for i in range(len(X))]
#print(y)
print(len(X), 'traing samples loaded.')

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

"""
#print(len(X), len(y), X[0], y[0])

for i in range(len(y)):
    print(X[i])
for i in range(len(y)):
    val = (( (int) (y[i]*100))/100 )
    print(val)

print(len(X))
"""

#regressor = MLPRegressor(solver='adam', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1, max_iter=1000000)
regressor = MLPRegressor(solver='adam', alpha=1e-5, hidden_layer_sizes=(10, 4),activation="logistic", random_state=1, max_iter=1000000)
regressor.fit(X_train, y_train)
print(regressor.score(X_test, y_test))

pickle.dump(regressor,open("trained_net_305000_logistic_test_size_50.p", "wb"))
