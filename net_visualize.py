import warnings
import pickle

import matplotlib.pyplot as plt
from sklearn.neural_network import MLPClassifier

#mlp = MLPClassifier(hidden_layer_sizes=(50,), max_iter=10, alpha=1e-4,
#                    solver='sgd', verbose=10, random_state=1,
#                    learning_rate_init=.1)

filenamesOnline_vs_NetHitPlayer = [
"trained_net_online_2020-06-04 05:53:27.075578.p",
"trained_net_online_2020-06-04 05:53:36.331969.p",
"trained_net_online_2020-06-04 05:53:45.161912.p",
"trained_net_online_2020-06-04 05:53:58.013700.p",
"trained_net_online_2020-06-04 05:54:09.168346.p",
"trained_net_online_2020-06-04 05:54:19.460317.p",
"trained_net_online_2020-06-04 05:54:30.556983.p",
"trained_net_online_2020-06-04 05:54:42.719266.p",
"trained_net_online_2020-06-04 05:54:53.260770.p",
"trained_net_online_2020-06-04 05:55:04.259970.p",
"trained_net_online_2020-06-04 05:55:17.229827.p",
"trained_net_online_2020-06-04 05:55:28.271982.p",
"trained_net_online_2020-06-04 05:55:39.357085.p",
"trained_net_online_2020-06-04 05:55:50.099021.p",
"trained_net_online_2020-06-04 05:56:00.250391.p",
"trained_net_online_2020-06-04 05:56:12.100853.p",
"trained_net_online_2020-06-04 05:56:23.706693.p",
"trained_net_online_2020-06-04 05:56:34.049391.p",
"trained_net_online_2020-06-04 05:56:45.526778.p",
"trained_net_online_2020-06-04 05:56:58.148849.p",
"trained_net_online_2020-06-04 05:57:09.044558.p",
"trained_net_online_2020-06-04 05:57:18.637180.p",
"trained_net_online_2020-06-04 05:57:29.697653.p",
"trained_net_online_2020-06-04 05:57:40.396774.p",
"trained_net_online_2020-06-04 05:57:50.737755.p",
"trained_net_online_2020-06-04 05:58:01.968413.p",
"trained_net_online_2020-06-04 05:58:12.732917.p",
"trained_net_online_2020-06-04 05:58:23.241483.p",
"trained_net_online_2020-06-04 05:58:34.465134.p",
"trained_net_online_2020-06-04 05:58:46.220298.p",
"trained_net_online_2020-06-04 06:02:04.722182.p",
"trained_net_online_2020-06-04 06:03:48.693580.p",
"trained_net_online_2020-06-04 06:05:27.264100.p",
"trained_net_online_2020-06-04 06:07:46.915663.p",
"trained_net_online_2020-06-04 06:09:19.857940.p",
"trained_net_online_2020-06-04 06:10:55.425277.p",
"trained_net_online_2020-06-04 06:12:20.362321.p",
"trained_net_online_2020-06-04 06:15:35.796342.p",
"trained_net_online_2020-06-04 06:17:03.794620.p",
"trained_net_online_2020-06-04 06:18:30.289105.p",
"trained_net_online_2020-06-04 06:19:59.773896.p",
"trained_net_online_2020-06-04 06:23:21.489994.p",
"trained_net_online_2020-06-04 06:24:46.555703.p",
"trained_net_online_2020-06-04 06:26:19.178912.p",
"trained_net_online_2020-06-04 06:27:49.825417.p",
"trained_net_online_2020-06-04 06:31:45.624514.p",
"trained_net_online_2020-06-04 06:33:23.485789.p",
"trained_net_online_2020-06-04 06:35:07.723431.p",
"trained_net_online_2020-06-04 06:37:10.435917.p",
"trained_net_online_2020-06-04 06:38:45.568832.p",
"trained_net_online_2020-06-04 06:41:25.683979.p",
"trained_net_online_2020-06-04 06:42:56.153135.p",
"trained_net_online_2020-06-04 06:44:30.220213.p",
"trained_net_online_2020-06-04 06:45:59.110979.p",
"trained_net_online_2020-06-04 06:47:34.735211.p",
"trained_net_online_2020-06-04 06:53:02.887983.p",
"trained_net_online_2020-06-04 06:55:05.771915.p",
"trained_net_online_2020-06-04 06:56:44.391969.p",
"trained_net_online_2020-06-04 06:58:19.725804.p",
"trained_net_online_2020-06-04 07:00:00.665386.p",
"trained_net_online_2020-06-04 07:03:44.840976.p",
"trained_net_online_2020-06-04 07:05:18.159068.p",
"trained_net_online_2020-06-04 07:06:55.435277.p",
"trained_net_online_2020-06-04 07:08:31.633712.p",
"trained_net_online_2020-06-04 07:10:05.224282.p"
]


