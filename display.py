# Skeleton Tk interface example
# Written by Bruce Maxwell
# Modified by Stephanie Taylor
# Modified again by Luc Yuki Marrie
# CS251
# Spring 2015

import Tkinter as tk
import tkFileDialog
import tkFont as tkf
import math
import random
import view
import numpy as np
import numpy.linalg
import data
import sys
import analysis
import machine_learning_naivebayes as mln
import machine_learning_KNN as mlk
import writeToCSV
# from tkintertable.Tables import TableCanvas
# from tkintertable.TableModels import TableModel


# create a class to build and manage the display
class DisplayApp:

	def __init__(self, width, height):

		# create a tk object, which is the root window
		self.root = tk.Tk()

		# width and height of the window
		self.initDx = width
		self.initDy = height

		# set up the geometry for the window
		self.root.geometry( "%dx%d+50+30" % (self.initDx, self.initDy) )

		# set the title of the window
		self.root.title("Luc's Interactive Visualization System")

		# set the maximum size of the window for resizing
		self.root.maxsize( 1600, 900 )	
		
		# setup the menus
		
		self.buildMenus()

		# build the controls
	
		self.buildControls()

		# build the Canvas
		self.buildCanvas()

		# bring the window to the front
		self.root.lift()

		# - do idle events here to get actual canvas size
		self.root.update_idletasks()

		# set up the key bindings
		self.setBindings()

		# set up the application state
		self.objects = [] # list of data objects that will be drawn in the canvas
		self.objects2 = []
		self.baseClick = None # used to keep track of mouse movement
		
	# Axes implementation 
		# View object
		self.view = view.View()

		# axis endpoints 
		self.axes = np.matrix([[0,1,0,0,0,0],
							   [0,0,0,1,0,0],
							   [0,0,0,0,0,1],
							   [1,1,1,1,1,1]])
		
		self.lines = []
		self.labels = []
		self.file = ''
		
		self.buildAxes()		
		self.baseExtent = np.matrix([0,0,0])
		
		self.data = None
		global data2
		self.selectedHeaders = []
		self.selectedColumns = []
		self.selectedPA = []
		self.axisPoints = None
		self.vMatrix = None
 		self.colorMatrix = None
 		self.colorMatrix2 = None
 		self.zerosMatrix = None
 		self.axis = 0
		self.sizeAxis = 0
		self.window = None
		self.window2 = None
		self.gradient = None
		self.shape = None
		self.linePts1 = None
		self.linePts2 = None
		self.lp1 = None
		self.lp2 = None
		self.PCAname = None
		self.pcaDict = {}
		self.normDict = {}
		self.selectedPCs = []
		self.evColorSize = []
		self.listForPCA = []
		self.list = []
		self.normalizeBool = None
		self.pca = None
		self.K = None
		self.IDnums = None
		self.means = None
		self.selectedColor = None
		self.pts1 = None
		self.selectedMetric = None
		self.handleOpen()

	
	def buildMenus(self):
		
		# create a new menu
		menu = tk.Menu(self.root)

		# set the root menu to our new menu
		self.root.config(menu = menu)

		# create a variable to hold the individual menus
		menulist = []

		# create a file menu
		filemenu = tk.Menu( menu )
		menu.add_cascade( label = "File", menu = filemenu )
		menulist.append(filemenu)

		# create another menu for kicks
		cmdmenu = tk.Menu( menu )
		menu.add_cascade( label = "Command", menu = cmdmenu )
		menulist.append(cmdmenu)

		# menu text for the elements
		# the first sublist is the set of items for the file menu
		# the second sublist is the set of items for the option menu
		menutext = [ [ '-', 'Open \xE2\x8C\x98-O', 'Quit	\xE2\x8C\x98-Q' ],
					 [ 'Command 1', '-', '-' ]]

		# menu callback functions (note that some are left blank,
		# so that you can add functions there if you want).
		# the first sublist is the set of callback functions for the file menu
		# the second sublist is the set of callback functions for the option menu
		menucmd = [ [None, self.handleOpen, self.handleQuit],
					[self.handleMenuCmd1, None, None] ]
		
		
		# build the menu elements and callbacks
		for i in range( len( menulist ) ):
			for j in range( len( menutext[i]) ):
				if menutext[i][j] != '-':
					menulist[i].add_command( label = menutext[i][j], command=menucmd[i][j] )
				else:
					menulist[i].add_separator()

	# create the canvas object
	def buildCanvas(self):
		self.canvas = tk.Canvas( self.root, width=self.initDx, height=self.initDy )
		self.canvas.pack( expand=tk.YES, fill=tk.BOTH )
		return

	# build a frame and put controls in it
	def buildControls(self):

		### Control ###
		# make a control frame on the right
		rightcntlframe = tk.Frame(self.root)
		rightcntlframe.pack(side=tk.RIGHT, padx=2, pady=2, fill = tk.Y)

		# make a separator frame
		sep = tk.Frame( self.root, height=self.initDy, width=2, bd=1, relief=tk.SUNKEN )
		sep.pack( side=tk.RIGHT, padx = 2, pady = 2, fill=tk.Y)

		# use a label to set the size of the right panel
		label = tk.Label( rightcntlframe, text="Control Panel", width=20 )
		label.pack( side=tk.TOP, pady=10)
		
		openButton = tk.Button(rightcntlframe, text = "Open File", height = 1, width = 10, command = self.handleOpen)
		openButton.pack(side=tk.TOP, pady=2)
		
		# select axes button
		selectAxesButton = tk.Button(rightcntlframe, text = "Plot Data", height = 1, width = 10, command = self.handlePlotData)
		selectAxesButton.pack(side=tk.TOP, pady=2)	
		
		# Gradient button
# 		gradientButton = tk.Label(rightcntlframe, text = "Select Color")
# 		gradientButton.pack(side=tk.TOP)
		self.gradientOption = tk.StringVar(self.root)
		self.gradientOption.set("Yellow to Blue")
# 		gradientMenu = tk.OptionMenu(rightcntlframe, self.gradientOption, "Green to Red", "Yellow to Blue", "Blues", "Sunset Theme")
# 		gradientMenu.pack(side=tk.TOP)
		
		# Update Color button
		clusterButton = tk.Button(rightcntlframe, text = "Run Clustering", height=1, width = 13, command = self.handleCluster)
		clusterButton.pack(side=tk.TOP, pady=8)	
		
		classifierButton = tk.Button(rightcntlframe, text = "Classification", height=1, width = 13, command = self.handleClassify)
		classifierButton.pack(side=tk.TOP, pady=8)
		
		# button that builds linear regression
		pcaButton = tk.Button(rightcntlframe, text = "Add PCA Analysis", height = 1, width = 14, command = self.handlePCA)
		pcaButton.pack(side=tk.TOP, pady=8)
		
		self.pcaListBox = tk.Listbox(rightcntlframe, selectmode=tk.SINGLE, height = 5, width = 20, exportselection=0)
		self.pcaListBox.pack(side=tk.TOP, pady=3)
		# button that builds linear regression
		deleteButton = tk.Button(rightcntlframe, text = "Delete PCA", height = 1, width = 9, command = self.deletePCA)
		deleteButton.pack(side=tk.TOP)
		
		showPCAButton = tk.Button(rightcntlframe, text = "Show PCA Table", height = 1, width = 12, command = self.showPCA)
		showPCAButton.pack(side=tk.TOP, pady=2)
		
		projectionButton = tk.Button(rightcntlframe, text = "Project Data", height = 1, width = 10, command = self.handleproject)
		projectionButton.pack(side=tk.TOP, pady=2)
		
		PCAClusterButton = tk.Button(rightcntlframe, text = "Cluster PCA", height = 1, width = 10, command = self.handleproject2)
		PCAClusterButton.pack(side=tk.TOP, pady=2)
		
		self.colorOption = tk.StringVar( self.root )
		self.colorOption.set("black")
		
		# Translation Speed
		self.translationVariable = tk.StringVar(self.root)
		self.translationVariable.set("Normal")
		translationController = tk.Label(rightcntlframe, text = "Translation Speed:")
		translationMenu = tk.OptionMenu(rightcntlframe, self.translationVariable, "Slow", "Normal", "Fast")
		
		# Scaling Speed
		self.scalingVariable = tk.StringVar(self.root)
		self.scalingVariable.set("Normal")
		scalingController = tk.Label(rightcntlframe, text = "Scaling Speed:")
		scalingMenu = tk.OptionMenu(rightcntlframe, self.scalingVariable, "Slow", "Normal", "Fast")
		
		# Rotation Speed
		self.rotationVariable = tk.StringVar(self.root)
		self.rotationVariable.set("Normal")
		rotationController = tk.Label(rightcntlframe, text = "Rotation Speed:")
		rotationMenu = tk.OptionMenu(rightcntlframe, self.rotationVariable, "Slow", "Normal", "Fast")
		
		# Reset Button
		resetButton = tk.Button( rightcntlframe, text="Reset View", 
								command=self.resetAxes )
		resetButton.pack(side=tk.TOP, pady=10)  # default side is top	

		# Orientation Help display
		self.orientation = tk.StringVar()
		self.orientation.set("[[0, 0, -1]]")
		scaleDisplayMessage = tk.Message(rightcntlframe, textvariable = self.orientation, width = 150)
		scaleDisplayMessage.pack(side=tk.BOTTOM)	
		scaleDisplay = tk.Label(rightcntlframe, text = "Orientation:")
		scaleDisplay.pack(side = tk.BOTTOM)
		
		
		# Scale Help display
		self.scale = tk.StringVar()
		self.scale.set("1")
		scaleDisplayMessage = tk.Message(rightcntlframe, textvariable = str(self.scale), width = 150)
		scaleDisplayMessage.pack(side=tk.BOTTOM)	
		scaleDisplay = tk.Label(rightcntlframe, text = "Scale:")
		scaleDisplay.pack(side = tk.BOTTOM)
		
		return
		

	def setBindings(self):
		# bind mouse motions to the canvas
		self.canvas.bind( '<Button-1>', self.handleMouseButton1 )
		self.canvas.bind( '<Control-Button-1>', self.handleMouseButton2 )
		self.canvas.bind( '<Button-2>', self.handleMouseButton2 )
		self.canvas.bind( '<Control-Button-2>', self.handleMouseButton3 )
		self.canvas.bind( '<B1-Motion>', self.handleMouseButton1Motion )
		self.canvas.bind( '<B2-Motion>', self.handleMouseButton2Motion )
		self.canvas.bind( '<Control-B1-Motion>', self.handleMouseButton2Motion )
		self.canvas.bind( '<Control-B2-Motion>', self.handleMouseButton3Motion )
		self.canvas.bind( '<Configure>', self.resize )

		# bind command sequences to the root window
		self.root.bind( '<Command-q>', self.handleQuit )
		self.root.bind( '<Command-o>', self.handleOpen )
		self.root.bind( '<Command-r>', self.resetAxes )
		self.root.bind( '<Command-x>', self.viewXYplane )
		self.root.bind( '<Command-y>', self.viewYZplane )
		self.root.bind( '<Command-z>', self.viewXZplane )





