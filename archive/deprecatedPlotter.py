import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np


def plot_initialize():
	global fig
	global ax
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	global actualHeader
	global actualW0
	global actualW1
	global actualW2
	global actualW3
	global expHeader
	global expW0
	global expW1
	global expW2
	global expW3

	actualHeader = []
	actualW0 = []
	actualW1 = []
	actualW2 = []
	actualW3 = []
	expHeader = []
	expW0 = []
	expW1 = []
	expW2 = []
	expW3 = []

	return fig

def plotter(it, rawActual, expected):

    # Temporary: Plot graph of 20 iterations only for now    
    if(it != 20):
        return
    
    temp_x = np.arange(0,20)
    data_as_list = rawActual.split(b',')
'''
    data_as_list = data_as_list[1]
    # I dont know how read data looks yet but thats how splitting works i think

    xs.append(it)
    actual_header_byte = data_as_list[0]
    actual_w0_bytes = int(data_as_list[1] + data_as_list[2])
    actual_w1_bytes = int(data_as_list[3] + data_as_list[4])
    actual_w2_bytes = int(data_as_list[5] + data_as_list[6])
    actual_w3_bytes = int(data_as_list[7] + data_as_list[8])

    actualW0.append(actual_w0_bytes)
    actualW1.append(actual_w1_bytes)
    actualW2.append(actual_w2_bytes)
    actualW3.append(actual_w3_bytes)

    expW0.append(exp_w0_bytes)
    expW1.append(exp_w1_bytes)
    expW2.append(exp_w2_bytes)
    expW3.append(exp_w3_bytes)
'''
    # Only plotting wheel 0 speed for now
    
    for i in range(20):
        actual_w0_bytes.add(int(rawActual[i]), 16)
        exp_w0_bytes.add(int(expected[i]), 16)


    ax.clear()
    ax.plot(temp_x, actual_w0_bytes, label="Actual Wheel 0 Speed")
    ax.plot(temp_x, exp_w0_bytes, label="Expected Wheel 0 Speed")

    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.ylabel('Speeds')
