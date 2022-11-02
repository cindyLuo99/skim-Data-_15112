# TP: skim(Data)

from cmu_112_graphics import *
from fractions import Fraction
import os

# Define class Variable & Data 
class Variable:
    def __init__(self, oneDList):
        self.list = oneDList
        self.varName = self.list[0]
        self.varValues = self.list[1:]
        self.observations = len(self.varValues)
        if isinstance(self.varName, str):
            self.conditions = set(self.varValues)

    # height = Variable(["height",1,2,3,4,5])
    # print(height) should return "["height",1,2,3,4,5]"
    def __repr__(self):
        if len(self.list) <= 21:
            return f'{self.list}'
        else:
            return str(f'{self.list[:21]}')[:-1] + ", ...]"

    # return the occurrences of certain value within the variable
    def count(self, value):
        total = 0
        for element in self.varValues:
            if element == value:
                total += 1
        return total

    # rename the variable
    def rename(self, newName):
        self.list[0] = newName
        self.varName = newName
        return Variable(self.list)

    # show the value of a given row (ignoring the variable name)
    def selectRow(self, row):
        return self.varValues[row]
        
    # slice (both sides inclusive, will keep the variable name)
    def slice(self, start = 0, end = -1):
        newVar = [self.varName] + self.varValues[start:end]
        newVar.append(self.varValues[end])
        return Variable(newVar)

    # return a 2d list (dataframe), similar to a frequency table
    def table(self):
        output = [["Value", "Frequency"]]
        for condition in self.conditions:
            count = self.count(condition)
            output.append([condition, count])
        return Dataframe(output)

class Dataframe(Variable):
    def __init__(self, twoDList, nameOfDataframe = "NA"):
        super().__init__(twoDList)
        self.variables = twoDList[0]
        self.numberOfVars = len(self.variables) if isinstance(self.variables, list) else 1
        self.title = nameOfDataframe

    # returns the variable selected
    def selectVar(self, varName):
        col = self.varCol(varName)
        if col == None: 
            print(f'{varName} does not exist.')
            pass
        varList = [varName]
        for row in range(self.observations):
            varList.append(self.varValues[row][col])
        return Variable(varList)

    # returns the col number of the variable
    def varCol(self, varName):
        col = None
        for i in range(self.numberOfVars):
            var = self.variables[i]
            if varName == var:
                col = i
        if col == None:
            print(f'{varName} does not exist.')
        return col

    def selectRowCol(self, row, col):
        return self.varValues[row][col]

    # return a new dataframe by merging the two dataframes
    def merge(self, df1, df2):
        if df1.observations != df2.observations:
            raise Exception("Unable to merge since" +
            f'{df1.title} and {df2.title} have different number of observations.')
        else: 
            output = [[]]
            for dataframe in (df1, df2):
                if dataframe.numberOfVars == 1:
                    vars = [dataframe.variables]
                else:
                    vars = dataframe.variables
                output[0].extend(vars)
            for row in range(df1.observations):
                newRow = []
                if df1.numberOfVars == 1:
                    entry1 = [df1.varValues[row]]
                else: 
                    entry1 = df1.varValues[row]
                if df2.numberOfVars == 1:
                    entry2 = [df2.varValues[row]]
                else: 
                    entry2 = df2.varValues[row]
                newRow.extend(entry1 + entry2)
                output.append(newRow)
            return Dataframe(output)

    # returns a list of values of variable var, under certain conditions
    def filter(self, var, conditionVar1, condition1, conditionVar2 = None, condition2 = None):
        values = list()
        varList = self.selectVar(var).list
        cVar1List = self.selectVar(conditionVar1).list
        if conditionVar2 != None: cVar2List = self.selectVar(conditionVar2).list
        for index in range(1,self.observations+1):
            entry1 = cVar1List[index]
            if entry1 == condition1:
                if conditionVar2 != None:
                    entry2 = cVar2List
                    if entry2 == condition2:
                        values.append(varList[index])
                    else: pass
                else:
                    values.append(varList[index])
        return values

# return the standard deviation of the list 
def sd(L):
    average = sum(L)/len(L)
    sumOfSquares = 0
    for value in L:
        sumOfSquares += (value - average)**2
    result = (sumOfSquares/(len(L) - 1))**0.5
    return result

# demo dataset obtained from my iPhone

#########################
# startMode
#########################
def startMode_redrawAll(app, canvas):
    canvas.create_text(300,592,text = "Coming... \nMore Features" , anchor = "nw",
    font = f"Helvetica {int(80/800*app.height)} bold",fill = "grey80")

    # Buttons
    for button in app.buttonChars:
        (x0,y0,x1,y1) = app.buttonChars[button][0]
        color = app.buttonChars[button][1]
        fpDesign = app.buttonChars[button][2]
        (textX,textY) = app.buttonChars[button][3]
        text = app.buttonChars[button][4]
        anchor = app.buttonChars[button][5]
        fontSize = app.buttonChars[button][6]
        angle = app.buttonChars[button][7]
        canvas.create_rectangle(x0,y0,x1,y1,fill='white'if fpDesign else color,width = 0)
        canvas.create_text(textX, textY, text = text,anchor = anchor,
                                        font = f"Helvetica {fontSize} bold", 
                                        fill=color if fpDesign else "white", angle=angle)

    # text instructions
    canvas.create_text(app.width*8/9, app.height*8/9+10,
                       text='skim(Data)', font = "Futura 20 bold",fill='black')
    canvas.create_text(app.width*8/9, app.height*10/11+10,
                       text='Version 1.0', font = "Futura 8",fill='black')
    canvas.create_image(app.width*10/11, app.height/12, image=ImageTk.PhotoImage(app.infoImage))

def startMode_mousePressed(app, event): # (only work for the canvas.size (1200*800))
    if (app.width*10/11 - 20 <= event.x <= app.width*10/11 + 20 and
        app.height/12 - 20 <= event.y <= app.height/12 + 20):
        app.mode = 'infoMode'
    # (849,120,990,143)
    elif 849 <= event.x <= 990 and 120 <= event.y <= 143:
        app.mode = 'importDataMode'
    # (20, 34, 205, 766)
    elif app.dataImported:
        if 20 <= event.x <= 205 and 34 <= event.y <= 766:
            app.mode = 'barGraphMode'
        #(204,20,821,170)
        elif 204 <= event.x <= 821 and 20 <= event.y <= 170:
            app.mode = 'viewTableMode'
        # (204,150,967,254)
        elif 204 <= event.x <= 967 and 150 <= event.y <= 254:
            app.mode = 'analysisMode'
        elif 190 <= event.x <= 305 and 239 <= event.y <= 769:
            app.mode = 'lineGraphMode'
        elif 299 <= event.x <= 778 and 218 <= event.y <= 518:
            app.mode = 'scatterPlotMode'
        elif 740 <= event.x <= 844 and 249 <= event.y <= 647:
            app.mode = 'pieChartPreMode'
    
def startMode_mouseMoved(app, event):
    for button in app.buttonChars:
        (x0,y0,x1,y1) = app.buttonChars[button][0]
        fpDesign = app.buttonChars[button][2]
        fpDesign = True if (x0 <= event.x <= x1 and y0 <= event.y <= y1) else False 
        app.buttonChars[button][2] = True if (x0 <= event.x <= x1 and y0 <= event.y <= y1) else False

# Short-cut command to load demo data from the folder (press 'd' to load demo data)
def startMode_keyPressed(app, event):
    if event.key == "d":
        rawData = readFile("Data File.csv")
        newData = list()
        for line in rawData.splitlines():
            newData.append(line.split(","))
        finalData = turnStringToNum(newData)
        app.dataImported = True
        app.data = finalData
        app.dataframe = Dataframe(finalData, "Data Imported")
        app.rows = len(app.data)
        app.cols = len(app.data[0])

def showLabel(app, canvas):
    canvas.create_text(app.width*8/9, app.height*8/9+10,
                       text='skim(Data)', font = "Futura 20 bold",fill='snow3')
    canvas.create_text(app.width*8/9, app.height*10/11+10,
                       text='Version 1.0', font = "Futura 8",fill='snow3')

def showCrossIcon(app,canvas):
    canvas.create_image(app.width*10/11, app.height/12, image=ImageTk.PhotoImage(app.crossImage))

#######################
# infoMode
#######################
def infoMode_redrawAll(app,canvas):
    # showBoard(app, canvas)
    showLabel(app, canvas)
    projectDescription = """
    skim(Data) is a handy tool that allows users to import a dataset and generate 
    different charts and data visualizations through an interactive dashboard with 
    just a few clicks. Requiring no prior experience with data, skim(Data) is 
    accessible to users with all levels of expertise. Moreover, it is compatible 
    with data with varying levels of complexity. 

    It will quickly provide users with an overview of the data frame. By displaying 
    the potentials correlations between the variables through clear and insightful 
    visualizations, skim(Data) can suggest interesting directions & questions, 
    serving as an easy and flexible tool for anyone who wants to take a look at 
    the dataset. Its embedded analytic feature also produces reliable results for 
    ad-hoc analysis.

    This project is a Term Project for CMU-15112. The required module to run this
    project is cmu_112_graphics.py.
    (Retrieved from https://www.cs.cmu.edu/~112/notes/cmu_112_graphics.py)

    All rights reserved to its developer, Kexin (Cindy) Luo.

    Hope you like my project! :D
    """
    canvas.create_text(app.width*48/100, app.height*35/80,
                    text=projectDescription, font = 'Helvetica 20', fill='black')
    showCrossIcon(app,canvas)
    # imageWidth, imageHeight = app.crossImage.size #(34,34)
    
def infoMode_mousePressed(app, event):
    if (app.width*10/11 - 20 <= event.x <= app.width*10/11 + 20 and
        app.height/12 - 20 <= event.y <= app.height/12 + 20):
        app.mode = 'startMode'
        appStarted(app)
        app.dataImported = True

#############################
# importDataMode
#############################

