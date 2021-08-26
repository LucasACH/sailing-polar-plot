from data import Data
from xml.dom import minidom
import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from numpy import arange,pi,linspace
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)


root = Tk()
root.configure(background='#1C2028', pady=10)
root.wm_iconbitmap('./assets/favicon.ico')
root.title('Polar plot')
root.geometry('700x700')

plt.rcParams.update({
        'lines.linestyle': 'dashed',
        'lines.linewidth': 1,
        'axes.facecolor': '#2C3039',
        'axes.edgecolor': '#484c57be',
        'axes.grid': True,
        'grid.color': '#484c57be',
        'xtick.color': '#F5F5F5',
        'ytick.color': '#F5F5F5',
        'figure.facecolor': '#1C2028',
    })

filename = StringVar()
maxS = StringVar()
maxS.set(0)
avgS = StringVar()
avgS.set(0)

def selectFile():
    filetypes = (
        ('TCX File', '*.tcx'),
        ('All files', '*.*')
    )

    selectedFileName = askopenfilename(filetypes=filetypes)
    filename.set(selectedFileName)
    filenameEntry.insert(tk.END, selectedFileName)

def polarPlot():
    doc = minidom.parse(filename.get())

    lats = doc.getElementsByTagName("LatitudeDegrees")
    longs = doc.getElementsByTagName("LongitudeDegrees")
    vels = doc.getElementsByTagName("ns3:Speed")

    data = Data(
        lats,
        longs, 
        vels,
        float(windDirectionEntry.get()),
        float(maxWindEntry.get()),
        float(minWindEntry.get()),
        float(maxAngleStarboardEntry.get()),
        float(minAngleStarboardEntry.get()),
        float(maxAnglePortEntry.get()),
        float(minAnglePortEntry.get())
    )

    maxS.set(data.maxSpeed())
    avgS.set(data.averageSpeed())

    dataSet = data.mergeDataSets()
    
    ax.clear()

    ax.set_rmax(30)
    ax.grid(True)

    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)

    ax.set_rticks(arange(0, 30, 5)) 
    ax.set_rlabel_position(40/2)

    ax.plot(
        dataSet['theta_avg'],
        dataSet['r_avg'],
        color='#2C3039'
    )

    ax.fill_between(
        dataSet['theta_max'],
        dataSet['r_max'],
        color='#0CE8CE'
    )

    canvas.draw()

fileBarWrapper = tk.Frame(root, bg='#1C2028')
fileBarWrapper.pack()

filenameEntry = tk.Entry(fileBarWrapper, width=60)
filenameEntry.pack(side='left', padx=(0, 10))

button = tk.Button(fileBarWrapper, text='Choose file', command=selectFile)
button.pack(side='left')

optionsWrapper = tk.Frame(root, bg='#1C2028')
optionsWrapper.pack(pady=(20, 0))

windDirectionLabel = tk.Label(optionsWrapper, bg='#1C2028', fg='white', text='Wind direction')
windDirectionLabel.grid(row=0, column=0, padx=(0, 10))
windDirectionEntry = tk.Entry(optionsWrapper, width=5)
windDirectionEntry.grid(row=0, column=1, padx=(0, 20), sticky='w')
windDirectionEntry.insert(tk.END, 45)

maxWindLabel = tk.Label(optionsWrapper, bg='#1C2028', fg='white', text='Max wind')
maxWindLabel.grid(row=0, column=2, padx=(0, 10))
maxWindEntry = tk.Entry(optionsWrapper, width=5)
maxWindEntry.grid(row=0, column=3, padx=(0, 20), sticky='w')
maxWindEntry.insert(tk.END, 30)

maxWindLabel = tk.Label(optionsWrapper, bg='#1C2028', fg='white', text='Min wind')
maxWindLabel.grid(row=0, column=4, padx=(0, 10))
minWindEntry = tk.Entry(optionsWrapper, width=5)
minWindEntry.grid(row=0, column=5, sticky='w')
minWindEntry.insert(tk.END, 0)

maxAngleStarboardLabel = tk.Label(optionsWrapper, bg='#1C2028', fg='white', text='Starboard tack max angle')
maxAngleStarboardLabel.grid(row=1, column=0, columnspan=2, padx=(0, 10), pady=10)
maxAngleStarboardEntry = tk.Entry(optionsWrapper, width=5)
maxAngleStarboardEntry.grid(row=1, column=2, sticky='w')
maxAngleStarboardEntry.insert(tk.END, 145)

minAngleStarboardLabel = tk.Label(optionsWrapper, bg='#1C2028', fg='white', text='Starboard tack min angle')
minAngleStarboardLabel.grid(row=1, column=3, columnspan=2, padx=(0, 10))
minAngleStarboardEntry = tk.Entry(optionsWrapper, width=5)
minAngleStarboardEntry.grid(row=1, column=5, sticky='w')
minAngleStarboardEntry.insert(tk.END, 30)

maxAnglePortLabel = tk.Label(optionsWrapper, bg='#1C2028', fg='white', text='Port tack max angle')
maxAnglePortLabel.grid(row=2, column=0, columnspan=2, padx=(0, 10))
maxAnglePortEntry = tk.Entry(optionsWrapper, width=5)
maxAnglePortEntry.grid(row=2, column=2, sticky='w')
maxAnglePortEntry.insert(tk.END, 330)

minAnglePortLabel = tk.Label(optionsWrapper, bg='#1C2028', fg='white', text='Port tack min angle')
minAnglePortLabel.grid(row=2, column=3, columnspan=2, padx=(0, 10))
minAnglePortEntry = tk.Entry(optionsWrapper, width=5)
minAnglePortEntry.grid(row=2, column=5, sticky='w')
minAnglePortEntry.insert(tk.END, 205)

plotWrapper = tk.Frame(root, bg='#1C2028')
plotWrapper.pack(pady=20)

maxSpeedLabel = tk.Label(plotWrapper, bg='#1C2028', fg='white', text='Max speed (kn):')
maxSpeedLabel.grid(row=0, column=0, sticky='w')
maxSpeed = tk.Label(plotWrapper, bg='#1C2028', fg='white', textvariable=maxS)
maxSpeed.grid(row=0, column=1, sticky='w', padx=(0, 10))

avgSpeedLabel = tk.Label(plotWrapper, bg='#1C2028', fg='white', text='Average speed (kn): ')
avgSpeedLabel.grid(row=0, column=2, sticky='w')
avgSpeed = tk.Label(plotWrapper, bg='#1C2028', fg='white', textvariable=avgS)
avgSpeed.grid(row=0, column=3, sticky='w', padx=(0, 20))

plotButton = tk.Button(plotWrapper, text='Plot', command=polarPlot)
plotButton.grid(row=0, column=4, sticky='w')

fig = Figure(figsize=(1, 1), dpi=100)
ax = fig.add_subplot(projection='polar')

ax.set_rmax(30)
ax.grid(True)

ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)

ax.set_rticks(arange(0, 30, 5)) 
ax.set_rlabel_position(40/2)

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

root.mainloop()