file = open("trained_net_online_2020-06-04 07:10:05.224282.p", "rb")
#file = open(filename, "rb")
mlp = pickle.load(file)

fig, axes = plt.subplots(2, 1)
# use global min / max to ensure all weights are shown on the same scale
vmin, vmax = mlp.coefs_[2].min(), mlp.coefs_[0].max()
for coef, ax in zip(mlp.coefs_[2].T, axes.ravel()):
    ax.matshow(coef.reshape(4,1), cmap=plt.cm.gray, vmin=.5 * vmin,
            vmax=.5 * vmax)
    ax.set_xticks(())
    ax.set_yticks(())

#plt.show()
plt.savefig("graph_layer_3.png")

"""
# show input layer weights
for filename in filenamesOnline_vs_NetHitPlayer:
    #file = open("trained_net_online_2l020-06-04 06:31:45.624514.p", "rb")
    file = open(filename, "rb")
    mlp = pickle.load(file)

    fig, axes = plt.subplots(3, 3)
    # use global min / max to ensure all weights are shown on the same scale
    vmin, vmax = mlp.coefs_[0].min(), mlp.coefs_[0].max()
    for coef, ax in zip(mlp.coefs_[0].T, axes.ravel()):
        ax.matshow(coef.reshape(28,1), cmap=plt.cm.gray, vmin=.5 * vmin,
                vmax=.5 * vmax)
        ax.set_xticks(())
        ax.set_yticks(())

    #plt.show()
    plt.savefig("graph_"+ filename +".png")
"""

# show first hidden layer weights
for filename in filenamesOnline_vs_NetHitPlayer:
    #file = open("trained_net_online_2l020-06-04 06:31:45.624514.p", "rb")
    file = open(filename, "rb")
    mlp = pickle.load(file)

    fig, axes = plt.subplots(3, 3)
    # use global min / max to ensure all weights are shown on the same scale
    vmin, vmax = mlp.coefs_[0].min(), mlp.coefs_[0].max()
    for coef, ax in zip(mlp.coefs_[1].T, axes.ravel()):
        ax.matshow(coef.reshape(10,1), cmap=plt.cm.gray, vmin=.5 * vmin,
                vmax=.5 * vmax)
        ax.set_xticks(())
        ax.set_yticks(())

    #plt.show()
    plt.savefig("layer_2/graph_"+ filename +"_layer_2.png")
    plt.close()

"""
# show last hidden layer weights
for filename in filenamesOnline_vs_NetHitPlayer:
    #file = open("trained_net_online_2l020-06-04 06:31:45.624514.p", "rb")
    file = open(filename, "rb")
    mlp = pickle.load(file)

    fig, axes = plt.subplots(3, 1)
    # use global min / max to ensure all weights are shown on the same scale
    vmin, vmax = mlp.coefs_[0].min(), mlp.coefs_[0].max()
    for coef, ax in zip(mlp.coefs_[2].T, axes.ravel()):
        ax.matshow(coef.reshape(4,1), cmap=plt.cm.gray, vmin=.5 * vmin,
                vmax=.5 * vmax)
        ax.set_xticks(())
        ax.set_yticks(())

    #plt.show()
    plt.savefig("graph_"+ filename +"_layer_3.png")
"""

# --> 2nd hidden layer: only 2 nodes are constant 1. remove layer!