def importDataMode_redrawAll(app,canvas):
    showLabel(app, canvas)
    showCrossIcon(app,canvas)
    canvas.create_text(app.width*48/100, app.height*3/8,
                text = app.message, font = 'Helvetica 20', fill='black')

def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def turnStringToNum(newData):
    finalData = list()
    for row in range(len(newData)):
        newRow = list()
        for col in range(len(newData[0])):
            entry = newData[row][col]
            if entry.isnumeric():
                entry = int(entry)
            elif "." in entry and entry.replace(".","").isnumeric:
                entry = Fraction(entry)
            newRow.append(entry)
        finalData.append(newRow)
    return finalData

def importDataMode_mousePressed(app, event):
    if (app.width*10/11 - 20 <= event.x <= app.width*10/11 + 20 and
        app.height/12 - 20 <= event.y <= app.height/12 + 20):
        app.mode = 'startMode'
        app.message = 'Click the mouse to select from the options.'
    else:
        app.dataPath = app.getUserInput("Please enter the name of the data file.")
        if app.dataPath in os.listdir("/Users/luokexin/Desktop/CMU 2022 Spring/15112/Term Project/TP3"):
            app.message = "Data Imported. Please return to the main menu."
            rawData = readFile(app.dataPath)
            newData = list()
            for line in rawData.splitlines():
                newData.append(line.split(","))
            finalData = turnStringToNum(newData)
            app.dataImported = True
            app.data = finalData
            app.dataframe = Dataframe(finalData, "Data Imported")
            app.rows = len(app.data)
            app.cols = len(app.data[0])

#############################
# viewTableMode
#############################

def table_getDefaultCellBounds(app, row, col, cellWidth = 60, cellHeight = 15):
    x0 = app.margin + col * cellWidth
    x1 = app.margin + (col+1) * cellWidth
    y0 = app.margin + row * cellHeight
    y1 = app.margin + (row+1) * cellHeight
    return (x0, y0, x1, y1)

def table_pointInGrid(app, x, y):
    return ((app.margin <= x <= app.width-app.margin) and
            (app.margin <= y <= app.height-app.margin))

# getCell() & getCellBounds copied from course Notes
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html

def table_getCell(app, x, y):
    if (not table_pointInGrid(app, x, y)):
        return (-1, -1)
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth  = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    row = int((y - app.margin) / cellHeight)
    col = int((x - app.margin) / cellWidth)
    return (row, col)

def table_getCellBounds(app, row, col):
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    x0 = app.margin + col * cellWidth
    x1 = app.margin + (col+1) * cellWidth
    y0 = app.margin + row * cellHeight
    y1 = app.margin + (row+1) * cellHeight
    return (x0, y0, x1, y1)

def viewTableMode_mousePressed(app, event):
    (row, col) = table_getCell(app, event.x, event.y)
    # select this (row, col) unless it is selected
    if (app.width*10/11 - 20 <= event.x <= app.width*10/11 + 20 and
        app.height/12 - 20 <= event.y <= app.height/12 + 20):
        app.mode = 'startMode'
        appStarted(app)
        app.dataImported = True
    elif (app.selection == (row, col)):
        app.selection = (-1, -1)
    else:
        app.selection = (row, col)