###
##### Handle functions
###

	def handleOpen(self, event=None):
		fn = tkFileDialog.askopenfilename( parent=self.root, title='Choose a data file', initialdir='.' )
		self.file = fn
		try:
			self.data = data.Data(self.file)
		except IOError:
			pass
		else:
			self.data.read(self.file)
	
	# handles data plotting with PCA
	def handleproject(self,event=None):
		self.handlePlotData(pca = self.pca)
	
	# handles PCA clustering - EXTENSION 1
	def handleproject2(self, event=None):
		self.handlePlotData2(pca = self.pca)
		
	# handles data plotting	dialogbox	
	def handlePlotData(self, event=None, pca=None):
		self.data = data.Data(self.file) if pca == None else pca
		d = PCAClassify(self.root, self.data, "Select Axes", self.file)
		d.handleSelection
		self.selectedHeaders = d.selectedPCs
		self.selectedColor = d.selectedColor
		self.IDnums = self.data.get_all_data()[:,-1]
		self.buildPoints()
		
	# handles data plotting	PCA clustering	
	def handlePlotData2(self, event=None, pca=None):
		self.data = data.Data(self.file) if pca == None else pca
		d = BuildClusterDialog(self.root, self.data, "Select Axes", self.file)
		d.handleSelection
		self.selectedHeaders = d.selectedHeaders
		self.color = self.colorOption.get()		
		num_clusters = d.number
		self.selectedColor = d.selectedColor
		try:
			self.cluster = analysis.cluster(self.data, self.selectedHeaders, int(num_clusters))
		except AttributeError:
			pass
		IDs = self.cluster.get_IDnums()
		self.cluster.add_column("Cluster_IDs", "numeric", IDs)
		self.K = self.cluster.get_K()
		self.IDnums = self.cluster.get_IDnums()
		self.means = self.cluster.get_means()
		self.buildClusterPoints()	
			

	# handles PCA
	def handlePCA(self, event=None):
		p = PCADialog(self.root, self.data, "Data Columns", self.file, None, self.pcaDict, self.normDict)
		headers = self.data.get_raw_headers()
		self.selectedColumns = p.selectedColumns
		print self.selectedColumns, "selected columns"
		self.listForPCA = []
		for i in range(0, len(self.selectedColumns)):
			self.listForPCA.append(headers[int(self.selectedColumns[i])])
		self.pca = analysis.pca(self.data, self.listForPCA, True)
		rows = self.pca.matrix_data.shape[0]
		columns = self.pca.matrix_data.shape[1]
		headers1 = self.pca.raw_headers
		types = self.pca.raw_types
		data = self.pca.matrix_data
		writeToCSV.writeToCSV(rows, columns, headers1, types, data, "PCA.csv")
		self.PCAname = p.PCAname
		self.pcaDict = p.pcaDict
		self.normDict = p.normDict
		self.pcaListBox.insert(tk.END, self.PCAname)
		self.selectedColumns = p.selectedColumns
		self.normalizeBool = p.normalizeBool

	
	# handles PCA Data table	
	def showPCA(self, event=None):
		global data2
		data2 = self.data.get_all_data()
		selection = self.pcaListBox.get(self.pcaListBox.curselection())			
		self.list = self.pcaDict.get(str(selection))			
		headers = self.data.get_raw_headers()
		newNormBool = self.normDict.get(selection)
		self.listForPCA = []
		for i in range(0, len(self.list)):
			self.listForPCA.append(headers[int(self.list[i])])
  		s = PCATableDialog(self.root, self.listForPCA, "PCA Data Table", self.file, newNormBool, self.pcaDict, self.normDict)
	
		
	# deletes PCA from listbox
	def deletePCA(self, event=None):
		selection = self.pcaListBox.curselection()
		self.pcaListBox.delete(selection)

	# handles cluster
	def handleCluster(self, event=None): 			
		headers = self.data.get_raw_headers()
		b = BuildClusterDialog(self.root, self.data, "Select Axes", self.file)
		self.selectedHeaders = b.selectedHeaders
		num_clusters = b.number
		self.selectedColor = b.selectedColor
		self.cluster = analysis.cluster(self.data, self.selectedHeaders, int(num_clusters), '')
		IDs = self.cluster.get_IDnums()
		self.cluster.add_column("Cluster_IDs", "numeric", IDs)
		self.K = self.cluster.get_K()
		self.IDnums = self.cluster.get_IDnums()
		self.means = self.cluster.get_means()
		self.buildClusterPoints()

	def handleClassify(self, event=None): 			
		self.IDnums = self.data.get_all_data()[:,-1]
		d = PCAClassify(self.root, self.data, "Select PCA Axes", self.file)
		d.handleSelection
		self.selectedHeaders = d.selectedPCs
		print self.selectedHeaders, "Selected Headers"
		num_clusters = self.IDnums
		for i in range(0, self.IDnums.shape[0]):
			num_clusters[i,0] = int(num_clusters[i,0])
		self.selectedColor = d.selectedColor
		unique, mapping = np.unique( np.array(self.IDnums.T), return_inverse=True)
		self.K = len(unique)
		self.buildClusterPoints()
		
	def handleClassify2(self, event=None): 			
		self.IDnums = self.data.get_all_data()[:,-1]
		num_clusters = self.IDnums
		for i in range(0, self.IDnums.shape[0]):
			num_clusters[i,0] = int(num_clusters[i,0])
		self.selectedColor = "Preselected Colors"
		unique, mapping = np.unique( np.array(self.IDnums.T), return_inverse=True)
		self.K = len(unique)
		self.buildClusterPoints()	
		
		
			

	# handles building of cluster points
	def buildClusterPoints(self, event=None):
		
		# if there are points on the canvas, delete them
		if self.objects != []:
			for object in self.objects:
				self.canvas.delete(object)
			self.objects = []
		
		# if there are cluster means on the canvas, delete them	
		if self.objects2 != []:
			for object in self.objects2:
				self.canvas.delete(object)
			self.objects2 = []
		
		# if there are cluster mean labels on the canvas, delete them
		for i in range(3, len(self.labels)):
			self.canvas.delete(self.labels[i])
		labels2 = []
		for i in range(0,3):
			labels2.append(self.labels[i])
		self.labels = labels2
				
