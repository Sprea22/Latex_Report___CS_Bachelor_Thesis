import os
import sys 
import pylab 
import pandas as pd
import numpy as np 
import matplotlib.pyplot as pyplot
from PIL import Image
from fpdf import FPDF

# Graphic's different design
pyplot.style.use('ggplot')

# User input that allowed to DISPLAY AND SAVE the graphic otherwise just SAVE it.
choice = input("Do you want to display the graphic?\n 0 = NO \n 1 = YES\n\n")

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# SINGLE INPUT GRAPHICS OVERVIEW #
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def create_single_overview(cols, rows, dest, width, height, listofimages):
    # Setting the images size
    thumbnail_width = width//cols
    thumbnail_height = height//rows
    size = thumbnail_width, thumbnail_height
    new_im = Image.new('RGB', (width, height))
    ims = []
    for p in listofimages:
        im = Image.open(p)
        im.thumbnail(size)
        ims.append(im)
    i = 0
    x = 0
    y = 0
    # Pasting each single picture inside the total overview image
    # using the sizes just calculated.
    for col in range(cols):
        for row in range(rows):
            new_im.paste(ims[i], (x, y))
            i += 1
            y += thumbnail_height
        x += thumbnail_width
        y = 0
    # Saving the current input overview image
    if dest==0:
    	script_dir = os.path.dirname(__file__)
    	results_dir = os.path.join(script_dir, sys.argv[1]+"/")
    	if not os.path.isdir(results_dir):
    		os.makedirs(results_dir)
        new_im.save(results_dir+"/"+sys.argv[1]+"_Graphics_Overview.jpg")
    # Saving the current input overview image that will be used for the total overview pdf
    if dest==1:
    	script_dir = os.path.dirname(__file__)
    	results_dir = os.path.join(script_dir, "Total_Evidences/Single_Inputs")
    	if not os.path.isdir(results_dir):
    		os.makedirs(results_dir)
        new_im.save(results_dir+"/"+sys.argv[1]+"_Overview.jpg")
    # Showing the current input overview image
    if (choice==1 and dest==0):
        new_im.show()
#-------------------------------------------------------------------------------------------

#%%%%%%%%%%%%%%%%%%%%%%
# TRENDLINE EQUATION #
#%%%%%%%%%%%%%%%%%%%%%%
def trendline(x, y, col):
    # Add correlation line
	# calc the trendline
	z = np.polyfit(x, y, 1)
	p = np.poly1d(z)
	pylab.plot(x,p(x), c=col)
	# Display the line equation:
	# print "y=%.6fx+(%.6f)"%(z[0],z[1])
#-------------------------------------------------------------------------------------------

#%%%%%%%%%%%%%%%%%%%%%%%%%
# SAVE GRAPHIC LIKE IMAGE#
#%%%%%%%%%%%%%%%%%%%%%%%%%
def saveFigure(descr):
    script_dir = os.path.dirname(__file__)
    results_dir = os.path.join(script_dir, sys.argv[1]+"/")
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)
    pyplot.savefig(results_dir + sys.argv[1]+descr, format="jpg")
#-------------------------------------------------------------------------------------------

#%%%%%%%%%%%%%%%%%%
# ANALYSIS PART 1 #
#%%%%%%%%%%%%%%%%%%
#-------------------------------------------------------------------------------------------
# Graphic setup about current input with total data from 2005 to 2016
#-------------------------------------------------------------------------------------------

# Reading the total dataset about the current input from 2005 to 2016
series = pd.read_csv("Dataset.csv", usecols=[1,sys.argv[1]])
# Displaying the current plot
series.plot(color="blue", linewidth=1.5)
years = ["2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016"]
x = range(144)
pyplot.xticks(np.arange(min(x), max(x)+1, 12.0), years)
# Setting the graphic's title
pyplot.title(sys.argv[1]+ ": Total graphic from 2005 to 2016")
series2 = pd.read_csv("Dataset.csv", usecols=[sys.argv[1]], squeeze=True)
trendline(x, series2.values, "red")
saveFigure("_Total.jpg")


#%%%%%%%%%%%%%%%%%%
# ANALYSIS PART 2 #
#%%%%%%%%%%%%%%%%%%
#-------------------------------------------------------------------------------------------
# Graphic setup about current input for each year from 2005 to 2016
#-------------------------------------------------------------------------------------------
# Reading the dataset about the current input for each year from 2005 to 2016
series2 = pd.read_csv("Dataset.csv", index_col=['Month'], usecols=[0,1,sys.argv[1]])
# Initialize the graphic's figure
fig2 = pyplot.figure()
ax = fig2.add_subplot(111)

