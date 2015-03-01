from numpy.random import random
from bokeh.plotting import *
from bokeh.sampledata import us_counties, us_states, unemployment
from bokeh.models import HoverTool, ColumnDataSource
import pandas as pd
from collections import OrderedDict

populationfile = pd.read_csv("/Users/bvenkatesan/Documents/workspace/PyCharmProjects/capstone/data/statepops.csv")
populations = pd.DataFrame(populationfile, columns=['state','2012pop'])





def mtext(p, x, y, textstr):
    p.text(x, y, text=textstr,
         text_color="#449944", text_align="center", text_font_size="10pt")


def getPopulation(state):

    for i, row in enumerate(populations.values):
        stateName = row[0]
        if(stateName == state):
            population = row[1]

    return population




########################################################################
# Loading accident data by state
# breaking it out into 4 quartiles
########################################################################
datafile = pd.read_csv("/Users/bvenkatesan/Documents/workspace/PyCharmProjects/capstone/data/incidents_state_totals.csv")


accidents = pd.DataFrame(datafile, columns=['code','state', 'totals'])

quartiles = pd.qcut(datafile["totals"],4,labels=[1, 2, 3, 4], precision=1)

########################################################################
# color palate
########################################################################
colormap = {
    '1'         : "#ffffb2",
    '2' : "#fecc5c",
    '3'              : "#fd8d3c",
    '4'                : "#f03b20",
    '0':  "#f7f7f7",
}


def drawFile(removeOutliers, filename):
    state_colors = []
    state_names = []
    pops = []
    fatalities=[]

    p = figure(title="Fatalities Plot")

    ########################################################################
    # looping through the datafile to create state-by-state mapping
    ########################################################################
    for i, row in enumerate(accidents.values):

        try:
            code = row[0]
            state = row[1]
            total = row[2]
            if( removeOutliers and (code == 'CA')):
                print removeOutliers
                print 'remove outlier is true '+ code
                pass
            else:
                print 'remove outlier is false '+ code
                pop = (getPopulation(state)/1000)
                pops.append(pop)
                fatalities.append(total)
                state_colors.append(colormap[str(quartiles[i])])
                state_names.append(state)

            #idx = min(int(rate/2), 5)
            #state_colors.append(colors[idx])
        except KeyError:
            state_colors.append(colormap['0'])



    ########################################################################
    # Creating columndatasource for hover tool
    ########################################################################
    hoverLabels = ColumnDataSource(
        data=dict(
            x=fatalities,
            y=pops,
            state= state_names,
        )
    )

    ########################################################################
    # Loading accident data by state
    ########################################################################
    p = figure(title="Fatalities Total without Outlier", toolbar_location="left", tools="resize,hover,save", plot_width=1100, plot_height=700)

    hover = p.select(dict(type=HoverTool))
    hover.tooltips = OrderedDict([
        ('State: ', '@state'),
        ('Fatalities: ', '@x'),
        ('Population (in 000s): ', '@y')
    ])


    output_file(filename)

    p.scatter(fatalities, pops, marker="circle", line_color="#6666ee", ylabel='fatality', source=hoverLabels,  fill_color=state_colors, fill_alpha=0.5, size=12)

    show(p)  # open a browser

if __name__ == '__main__':
    drawFile(False,'scatter_with_outlier.html')
    drawFile(True,'scatter_without_outlier.html')