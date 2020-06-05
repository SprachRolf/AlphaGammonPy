import pickle
from sklearn.neural_network import MLPRegressor

file = open("trained_net_online_2020-06-04 06:31:45.624514.p", "rb")

regressor = pickle.load(file)
print("ende")