from plotter import *
from time import sleep

actual = b'\x11\x00\x08\xcf\x0b\xb8\xf7\xf1\xf5\x08\x00\x00'
expected = b'\x11\x00\x04\xbd\xf7\xf6\x83\x04\x01\x00\x00'

graph = Plotter()
print("initialized")
for t in range(60):
    print("SOS")
    graph.update_plot(t, [300, 250, 412, 542], [542, 143, 1232, 200])
    sleep(1)

save = input("Graph plotted. Save to png? (Y/n)\n").upper()

if save == 'Y':
    saveName = input("What would you like to name this file?\n")
    graph.save(saveName)