# Set the x axis tick
months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
x_pos = np.arange(len(months))
test = []
j = 0
# Collecting and displaying the correct values: a plot for values of every single year.
for i in range(len(series2.values)):
	if j in range(12):
		test.append(series2.values[i][1])
		j = j + 1
	else:
		pyplot.plot(x_pos, test, linewidth=2, alpha=0.8, label = int(series2.values[i-1][0]))
		test = []
		test.append(series2.values[i][1])
		j = 1

ax.legend(loc=4, ncol=1, fancybox=True, shadow=True)
pyplot.xticks(x_pos,months)
pyplot.xlim(0,11)
pyplot.title(sys.argv[1]+ ": Single year's graphic from 2005 to 2016")
saveFigure("_Years.jpg")

#%%%%%%%%%%%%%%%%%%
# ANALYSIS PART 3 #
#%%%%%%%%%%%%%%%%%%
#-------------------------------------------------------------------------------------------
# Correlation matrix about current input between each year from 2005 to 2016 
#-------------------------------------------------------------------------------------------
# Reading the dataset about the current input between each single year from 2005 to 2016
series3 = pd.read_csv("Dataset.csv", index_col=['Year'], usecols=[0,sys.argv[1]])
corr = []
test = []
j = 0
# Collecting the correct values to elaborate.
for i in range(len(series2.values)+1):
	if j in range(12):
		test.append(series2.values[i][1])
		j = j + 1
	else:
		corr.append(test)
		test = []
		if i in range(144):
			test.append(series2.values[i][1])
			j = 1
# Calculatic che correlation coefficent between each year of the input dataset
test = np.corrcoef(corr)
# Displaying the figure for the current matrix
fig2 = pyplot.figure()
ax = fig2.add_subplot(111)
# Displaying the matrix with the results about correlation coefficents
cax = ax.matshow(test, interpolation='nearest')
# Setting the graphic's title
pyplot.title(sys.argv[1]+ ": Correlation between different years")
# Setting the x and y axis of the matrix
x_pos = np.arange(len(years))
y_pos = np.arange(len(years))
pyplot.yticks(y_pos,years)
pyplot.xticks(x_pos,years)
#cax.set_clim(vmin=0.5, vmax=1)
pyplot.colorbar(cax)
# Saving the current graphic in the right folder
saveFigure("_Years_Matrix.jpg")

#%%%%%%%%%%%%%%%%%%
# ANALYSIS PART 4 #
#%%%%%%%%%%%%%%%%%%
#-------------------------------------------------------------------------------------------
# Correlation matrix about current input between each single month from 2005 to 2016
#-------------------------------------------------------------------------------------------
# Reading the dataset about the current input for each year from 2005 to 2016
series4 = pd.read_csv("Dataset.csv", usecols=[0,1,sys.argv[1]])
# Calculatic che correlation coefficent between each year of the input dataset
corr = []
for Month, Year in series4.groupby(["Month"], sort=False):
	corr.append(Year[sys.argv[1]].values)
corrRes = np.corrcoef(corr)
# Displaying the figure for the current matrix
fig2 = pyplot.figure()
ax = fig2.add_subplot(111)
# Displaying the matrix with the results about correlation coefficents
cax = ax.matshow(corrRes, interpolation='nearest')
# Setting the graphic's title
pyplot.title(sys.argv[1]+ ": Correlation between different months")
# Setting the x and y axis of the matrix
months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
x_pos = np.arange(len(months))
y_pos = np.arange(len(months))
pyplot.yticks(y_pos,months)
pyplot.xticks(x_pos,months)
#cax.set_clim(vmin=0, vmax=1)
pyplot.colorbar(cax)
saveFigure("_Months_Matrix.jpg")
#-------------------------------------------------------------------------------------------

#%%%%%%%%%%%%%%%%%%
# ANALYSIS PART 5 #
#%%%%%%%%%%%%%%%%%%
#-------------------------------------------------------------------------------------------
# Autogenerate the overview image for the current input and update the total overview pdf
#-------------------------------------------------------------------------------------------
# Filling the array with the current input's graphics
listofimages=[sys.argv[1]+"/"+sys.argv[1]+"_Total.jpg",
            sys.argv[1]+"/"+sys.argv[1]+"_Years_Matrix.jpg", 
            sys.argv[1]+"/"+sys.argv[1]+"_Years.jpg",
            sys.argv[1]+"/"+sys.argv[1]+"_Months_Matrix.jpg"]
# Creating current single input overview
create_single_overview(2, 2, 0, 1600, 1200, listofimages)
# Updating the current single input overview used in the total overview pdf
create_single_overview(4, 1, 1, 3200, 600, listofimages)
#-------------------------------------------------------------------------------------------