# 		rows = self.rows
# 		columns = self.columns			
		rows = self.data.get_raw_num_rows()
		columns = self.data.get_num_columns()		
					 			 		
  		self.axisPoints = np.matrix(np.zeros((rows,4)))
  		homogenousColumn = [1] * self.axisPoints.shape[1]
		self.axisPoints[:] = np.matrix(homogenousColumn)	
		z = -1
		self.zerosMatrix = np.matrix(np.zeros((rows, 4)))
		for j in range(0,3):
			z += 1
			for i in range(0,rows):
				self.axisPoints[i,z] = self.zerosMatrix[0,0]
				
 		z = -1
 		for header in self.selectedHeaders:
 			if z != 3:
				if header != "None" and header != "Apply to x axis" and header != "Apply to y axis" and header != "Apply to z axis":
					column = self.data.get_column(header)
					for i in range(0,rows):
						self.axisPoints[i,z+1] = column[i]
					z += 1
				else:
					pass
			else:
				pass

	 		
  		self.maxAndMins = []
 		for header in self.selectedHeaders:
 			column = self.data.get_column(header)
 			min = np.min(column)
 			max = np.max(column)
 			self.maxAndMins.append(min)
 			self.maxAndMins.append(max)
 		
 		print self.maxAndMins, "max and mins"
 		
 		self.mnm = np.matrix([[self.maxAndMins[0],self.maxAndMins[1]], 
 							  [self.maxAndMins[2],self.maxAndMins[3]],
 							  [self.maxAndMins[4],self.maxAndMins[5]]])
 		 		 		
 		z = -1
		if self.selectedHeaders[2] != "None":
			for j in range(0,3):
				z += 1
				for i in range(0,rows):
					self.axisPoints[i,z] = float(self.axisPoints[i,z] - self.mnm[z,0])/float(self.mnm[z,1] - self.mnm[z,0])
		else:
			for j in range(0,2):
				z += 1
				for i in range(0,rows):
					self.axisPoints[i,z] = float(self.axisPoints[i,z] - self.mnm[z,0])/float(self.mnm[z,1] - self.mnm[z,0])
		
		
		
		VTM = self.view.build()
		pts = VTM * self.axisPoints.T
		pts = pts.T
		extent = self.view.getExtent()
		
		red = '#%02x%02x%02x' % (255, 0, 0)  # rgb color
		blue = '#%02x%02x%02x' % (0, 0, 255)  # rgb color
		yellow = '#%02x%02x%02x' % (255, 255, 0)  # rgb color
		green = '#%02x%02x%02x' % (0, 128, 0)  # rgb color
		orange = '#%02x%02x%02x' % (255, 165, 0)  # rgb color
		purple = '#%02x%02x%02x' % (128, 0, 128)  # rgb color
		cyan = '#%02x%02x%02x' % (0, 255, 255)  # rgb color
		fuchsia = '#%02x%02x%02x' % (255, 0, 255)  # rgb color
		grey = '#%02x%02x%02x' % (128, 128, 128)  # rgb color
		olive = '#%02x%02x%02x' % (128, 128, 0)  # rgb color
		paleturquoise = '#%02x%02x%02x' % (175,238,238)  # rgb color
		pink = '#%02x%02x%02x' % (255,192,203)  # rgb color
		lime = '#%02x%02x%02x' % (0,255,0)  # rgb color
		
		black = self.colorOption.get()

		if self.selectedColor == "Preselected Colors":		
			# establishes cluster colors
			for i in range(0, rows):
				if self.IDnums[i] == 12:
					color = red
				elif self.IDnums[i] == 13:
					color = blue
				elif self.IDnums[i] == 2:
					color = yellow
				elif self.IDnums[i] == 15:
					color = green
				elif self.IDnums[i] == 14:
					color = orange
				elif self.IDnums[i] == 5:
					color = purple
				elif self.IDnums[i] == 16:
					color = cyan				
				elif self.IDnums[i] == 17:
					color = fuchsia				
				elif self.IDnums[i] == 18:
					color = black				
				elif self.IDnums[i] == 19:
					color = lime
				elif self.IDnums[i] == 20:
					color = paleturquoise
				elif self.IDnums[i] == 11:
					color = pink
				if self.IDnums[i] == 18:
					pt = self.canvas.create_oval(pts[i,0]-float(0.3/extent[0,0]),pts[i,1]-float(0.3/extent[0,1]),pts[i,0]+float(0.3/extent[0,0])*20,pts[i,1]+float(0.3/extent[0,0])*20,fill=color, outline = '')
					self.objects.append(pt)
				elif self.IDnums[i] == 19:
					pt = self.canvas.create_oval(pts[i,0]-float(0.3/extent[0,0]),pts[i,1]-float(0.3/extent[0,1]),pts[i,0]+float(0.3/extent[0,0])*20,pts[i,1]+float(0.3/extent[0,0])*20,fill=color, outline = '')
					self.objects.append(pt)
				elif self.IDnums[i] == 20:
					pt = self.canvas.create_oval(pts[i,0]-float(0.3/extent[0,0]),pts[i,1]-float(0.3/extent[0,1]),pts[i,0]+float(0.3/extent[0,0])*20,pts[i,1]+float(0.3/extent[0,0])*20,fill=color, outline = '')
					self.objects.append(pt)					
				else:
					pt = self.canvas.create_oval(pts[i,0]-float(0.3/extent[0,0]),pts[i,1]-float(0.3/extent[0,1]),pts[i,0]+float(0.3/extent[0,0])*20,pts[i,1]+float(0.3/extent[0,0])*20, outline = '')
					self.objects.append(pt)
		else:
			for i in range(0, rows):	
				multiplier = 255/self.K				
				color = '#%02x%02x%02x' % (int(255-int((255 - self.IDnums[i]*multiplier))), int(255-int((255-self.IDnums[i]*multiplier))), int(255-self.IDnums[i]*multiplier))  # rgb color
				pt = self.canvas.create_oval(pts[i,0]-float(0.3/extent[0,0]),pts[i,1]-float(0.3/extent[0,1]),pts[i,0]+float(0.3/extent[0,0])*20,pts[i,1]+float(0.3/extent[0,0])*20,fill=color, outline = '')
				self.objects.append(pt)
					
		
	# handles projection of data onto eigenvectors and building of data points
	def buildPoints(self, event=None):
		
		if self.objects != []:
			for object in self.objects:
				self.canvas.delete(object)
			self.objects = []
			
		for i in range(3, len(self.labels)):
			self.canvas.delete(self.labels[i])
		labels2 = []
		for i in range(0,3):
			labels2.append(self.labels[i])
		self.labels = labels2			
			
		rows = self.data.get_raw_num_rows()
		columns = self.data.get_num_columns()		
		
		print "X: ", self.selectedHeaders[0]
		print "Y: ", self.selectedHeaders[1]
		print "Z: ", self.selectedHeaders[2]
					 			 		
  		self.axisPoints = np.matrix(np.zeros((rows,4)))
  		homogenousColumn = [1] * self.axisPoints.shape[1]
		self.axisPoints[:] = np.matrix(homogenousColumn)	
		z = -1
		self.zerosMatrix = np.matrix(np.zeros((rows, 4)))
		for j in range(0,3):
			z += 1
			for i in range(0,rows):
				self.axisPoints[i,z] = self.zerosMatrix[0,0]
				
 		z = -1
 		for header in self.selectedHeaders:
 			if z != 3:
				if header != "None" and header != "Apply to x axis" and header != "Apply to y axis" and header != "Apply to z axis":
					column = self.data.get_column(header)
					for i in range(0,rows):
						self.axisPoints[i,z+1] = column[i]
					z += 1
				else:
					pass
			else:
				pass
	 		
  		self.maxAndMins = []
 		for header in self.selectedHeaders:
 			column = self.data.get_column(header)
 			min = np.min(column)
 			max = np.max(column)
 			self.maxAndMins.append(min)
 			self.maxAndMins.append(max)
 		
 		self.mnm = np.matrix([[self.maxAndMins[0],self.maxAndMins[1]], 
 							  [self.maxAndMins[2],self.maxAndMins[3]],
 							  [self.maxAndMins[4],self.maxAndMins[5]]])
 		 		 		
 		z = -1
		if self.selectedHeaders[2] != "None":
			for j in range(0,3):
				z += 1
				for i in range(0,rows):
					self.axisPoints[i,z] = float(self.axisPoints[i,z] - self.mnm[z,0])/float(self.mnm[z,1] - self.mnm[z,0])
		else:
			for j in range(0,2):
				z += 1
				for i in range(0,rows):
					self.axisPoints[i,z] = float(self.axisPoints[i,z] - self.mnm[z,0])/float(self.mnm[z,1] - self.mnm[z,0])
		
		VTM = self.view.build()
		pts = VTM * self.axisPoints.T
		pts = pts.T
		extent = self.view.getExtent()	
				
		red = '#%02x%02x%02x' % (255, 0, 0)  # rgb color
		blue = '#%02x%02x%02x' % (0, 0, 255)  # rgb color
		yellow = '#%02x%02x%02x' % (255, 255, 0)  # rgb color
		green = '#%02x%02x%02x' % (0, 128, 0)  # rgb color
		orange = '#%02x%02x%02x' % (255, 165, 0)  # rgb color
		purple = '#%02x%02x%02x' % (128, 0, 128)  # rgb color
		cyan = '#%02x%02x%02x' % (0, 255, 255)  # rgb color
		fuchsia = '#%02x%02x%02x' % (255, 0, 255)  # rgb color
		grey = '#%02x%02x%02x' % (128, 128, 128)  # rgb color
		olive = '#%02x%02x%02x' % (128, 128, 0)  # rgb color
		paleturquoise = '#%02x%02x%02x' % (175,238,238)  # rgb color
		pink = '#%02x%02x%02x' % (255,192,203)  # rgb color
		lime = '#%02x%02x%02x' % (0,255,0)  # rgb color
		
		black = self.colorOption.get()
				
		if self.selectedColor == "Preselected Colors":		
			# establishes cluster colors
			for i in range(0, rows):
				if self.IDnums[i] == 7:
					color = red
				elif self.IDnums[i] == 19:
					color = cyan
				elif self.IDnums[i] == 12:
					color = fuchsia
				elif self.IDnums[i] == 11:
					color = orange
				elif self.IDnums[i] == 18:
					color = cyan
				elif self.IDnums[i] == 16:
					color = black
				elif self.IDnums[i] == 10:
					color = orange				
				elif self.IDnums[i] == 9:
					color = red				
				elif self.IDnums[i] == 8:
					color = red				
				elif self.IDnums[i] == 17:
					color = black
				elif self.IDnums[i] == 20:
					color = cyan
				elif self.IDnums[i] == 15:
					color = black
				self.noise = random.randint(0,25)
				self.noise2 = random.randint(-20,20)
				if self.IDnums[i] ==8:
					pt = self.canvas.create_oval(pts[i,0]+self.noise2-float(0.3/extent[0,0])+self.noise,pts[i,1]+5-float(0.3/extent[0,1])+self.noise,pts[i,0]+self.noise2+float(0.3/extent[0,0])*20+self.noise,pts[i,1]+5+float(0.3/extent[0,0])*20+self.noise,fill=color, outline = 'black')
					self.objects.append(pt)
				elif self.IDnums[i] == 9:
					pt = self.canvas.create_oval(pts[i,0]+self.noise2-float(0.3/extent[0,0])+self.noise,pts[i,1]+13-float(0.3/extent[0,1])+self.noise,pts[i,0]+self.noise2+float(0.3/extent[0,0])*20+self.noise,pts[i,1]+13+float(0.3/extent[0,0])*20+self.noise,fill=color, outline = 'black')
					self.objects.append(pt)
				elif self.IDnums[i] == 10:
					pt = self.canvas.create_oval(pts[i,0]+self.noise2-float(0.3/extent[0,0])+self.noise,pts[i,1]-10-float(0.3/extent[0,1])+self.noise,pts[i,0]+self.noise2+float(0.3/extent[0,0])*20+self.noise,pts[i,1]-10+float(0.3/extent[0,0])*20+self.noise,fill=color, outline = 'black')
					self.objects.append(pt)
				elif self.IDnums[i] == 11:
					pt = self.canvas.create_oval(pts[i,0]+self.noise2-float(0.3/extent[0,0])+self.noise,pts[i,1]+8-float(0.3/extent[0,1])+self.noise,pts[i,0]+self.noise2+float(0.3/extent[0,0])*20+self.noise,pts[i,1]+8+float(0.3/extent[0,0])*20+self.noise,fill=color, outline = 'black')
					self.objects.append(pt)
				elif self.IDnums[i] == 12:
					pt = self.canvas.create_oval(pts[i,0]+self.noise2-float(0.3/extent[0,0])+self.noise,pts[i,1]-float(0.3/extent[0,1])+self.noise,pts[i,0]+self.noise2+float(0.3/extent[0,0])*20+self.noise,pts[i,1]+float(0.3/extent[0,0])*20+self.noise,fill=color, outline = 'black')
					self.objects.append(pt)
				elif self.IDnums[i] == 7:
					pt = self.canvas.create_oval(pts[i,0]+self.noise2-float(0.3/extent[0,0])+self.noise,pts[i,1]-float(0.3/extent[0,1])+self.noise,pts[i,0]+self.noise2+float(0.3/extent[0,0])*20+self.noise,pts[i,1]+float(0.3/extent[0,0])*20+self.noise,fill=color, outline = 'black')
					self.objects.append(pt)
			########
				elif self.IDnums[i] == 18:
					pt = self.canvas.create_oval(pts[i,0]+12-float(0.3/extent[0,0])+self.noise,pts[i,1]-float(0.3/extent[0,1])+self.noise,pts[i,0]+12+float(0.3/extent[0,0])*20+self.noise,pts[i,1]+float(0.3/extent[0,0])*20+self.noise,fill=color, outline = 'black')
					self.objects.append(pt)
				elif self.IDnums[i] == 16:
					pt = self.canvas.create_oval(pts[i,0]-5-float(0.3/extent[0,0])+self.noise,pts[i,1]+10-float(0.3/extent[0,1])+self.noise,pts[i,0]-5+float(0.3/extent[0,0])*20+self.noise,pts[i,1]+10+float(0.3/extent[0,0])*20+self.noise,fill=color, outline = 'black')
					self.objects.append(pt)
				elif self.IDnums[i] == 17:
					pt = self.canvas.create_oval(pts[i,0]+5-float(0.3/extent[0,0])+self.noise,pts[i,1]-float(0.3/extent[0,1])+self.noise,pts[i,0]+5+float(0.3/extent[0,0])*20+self.noise,pts[i,1]+float(0.3/extent[0,0])*20+self.noise,fill=color, outline = 'black')
					self.objects.append(pt)
				elif self.IDnums[i] == 19:
					pt = self.canvas.create_oval(pts[i,0]-float(0.3/extent[0,0])+self.noise,pts[i,1]-float(0.3/extent[0,1])+self.noise,pts[i,0]+float(0.3/extent[0,0])*20+self.noise,pts[i,1]+float(0.3/extent[0,0])*20+self.noise,fill=color, outline = 'black')
					self.objects.append(pt)
				elif self.IDnums[i] == 15:
					pt = self.canvas.create_oval(pts[i,0]-10-float(0.3/extent[0,0])+self.noise,pts[i,1]-float(0.3/extent[0,1])+self.noise,pts[i,0]-10+float(0.3/extent[0,0])*20+self.noise,pts[i,1]+float(0.3/extent[0,0])*20+self.noise,fill=color, outline = 'black')
					self.objects.append(pt)
				elif self.IDnums[i] == 20:
					pt = self.canvas.create_oval(pts[i,0]-float(0.3/extent[0,0])+self.noise,pts[i,1]-float(0.3/extent[0,1])+self.noise,pts[i,0]+float(0.3/extent[0,0])*20+self.noise,pts[i,1]+float(0.3/extent[0,0])*20+self.noise,fill=color, outline = 'black')
					self.objects.append(pt)						
				else:
					pt = self.canvas.create_oval(pts[i,0]-float(0.3/extent[0,0]),pts[i,1]-float(0.3/extent[0,1]),pts[i,0]+float(0.3/extent[0,0])*20,pts[i,1]+float(0.3/extent[0,0])*20, outline = '')
					self.objects.append(pt)
		else:
			for i in range(0, rows):	
				multiplier = 255/self.K				
				color = '#%02x%02x%02x' % (int(255-int((255 - self.IDnums[i]*multiplier))), int(255-int((255-self.IDnums[i]*multiplier))), int(255-self.IDnums[i]*multiplier))  # rgb color
				pt = self.canvas.create_oval(pts[i,0]-float(0.3/extent[0,0]),pts[i,1]-float(0.3/extent[0,1]),pts[i,0]+float(0.3/extent[0,0])*20,pts[i,1]+float(0.3/extent[0,0])*20,fill=color, outline = '')
				self.objects.append(pt)
					
		
	def handleQuit(self, event=None):
		print 'Terminating'
		self.root.destroy()

	def handleButton1(self):
		print 'handling command button:', self.colorOption.get()
		for obj in self.objects:
			self.canvas.itemconfig(obj, fill=self.colorOption.get() )

	def handleMenuCmd1(self):
		print 'handling menu command 1'

	# Handles mouse button 1 (left click)
	def handleMouseButton1(self, event):
		self.baseClick = (event.x, event.y)
		self.baseView = self.view.clone()
		

	# Handles mouse button 1 motion (left click)
	def handleMouseButton1Motion(self, event):
		# calculate the difference
		dx = float(event.x - self.baseClick[0])
		dy = float(event.y - self.baseClick[1])
		screenSize = self.baseView.screen
		extent = self.baseView.extent
		tv = self.translationVariable.get()
		if tv == "Slow":
			tv = 0.6
		elif tv == "Normal":
			tv = 1
		else:
			tv = 2
		du = (dx * extent[0,0] / screenSize[0,0]) * tv
		dv = (dy * extent[0,1] / screenSize[0,1]) * tv
		vrp = self.baseView.vrp
		viewVrp = self.view.vrp
		dvrp = self.baseView.vrp
		u = self.baseView.u
		vup = self.baseView.vup
		dvrp[0,0] = ((du * u[0,0]) + (dv * vup[0,0]))
		dvrp[0,1] = ((du * u[0,1]) + (dv * vup[0,1]))		
		dvrp[0,2] = ((du * u[0,2]) + (dv * vup[0,2]))
		self.view.vrp[0,0] = (self.view.vrp[0,0] + dvrp[0,0])
		self.view.vrp[0,1] = (self.view.vrp[0,1] + dvrp[0,1])
		self.view.vrp[0,2] = (self.view.vrp[0,2] + dvrp[0,2])
		self.updateAxes()
		self.baseClick = ( event.x , event.y)
		self.updateDataPoints()
		
		
	# Handles mouse button 2 (right click)
	def handleMouseButton2(self, event):
		self.baseClick2 = (event.x, event.y)
		self.baseView = self.view.clone()
		
			
	# Handles mouse button 2 motion 2 (rotation)
	def handleMouseButton2Motion(self, event):
		dx = float(event.x - self.baseClick2[0])
		dy = float(event.y - self.baseClick2[1])
		rv = self.rotationVariable.get()
		
		# user interaction for speed
		if rv == "Normal":
			rv = 0.8
		elif rv == "Slow":
			rv = 0.3
		else:
			rv = 1.5
			
		d0 = float(dx / 200 * math.pi ) * rv
		d1 = float(dy / 200 * math.pi ) * rv
		self.view = self.baseView.clone()
		self.view.rotateVRC(-d0, d1)
		self.orientation.set(self.view.vpn)
		self.updateAxes()
		self.updateDataPoints()
		


	# Handles mouse button 3 (control + right click)
	def handleMouseButton3(self, event):
		self.baseClick = (event.x, event.y)
		self.baseExtent = self.view.extent

	# Handles mouse button 3 motion (scaling)
	def handleMouseButton3Motion(self, event):
		# calculate vertical distance
		dy = float(event.y - self.baseClick[1])
		scale_rate = 0.1
		scale_factor = 1 + scale_rate * dy/20
		sv = self.scalingVariable.get()
		if sv == "Slow":
			scale_factor = 1 + scale_rate * dy/60	
		elif sv == "Normal":
			scale_factor = 1 + scale_rate * dy/20
		else:
			scale_factor = 1 + scale_rate * dy/10
		scale_factor = np.max( [scale_factor, 0.1] )
		scale_factor = np.min( [scale_factor, 3.0] )
		self.view.extent = self.baseExtent * scale_factor
		self.scale.set(scale_factor)
		self.updateAxes()
		self.updateDataPoints()

	
		
