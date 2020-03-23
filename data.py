# file: data.py
# author: Luc Yuki Marrie
# date: 3/30/2015
# class: CS251

import csv
import sys
import analysis

class Data:
	
	# Data class constructor method
	def __init__(self, filename):
	
		self.filename = file(filename, 'r')
		self.read(filename)
	
	# Reads in data from file
	def read(self, filename):
		
		# read through lines
		self.filename = file(filename, 'r')
		lines = self.filename.readlines()
		
# list of all headers
# 		self.raw_headers = lines[0].rstrip().split(';')
# 		
# list of all types
# 		self.raw_types = lines[1].rstrip().split(';')
# 		
# list of lists of data, each row is a list of strings
# 		self.raw_data = []
# 		for i in range(2, len(lines)):
# 			data = lines[i].lstrip().split(';')
# 			self.raw_data.append(data)
			
		# list of all headers
		self.raw_headers = lines[0].rstrip().split(',')
		
		# list of all types
		self.raw_types = lines[1].rstrip().split(',')
		
		# list of lists of data, each row is a list of strings
		self.raw_data = []
		for i in range(2, len(lines)):
			data = lines[i].lstrip().split(',')
			self.raw_data.append(data)
			
		# dictionary mapping header string to index of column in raw data
		self.header2raw = dict()
		for i in range (0, len(self.raw_headers)):
			self.header2raw.update({self.raw_headers[i]:i})


		# increments columns variable when column has numeric data
		columns = 0
		for column in self.raw_types:
			if column == "numeric":
				columns += 1 
		
		# matrix of numeric data
		self.matrix_data = np.matrix(np.zeros((len(self.raw_data),columns)))
	# Code to convert string data in numeric column to numbers
		rdx = -1
		i = -1
		
		rows = self.get_raw_num_rows()
		types = self.get_raw_types()
		for type in types:
			i += 1
			if type == "numeric":
				rdx += 1
				for j in range(0, rows):
					self.matrix_data[j,rdx] = self.raw_data[j][i]
		
		# dictionary mapping header string to index of column in matrix data
		self.header2matrix = dict()
		index = 0
		for i in range(0, len(self.raw_types)):
			if self.raw_types[i] == "numeric":
				self.header2matrix.update({self.raw_headers[i]:index})
				index += 1
		
	## Accessor Methods ##
	
	# Returns a list of all of the headers
	def get_raw_headers(self):
		return self.raw_headers
	
	# Returns a list of all of the types
	def get_raw_types(self):
		return self.raw_types
	
	# Returns the number of columns in the raw data set
	def get_raw_num_columns(self):
		return len(self.raw_data[0])
		
	# Returns the number of rows in the data set
	def get_raw_num_rows(self):
		return len(self.raw_data)
	
	# Returns a row of data (the type is list) (Note: since there will be the same number of rows
	# in the raw and numerica data, Stephanie is writing just one method and isn't added the name raw to this one.
	def get_raw_row(self, i):
		return self.raw_data[i]

	# Takes a row index (an int) and column header (a string) and returns the raw data at that location. 
	# (The return type will be a string)
	def get_raw_value(self, i, header): 
		column = self.header2raw[header];
		return self.raw_data[i][column]
		
    # prints data to command line
	def print_data(self):
		for i in range(0, len(self.raw_headers)):
			print self.raw_headers[i],
		for i in range(0, len(self.raw_data)):
			for j in range(0, len(self.raw_data[i])):
				print self.raw_data[i][j],
				
	# list of headers of columns with numeric data			
	def get_headers(self):
		headers = []
		for i in range(0, len(self.raw_headers)):
			if self.raw_types[i] == "numeric":
				headers.append(self.raw_headers[i])
		return headers
		
	# returns the number of columns of numeric data
	def get_num_columns(self):
		columns = 0
		for column in self.raw_types:
			if column == "numeric":
				columns += 1 
		return columns
	
	# returns number of rows of numeric data
	def get_num_rows(self):
		shape = self.matrix_data.shape
		return shape[0]
	
	# take a row index and returns a row of numeric data
	def get_row(self, i):
		return self.matrix_data[i,:]
	
	def get_column(self, i):
		return self.matrix_data[:,i]
			
    # takes in a column header and returns matrix with data USE THIS ONE
	def get_column(self,header):
		if header != "None" and header != "Apply to x axis" and header != "Apply to y axis" and header != "Apply to z axis":
			column = self.header2matrix[header]
			return self.matrix_data[:,column]
		else:
			pass


	# takes a row index (int) and column header (string) and returns 
	# the data in the numeric matrix.
	def get_value(self, rowIndex, header):
		column = self.header2matrix[header]
		return self.matrix_data.item((rowIndex, column))
	
	# At a minimum, this should take a list of columns headers and return a matrix
	# with the data for all rows but just the specified columns. It is optional to also
	# allow the caller to specify a specific set of rows.
	def get_data(self, headers, rows = None): 
		list = []
		if rows != None:
			for header in headers:
				list.append(self.header2matrix[header])
			Matrix = self.matrix_data[(np.meshgrid(rows, list))]
			Matrix = Matrix.T
			return Matrix
		else:
			rows = []
			numRows = self.get_raw_num_rows()
			for i in range(0, numRows):
				rows.append(i)
			for header in headers:
				if header != "None":
					list.append(self.header2matrix[header])	
				else:
					pass
			Matrix = self.matrix_data[np.ix_(rows, list)]
			return Matrix
		
    # returns all the data stored in the matrix
	def get_all_data(self):
		return self.matrix_data			
		