def table_drawEachCell(app, canvas, row, col, x0, y0, x1, y1):
    if (app.selection == (row, col)):
        color = "lightgreen"
    elif row == 0: 
        color = "cornflower blue"
    elif row % 2 == 1:
        color = "light steel blue"
    else:
        color = "white"
    canvas.create_rectangle(x0, y0, x1, y1, fill = color,
    outline = "lightgreen" if (app.selection == (row, col)) else "Slategray3",
    width = min((x1-x0)//7, (y1-y0)//7))

def drawText(app, canvas, row, col, x0, y0, x1, y1):
    entry = str(app.data[row][col])
    fontSize = int(min(y1-y0, x1-x0)) - 5
    textX = x0 + (x1-x0)/2
    textY = y0 + (y1-y0)/2
    # Adjusting the size of the text, with help from Emily
    while True:
        entryID = canvas.create_text(textX, textY,text = entry, 
        font=f"Arial {fontSize} bold" if row == 0 else f"Arial {fontSize}", 
        fill="darkblue")
        tX0, tY0, tX1, tY1 = canvas.bbox(entryID) 
        w = tX1 - tX0
        h = tY1 - tY0
        if w >= x1 - x0 or h >= y1 - y0:
            canvas.delete(entryID)
            fontSize -= 1
            if fontSize <= 5 and row == 0 and (" " in entry):
                entryList = entry.split()
                entry = entryList[0][0] + " " + " ".join(entryList[1:])
        else: break  

def viewTableMode_redrawAll(app, canvas):
    showLabel(app, canvas)
    showCrossIcon(app,canvas)
    for row in range(app.rows):
        for col in range(app.cols):
            (x0, y0, x1, y1) = table_getCellBounds(app, row, col)
            if x1 - x0 <= 60 or y1 - y0 <= 15:
                width = max(x1 - x0, 60)
                height = max(y1 - y0, 15)
                (x0, y0, x1, y1) = table_getDefaultCellBounds(app, row, col, width, height)
            table_drawEachCell(app, canvas, row, col, x0, y0, x1, y1)
            drawText(app, canvas, row, col, x0, y0, x1, y1)

#######################
# barGraphMode - buttons
#######################

def getButtonsUp(app, panel):
    if panel == "X":
        return app.XVarButtonsUp
    elif panel == "Y":
        return app.YVarButtonsUp

def button_pointInGrid(app, x, y, panel):
    buttonsUp = getButtonsUp(app, panel)
    return ((app.buttonsLeft <= x <= app.width-app.buttonSideMargin) and
            (buttonsUp <= y <= buttonsUp+app.buttonHeight*(app.cols//4+1)))

def button_getCell(app, x, y, panel):
    buttonsUp = getButtonsUp(app, panel)
    if (not button_pointInGrid(app, x, y, panel)):
        return (-1, -1)
    row = int((y - buttonsUp) / app.buttonHeight)
    col = int((x - app.buttonsLeft) / app.buttonWidth)
    return (row, col)

def button_getCellBounds(app, row, col, panel):
    buttonsUp = getButtonsUp(app, panel)
    x0 = app.buttonsLeft + col * app.buttonWidth
    x1 = app.buttonsLeft + (col+1) * app.buttonWidth
    y0 = buttonsUp + row * app.buttonHeight
    y1 = buttonsUp + (row+1) * app.buttonHeight
    return (x0, y0, x1, y1)

def button_mousePressed(app, mouseX, mouseY):
    x0, y0, x1, y1 = app.generateButton
    rx0, ry0, rx1, ry1 =  app.resetButton
    # select this (row, col) unless it is selected
    if (app.width*10/11 - 20 <= mouseX <= app.width*10/11 + 20 and
        app.height/12 - 20 <= mouseY <= app.height/12 + 20):
        app.mode = 'startMode'
        appStarted(app)
        app.dataImported = True
    elif  app.XVarButtonsUp <= mouseY < app.YVarButtonsUp:
        (row, col) = button_getCell(app, mouseX, mouseY,"X")
        if app.mode == "barGraphMode" or app.mode == "scatterPlotMode" or app.mode == "analysisMode":
            if (app.xButtonSelection == (row, col) or (app.yButtonSelection != None and
            (row, col) == app.yButtonSelection)):
                app.xButtonSelection = (-1, -1)
                app.xAxis = None
                if app.mode == "analysisMode": app.yAxis = None
            else:
                if 0 <= row*4+col < app.cols:
                    varX = app.dataframe.variables[row*4+col]
                    if ((app.mode == "barGraphMode" and isinstance(app.dataframe.selectVar(varX).varValues[0],str)) 
                    or ((app.mode == "scatterPlotMode" or app.mode == "analysisMode") and 
                    not isinstance(app.dataframe.selectVar(varX).varValues[0],str))):
                        app.xButtonSelection = (row, col)
                        app.xAxis = varX
                        if app.mode == "analysisMode": app.yAxis = varX
        elif app.mode == "lineGraphMode":
            if (app.xButtonSelection == (row, col) or (app.yButtonSelectionsForLine != list() and
            (row, col) in app.yButtonSelectionsForLine)):
                app.xButtonSelection = (-1, -1)
                app.xAxis = None
            else:
                if 0 <= row*4+col < app.cols:
                    varX = app.dataframe.variables[row*4+col]
                    if  (isinstance(app.dataframe.selectVar(varX).varValues[0],str)
                    and len(app.dataframe.selectVar(varX).conditions) > 1):
                        app.xButtonSelection = (row, col)
                        app.xAxis = varX
    elif app.YVarButtonsUp < mouseY < app.height*3/7+15: # needs modification
        (row, col) = button_getCell(app, mouseX, mouseY,"Y")
        if app.mode == "barGraphMode" or app.mode == "scatterPlotMode":
            if (app.yButtonSelection == (row, col) or (app.xButtonSelection != None and
                (row, col) == app.xButtonSelection)):
                app.yButtonSelection = (-1, -1)
                app.yAxis = None
            else:
                if 0 <= row*4+col < app.cols:
                    varY = app.dataframe.variables[row*4+col]
                    if not isinstance(app.dataframe.selectVar(varY).varValues[0],str):
                        app.yButtonSelection = (row, col)
                        app.yAxis = varY
        elif app.mode == "lineGraphMode" or app.mode == "pieChartMode" or app.mode == "analysisMode":
            if (row, col) in app.yButtonSelectionsForLine:
                app.yButtonSelectionsForLine.remove((row,col))
                if app.mode == "pieChartMode":
                    app.pieChartVars.remove(app.dataframe.variables[row*4+col])
                else:
                    app.lineGraphVars.remove(app.dataframe.variables[row*4+col])
            elif (app.xButtonSelection != None and (row, col) == app.xButtonSelection):
                pass
            else:
                if 0 <= row*4+col < app.cols:
                    varY = app.dataframe.variables[row*4+col]
                    if ((app.mode == "lineGraphMode" or app.mode == "analysisMode")
                    and (not isinstance(app.dataframe.selectVar(varY).varValues[0],str))):
                        app.yButtonSelectionsForLine.append((row, col))
                        app.lineGraphVars.append(varY)
                    elif app.mode == "pieChartMode" and isinstance(app.dataframe.selectVar(varY).varValues[0],int): 
                        app.yButtonSelectionsForLine.append((row, col))
                        # can only add data of the same type to the pie chart (e.g. all numbers/integers)
                        app.pieChartVars.append(varY)
            app.analysisVars = app.lineGraphVars
    elif abs(mouseX - (app.buttonsLeft+160)) <= 25 and abs(mouseY - (app.height*3/7 + 31)) <= 15:
        if app.mode != "analysisMode":
            app.dataLabelSelectionY = not app.dataLabelSelectionY
            app.showDataLabel = True
            if app.dataLabelSelectionN:
                app.dataLabelSelectionN = False
    elif abs(mouseX - (app.buttonsLeft+210)) <= 25 and abs(mouseY - (app.height*3/7 + 31)) <= 15:
        if app.mode != "analysisMode":
            app.dataLabelSelectionN = not app.dataLabelSelectionN
            app.showDataLabel = False
            if app.dataLabelSelectionY:
                app.dataLabelSelectionY = False
    elif abs(mouseX - (app.buttonsLeft+160)) <= 25 and abs(mouseY - (app.height*3/7 + 76)) <= 15:
        if app.mode == "barGraphMode":
            app.errorBarSelectionY = not app.errorBarSelectionY
            app.showErrorBar = True
            if app.errorBarSelectionN:
                app.errorBarSelectionN = False
    elif abs(mouseX - (app.buttonsLeft+210)) <= 25 and abs(mouseY - (app.height*3/7 + 76)) <= 15:
        if app.mode == "barGraphMode":
            app.errorBarSelectionN = not app.errorBarSelectionN
            app.showErrorBar = False
            if app.errorBarSelectionY:
                app.errorBarSelectionY = False
    elif x0 <= mouseX <= x1 and y0 <= mouseY <= y1:
        app.clickGenerate = True
        if app.mode == "barGraphMode":
            app.displayBarGraph = True
        elif app.mode == "lineGraphMode":
            app.displayLineGraph = True
        elif app.mode == "scatterPlotMode":
            app.displayScatterPlot = True
        elif app.mode == "pieChartMode":
            app.displayPieChart = True
        elif app.mode == "analysisMode":
            app.displayAnalysis = True
    elif rx0 <= mouseX <= rx1 and ry0 <= mouseY <= ry1:
        app.clickReset = True
        app.xButtonSelection = (-1,-1)
        app.yButtonSelection = (-1,-1)
        app.dataLabelSelectionY = False
        app.dataLabelSelectionN = False
        app.clickGenerate = False
        app.showDataLabel = None
        if app.mode == "barGraphMode":
            app.errorBarSelectionY = None
            app.errorBarSelectionN = None
            app.showErrorBar = None
            app.displayBarGraph = False
        if app.mode == "lineGraphMode":
            app.yButtonSelectionsForLine = list()
            app.lineGraphVars = list()
            app.displayLineGraph = False
        if app.mode == "scatterPlotMode":
            app.displayScatterPlot = False
        elif app.mode == "pieChartMode":
            app.displayPieChart = False
            app.yButtonSelectionsForLine = list()
            app.pieChartVars = list()
        elif app.mode == "analysisMode":
            app.displayAnalysis = False
            app.yButtonSelectionsForLine = list()
            app.analysisVars = list()

def barGraphMode_mousePressed(app, event):
    button_mousePressed(app, event.x, event.y)

def button_mouseReleased(app, mouseX, mouseY):
    x0, y0, x1, y1 = app.generateButton
    rx0, ry0, rx1, ry1 = app.resetButton
    if x0 <= mouseX <= x1 and y0 <= mouseY <= y1:
        app.clickGenerate = False
    elif rx0 <= mouseX <= rx1 and ry0 <= mouseY <= ry1:
        app.clickReset = False

def barGraphMode_mouseReleased(app, event):
    button_mouseReleased(app, event.x, event.y)

def button_mouseMoved(app, mouseX, mouseY):
    if  app.XVarButtonsUp <= mouseY < app.YVarButtonsUp:
        (row, col) = button_getCell(app, mouseX, mouseY,"X")
        app.onXButton = (row, col)
        app.onYButton = None
    elif app.YVarButtonsUp <= mouseY < app.height*3/5: # needs modification
        (row, col) = button_getCell(app, mouseX, mouseY,"Y")
        app.onYButton = (row, col)
        app.onXButton = None
    else:
        app.onYButton = None
        app.onXButton = None

def barGraphMode_mouseMoved(app, event):
    button_mouseMoved(app, event.x, event.y)
    
def button_drawEachCell(app, canvas, row, col, x0, y0, x1, y1,panel):
    if app.mode == "barGraphMode" or app.mode == 'scatterPlotMode':
        if panel == "X" and app.xButtonSelection == (row, col):
            color = "CadetBlue1"
        elif panel == "Y" and app.yButtonSelection == (row, col):
            color = "CadetBlue1"
        elif panel == "X" and app.onXButton == (row, col): 
            color = "grey85"
        elif panel == "Y" and app.onYButton == (row, col):
            color = "grey85"
        else: color = "white"
    elif app.mode == "lineGraphMode" or app.mode == 'pieChartMode' or app.mode == 'analysisMode':
        if panel == "X" and app.xButtonSelection == (row, col):
            color = "CadetBlue1"
        elif panel == "Y" and (row, col) in app.yButtonSelectionsForLine:
            color = "CadetBlue1"
        elif panel == "X" and app.onXButton == (row, col): 
            color = "grey85"
        elif panel == "Y" and app.onYButton == (row, col):
            color = "grey85"
        else: color = "white"
    canvas.create_rectangle(x0, y0, x1, y1, fill = color,outline = color,
    width = 3)

def button_drawText(app, canvas, row, col, x0, y0):
    entry = app.dataframe.variables[row*4+col]
    canvas.create_text(x0, y0,text = entry, anchor = "nw",
        font=f"Helvetica 14", 
        fill="black")

def drawInteractiveBoard(app, canvas, panel):
    for row in range(app.cols//4+1):
        for col in range(4):
            if 0 <= row*4+col < app.cols:
                (x0, y0, x1, y1) = button_getCellBounds(app, row, col,panel)
                button_drawEachCell(app, canvas, row, col, x0, y0, x1, y1,panel)
                button_drawText(app, canvas, row, col, x0, y0)

def drawOptions(app, canvas):
    if app.mode != "pieChartMode":
        canvas.create_text(app.buttonsLeft,app.XVarButtonsUp-3,
        text = "X Variable(s):" if app.mode != "analysisMode" else "Dependent Variable:", anchor = "sw",
            font=f"Helvetica 15 bold", 
            fill="black")
    canvas.create_text(app.buttonsLeft,app.YVarButtonsUp-3,
    text = "Y Variable(s):" if app.mode != "analysisMode" else "Independent Variable(s):", anchor = "sw",
        font=f"Helvetica 15 bold", 
        fill="black")
    if app.mode != "analysisMode":
        canvas.create_text(app.buttonsLeft,app.height*3/7 + 40,text = "Add Data Label:", anchor = "sw",
        font=f"Helvetica 15 bold", 
        fill="black")
    if app.mode == "barGraphMode":
        canvas.create_text(app.buttonsLeft,app.height*3/7 + 85,text = "Add Error Bar:", anchor = "sw",
            font=f"Helvetica 15 bold", 
            fill="black")

def drawDataLabelYesOrNo(app,canvas, x, y):
    canvas.create_rectangle(x-25,y-15,x+25,y+15,fill="CadetBlue1" if app.dataLabelSelectionY else"white",width = 0)
    canvas.create_rectangle(x+25,y-15,x+75, y+15,fill="CadetBlue1" if app.dataLabelSelectionN else"white",width = 0)
    canvas.create_text(x,y,text = "Yes",font=f"Helvetica 15 bold", fill="grey37")
    canvas.create_text(x+50,y,text = "No", font=f"Helvetica 15 bold", fill="grey37")

def drawErrorBarYesOrNo(app,canvas, x, y):
    canvas.create_rectangle(x-25,y-15,x+25,y+15,fill="CadetBlue1" if app.errorBarSelectionY else"white",width = 0)
    canvas.create_rectangle(x+25,y-15,x+75, y+15,fill="CadetBlue1" if app.errorBarSelectionN else"white",width = 0)
    canvas.create_text(x,y,text = "Yes",font=f"Helvetica 15 bold", fill="grey37")
    canvas.create_text(x+50,y,text = "No", font=f"Helvetica 15 bold", fill="grey37")

def drawGenerate(app, canvas):
    x0, y0, x1, y1 = app.generateButton
    if app.clickGenerate:
        canvas.create_rectangle(x0-2,y0-2,x1+2,y1+2,fill="cornflower blue",width = 6,outline = "cornflower blue")
    canvas.create_rectangle(x0,y0,x1,y1,fill="LightBlue1" if app.clickGenerate else "white",width = 4, outline = "CadetBlue1")
    canvas.create_text(app.width*11/14,app.height*13/20,text = "GENERATE",font=f"Helvetica 20 bold", fill="grey37")

def drawReset(app, canvas):
    x0, y0, x1, y1 = app.resetButton
    if app.clickReset:
        canvas.create_rectangle(x0-2,y0-2,x1+2,y1+2,fill="cornflower blue",width = 6,outline = "cornflower blue")
    canvas.create_rectangle(x0,y0,x1,y1,fill="LightBlue1" if app.clickReset else "white",width = 4, outline = "CadetBlue1")
    canvas.create_text(app.width*11/14,app.height*15/20,text = "RESET",font=f"Helvetica 20 bold", fill="grey37")

#############################
# barGraphMode
#############################
def barGraphMode_redrawAll(app, canvas):
    showLabel(app, canvas)
    showCrossIcon(app,canvas)
    drawInteractiveBoard(app, canvas, "X")
    drawInteractiveBoard(app, canvas, "Y")
    drawOptions(app, canvas)
    drawDataLabelYesOrNo(app, canvas, app.buttonsLeft + 160, app.height*3/7+31)
    drawErrorBarYesOrNo(app, canvas, app.buttonsLeft + 160, app.height*3/7+76)
    drawGenerate(app, canvas)
    drawReset(app, canvas)
    if app.displayBarGraph:
        barGraphMode_drawSimpleBarChart(app, canvas)
    
def barGraphMode_drawSimpleBarChart(app, canvas):
    if None not in (app.xAxis,app.yAxis):
        graphMode_drawAxes(app, canvas)
        graphMode_drawAxisTitles(app, canvas)
        graphMode_drawXAxisGridlinesAndLabel(app, canvas)
        graphMode_drawYAxisGridlinesAndLabel(app, canvas)
        graphMode_drawBars(app, canvas)
        if app.showDataLabel:
            graphMode_drawDataLabels(app, canvas)
        if app.showErrorBar:
            graphMode_drawErrorBars(app, canvas)
    
def graphMode_drawAxes(app, canvas):
    # x-axis
    canvas.create_line( app.xAxisStart, app.yAxisEnd, 
                    app.xAxisEnd, app.yAxisEnd, fill='black')
    # y-axis
    canvas.create_line(app.xAxisStart, app.yAxisStart, 
                    app.xAxisStart, app.yAxisEnd, fill='black')         

def graphMode_drawAxisTitles(app, canvas):
    # x-axis
    canvas.create_text((app.xAxisEnd - app.xAxisStart)/2+app.xAxisStart, 
    app.height*3/4,text = app.xAxis,font = "Calibri 14 bold", fill='black')
    # y-axis
    canvas.create_text(app.xAxisStart/2, (app.yAxisEnd - app.yAxisStart)/2+app.yAxisStart, 
    text = app.yAxis,font = "Calibri 14 bold", fill='black', angle=90)

# returns the nearest value that is "good" for the grid (multiples of 10)
def nearestGoodValue(n):
    newN = n * 1.2
    i = 0
    if newN <= 100:
        while newN > 0 and newN % 100 != 0:
            newN *= 10
            i += 1
        newN = int(newN)
        axisMax = newN/10**i
    else:
        newN = int(newN)
        if newN % 100 != 0:
            axisMax = newN + 10 - newN%10
        else: axisMax = newN
    return axisMax

# returns the new list that sorts the days by the order they are in a week
def sortedDoW(list):
    dayOfWeek = {"Sunday":0, "Monday":1, "Tuesday":2,"Wednesday":3,"Thursday":4,
                "Friday":5, "Saturday":6}
    newList = [None]*7
    for day in list:
        index = dayOfWeek[day]
        newList[index] = day
    while None in newList:
        newList.remove(None)
    return newList

# returns the new list that sorts the date
def sortedDate(L):
    d = dict()
    l = list()
    for element in L:
        month = element.split("/")[0]
        while len(month) < 2:
            month = "0" + month
        day = element.split("/")[1]
        while len(day) < 2:
            day = "0" + day
        year = element.split("/")[2]
        formattedDate = year + month + day
        l.append(formattedDate)
        d[formattedDate] = element
    sortedl = sorted(l)
    newList = list()
    for date in sortedl:
        newList.append(d[date])
    return newList

# returns the sorted list of conditions of the x-axis variable
def getXAxisVariables(app):
    if app.xAxis == "Day of the Week":
        return sortedDoW(list(app.dataframe.selectVar(app.xAxis).conditions))
    elif app.xAxis == "Date":
        return sortedDate(list(app.dataframe.selectVar(app.xAxis).conditions))
    else:
        return sorted(app.dataframe.selectVar(app.xAxis).conditions)

# returns the "good" value of the variable to determine the grid range
def getGridRange(dataframe, variable):
    varMax = nearestGoodValue(max(dataframe.selectVar(variable).varValues))
    return varMax

def graphMode_drawXAxisGridlinesAndLabel(app, canvas):
    L = getXAxisVariables(app)
    if app.mode == 'barGraphMode' or app.mode == 'lineGraphMode':
        gridX = app.graphSize/len(L)
        for i in range(len(L)+1):
            x = app.xAxisStart + i*gridX
            canvas.create_line(x, app.yAxisEnd, x, app.yAxisEnd + 3, fill='black')
            if i < len(L):
                textX = app.xAxisStart + gridX/2 + i*gridX
                canvas.create_text(textX, app.yAxisEnd + 8 if len(L) <= 10 else app.yAxisEnd + 22, text = L[i],
                font = "Calibri 12", fill='black',angle = 0 if len(L) <= 10 else 60)
    
    elif app.mode == 'scatterPlotMode':
        xValues = app.dataframe.selectVar(app.xAxis).varValues
        xMax = nearestGoodValue(max(xValues))
        gridX = app.graphSize/4
        for i in range(5):
            x = app.xAxisStart + i*gridX
            canvas.create_line(x, app.yAxisEnd, x, app.yAxisEnd + 3, fill='black')
            xTextLabel = str(round(xMax*i/4,1 if xMax > 1 else 2))
            canvas.create_text(x, app.yAxisEnd + 8, text = xTextLabel ,
            font = "Calibri 12", fill='black')

def graphMode_drawYAxisGridlinesAndLabel(app, canvas):
        if app.mode == 'barGraphMode'or app.mode =='scatterPlotMode':
            yValues = app.dataframe.selectVar(app.yAxis).varValues
            yMax = nearestGoodValue(max(yValues))
        elif app.mode == 'lineGraphMode':
            yMax = getLineYGridMax(app,app.lineGraphVars)
        gridY = app.height/2/4
        for i in range(5):
            y = app.yAxisStart + i*gridY
            canvas.create_line(app.xAxisStart, y,app.xAxisStart - 3, y,fill='black')
            yTextLabel = str(round(yMax - yMax*i/4,2))
            canvas.create_text(app.xAxisStart - 20, y, text = yTextLabel ,
            font = "Calibri 12", fill='black')

def graphMode_drawBars(app, canvas):
    L = getXAxisVariables(app)
    grid =  app.graphSize/len(L)
    barWidth = grid/2
    yMax = getGridRange(app.dataframe, app.yAxis)
    for i in range(len(L)):
        x0, x1 = app.xAxisStart + i*grid + grid/4,  app.xAxisStart + i*grid + grid/4 + barWidth
        barValues = app.dataframe.filter(app.yAxis, app.xAxis, L[i])
        average = round(sum(barValues)/len(barValues),1 if sum(barValues)/len(barValues) > 1 else 2)
        barHeight = average/yMax*(app.height/2)
        y0, y1 = app.yAxisEnd - barHeight, app.yAxisEnd 
        colorIndex = randomizedColor(app, i) 
        canvas.create_rectangle(x0,y0,x1,y1,fill=app.colors[colorIndex], width = 0)

def graphMode_drawErrorBars(app, canvas):
    L = getXAxisVariables(app)
    grid = app.graphSize/len(L)
    yMax = getGridRange(app.dataframe, app.yAxis)
    for i in range(len(L)):
        errorX = app.xAxisStart + grid/2 + i*grid
        barValues = app.dataframe.filter(app.yAxis, app.xAxis, L[i])
        if len(barValues) == 1: return
        else:
            average = round(sum(barValues)/len(barValues),1 if sum(barValues)/len(barValues) > 1 else 2)
            errorBarValues = sd(barValues)/(len(barValues)**0.5)
            barHeight = average/yMax*(app.height/2)
            errorBarHeight = errorBarValues/yMax*app.graphSize
            errorY0, errorY1 = (app.yAxisEnd - barHeight - errorBarHeight/2,
            app.yAxisEnd - barHeight + errorBarHeight/2)
            canvas.create_line(errorX, errorY0, errorX,errorY1,fill='black')
            canvas.create_line(errorX-3, errorY0, errorX+3,errorY0,fill='black')
            canvas.create_line(errorX-3, errorY1, errorX+3,errorY1,fill='black')

def graphMode_drawDataLabels(app, canvas):
    L = getXAxisVariables(app)
    grid = app.graphSize/len(L)
    yMax = getGridRange(app.dataframe, app.yAxis)
    for i in range(len(L)):
        textX = app.xAxisStart + grid/2 + i*grid
        barValues = app.dataframe.filter(app.yAxis, app.xAxis, L[i])
        average = round(sum(barValues)/len(barValues),1 if sum(barValues)/len(barValues) > 1 else 2)
        barHeight = average/yMax*(app.height/2)
        textY = app.yAxisEnd - barHeight - 10
        canvas.create_text(textX, textY, text = str(float(average) if isinstance(average,Fraction) else average),
            font = "Calibri 12", fill='black')

#######################
# lineGraphButtons
#######################

def lineGraphMode_mousePressed(app, event):
    button_mousePressed(app, event.x, event.y)
    
def lineGraphMode_mouseReleased(app, event):
    button_mouseReleased(app, event.x, event.y)

def lineGraphMode_mouseMoved(app, event):
    button_mouseMoved(app, event.x, event.y)

#############################
# lineGraphMode
#############################

def lineGraphMode_redrawAll(app, canvas):
    showLabel(app, canvas)
    showCrossIcon(app,canvas)
    drawInteractiveBoard(app, canvas, "X")
    drawInteractiveBoard(app, canvas, "Y")
    drawOptions(app, canvas)
    drawDataLabelYesOrNo(app, canvas, app.buttonsLeft + 160, app.height*3/7+31)
    drawGenerate(app, canvas)
    drawReset(app, canvas)
    if app.displayLineGraph:
        lineGraphMode_drawLineChart(app, canvas)

def lineGraphMode_drawLineChart(app, canvas):
    if app.lineGraphVars != list() and app.xAxis != None:
        graphMode_drawAxes(app, canvas)
        graphMode_drawAxisTitles(app, canvas)
        graphMode_drawLines(app, canvas)
        graphMode_drawXAxisGridlinesAndLabel(app, canvas)
        graphMode_drawYAxisGridlinesAndLabel(app, canvas)

def getLineEnds(app,grid, gridMax,L, listOfVars, varIndex,i,side):
    if side == "right": i = i+1
    x = app.xAxisStart + grid/2 + i*grid
    values = app.dataframe.filter(listOfVars[varIndex], app.xAxis, L[i])
    average = round(sum(values)/len(values),1)
    height = average/gridMax*(app.height/2)
    y = app.yAxisEnd - height
    return x, y, average

def getLineYGridMax(app,listOfVars):
    gridMax = None
    for varIndex in range(len(listOfVars)):
        variable = listOfVars[varIndex]
        varMax = getGridRange(app.dataframe, variable)
        if gridMax == None or varMax >= gridMax:
            gridMax = varMax
        else: pass
    return gridMax

def graphMode_drawLines(app, canvas):
    L = getXAxisVariables(app)
    grid = app.graphSize/len(L)
    listOfVars = app.lineGraphVars
    gridMax = getLineYGridMax(app,listOfVars)
    for varIndex in range(len(listOfVars)):
        for i in range(len(L) - 1):
            leftEndX, leftEndY,leftAverage = getLineEnds(app,grid, gridMax,L, 
                                                listOfVars, varIndex,i,"left")
            rightEndX, rightEndY,rightAverage = getLineEnds(app,grid, gridMax,L, 
                                                listOfVars, varIndex,i,"right")
            colorIndex = randomizedColor(app, (varIndex + 5)) 
            if app.showDataLabel:
                canvas.create_text(leftEndX, leftEndY, 
                text =  str(float(leftAverage) if isinstance(leftAverage,Fraction) else leftAverage),
                fill=app.colors[colorIndex])
                canvas.create_text(rightEndX, rightEndY, 
                text =  str(float(rightAverage) if isinstance(rightAverage, Fraction) else rightAverage),
                fill=app.colors[colorIndex])
            canvas.create_line(leftEndX, leftEndY, rightEndX, rightEndY,fill=app.colors[colorIndex])
            # draw legend
        margin = app.xAxisStart
        textX = margin + (varIndex % 5)* app.width*3/30
        textY = app.height*4/5 + (varIndex//5)*25
        canvas.create_text(textX, textY, text = listOfVars[varIndex],anchor = "w",fill="black")
        canvas.create_rectangle(textX-12, 
                        textY-5, textX-2,textY+5,fill=app.colors[colorIndex],width = 0)

#############################
# scatterPlotButtons
#############################

def scatterPlotMode_mousePressed(app, event):
    button_mousePressed(app, event.x, event.y)
    
def scatterPlotMode_mouseReleased(app, event):
    button_mouseReleased(app, event.x, event.y)

def scatterPlotMode_mouseMoved(app, event):
    button_mouseMoved(app, event.x, event.y)
    
#############################
# scatterPlotMode
#############################

def scatterPlotMode_redrawAll(app, canvas):
    showLabel(app, canvas)
    showCrossIcon(app,canvas)
    drawInteractiveBoard(app, canvas, "X")
    drawInteractiveBoard(app, canvas, "Y")
    drawOptions(app, canvas)
    drawDataLabelYesOrNo(app, canvas, app.buttonsLeft + 160, app.height*3/7+31)
    drawGenerate(app, canvas)
    drawReset(app, canvas)
    if app.displayScatterPlot:
        scatterPlotMode_drawScatterPlot(app, canvas)

def scatterPlotMode_drawScatterPlot(app, canvas):
    if None not in (app.xAxis, app.yAxis):
        graphMode_drawAxes(app, canvas)
        graphMode_drawAxisTitles(app, canvas)
        graphMode_drawXAxisGridlinesAndLabel(app, canvas)
        graphMode_drawYAxisGridlinesAndLabel(app, canvas)
        graphMode_drawDots(app, canvas)

# returns ((xCoord,yCoord),(xValue,yValue))
def getDotCoordsAndVals(app,xGridMax, yGridMax,index):
    xValue = app.dataframe.selectVar(app.xAxis).varValues[index]
    yValue = app.dataframe.selectVar(app.yAxis).varValues[index]
    xCoord = xValue/xGridMax*app.graphSize + app.xAxisStart
    yCoord = app.yAxisEnd - yValue/yGridMax*(app.height/2)
    return ((xCoord,yCoord),(xValue,yValue))

def graphMode_drawDots(app, canvas):
    yValues = app.dataframe.selectVar(app.yAxis).varValues
    yGridMax = nearestGoodValue(max(yValues))
    xValues = app.dataframe.selectVar(app.xAxis).varValues
    xGridMax = nearestGoodValue(max(xValues))
    for i in range(len(xValues)):
        colorIndex = randomizedColor(app, (i + 10086))
        (xCoord,yCoord) = getDotCoordsAndVals(app,xGridMax, yGridMax,i)[0]
        (xValue,yValue) = getDotCoordsAndVals(app,xGridMax, yGridMax,i)[1]
        # if isinstance(yValue, Fraction): yValue = float(yValue)
        canvas.create_oval(xCoord-app.dotR, yCoord-app.dotR,
                           xCoord+app.dotR, yCoord+app.dotR,
                           fill=app.colors[colorIndex], width = 0)
        if app.showDataLabel:
            if isinstance(xValue,Fraction): xValue = float(xValue)
            elif isinstance(yValue,Fraction): yValue = float(yValue)
            canvas.create_text(xCoord, yCoord - 16, anchor = "s",
                        text = f'{xValue,yValue}',font = "Calibri 10",fill="grey40")
    
#############################
# pieChartButtons
############################

def pieChartPreMode_redrawAll(app,canvas):
    showLabel(app, canvas)
    font = 'Arial 15 bold'
    canvas.create_text(app.width/2,  app.height/2,
                       text=app.message, font=font, fill='black')
    showCrossIcon(app,canvas)

def pieChartPreMode_mousePressed(app, event):
    if (app.width*10/11 - 20 <= event.x <= app.width*10/11 + 20 and
        app.height/12 - 20 <= event.y <= app.height/12 + 20):
        app.mode = 'startMode'
        appStarted(app)
        app.dataImported = True
    else:
        app.xAxis = "Date" # should be adjustable to the data, hardcoded here for demo purpose
        L = getXAxisVariables(app)
        app.message = f"Select a date from {L[0]} to {L[-1]}"
        dateChosen = app.getUserInput(f'Enter the date you want to look at. Select a date from {L[0]} to {L[-1]}')
        app.pieChartDateChosen = dateChosen
        if dateChosen not in app.dataframe.selectVar("Date").list:
            app.message = f'{dateChosen} is out of range. Click to re-enter.'
        else: app.mode = 'pieChartMode'

#############################
# pieChartMode
#############################

# returns a sorted list of value and a sorted var names
def getPieData(app):
    dataForPieChart = dict()
    for var in app.pieChartVars:
        cellValue = app.dataframe.filter(var, app.xAxis, app.pieChartDateChosen)[0]
        dataForPieChart[cellValue] = var
    valuesForPieChart = sorted(dataForPieChart)[::-1]
    varNamesForPieChart = list()
    for value in valuesForPieChart:
        varNamesForPieChart.append(dataForPieChart[value])
    return (valuesForPieChart,varNamesForPieChart)

def distance(x0,y0,x1,y1):
    return ((x0-x1)**2+(y0-y1)**2)**(0.5)

def getArcIndex(app,x,y,listOfValues):
    import math
    if distance(x,y,app.centerX,app.centerY) > app.radius + 3:
        return None
    else:
        rX, rY = x - app.centerX, y - app.centerY
        degree = -math.atan2(rY,rX)*180/math.pi
        if degree > 90: degree -= 360
        for index in range(len(listOfValues)-1):
            start1 = getArcBound(index,listOfValues)[0]
            start2 = getArcBound(index+1,listOfValues)[0]
            if start2 <= degree <= start1:
                return index
        return len(listOfValues) - 1

# given the index, returns the start and the extend of the arc
def getArcBound(index,listOfValues):
    total = sum(listOfValues)
    if total != 0:
        extent = - listOfValues[index]/total*360
        start = 90 - sum(listOfValues[:index])/total*360
        return start, extent

def pieChartMode_mousePressed(app, event):
    button_mousePressed(app, event.x, event.y)
    if app.displayPieChart and (app.xAxis != None and len(app.pieChartVars) > 1):
        valuesForPieChart = getPieData(app)[0]
        app.pieSelection = getArcIndex(app,event.x,event.y,valuesForPieChart)
    
def pieChartMode_mouseReleased(app, event):
    button_mouseReleased(app, event.x, event.y)

def pieChartMode_mouseMoved(app, event):
    button_mouseMoved(app, event.x, event.y)

def pieChartMode_redrawAll(app, canvas):
    import math
    showLabel(app, canvas)
    showCrossIcon(app,canvas)
    drawInteractiveBoard(app, canvas, "Y")
    drawOptions(app, canvas)
    drawDataLabelYesOrNo(app, canvas, app.buttonsLeft + 160, app.height*3/7+31)
    drawGenerate(app, canvas)
    drawReset(app, canvas)
    if app.displayPieChart and (app.xAxis != None and app.pieChartVars != list()):
        (valuesForPieChart,varNamesForPieChart) = getPieData(app)
        for i in range(len(valuesForPieChart)):
            ss, ee = getArcBound(i,valuesForPieChart)
            colorIndex = randomizedColor(app, (i + 803)) 
            color = app.colors[colorIndex]
            canvas.create_arc(app.width/3 - app.height/4, app.height*2/5 - app.height/4, 
            app.width/3 + app.height/4, app.height*2/5+ app.height/4, start=ss, 
            extent=ee, fill=color, outline = color)

            # show data label
            if app.showDataLabel:
                if i != len(valuesForPieChart) - 1:
                    start1 = getArcBound(i,valuesForPieChart)[0] 
                    start2 = getArcBound(i+1,valuesForPieChart)[0]
                else:
                    start1 = getArcBound(i,valuesForPieChart)[0]
                    start2 = -270
                midAngle = start1 - (start1 - start2)/2
                textX = app.centerX + (app.radius+20)*math.cos(midAngle*2*math.pi/360)
                textY = app.centerY - (app.radius+20)*math.sin(midAngle*2*math.pi/360)
                canvas.create_text(textX, textY, text = str(valuesForPieChart[i]),fill="black")

            leftMargin = app.width/5
            textX = leftMargin + (i % 3)* (app.width/2 - leftMargin)/3
            textY = app.height*3/4 + (i//3)*25
            canvas.create_text(textX, textY, text = varNamesForPieChart[i],anchor = "w",fill="black")
            canvas.create_rectangle(textX-12, 
                            textY-5, textX-2,textY+5,fill=color,width = 0)

        if app.pieSelection != None:
            selectStart, selectExent = getArcBound(app.pieSelection,valuesForPieChart)
            colorIndex = randomizedColor(app, (app.pieSelection + 803)) 
            color = app.colors[colorIndex]
            canvas.create_arc(app.width/3 - app.height/4, app.height*2/5 - app.height/4, 
            app.width/3 + app.height/4, app.height*2/5+ app.height/4, start=selectStart, 
            extent=selectExent, fill=color,outline = "cyan",width = 5)

            # show percentage
            percentage = round(round(valuesForPieChart[app.pieSelection]/sum(valuesForPieChart),3)*100,1)
            if app.pieSelection != len(valuesForPieChart) - 1:
                start1 = getArcBound(app.pieSelection,valuesForPieChart)[0] 
                start2 = getArcBound(app.pieSelection+1,valuesForPieChart)[0]
            else:
                start1 = getArcBound(app.pieSelection,valuesForPieChart)[0]
                start2 = -270
            midAngle = start1 - (start1 - start2)/2
            textX = app.centerX + (app.radius/2)*math.cos(midAngle*2*math.pi/360)
            textY = app.centerY - (app.radius/2)*math.sin(midAngle*2*math.pi/360)
            canvas.create_text(textX, textY, text = str(percentage) + "%",
                            font = 'Arial 15 bold',fill="white")

#############################
# simpleLinearRegression
#############################

# Mathematical equations referenced from 
# https://en.wikipedia.org/wiki/Correlation#Sample_correlation_coefficient
# and https://en.wikipedia.org/wiki/Simple_linear_regression 


def analysisMode_mousePressed(app, event):
    button_mousePressed(app, event.x, event.y)
    if app.displayAnalysis and (app.analysisVars != list() and app.yAxis != None):
        if len(app.analysisVars) == 1:
            list1 = app.dataframe.selectVar(app.analysisVars[0]).varValues
            list2 = app.dataframe.selectVar(app.yAxis).varValues
            app.message = sLMOutput(list1,list2,app.analysisVars,app.yAxis)
        else:
            newDataframe = Dataframe(app.dataframe.selectVar(app.analysisVars[0]).list)
            for varIndex in range(1,len(app.analysisVars)):
                newDataframe = newDataframe.merge(newDataframe, Dataframe(app.dataframe.selectVar(app.analysisVars[varIndex]).list))
            data = newDataframe.list
            list1 = [[1] + data[i] for i in range(1,len(data))]
            list2 = app.dataframe.selectVar(app.yAxis).varValues
            list2 = [[list2[i]] for i in range(len(list2))]
            app.message = mLMOutput(app,list1,list2,app.analysisVars,app.yAxis)

def analysisMode_mouseReleased(app, event):
    button_mouseReleased(app, event.x, event.y)

def analysisMode_mouseMoved(app, event):
    button_mouseMoved(app, event.x, event.y)

def analysisMode_redrawAll(app,canvas):
    showLabel(app, canvas)
    showCrossIcon(app,canvas)
    drawInteractiveBoard(app, canvas, "X")
    drawInteractiveBoard(app, canvas, "Y")
    drawOptions(app, canvas)
    drawGenerate(app, canvas)
    drawReset(app, canvas)
    if app.displayAnalysis and (app.analysisVars != list() and app.yAxis != None):
        font = 'Arial 15 bold'
        canvas.create_text(app.width/25,  app.height/5,anchor = "nw",
                       text=app.message, font=font, fill='black')

def mean(list):
    return sum(list)/len(list)

def sumOfSquares(list):
    average = mean(list)
    sumOfSquares = 0
    for value in list:
        sumOfSquares += (value - average)**2
    return sumOfSquares

# list1 (independent) and list2 (dependent) are the same length
# returns (slope, intercept)
def getSlopeAndIntercept(list1, list2):
    total = 0
    xBar, yBar = mean(list1), mean(list2)
    for i in range(len(list1)):
        xi, yi = list1[i], list2[i]
        total += (xi - xBar)*(yi - yBar)
    slope = total/sumOfSquares(list1)
    intercept = yBar - slope*xBar
    return (slope, intercept)

# list1 (independent) and list2 (dependent) are the same length
# returns r_xy
def getSampleCorrelationCoefficient(list1, list2):
    total = 0
    xBar, yBar = mean(list1), mean(list2)
    for i in range(len(list1)):
        xi, yi = list1[i], list2[i]
        total += (xi - xBar)*(yi - yBar)
    sOSX = sumOfSquares(list1)
    sOSY = sumOfSquares(list2)
    r_xy = total/(sOSX*sOSY)**0.5
    return r_xy

# returns the standard error of the estimator(slope)
def getSEOfSlope(list1, list2, slope, intercept):
    n = len(list1)
    errorSumOfSquares = 0
    for i in range(len(list1)):
        errorSumOfSquares += (list2[i] - (list1[i]*slope+intercept))**2
    se = ((errorSumOfSquares/(n-2))/sumOfSquares(list1))**0.5
    return se

def getSEOfIntercept(list1,SEOfSlope):
    squaredXSum = 0
    for i in range(len(list1)):
        squaredXSum += (list1[i])**2
    return SEOfSlope*((squaredXSum/len(list1))**0.5)

# interpretation format
# referenced Moore, McCabe, Craig, Introduction to the Practice of Statistics, 6ed, Freeman, 2009. (p.150)

def sLMOutput(list1,list2,varXName,varYName):
    n = len(list1)
    xBar, sdX = mean(list1), sd(list1)
    yBar, sdY = mean(list2), sd(list2)
    slope, intercept = getSlopeAndIntercept(list1, list2)
    sampleR = getSampleCorrelationCoefficient(list1, list2)
    slopeSE = getSEOfSlope(list1, list2, slope, intercept)
    interceptSE = getSEOfIntercept(list1,slopeSE)
    return(f'''
    We have data on an explanatory variable {varXName} and a response variable 
    {varYName} for {n} individuals. The means and standart deviations of the sample
    data are {round(xBar,2)} and {round(sdX,2)} for {varXName} and {round(yBar,2)} and {round(sdY,2)} for {varYName}. 
    
    The correlation between {varXName} and {varYName} is {round(sampleR,2)}. 
    The equation of the least-squares regression line of {varYName} on {varXName} is:

                {varYName} = {round(intercept,2)} + {round(slope,2)} * {varXName}

    The t-stat for the slope is {round(slope/slopeSE,2)} with a df of {n-2}.
    The t-stat for the intercept is {round(intercept/interceptSE,2)} with a df of {n-2}.''')

##################################
# Multiple Linear Regression (now only works for numberical variables, can be fixed to fit categorical/boolean)
##################################

#############
# Calculation
#############

# Fraction
# https://docs.python.org/3/library/fractions.html

# General Calculation
# https://en.wikipedia.org/wiki/Ordinary_least_squares#Linear_model

# Matrix Inverse
# https://en.wikipedia.org/wiki/Gaussian_elimination#:~:text=A%20variant%20of%20Gaussian%20elimination,inverse%20matrix%2C%20if%20it%20exists.
# https://en.wikipedia.org/wiki/Invertible_matrix
# https://en.wikipedia.org/wiki/Gaussian_elimination#Finding_the_inverse_of_a_matrix

# Matrix Transpose
# https://en.wikipedia.org/wiki/Transpose

# Matrix Dot Product
# https://en.wikipedia.org/wiki/Matrix_multiplication#:~:text=from%20two%20matrices.-,For%20matrix%20multiplication%2C%20the%20number%20of%20columns%20in%20the%20first,B%20is%20denoted%20as%20AB.
# https://en.wikipedia.org/wiki/Dot_product

# Other sources:
# this is too advanced & complex for me, so I did not reference anything from it
# https://stackoverflow.com/questions/32114054/matrix-inversion-without-numpy

# Store the values in the matrix-like format
from fractions import Fraction

# Matrix Transpose

def transpose(matrix):
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

# Matrix Dot Product
# https://en.wikipedia.org/wiki/Matrix_multiplication#:~:text=from%20two%20matrices.-,For%20matrix%20multiplication%2C%20the%20number%20of%20columns%20in%20the%20first,B%20is%20denoted%20as%20AB.
# https://en.wikipedia.org/wiki/Dot_product

def getTermsProduct(matrix1,matrix2,row,col):
    total = 0
    for index1 in range(len(matrix1[0])):
        entry1 = matrix1[row][index1]
        entry2 = matrix2[index1][col]
        total += entry1*entry2
    return total

def dotProduct(matrix1, matrix2):
    if len(matrix1[0]) != len(matrix2):
        print("Unable to perform multiplication due to incompatible matrix size.")
        return None
    else:
        result = [[getTermsProduct(matrix1,matrix2,i,j) for j in range(len(matrix2[0]))] for i in range(len(matrix1))]
        return result

def getIdentityMatrix(matrix):
    return [[1 if i==j else 0 for j in range(len(matrix[0]))] for i in range(len(matrix))]

def formBlockMatrix(matrix, augM):
    return [[matrix[i][j] for j in range(len(matrix[0]))]+[augM[i][k] for k in range(len(matrix[0]))] for i in range(len(matrix))]

# check if the left half of the block matrix is an identity matrix
def isHalfIdentity(blockMatrix):
    leftHalf = getLeftHalf(blockMatrix)
    return leftHalf == getIdentityMatrix(leftHalf)

def getRightHalf(blockMatrix):
    return [[blockMatrix[i][j] for j in range(len(blockMatrix[0])//2, len(blockMatrix[0]))] for i in range(len(blockMatrix))]

def getLeftHalf(blockMatrix):
    return [[blockMatrix[i][j] for j in range(len(blockMatrix[0])//2)] for i in range(len(blockMatrix))]

def multipleByScalar(row, scalar):
    return [row[i]*scalar for i in range(len(row))]

# add two rows of the same length
def addRows(row1,row2):
    return [row1[i]+row2[i] for i in range(len(row1))]

# find the index of the 1st NonZero element in the row
def find1stNonZeroIndex(row):
    index = None
    for i in range(len(row)):
        if row[i] != 0:
            index = i
            break
    return index

# sort the matrix by the index of the non zero term in the row
# size here is to make the function work for the block matrix
# if there is a row of zeros (that exceeds the size), returns None
# for example, a block matrix with 3 rows & 6 cols, if the index >= 3, then there 
# is a row of zeros in the original matrix, so original matrix not invertible

# can sort from the left or right
def sortBy1stNonZero(matrix, size, direction):
    sortedMatrix = list()
    result = dict()
    for row in matrix:
        if direction == "left":
            index = find1stNonZeroIndex(row)
        else:
            index = find1stNonZeroIndex(row[size-1::-1]) # notice that the matrix is a block matrix
        if index == None or index >= size: return None
        elif index not in result:
            result[index] = [row]
        else:
            result[index].append(row)
    if direction == "left":
        sortedResult = sorted(result)
    else: sortedResult = sorted(result)[::-1]
    for key in sortedResult:
        value = result[key]
        for row in value:
            sortedMatrix.append(row)
    return sortedMatrix

# will only work if it is a n*n matrix with its augmented matrix

def reduce(blockMatrix):
    rows = len(blockMatrix)
    blockMatrix = sortBy1stNonZero(blockMatrix,rows,"left")
    if blockMatrix == None: 
        print("Matrix is invertible")
        return None
    while find1stNonZeroIndex(blockMatrix[-1]) < rows - 1:
        for topRow in range(rows):
            for index in range(rows-1,topRow,-1):
                row1 = blockMatrix[index]
                row1Val = row1[topRow]
                if row1Val == 0: continue
                row2 = blockMatrix[index-1]
                row2Val = row2[topRow]
                scalar = Fraction(row2Val,row1Val)
                blockMatrix[index] = addRows(blockMatrix[index-1], multipleByScalar(blockMatrix[index], -1*scalar))
            blockMatrix = sortBy1stNonZero(blockMatrix,rows,"left")
            if blockMatrix == None: 
                print("Matrix is invertible")
                return None
    while find1stNonZeroIndex(blockMatrix[0][rows-1::-1]) < rows - 1:
        for bottomRow in range(rows-1,0,-1):
            for index in range(0,bottomRow):
                step = 1
                row1 = blockMatrix[index]
                row1Val = row1[bottomRow]
                if row1Val == 0: continue
                row2 = blockMatrix[index+step]
                row2Val = row2[bottomRow]
                while row2Val == 0:
                    if index < bottomRow:
                        step += 1
                        row2 = blockMatrix[index+step]
                        row2Val = row2[bottomRow]
                    else: 
                        print("Matrix is invertible")
                        return None
                scalar = Fraction(row2Val,row1Val)
                blockMatrix[index] = addRows(blockMatrix[index+step], multipleByScalar(blockMatrix[index], -1*scalar))
            if blockMatrix == None: 
                print("Matrix is invertible")
                return None
    return blockMatrix

def reducePlus(blockMatrix):
    for index in range(len(blockMatrix)):
        row = blockMatrix[index]
        blockMatrix[index] = multipleByScalar(row, Fraction(1,row[find1stNonZeroIndex(row)]))
    return blockMatrix

def getNumeric(matrix):
    newM = []
    for row in range(len(matrix)):
        newRow = list()
        for col in range(len(matrix[0])):
            entry = matrix[row][col]
            if isinstance(entry, Fraction):
                entry = float(matrix[row][col])
            newRow.append(entry)
        newM.append(newRow)
    return newM

def getInverse(matrix):
    augmentM = getIdentityMatrix(matrix)
    blockMatrix = formBlockMatrix(matrix, augmentM)
    blockMatrix = reducePlus(reduce(blockMatrix))
    return getRightHalf(blockMatrix)

def multipleRegression(XData, YData):
    finalX_T = transpose(XData)
    inverse = getInverse(dotProduct(finalX_T,XData))
    result = dotProduct(inverse,finalX_T)
    finalResult = dotProduct(result, YData)
    return getNumeric(finalResult)

def mLMOutput(app,list1,list2,varXNames,varYName):
    n = len(list1)
    listOfCoefficients = multipleRegression(list1, list2)
    result = {"intercept":round(listOfCoefficients[0][0],2)}
    means = dict()
    sds = dict()
    meanTable = ""
    equation = f"{varYName} = {result['intercept']} "
    for index in range(len(varXNames)):
        var = varXNames[index]
        result[var] = round(listOfCoefficients[index+1][0],2)
        equation += f'+ {result[var]} * {var}'
        means[var] = round(float(mean(app.dataframe.selectVar(var).varValues)),2)
        sds[var] = round(float(sd(app.dataframe.selectVar(var).varValues)),2)
        meanTable += f'Variable:{var}                 Mean:{means[var]}       Standard Deviation:{sds[var]}\n    '
    yBar = round(float(mean(app.dataframe.selectVar(varYName).varValues)),2)
    sdY  = round(float(sd(app.dataframe.selectVar(varYName).varValues)),2)
    meanTable += f'Variable:{varYName}                 Mean:{yBar}       Standard Deviation:{sdY}'
    return(f'''
    We have data on explanatory variables {varXNames} 
    and a response variable [{varYName}] for {n} individuals. The means and standart 
    deviations of the sample data are:

    {meanTable}

    The equation of the least-squares regression line of [{varYName}] on 
    {varXNames} is:

    {equation}
    ''')

#############################
# Main App
#############################
def appStarted(app):
    app.mode = "startMode"
    app.message = 'Click the mouse to select from the options.'
    app.xAxis = None
    app.yAxis = None
    app.dataImported = False
    app.xAxisStart = app.width/7
    app.xAxisEnd = app.width*4/7
    app.yAxisStart = app.height/6
    app.yAxisEnd = app.height*4/6
    app.graphSize = app.xAxisEnd - app.xAxisStart
    app.margin = max(app.width/12,app.height/12)
    app.selection = (-1, -1)

    # Buttons for generating graphs:

    # Bar chart
    app.buttonSideMargin = 5
    app.buttonsLeft = app.width*18/30 + app.buttonSideMargin
    app.XVarButtonsUp = app.height/8
    app.YVarButtonsUp = app.height/4 + 45
    app.buttonWidth = 110
    app.buttonHeight = 20
    app.buttonsPerRow = 4
    app.onXButton = None
    app.onYButton = None
    app.xButtonSelection = (-1,-1)
    app.yButtonSelection = (-1,-1)
    app.errorBarSelectionY = None
    app.errorBarSelectionN = None

    app.dataLabelSelectionY = False
    app.dataLabelSelectionN = False

    app.generateButton = app.width*5/7, app.height*62/100, app.width*6/7,app.height*68/100
    app.resetButton = app.width*5/7, app.height*72/100, app.width*6/7,app.height*78/100
    app.clickGenerate = False
    app.clickReset = False
    app.displayBarGraph = False

    # Line Graph:
    app.yButtonSelectionsForLine = list()
    app.lineGraphVars = list()
    app.displayLineGraph = False

    # Scatter Plot
    app.displayScatterPlot = False

    # Pie Chart
    app.displayPieChart = False
    app.pieChartVars = list()
    # Image obtained from https://stock.adobe.com/search?k=information+icon&asset_id=322639135
    app.rawInfoImage = app.loadImage("Information-icon.png")
    app.infoImage = app.scaleImage(app.rawInfoImage, 1/30)
    # Image obtained from https://commons.wikimedia.org/wiki/File:Flat_cross_icon.svg
    app.rawCrossImage = app.loadImage("Cross_icon.png")
    app.crossImage = app.scaleImage(app.rawCrossImage, 1/35)
    app.showDataLabel = None
    app.showErrorBar = None
    # app.lineGraphVars = None
    app.lineGridMax = None
    # Scatter Plot
    app.dotR = 5
    # Analysis Mode
    app.displayAnalysis = False
    app.analysisVars = list()
    app.analysisType = None
    # app.pause = False # trying to correct the constantly changing colors 
    # colors obtained from 
    # https://stackoverflow.com/questions/4969543/colour-chart-for-tkinter-and-tix
    app.colors =   ['papaya whip', 'blanched almond', 'bisque', 'peach puff',
    'navajo white', 'lemon chiffon',  'lavender',
    'lavender blush', 'misty rose', 'dark slate gray', 'dim gray', 'slate gray',
    'light slate gray', 'gray', 'light grey', 'midnight blue', 'navy', 'cornflower blue', 'dark slate blue',
    'slate blue', 'medium slate blue', 'light slate blue', 'medium blue', 'royal blue',  'blue',
    'dodger blue', 'deep sky blue', 'sky blue', 'light sky blue', 'steel blue', 'light steel blue',
    'light blue', 'powder blue', 'pale turquoise', 'dark turquoise', 'medium turquoise', 'turquoise',
    'cyan', 'light cyan', 'cadet blue', 'medium aquamarine', 'aquamarine', 'dark green', 'dark olive green',
    'dark sea green', 'sea green', 'medium sea green', 'light sea green', 'pale green', 'spring green',
    'lawn green', 'medium spring green', 'green yellow', 'lime green', 'yellow green',
    'forest green', 'olive drab', 'dark khaki', 'khaki', 'pale goldenrod', 'light goldenrod yellow',
    'light yellow', 'yellow', 'gold', 'light goldenrod', 'goldenrod', 'dark goldenrod', 'rosy brown',
    'indian red', 'saddle brown', 'sandy brown','dark salmon', 'salmon', 'light salmon', 'orange', 'dark orange',
    'coral', 'light coral', 'tomato', 'orange red', 'red', 'hot pink', 'deep pink', 'pink', 'light pink',
    'pale violet red', 'maroon', 'medium violet red', 'violet red',
    'medium orchid', 'dark orchid', 'dark violet', 'blue violet', 'purple', 'medium purple',
    'thistle', 'snow2', 'snow3','snow4', 'seashell2', 'seashell3', 'seashell4', 'AntiqueWhite1', 'AntiqueWhite2',
    'AntiqueWhite3', 'AntiqueWhite4', 'bisque2', 'bisque3', 'bisque4', 'PeachPuff2',
    'PeachPuff3', 'PeachPuff4', 'NavajoWhite2', 'NavajoWhite3', 'NavajoWhite4',
    'LemonChiffon2', 'LemonChiffon3', 'LemonChiffon4', 'cornsilk2', 'cornsilk3',
    'cornsilk4', 'ivory2', 'ivory3', 'ivory4', 'honeydew2', 'honeydew3', 'honeydew4',
    'LavenderBlush2', 'LavenderBlush3', 'LavenderBlush4', 'MistyRose2', 'MistyRose3',
    'MistyRose4', 'azure2', 'azure3', 'azure4', 'SlateBlue1', 'SlateBlue2', 'SlateBlue3',
    'SlateBlue4', 'RoyalBlue1', 'RoyalBlue2', 'RoyalBlue3', 'RoyalBlue4', 'blue2', 'blue4',
    'DodgerBlue2', 'DodgerBlue3', 'DodgerBlue4', 'SteelBlue1', 'SteelBlue2',
    'SteelBlue3', 'SteelBlue4', 'DeepSkyBlue2', 'DeepSkyBlue3', 'DeepSkyBlue4',
    'SkyBlue1', 'SkyBlue2', 'SkyBlue3', 'SkyBlue4', 'LightSkyBlue1', 'LightSkyBlue2',
    'LightSkyBlue3', 'LightSkyBlue4', 'SlateGray1', 'SlateGray2', 'SlateGray3',
    'SlateGray4', 'LightSteelBlue1', 'LightSteelBlue2', 'LightSteelBlue3',
    'LightSteelBlue4', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4',
    'LightCyan2', 'LightCyan3', 'LightCyan4', 'PaleTurquoise1', 'PaleTurquoise2',
    'PaleTurquoise3', 'PaleTurquoise4', 'CadetBlue1', 'CadetBlue2', 'CadetBlue3',
    'CadetBlue4', 'turquoise1', 'turquoise2', 'turquoise3', 'turquoise4', 'cyan2', 'cyan3',
    'cyan4', 'DarkSlateGray1', 'DarkSlateGray2', 'DarkSlateGray3', 'DarkSlateGray4',
    'aquamarine2', 'aquamarine4', 'DarkSeaGreen1', 'DarkSeaGreen2', 'DarkSeaGreen3',
    'DarkSeaGreen4', 'SeaGreen1', 'SeaGreen2', 'SeaGreen3', 'PaleGreen1', 'PaleGreen2',
    'PaleGreen3', 'PaleGreen4', 'SpringGreen2', 'SpringGreen3', 'SpringGreen4',
    'green2', 'green3', 'green4', 'chartreuse2', 'chartreuse3', 'chartreuse4',
    'OliveDrab1', 'OliveDrab2', 'OliveDrab4', 'DarkOliveGreen1', 'DarkOliveGreen2',
    'DarkOliveGreen3', 'DarkOliveGreen4', 'khaki1', 'khaki2', 'khaki3', 'khaki4',
    'LightGoldenrod1', 'LightGoldenrod2', 'LightGoldenrod3', 'LightGoldenrod4',
    'LightYellow2', 'LightYellow3', 'LightYellow4', 'yellow2', 'yellow3', 'yellow4',
    'gold2', 'gold3', 'gold4', 'goldenrod1', 'goldenrod2', 'goldenrod3', 'goldenrod4',
    'DarkGoldenrod1', 'DarkGoldenrod2', 'DarkGoldenrod3', 'DarkGoldenrod4',
    'RosyBrown1', 'RosyBrown2', 'RosyBrown3', 'RosyBrown4', 'IndianRed1', 'IndianRed2',
    'IndianRed3', 'IndianRed4', 'sienna1', 'sienna2', 'sienna3', 'sienna4', 'burlywood1',
    'burlywood2', 'burlywood3', 'burlywood4', 'wheat1', 'wheat2', 'wheat3', 'wheat4', 'tan1',
    'tan2', 'tan4', 'chocolate1', 'chocolate2', 'chocolate3', 'firebrick1', 'firebrick2',
    'firebrick3', 'firebrick4', 'brown1', 'brown2', 'brown3', 'brown4', 'salmon1', 'salmon2',
    'salmon3', 'salmon4', 'LightSalmon2', 'LightSalmon3', 'LightSalmon4', 'orange2',
    'orange3', 'orange4', 'DarkOrange1', 'DarkOrange2', 'DarkOrange3', 'DarkOrange4',
    'coral1', 'coral2', 'coral3', 'coral4', 'tomato2', 'tomato3', 'tomato4', 'OrangeRed2',
    'OrangeRed3', 'OrangeRed4', 'red2', 'red3', 'red4', 'DeepPink2', 'DeepPink3', 'DeepPink4',
    'HotPink1', 'HotPink2', 'HotPink3', 'HotPink4', 'pink1', 'pink2', 'pink3', 'pink4',
    'LightPink1', 'LightPink2', 'LightPink3', 'LightPink4', 'PaleVioletRed1',
    'PaleVioletRed2', 'PaleVioletRed3', 'PaleVioletRed4', 'maroon1', 'maroon2',
    'maroon3', 'maroon4', 'VioletRed1', 'VioletRed2', 'VioletRed3', 'VioletRed4',
    'magenta2', 'magenta3', 'magenta4', 'orchid1', 'orchid2', 'orchid3', 'orchid4', 'plum1',
    'plum2', 'plum3', 'plum4', 'MediumOrchid1', 'MediumOrchid2', 'MediumOrchid3',
    'MediumOrchid4', 'DarkOrchid1', 'DarkOrchid2', 'DarkOrchid3', 'DarkOrchid4',
    'purple1', 'purple2', 'purple3', 'purple4', 'MediumPurple1', 'MediumPurple2',
    'MediumPurple3', 'MediumPurple4', 'thistle1', 'thistle2', 'thistle3', 'thistle4',
    'gray1', 'gray2', 'gray3', 'gray4', 'gray5', 'gray6', 'gray7', 'gray8', 'gray9', 'gray10',
    'gray11', 'gray12', 'gray13', 'gray14', 'gray15', 'gray16', 'gray17', 'gray18', 'gray19',
    'gray20',  'gray25', 'gray26', 'gray27', 'gray28',
    'gray29', 'gray30', 'gray31', 'gray32', 'gray33', 'gray34', 'gray35', 'gray36', 'gray37',
    'gray38', 'gray39', 'gray40', 'gray42', 'gray43', 'gray44', 'gray45', 'gray46', 'gray47',
    'gray48', 'gray49', 'gray50', 'gray51', 'gray52', 'gray53', 'gray54', 'gray55', 'gray56',
    'gray57', 'gray58', 'gray59', 'gray60']
    app.totalColors = len(app.colors)
    # For mode switching:
    # app.generateLineGraph = True
    # For Pie Chart
    app.centerX, app.centerY = app.width/3, app.height*2/5
    app.radius = app.height/4
    app.pieSelection = None
    # Font Page Design
    app.fpBarChart = False
    app.fpViewData = False
    app.fpConAnalysis = False
    app.fpLineGraph = False
    app.fpScatterPlot = False
    app.fpPieChart = False
    app.fpImportData = False
    # Button characteristics
    '''dict[button]: 
        [(x0,y0,x1,y1)#rectangle,  index 0
        color,                     index 1
        fpDesign,                  index 2
        (textX,textY),             index 3
        text,                      index 4
        anchor,                    index 5
        fontSize,                  index 6
        angle]                     index 7'''
    app.buttonChars = {
    "barChart":[(30, 34, 192, 766),
    "maroon1",
    app.fpBarChart,
    (20, app.height/2),
    "Bar Chart",
    "s",
    int(160/800*app.height),
    270],
    "viewData":[(197, 33, 821, 149),
    "deep sky blue",
    app.fpViewData,
    (205, 20),
    "View Data",
    "nw",
    int(130/800*app.height),
    0],
    "importData":[(823, 122, 970, 149),
    "RoyalBlue3",
    app.fpImportData,
    (826, 125),
    "IMPORT DATA",
    "nw",
    int(20/800*app.height),
    0],
    "conAnalysis":[(197, 150, 970, 235),
    "coral",
    app.fpConAnalysis,
    (205, 140),
    "Conduct Analysis",
    "nw",
    int(90/800*app.height),
    0],
    "lineGraph":[(197, 238, 295, 769),
    "SeaGreen1",
    app.fpLineGraph,
    (190, 240),
    "Line Graph",
    "sw",
    int(100/800*app.height),
    270],
    "scatterPlot":[(298, 237, 745, 518),
    "orange",
    app.fpScatterPlot,
    (300, 222),
    "Scatter\nPlot",
    "nw",
    int(130/800*app.height),
    0],
    "pieChart":[(747, 237, 844, 655),
    'SlateBlue1',
    app.fpPieChart,
    (740, 250),
    "Pie Chart",
    "sw",
    int(90/800*app.height),
    270]}

def randomizedColor(app, i):
    colorIndex = (2**i*15112 + i**5*1224 - i**4*1999 + i**2*1240 + 520*3**(2*i) - 21*i + 4021) % app.totalColors
    return colorIndex


runApp(width=1300, height=800)