####		
###### Axis functions ########
####

	# Builds VTM, multiplies axis endpoints by VTM
	# then creates three new line objects - one for each axis. 
	# Store the axis endpoints and the three line objects
	def buildAxes(self):
		VTM = self.view.build()
		aep = np.matrix(np.zeros((4,6)))
		aep = VTM * self.axes
		for i in range(0, 6, 2):
			line = self.canvas.create_line(aep[0,i], aep[1,i],
								   aep[0,i+1], aep[1,i+1], fill = 'black')	
			self.lines.append(line)
		
		extent = self.view.getExtent()	

		xAxis = self.canvas.create_text(aep[0,1], aep[1,1] + 7, text = 'X', font = ("Verdana",12))
		yAxis = self.canvas.create_text(aep[0,3], aep[1,3] - 7, text = 'Y', font = ("Verdana",12))
		zAxis = self.canvas.create_text(aep[0,5], aep[1,5] + 7, text = 'Z', font = ("Verdana",12))
		# append axes to list ----- EXTENSION 1
		self.labels.append(xAxis)
		self.labels.append(yAxis)
		self.labels.append(zAxis)


	# Builds the VTM, multiplies axis endpoints by VTM, updates coordinates of object
	def updateAxes(self):
		extent = self.view.getExtent()
		VTM = self.view.build()
		aep = np.matrix(np.zeros((4,6)))
		aep = VTM * self.axes
		for i in range(0, 3):
			self.canvas.coords(self.lines[i], aep[0,i*2], aep[1,i*2], aep[0,i*2+1], aep[1,i*2+1])
		# refresh axes labels --- EXTENSION 1									 
		self.canvas.coords(self.labels[0], aep[0,1], aep[1,1] + 7)
		self.canvas.coords(self.labels[1], aep[0,3], aep[1,3] - 7)
		self.canvas.coords(self.labels[2], aep[0,5], aep[1,5] + 7)

		
	# updates data points
	def updateDataPoints(self):
		self.data = data.Data(self.file)
		self.data.read(self.file)
		rows = self.data.get_raw_num_rows()
		
		VTM = self.view.build()
		try:
			pts = VTM * self.axisPoints.T
		except AttributeError:
			pass
		else:
			pts = pts.T
				
		self.gradient = self.gradientOption.get()
		extent = self.view.getExtent()
		
		try:
			if len(self.selectedHeaders) == 3:
				for i in range(0,rows):
					self.canvas.coords(self.objects[i], pts[i,0]-float(0.3/extent[0,0]),pts[i,1]-float(0.3/extent[0,1]),pts[i,0]+float(0.3/extent[0,0])*20,pts[i,1]+float(0.3/extent[0,0])*20)
			else:
				for i in range(0,rows):
					if self.selectedHeaders[4] != "None":
						size = ((30 * self.colorMatrix[i,self.sizeAxis]) + 0.001)
						self.canvas.coords(self.objects[i], pts[i,0]-float(0.3/extent[0,0])*size,pts[i,1]-float(0.3/extent[0,1])*size,pts[i,0]+float(0.3/extent[0,0])*20,pts[i,1]+float(0.3/extent[0,0])*20)
					else:
						self.canvas.coords(self.objects[i], pts[i,0]-float(0.3/extent[0,0]),pts[i,1]-float(0.3/extent[0,1]),pts[i,0]+float(0.3/extent[0,0])*20,pts[i,1]+float(0.3/extent[0,0])*20)
		except IndexError:
			pass

		
	# updates color of points for color extension
	def updateColor(self):
		axis = self.axis
		if self.objects != []:
			try:
				for i in range(0,len(self.objects)):
					if self.selectedHeaders[3] != "None":
						if self.gradientOption.get() == "Green to Red":
							color = '#%02x%02x%02x' % (int(255 * self.colorMatrix[i,axis]), int(255-(255*self.colorMatrix[i,axis])), 0)  # rgb color
						elif self.gradientOption.get() == "Yellow to Blue":
							color = '#%02x%02x%02x' % (int(255-(255 * self.colorMatrix[i,axis])), int(255-(255*self.colorMatrix[i,axis])), int(255*self.colorMatrix[i,axis]))  # rgb color
						elif self.gradientOption.get() == "Blues":
							color = '#%02x%02x%02x' % (0, int(255-(255*self.colorMatrix[i,axis])), 255)  # rgb color
						else:
							color = '#%02x%02x%02x' % (255, int(255-(255*self.colorMatrix[i,axis])), (int(255 * self.colorMatrix[i,axis])))  # rgb color	
						point = self.objects[i]
						loc = self.canvas.coords(point)
						updatedPoint = self.canvas.create_oval(loc[0],loc[1],loc[2],loc[3], fill=color, outline = '')
						self.objects.insert(i,updatedPoint)
						self.objects.remove(point)			
						self.canvas.delete(point)
						self.color = color
					elif self.selectedHeaders[3] == "None":
						if self.gradientOption.get() == "Green to Red":
							color = '#%02x%02x%02x' % (int(255 * self.colorMatrix[i,axis]), int(255-(255*self.colorMatrix[i,axis])), 0)  # rgb color
						elif self.gradientOption.get() == "Yellow to Blue":
							color = '#%02x%02x%02x' % (int(255-(255 * self.colorMatrix[i,axis])), int(255-(255*self.colorMatrix[i,axis])), int(255*self.colorMatrix[i,axis]))  # rgb color
						elif self.gradientOption.get() == "Blues":
							color = '#%02x%02x%02x' % (0, int(255-(255*self.colorMatrix[i,axis])), 255)  # rgb color
						else:
							color = '#%02x%02x%02x' % (255, int(255-(255*self.colorMatrix[i,axis])), (int(255 * self.colorMatrix[i,axis])))  # rgb color
						loc = self.canvas.coords(point)
						updatedPoint = self.canvas.create_oval(loc[0],loc[1],loc[2],loc[3], fill=color, outline = '')
						self.objects.insert(i,updatedPoint)
						self.objects.remove(point)			
						self.canvas.delete(point)
						self.color = color
				self.updateDataPoints()
			except IndexError:
				pass


	# resizes screen
	def resize(self, event=None):
		self.originalWidth = float(self.initDx)
		self.originalHeight = float(self.initDy)
		dwidth = event.width
 		dheight = event.height
		diffw = (self.originalWidth - dwidth)
		diffh = (self.originalHeight - dheight)
		screen = self.view.getScreen()
		if diffw == 0 and diffh == 0:
			exit()
		else:
			self.view.setScreen(np.matrix([((float(screen[0,0])*(dwidth/float(screen[0,0])))-diffw),((float(screen[0,1])*(dheight/float(screen[0,1])))-diffh)]))
			self.updateAxes()
			self.updateDataPoints()
	
		
	#  Resets screen 
	def resetAxes(self, event=None):
		self.view.setVRP(np.matrix([[0.5,0.5,1]]))
		self.view.setVPN(np.matrix([[0,0,-1]]))
		self.view.setVUP(np.matrix([[0,1,0]]))
		self.view.setU(np.matrix([[-1, 0, 0]]))
		self.view.setExtent(np.matrix([[1,1,1]]))
		self.updateAxes()
		self.scale.set(1)
		self.orientation.set(str([[0, 0, -1]]))
		self.updateDataPoints()
		print "Screen Reset"
		
	# sets the view to the xy plane using command x
	def viewXYplane(self, event=None):
		self.resetAxes()
		self.updateAxes()
		self.updateDataPoints()
		print "XY plane view"
	
	# sets view to the xz plane using command z	
	def viewXZplane(self, event=None):
		self.resetAxes()
 		self.view.rotateVRC(0, -math.pi/2)
		self.updateAxes()
		self.updateDataPoints()
		print "XZ plane view"
		
	# sets the view to the yz plane using command y	
	def viewYZplane(self, event=None):
		self.resetAxes()
		self.view.rotateVRC(math.pi/2,-math.pi/2)
		self.updateAxes()
		self.updateDataPoints()
		print "YZ plane view"
			
	# main function	
	def main(self):
		print 'Entering main loop'
		self.root.mainloop()
		
			
