__author__ = 'bvenkatesan'

from bokeh.sampledata import us_counties, us_states, unemployment
from bokeh.plotting import *
from bokeh.models import HoverTool, ColumnDataSource
import pandas as pd
import numpy as np
import json
from collections import OrderedDict
import us


########################################################################
# Loading us_states from bokeh sampledata library.
# Removing Alaska & Hawaii for this excercise
########################################################################
us_states = us_states.data.copy()
del us_states["HI"]
del us_states["AK"]

########################################################################
# Loading accident data by state
# breaking it out into 4 quartiles
########################################################################
datafile = pd.read_csv("/Users/bvenkatesan/Documents/workspace/PyCharmProjects/capstone/data/incidents_state_totals.csv")
accidents = pd.DataFrame(datafile, columns=['code','state', 'totals'])
quartiles = pd.qcut(datafile["totals"],4,labels=["low", "moderate", "high", "very high"], precision=1)

########################################################################
# color palate
########################################################################
colormap = {
    'low'         : "#ffffb2",
    'moderate' : "#fecc5c",
    'high'              : "#fd8d3c",
    'very high'                : "#f03b20",
    'none':  "#f7f7f7",
}

print us.STATES

state_colors = []
state_xs = []
state_ys= []
state_names = []
totals = []
risk_factor=[]

########################################################################
# looping through the datafile to create state-by-state mapping
########################################################################
for i, row in enumerate(accidents.values):
    try:
        code = row[0]
        state = row[1]
        total = row[2]
        tabledata =  us_states[code]['name'].upper()
        q = quartiles[i]

        if (state == tabledata):
            state_colors.append(colormap[q])
            lons =  us_states[code]["lons"]
            lats = us_states[code]["lats"]
            state_xs.append(lons)
            state_ys.append(lats)
            state_names.append(state)
            totals.append(total)
            risk_factor.append(q)

        #idx = min(int(rate/2), 5)
        #state_colors.append(colors[idx])
    except KeyError:
        state_colors.append(colormap['none'])

output_file("heatmap.html", title="Fatalities - Heat Map")

########################################################################
# Creating columndatasource for hover tool
########################################################################
source = ColumnDataSource(
    data=dict(
        x=state_xs,
        y=state_ys,
        state= state_names,
        fatalities=totals,
        risk = risk_factor,
    )
)

########################################################################
# Loading accident data by state
########################################################################
p = figure(title="Fatalities Total", toolbar_location="left",tools="resize,hover,save", plot_width=1100, plot_height=700)

hover = p.select(dict(type=HoverTool))
hover.tooltips = OrderedDict([
    ('state: ', '@state'),
    ('fatalities: ', '@fatalities'),
    ('risk factor : ', '@risk')
])

#p.patches(county_xs, county_ys, fill_color=county_colors, fill_alpha=0.7,
#    line_color="white", line_width=0.5)

p.patches(state_xs, state_ys, fill_color=state_colors, fill_alpha=0.7, source=source, line_color="black", line_width=0.7)


show(p)
