#
#
# test, how much memory a board plus a float value need
#
#
#
# 
# /usr/bin/time -fpeak_used_memory:%M python3 memory_consumption.py
#
# expectation: 28*4 bytes + 8 bytes + 60 bytes = 120 + 60 = 180 bytes
#
# offsett: 7840 kb ~ 8 mb


#evaluatedBoard =  [[-15,1,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,14,0], 0.33238229]
#evaluatedBoard =  [-15,1,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,14,0]
#evaluatedBoard =  [-15,1,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,14,0, 0.32323123]
#evaluatedBoard =  [-15,1,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,14,0, 32323123]
#evaluatedBoard =  [-15,1,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,14,0, 3]
#evaluatedBoard =  [-15,1,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0]
evaluatedBoard =  [-15,1,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 25]
thousand = 1000

boards = []
for i in range(thousand*thousand*10):
    evaluatedBoard[0] = i
    boards.append(evaluatedBoard.copy())
print(len(boards))
print(boards[5000])

#  1.000.000 boards cost 332824 kb --> 340 byte per eval board
# 10.000.000 boards cost 3261016 kb --> 334 bytes per eval board
# 20.000.000 boards cost 6511712 kb --> difference/10.000.000 --> 333 bytes per board.
#
# 10.000.000 boards with an additional float --> 3538660 kb. difference without float: 277644 --> 28.4 byte per float
# with additional int:    3538676, --> for an int also 30 bytes more??
# again without the int:  3260916 OK
# again with a small int: 3538732 still??
# an int less (just 27 ints):
#                         3260952 j
# just 24 ints (instead of 28): 2943500 --> ((3261016-2943500)*1024)/10000000 = 32,5 byte less --> 8 byte per int
# 25 ints                      --> ((3144152-2943500)*1024)/10000000 = 20 bytes per int more ??
#
# Does an int cost 20 bytes or 8 bytes? 
# Does the python interpreter remember, how much memory it needed for the last run?