class Dialog(tk.Toplevel):

	def __init__(self, parent, headers, title, file, normalize, pcaDict, normDict):

		tk.Toplevel.__init__(self, parent)
		self.transient(parent)

		if title:
			self.title(title)

		self.parent = parent
		self.file = file
		
		self.headers = headers
		self.selectedHeaders = []
		self.selectedColumns = []
		self.selectedPCs = []
		self.evColorSize = []
		self.normalizeBool = normalize
		self.PCAname = None
		self.pcaDict = pcaDict
		self.normDict = normDict
		
		self.result = None
		
		body = tk.Frame(self)
		self.initial_focus = self.body(body)
		body.pack(padx=5, pady=5)
	
		self.handleSelection()
				
		self.grab_set()

		if not self.initial_focus:
			self.initial_focus = self

		self.protocol("WM_DELETE_WINDOW", self.cancel)

		self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
								  parent.winfo_rooty()+50))

		self.initial_focus.focus_set()

		self.wait_window(self)

	#
	# construction hooks

	def body(self, master):
		# create dialog body.  return widget that should have
		# initial focus.  this method should be overridden

		pass
		
		
	# lets the user select which columns of the data to plot
	def handleSelection(self):
		
		layer1 = tk.Frame(self)
		layer2 = tk.Frame(self)
		layer3 = tk.Frame(self)
		layer4 = tk.Frame(self)
		layer5 = tk.Frame(self)
		layer6 = tk.Frame(self)
				
		xLabel = tk.Label(layer1,text = "X axis", width = 17)
		xLabel.pack(side=tk.LEFT)
		self.xBox = tk.Listbox(layer2, selectmode=tk.SINGLE, width = 15, exportselection=0)
		self.xBox.pack(side=tk.LEFT, padx=5, pady=5)

		yLabel = tk.Label(layer1,text = "Y axis", width = 15)
		yLabel.pack(side=tk.LEFT)
		self.yBox = tk.Listbox(layer2, selectmode=tk.SINGLE, width = 15, exportselection=0)
		self.yBox.pack(side=tk.LEFT, padx=5, pady=5)

		zLabel = tk.Label(layer1,text = "Z axis", width = 15)
		zLabel.pack(side=tk.LEFT)
		self.zBox = tk.Listbox(layer2, selectmode=tk.SINGLE, width = 15, exportselection=0)
		self.zBox.pack(side=tk.LEFT, padx=5, pady=5)
		self.zBox.insert(0, "None")
		
		colorLabel = tk.Label(layer1,text = "Color", width = 15)
		colorLabel.pack(side=tk.LEFT)
		self.colorBox = tk.Listbox(layer2, selectmode=tk.SINGLE, width = 15, exportselection=0)
		self.colorBox.pack(side=tk.LEFT, padx=5, pady=5)
		self.colorBox.insert(0, "None")
		
		sizeLabel = tk.Label(layer1,text = "Size", width = 15)
		sizeLabel.pack(side=tk.TOP)
		self.sizeBox = tk.Listbox(layer2, selectmode=tk.SINGLE, width = 15, exportselection=0)
		self.sizeBox.pack(side=tk.LEFT, padx=5, pady=5)
		self.sizeBox.insert(0, "None")
		
		print self.headers.raw_types
		
		try:
			headers = self.headers.get_raw_headers()
		except AttributeError:
			headers = []
				
		# insert headers as selection choices
		for h in headers:
			self.xBox.insert(tk.END, h)
			self.yBox.insert(tk.END, h)
			self.zBox.insert(tk.END, h)
		
		# choices for color and size columns
		xAxis = "Apply to x axis"
		yAxis = "Apply to y axis"
		zAxis = "Apply to z axis"
		self.colorBox.insert(tk.END, xAxis)
		self.colorBox.insert(tk.END, yAxis)
		self.colorBox.insert(tk.END, zAxis)
		self.sizeBox.insert(tk.END, xAxis)
		self.sizeBox.insert(tk.END, yAxis)
		self.sizeBox.insert(tk.END, zAxis)
		

		okButton = tk.Button(layer6, text="OK", command=self.ok)
		okButton.pack(side=tk.LEFT, padx=10, pady=10)
		cancelButton = tk.Button(layer6,text= "Cancel", command = self.cancel)
		cancelButton.pack(side=tk.LEFT, padx=10, pady=10)

		self.bind("<Return>", self.ok)
		self.bind("<Escape>", self.cancel)
		
		layer1.pack()
		layer2.pack()
		layer6.pack()

	#
	# standard button semantics

	def ok(self, event=None):

		if not self.validate():
			self.initial_focus.focus_set() # put focus back
			return
		
		# appends selection to selectedHeaders when OK is pressed
		self.selectedHeaders.append(self.xBox.get(self.xBox.curselection()))
		self.selectedHeaders.append(self.yBox.get(self.yBox.curselection()))
		self.selectedHeaders.append(self.zBox.get(self.zBox.curselection()))
		self.selectedHeaders.append(self.colorBox.get(self.colorBox.curselection()))
		self.selectedHeaders.append(self.sizeBox.get(self.sizeBox.curselection()))		
		
		self.withdraw()
		self.update_idletasks()

		self.apply()
		print "Selected headers: " + str(self.selectedHeaders)
		self.cancel()

	def cancel(self, event=None):

		# put focus back to the parent window
		self.parent.focus_set()
		self.destroy()

	#
	# command hooks

	def validate(self):

		return 1 # override

	def apply(self):

		pass # override