# 	def add_column(self, header, type, data):
# 		self.raw_headers.append(header)
# 		self.raw_types.append(type)
# 		self.header2raw.update({header: len(self.get_raw_headers())})
# 		for i in range(0, len(self.raw_data)):
# 			self.raw_data[i].append(data[i])		
 		
	def add_column(self, header, type, data):
		self.raw_headers.append(header)
		self.raw_types.append(type)
		self.header2raw.update({header: len(self.get_raw_headers())})
		self.header2matrix.update({header: len(self.get_raw_headers())})
		for i in range(0, len(self.raw_data)):
			self.raw_data[i].append(data[i,0])
		self.matrix_data = np.matrix(self.raw_data)
		
	
			
	# Add a write function to your Data class, enabling you to write out
	# a selected set of headers to a specified file. The function should 
	# take in a filename and an optional list of the headers of the columns 
	# to write to the file. If you have not already done so, you should probably 
	# also give your Data object the ability to add a column of data.			
	def write(self, filename, headers=None):
		b = open(filename, 'wb')
		a = csv.writer(b)
		# this will overwrite the original csv file and replace it with just the headers you want
		data = None
		rows = len(self.get_data(headers[0]))
  		data = np.matrix(np.zeros((rows,len(headers))))
		for header in headers:
			data.add_column(header)
		for i in range(0, rows):
			for j in range(0, len(headers)):
				data[i,j] = self.get_data(headers[i,0])
		a.writerows(data)
		b.close()		
			

# PCA analysis class
class PCAData(Data):
	def __init__(self, headers, pdata, evals, evecs, means ):
		self.headers = headers
		self.pdata = pdata
		self.evals = evals
		self.evecs = evecs
		self.means = means
		
		self.raw_headers = []
		for i in range(0, len(self.headers)):
			self.raw_headers.append("P0" + str(i))
			
		self.raw_types = []
		for i in range(0, len(self.raw_headers)):
			self.raw_types.append("numeric")
						
		self.raw_data = pdata
		self.matrix_data = self.pdata
		self.header2matrix = dict()
		index = 0
		for i in range(0, len(self.raw_headers)):
			if self.raw_types[0] == "numeric":
				self.header2matrix.update({self.raw_headers[i]:index})
				index += 1

		
	# returns a copy of the eigenvalues as a single-row numpy matrix.
	def get_eigenvalues(self):
		return self.evals
	
	# returns a copy of the eigenvectors as a numpy matrix with the eigenvectors as columns.
	def get_eigenvectors(self):
		return self.evecs
	
	# returns the means for each column in the original data as a single row numpy matrix.
	def get_data_means(self):
		return self.means
	
	# returns a copy of the list of the headers from the original data used to generate the projected data.	
	def get_data_headers(self):
		return self.headers
	
# Cluster analysis class	
class ClusterData(Data):
	def __init__(self, data, headers, K, means, IDnums, data_rows, metric):
		self.headers = headers
		self.K = K
		self.means = means
		self.IDnums = IDnums
		self.data_rows = data_rows
		self.metric = metric
		
		self.raw_headers = []
		for i in range(0, len(self.headers)):
			self.raw_headers.append(self.headers[i])
			
		self.raw_types = []
		for i in range(0, len(self.raw_headers)):
			self.raw_types.append("numeric")
						
		self.raw_data = self.data_rows
		self.matrix_data = data
		
		self.headers = self.raw_headers
		
		self.header2raw = dict()
		for i in range (0, len(self.raw_headers)):
			self.header2raw.update({self.raw_headers[i]:i})
			
		self.header2matrix = dict()
		index = 0
		for i in range(0, len(self.raw_headers)):
			if self.raw_types[0] == "numeric":
				self.header2matrix.update({self.raw_headers[i]:index})
				index += 1
		
	# returns K
	def get_K(self):
		return self.K
	
	# returns IDnums
	def get_IDnums(self):
		return self.IDnums

	# returns means
	def get_means(self):
		return self.means
