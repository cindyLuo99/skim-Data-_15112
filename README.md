# skimData-15112

**Project Name**: skim(Data)

**Project Description**: (could also be found by clicking the 'i' button on the start page)

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

**How to run the project:**

1. User imports the dataset (stored in CSV format) from the same folder where the python file is stored by clicking 'import data' on the start page and entering the name of the data file
	- in the demo, the name of the data file is called "Data File.csv"
	- to quickly import the demo data, one can simply press 'd' to load the demo data 

2. To view the data imported, the user can click the 'View Data' button on the first page
	- font size auto-adjusted to the cell size
	- When click on the cell, it will highlight that cell

3. To view the description of this project, click the 'info' button on the top right corner

4. To generate different graphs & conduct analysis, click the buttons on the main menu to use each feature:
	- Notice that when data is first imported, skim(Data) will help the user determine if a variable
	is appropriate for certain graph types. Therefore, the user can not select the buttons that
	are illogical for the graph type/feature.
	Examples include but not limited to:
		- generate graphs/view data without importing the dataset
		- select a numerical valuable for the x-axis of a bar chart/line graph
		- select a categorical valuable for the x-axis of a scatter plot
		- select a categorical value for the y-axis
		- select the same variable for x & y-axis of the graph
		- select the same variable for dependent & independent variable for analysis
		- only selecting one variable for the graphs (at least two variables should be selected 
		for the x/y-axis)
		- select categorical values for data analysis (this feature is currently disabled)
		- select to display percentages in a pie chart (e.g. 'Social Percent', 'Other Percent'
		are percentages)
		- select less than 2 variables for a pie chart (If one of the variable value is 0, then at
		least 3 variables should be chosen
		- select a categorical variable for the pie chart

	- Can select & unselect, can select multiple variables based on the graph type

	- After selecting the variables & selecting the additional features, 
		click 'GENERATE' to generate the graph
		click 'RESET' to clear the selections 

	- The graph will change if the user changes their selections of the variables & additional features
		- No need to click 'GENERATE' or 'RESET' every time to change the selection of the variables

	- For pie chart:
		- When entering the date, please use the format "mm/dd/yy"; however, there is no need to
		enter 0 before a month/day if less than 10. So "4/2/22" instead of "4/02/22". The latter
		one will cause the screen to say "Date out of range"
		- when click on the pie chart, will show the percentage
	
5. Click the cross on the top right corner of the screen to exit certain mode

6. In general, skim(Data) is intuitive to use and will prevent crushing by itself. Users are encourage to 
try around by clicking around to discover additional features that are not included in this guide.



**Libraries used:** 
cmu_112_graphics (https://www.cs.cmu.edu/~112/notes/cmu_112_graphics.py)

No other libraries were used in this project.

**Shortcut commands:** press 'd' to load demo data

Link to the demo video: https://www.youtube.com/watch?v=4zF79chlR6U