# Derived dialog class that handles PCA
class PCADialog(Dialog):
	def __init__(self, parent, headers, title, file, normalize, pcaDict, normDict):
		Dialog.__init__(self, parent, headers, title, file, normalize, pcaDict, normDict)
			
	# lets the user select which columns of the data to plot
	def handleSelection(self):
		
		layer1 = tk.Frame(self)
		layer2 = tk.Frame(self)
		layer3 = tk.Frame(self)
		layer4 = tk.Frame(self)
		layer6 = tk.Frame(self)
				
		xLabel = tk.Label(layer1,text = "Select Data Columns", width = 17)
		xLabel.pack(side=tk.LEFT)
		self.xBox = tk.Listbox(layer2, selectmode=tk.MULTIPLE, width = 25, exportselection=0)
		self.xBox.pack(side=tk.LEFT, pady=5)		
		
		try:
			headers = self.headers.get_raw_headers()
		except AttributeError:
			headers = []
				
		# insert headers as selection choices
		for h in headers:
			self.xBox.insert(tk.END, h)

		#Extension 1 - ability to name analysis
		nameLabel = tk.Label(layer3, text = "Save as:", width = 7)
		nameLabel.pack(side=tk.LEFT)
		self.PCAname = tk.StringVar()
		self.name = tk.Entry(layer3, textvariable=self.PCAname)
		self.name.pack(side=tk.LEFT)
		
		self.CBSelection = tk.IntVar()
		self.checkButton = tk.Checkbutton(layer4, text="Normalize", variable=self.CBSelection)
		self.checkButton.pack()

		okButton = tk.Button(layer6, text="OK", command=self.ok)
		okButton.pack(side=tk.LEFT, padx=10, pady=10)
		cancelButton = tk.Button(layer6,text= "Cancel", command = self.cancel)
		cancelButton.pack(side=tk.LEFT, padx=10, pady=10)

		self.bind("<Return>", self.ok)
		self.bind("<Escape>", self.cancel)
		
		layer1.pack()
		layer2.pack()
		layer3.pack()
		layer4.pack()
		layer6.pack()

	#
	# standard button semantics

	def ok(self, event=None):

		if not self.validate():
			self.initial_focus.focus_set() # put focus back
			return	

		items = map(int, self.xBox.curselection())
		if len(items) < 3:
			return
		self.selectedColumns = items
		self.PCAname = self.name.get()
		self.pcaDict.update({self.PCAname:self.selectedColumns})
		if self.CBSelection.get() == 0:
			self.normalizeBool = 0
		else:
			self.normalizeBool = 1
		self.normDict.update({self.PCAname:self.normalizeBool})
		
		self.withdraw()
		self.update_idletasks()

		self.apply()
		self.parent.focus_set()
		self.destroy()
		
	def cancel(self, event=None):

		# put focus back to the parent window
		self.parent.focus_set()
		self.destroy()
		
		

# Derived dialog class that handles PCA data table
class PCATableDialog(Dialog):
	def __init__(self, parent, headers, title, file, normalize, pcaDict, normDict):
		Dialog.__init__(self, parent, headers, title, file, normalize, pcaDict, normDict)
			
	# displays data table
	def handleSelection(self):
		
		layer1 = tk.Frame(self)
		layer2 = tk.Frame(self)
		layer3 = tk.Frame(self)
		layer6 = tk.Frame(self)			
		
		d = data.Data(self.file)
		d.read(self.file)
		if self.normalizeBool == 0:
			ap = analysis.pca(d, self.headers, False)
		else:
			ap = analysis.pca(d, self.headers, True)

		evecs = ap.get_eigenvectors()
		evals = ap.get_eigenvalues()
		
		# handles E-vec label
		a = "E-vec"
		m1 = tk.Message(layer1, text=a)
		m1.grid(row=1, column=0, padx = 6)
		# handles E-vals
		b = "E-val"
		m2 = tk.Message(layer1, text=b)
		m2.grid(row=1, column=1, padx = 6)
		for i in range(0, len(self.headers)):
			c = str(evals[i])
			m3 = tk.Message(layer1, text=c)
			m3.grid(row=i+2, column=1)
		# cumulative calculation	
		d = "Cumulative"
		m4 = tk.Message(layer1, text=d)
		m4.grid(row=1, column=2, padx=6)
		self.total = 0
		cumulativeList = []
		for eval in evals:
			self.total = self.total + eval
		for eval in evals:
			listEntry = eval/self.total
			cumulativeList.append(listEntry)
		index = 1
		while index != len(cumulativeList):
			cumulativeList[index] = cumulativeList[index] + cumulativeList[index-1]
			index += 1
		for i in range(0, len(self.headers)):
			e = str(cumulativeList[i])
			m5 = tk.Message(layer1, text=e)
			m5.grid(row=i+2, column=2, padx=6)
		# handles E-vecs and headers
		for i in range(0, len(self.headers)):
			f = str(self.headers[i])
			m6 = tk.Message(layer1, text=f, borderwidth=8)
			m6.grid(row=1, column=i+3, padx=6)
			g = "P0" + str(i)
			if i >= 10:
				g = "P" + str(i)
			m7 = tk.Message(layer1, text=g)
			m7.grid(row=i+2, column=0)
		# handles eigenvectors
		for i in range(0, len(self.headers)):
			for j in range(0, len(self.headers)):
				h = str(evecs[i,j])
				m8 = tk.Message(layer1, text=h)
				m8.grid(row=i+2, column=j+3)
			
		
		# insert headers as selection choices

		okButton = tk.Button(layer6, text="OK", command=self.ok)
		okButton.pack(side=tk.LEFT, padx=10, pady=10)

		self.bind("<Return>", self.ok)
		self.bind("<Escape>", self.cancel)
		
		layer1.pack()
		layer2.pack()
		layer3.pack()
		layer6.pack()

	#
	# standard button semantics

	def ok(self, event=None):

		if not self.validate():
			self.initial_focus.focus_set() # put focus back
			return

		self.withdraw()
		self.update_idletasks()

		self.apply()
		self.cancel()
		
	def cancel(self, event=None):

		# put focus back to the parent window
		self.parent.focus_set()
		self.destroy()


# Derived dialog class that handles PCA projection onto eigenvectors
class ProjectionDialog(Dialog):
	def __init__(self, parent, headers, title, file, normalize, pcaDict, normDict):
		Dialog.__init__(self, parent, headers, title, file, normalize, pcaDict, normDict)
		
	# lets the user select onto which eigenvectors to project
	def handleSelection(self):
		
		layer1 = tk.Frame(self)
		layer2 = tk.Frame(self)
		layer6 = tk.Frame(self)
				
		p00 = tk.Label(layer1,text = "p00", width = 17)
		p00.pack(side=tk.LEFT)
		self.p00box = tk.Listbox(layer2, selectmode=tk.SINGLE, width = 15, exportselection=0)
		self.p00box.pack(side=tk.LEFT, padx=5, pady=5)

		p01 = tk.Label(layer1,text = "p01", width = 15)
		p01.pack(side=tk.LEFT)
		self.p01box = tk.Listbox(layer2, selectmode=tk.SINGLE, width = 15, exportselection=0)
		self.p01box.pack(side=tk.LEFT, padx=5, pady=5)

		p02 = tk.Label(layer1,text = "p02", width = 15)
		p02.pack(side=tk.LEFT)
		self.p02box = tk.Listbox(layer2, selectmode=tk.SINGLE, width = 15, exportselection=0)
		self.p02box.pack(side=tk.LEFT, padx=5, pady=5)
		
		colorLabel = tk.Label(layer1,text = "Color", width = 15)
		colorLabel.pack(side=tk.LEFT)
		self.colorBox = tk.Listbox(layer2, selectmode=tk.SINGLE, width = 15, exportselection=0)
		self.colorBox.pack(side=tk.LEFT, padx=5, pady=5)
		self.colorBox.insert(0, "None")
		
		sizeLabel = tk.Label(layer1,text = "Size", width = 15)
		sizeLabel.pack(side=tk.TOP)
		self.sizeBox = tk.Listbox(layer2, selectmode=tk.SINGLE, width = 15, exportselection=0)
		self.sizeBox.pack(side=tk.LEFT, padx=5, pady=5)
		self.sizeBox.insert(0, "None")
				
		print str(self.headers) + " Available headers"
				
		# insert headers as selection choices
		for h in self.headers:
			self.p00box.insert(tk.END, h)
			self.p01box.insert(tk.END, h)
			self.p02box.insert(tk.END, h)
		
		# choices for color and size columns
		xAxis = "Apply to x axis"
		yAxis = "Apply to y axis"
		zAxis = "Apply to z axis"
		self.colorBox.insert(tk.END, xAxis)
		self.colorBox.insert(tk.END, yAxis)
		self.colorBox.insert(tk.END, zAxis)
		self.sizeBox.insert(tk.END, xAxis)
		self.sizeBox.insert(tk.END, yAxis)
		self.sizeBox.insert(tk.END, zAxis)
		

		okButton = tk.Button(layer6, text="OK", command=self.ok)
		okButton.pack(side=tk.LEFT, padx=10, pady=10)
		cancelButton = tk.Button(layer6,text= "Cancel", command = self.cancel)
		cancelButton.pack(side=tk.LEFT, padx=10, pady=10)

		self.bind("<Return>", self.ok)
		self.bind("<Escape>", self.cancel)
		
		layer1.pack()
		layer2.pack()
		layer6.pack()

	#
	# standard button semantics

	def ok(self, event=None):

		if not self.validate():
			self.initial_focus.focus_set() # put focus back
			return
		
		# appends selection to selectedHeaders when OK is pressed
		self.selectedPCs.append(self.p00box.get(self.p00box.curselection()))
		self.selectedPCs.append(self.p01box.get(self.p01box.curselection()))
		self.selectedPCs.append(self.p02box.get(self.p02box.curselection()))
		self.evColorSize.append(self.colorBox.get(self.colorBox.curselection()))
		self.evColorSize.append(self.sizeBox.get(self.sizeBox.curselection()))	
		
		self.withdraw()
		self.update_idletasks()

		self.apply()
		self.cancel()



class BuildClusterDialog(tk.Toplevel):

	def __init__(self, parent, headers, title, file):

		tk.Toplevel.__init__(self, parent)
		self.transient(parent)

		if title:
			self.title(title)

		self.parent = parent
		self.file = file
		
		self.headers = headers
		self.selectedHeaders = []
		self.selectedColumns = []
		self.selectedClassifier = None
		self.selectedColor = None
		self.selectedMetric = None
		self.selectedPCs = []	
				
		body = tk.Frame(self)
		self.initial_focus = self.body(body)
		body.pack(padx=5, pady=5)
	
		self.handleSelection()
				
		self.grab_set()

		if not self.initial_focus:
			self.initial_focus = self

		self.protocol("WM_DELETE_WINDOW", self.cancel)

		self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
								  parent.winfo_rooty()+50))

		self.initial_focus.focus_set()

		self.wait_window(self)

	#
	# construction hooks

	def body(self, master):
		# create dialog body.  return widget that should have
		# initial focus.  this method should be overridden

		pass
		
		
	# lets the user select which columns of the data to plot
	def handleSelection(self):
		
		layer1 = tk.Frame(self)
		layer2 = tk.Frame(self)
		layer3 = tk.Frame(self)
		layer4 = tk.Frame(self)
		layer5 = tk.Frame(self)
		layer6 = tk.Frame(self)
				
		xLabel = tk.Label(layer1,text = "X axis", width = 17)
		xLabel.pack(side=tk.LEFT)
		self.xBox = tk.Listbox(layer2, selectmode=tk.SINGLE, width = 15, exportselection=0)
		self.xBox.pack(side=tk.LEFT, padx=5, pady=5)

		yLabel = tk.Label(layer1,text = "Y axis", width = 15)
		yLabel.pack(side=tk.LEFT)
		self.yBox = tk.Listbox(layer2, selectmode=tk.SINGLE, width = 15, exportselection=0)
		self.yBox.pack(side=tk.LEFT, padx=5, pady=5)

		zLabel = tk.Label(layer1,text = "Z axis", width = 15)
		zLabel.pack(side=tk.LEFT)
		self.zBox = tk.Listbox(layer2, selectmode=tk.SINGLE, width = 15, exportselection=0)
		self.zBox.pack(side=tk.LEFT, padx=5, pady=5)
		self.zBox.insert(0, "None")
			
		colorLabel = tk.Label(layer1,text = "Color", width = 15)
		colorLabel.pack(side=tk.LEFT)
		self.colorBox = tk.Listbox(layer2, selectmode=tk.SINGLE, width = 20, exportselection=0)
		self.colorBox.pack(side=tk.LEFT, padx=5, pady=5)

		try:
			headers = self.headers.get_raw_headers()
		except AttributeError:
			headers = []
		
		print str(headers) + " Available headers"
		
		# insert headers as selection choices
		for h in headers:
			self.xBox.insert(tk.END, h)
			self.yBox.insert(tk.END, h)
			self.zBox.insert(tk.END, h)
		
		c1 = "Preselected Colors"
		c2 = "Smooth Color Scheme"
		self.colorBox.insert(tk.END, c1)
		self.colorBox.insert(tk.END, c2)

		nameLabel = tk.Label(layer3, text = "Number of clusters:", width = 16)
		nameLabel.pack(side=tk.TOP)
		self.number = tk.IntVar()
		self.number.set(1)
		self.name = tk.Entry(layer3, textvariable=self.number, width=10)
		self.name.pack(side=tk.BOTTOM)	
	
		okButton = tk.Button(layer6, text="OK", command=self.ok)
		okButton.pack(side=tk.LEFT, padx=10, pady=10)
		cancelButton = tk.Button(layer6,text= "Cancel", command = self.cancel)
		cancelButton.pack(side=tk.LEFT, padx=10, pady=10)

		self.bind("<Return>", self.ok)
		self.bind("<Escape>", self.cancel)
		
		layer1.pack()
		layer2.pack()
		layer3.pack()
		layer6.pack()

	#
	# standard button semantics

	def ok(self, event=None):

		if not self.validate():
			self.initial_focus.focus_set() # put focus back
			return
		
		# appends selection to selectedHeaders when OK is pressed
		self.selectedHeaders.append(self.xBox.get(self.xBox.curselection()))
		self.selectedHeaders.append(self.yBox.get(self.yBox.curselection()))
		self.selectedHeaders.append(self.zBox.get(self.zBox.curselection()))
		self.number = self.name.get()
		self.selectedColor = self.colorBox.get(self.colorBox.curselection())
		
		self.withdraw()
		self.update_idletasks()

		self.apply()
		print "Selected headers: " + str(self.selectedHeaders)
		self.cancel()

	def cancel(self, event=None):

		# put focus back to the parent window
		self.parent.focus_set()
		self.destroy()

	#
	# command hooks

	def validate(self):

		return 1 # override

	def apply(self):

		pass # override

# Derived dialog class that handles PCA projection onto eigenvectors
class PCAClassify(BuildClusterDialog):
	def __init__(self, parent, headers, title, file):
		BuildClusterDialog.__init__(self, parent, headers, title, file)
		
	# lets the user select onto which eigenvectors to project
	def handleSelection(self):
		
		layer1 = tk.Frame(self)
		layer2 = tk.Frame(self)
		layer6 = tk.Frame(self)
		
		try:
			headers = self.headers.get_raw_headers()
		except AttributeError:
			headers = []	
						
		p00 = tk.Label(layer1,text = "X Axis", width = 17)
		p00.pack(side=tk.LEFT)
		self.p00box = tk.Listbox(layer2, selectmode=tk.SINGLE, width = 15, exportselection=0)
		self.p00box.pack(side=tk.LEFT, padx=5, pady=5)

		p01 = tk.Label(layer1,text = "Y Axis", width = 15)
		p01.pack(side=tk.LEFT)
		self.p01box = tk.Listbox(layer2, selectmode=tk.SINGLE, width = 15, exportselection=0)
		self.p01box.pack(side=tk.LEFT, padx=5, pady=5)

		p02 = tk.Label(layer1,text = "Z Axis", width = 15)
		p02.pack(side=tk.LEFT)
		self.p02box = tk.Listbox(layer2, selectmode=tk.SINGLE, width = 15, exportselection=0)
		self.p02box.pack(side=tk.LEFT, padx=5, pady=5)
		self.p02box.insert(0, "None")

					
		# insert headers as selection choices
		for h in headers:
			self.p00box.insert(tk.END, h)
			self.p01box.insert(tk.END, h)
			self.p02box.insert(tk.END, h)
		
		colorLabel = tk.Label(layer1,text = "Color", width = 15)
		colorLabel.pack(side=tk.LEFT)
		self.colorBox = tk.Listbox(layer2, selectmode=tk.SINGLE, width = 20, exportselection=0)
		self.colorBox.pack(side=tk.LEFT, padx=5, pady=5)
		
		c1 = "Preselected Colors"
		c2 = "Smooth Color Scheme"
		self.colorBox.insert(tk.END, c1)
		self.colorBox.insert(tk.END, c2)
		
		okButton = tk.Button(layer6, text="OK", command=self.ok)
		okButton.pack(side=tk.LEFT, padx=10, pady=10)
		cancelButton = tk.Button(layer6,text= "Cancel", command = self.cancel)
		cancelButton.pack(side=tk.LEFT, padx=10, pady=10)

		self.bind("<Return>", self.ok)
		self.bind("<Escape>", self.cancel)
		
		layer1.pack()
		layer2.pack()
		layer6.pack()

	#
	# standard button semantics

	def ok(self, event=None):

		if not self.validate():
			self.initial_focus.focus_set() # put focus back
			return
		
		# appends selection to selectedHeaders when OK is pressed
		self.selectedPCs.append(self.p00box.get(self.p00box.curselection()))
		self.selectedPCs.append(self.p01box.get(self.p01box.curselection()))
		self.selectedPCs.append(self.p02box.get(self.p02box.curselection()))	
		self.selectedColor = self.colorBox.get(self.colorBox.curselection())
		
		self.withdraw()
		self.update_idletasks()

		self.apply()
		self.cancel()
		
	def cancel(self, event=None):

		# put focus back to the parent window
		self.parent.focus_set()
		self.destroy()

if __name__ == "__main__":	
	dapp = DisplayApp(1200, 675)
	dapp.main()