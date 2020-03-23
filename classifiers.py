# Template by Bruce Maxwell
# Spring 2015
# CS 251 Project 8
#
# Classifier class and child definitions

import sys
import data
import analysis as an
import numpy as np
import math
import scipy.spatial.distance as ssd

class Classifier:

	def __init__(self, type):
		'''The parent Classifier class stores only a single field: the type of
		the classifier.	 A string makes the most sense.

		'''
		self._type = type

	def type(self, newtype = None):
		'''Set or get the type with this function'''
		if newtype != None:
			self._type = newtype
		return self._type

	def confusion_matrix( self, truecats, classcats ):
		'''Takes in two Nx1 matrices of zero-index numeric categories and
		computes the confusion matrix. The rows represent true
		categories, and the columns represent the classifier output.

		'''
		unique, mapping = np.unique( np.array(truecats.T), return_inverse=True)
		unique2, mapping2 = np.unique( np.array(classcats.T), return_inverse=True)
		u_length = len(unique)
		
		# build matrix that is length of unique by length of unique 
		matrix = np.matrix(np.zeros((u_length, u_length)))
		
		# increment parts of the matrix according to mapping 
		for i in range(0, len(mapping)):
			matrix[mapping[i], mapping2[i]] += 1
	
		return matrix, unique

	def confusion_matrix_str( self, cmtx, unique ):
		'''Takes in a confusion matrix and returns a string suitable for printing.'''
		for i in range(0, len(unique)):
			s = 'Cluster %d' % (i)
			for j in range(0,len(unique)):
				s += "%10d" % (int(cmtx.T[i,j]))
			print s
		print "\n"			
	def __str__(self):
		'''Converts a classifier object to a string.  Prints out the type.'''
		return str(self._type)
		print self._type


class NaiveBayes(Classifier):
	'''NaiveBayes implements a simple NaiveBayes classifier using a
	Gaussian distribution as the pdf.

	'''

	def __init__(self, dataObj=None, headers=[], categories=None):
		'''Takes in a Data object with N points, a set of F headers, and a
		matrix of categories, one category label for each data point.'''

		# call the parent init with the type
		Classifier.__init__(self, 'Naive Bayes Classifier')
		
		self.num_classes = None
		self.features = None
		self.class_labels = None
		self.headers = headers
		# unique data for the Naive Bayes: means, variances, scales
		self.class_means = None
		self.variances = None
		self.scales = None
		
		# if given data,
		if dataObj != None:
			self.headers = dataObj.get_headers()
			A = dataObj.get_all_data()
			A = A[:,-1]
			if categories == None:
				categories = A
				self.headers.remove(self.headers[-1])
			A = dataObj.get_data(self.headers)
			self.build(A, categories)
			# call the build function

	def build( self, A, categories ):
		'''Builds the classifier given the data points in A and the categories'''
		
		# figure out how many categories there are and get the mapping (np.unique)
		unique, mapping = np.unique( np.array(categories.T), return_inverse=True)
		self.unique1, self.mapping1 = np.unique( np.array(categories.T), return_inverse=True)
		
		# number of classes and number of features		
		self.num_classes = len(unique)
		self.features = A.shape[1]
		# original class labels
		self.class_labels = unique[mapping]
		
		
		C = len(unique)
		F = self.features
		# create the matrices for the means, vars, and scales
		self.class_means = np.matrix(np.zeros((C, F)))
		self.class_vars = np.matrix(np.zeros((C, F)))
		self.class_scales = np.matrix(np.zeros((C, F)))
		
		# compute the means/vars/scales for each class
		# loop through categories, calculate means and variances
		for i in range(0, C):
			indexes = np.where(categories==unique[i])[0]
			data = A[indexes.tolist()[0],:]
			mean = np.mean(np.array(data), axis=0)
			var = np.var(np.array(data), axis=0, ddof=1)
			self.class_means[i,:] = mean
			self.class_vars[i,:] = var
			
		# calculates class scales
		for i in range(0, C):
			for j in range(0, F):
				self.class_scales[i,j] = 1/(math.sqrt(2*math.pi*self.class_vars[i,j]))
				
		# store any other necessary information: # of classes, # of features, original labels
				
		self.num_classes = C
		self.features = F
		self.class_labels = unique[mapping]
		
		return self.class_means, self.class_vars, self.class_scales

	def classify( self, A, return_likelihoods=False ):
		'''Classify each row of A into one category. Return a matrix of
		category IDs in the range [0..C-1], and an array of class
		labels using the original label values. If return_likelihoods
		is True, it also returns the NxC likelihood matrix.

		'''

		N = A.shape[0]
		C = self.num_classes
		P = np.matrix(np.zeros((N, C))) 
		
		# calculate the probabilities by looping over the classes
		#  with numpy-fu you can do this in one line inside a for loop
		
		for i in range(0, N):
			for j in range(0, C):
				P[i,j] = np.prod(np.multiply(self.class_scales[j,:],np.exp(np.dot(-1, np.divide(np.square(A[i,:]-self.class_means[j,:]), np.dot(self.class_vars[j,:], 2))))))
		
		# calculate the most likely class for each data point
		cats = np.argmax(P, axis=1)
		# use the class ID as a lookup to generate the original labels
		labels = self.class_labels[cats]

		if return_likelihoods:
			return cats, labels, P

		return cats, labels

	def __str__(self):
		'''Make a pretty string that prints out the classifier information.'''
		s = "\nNaive Bayes Classifier\n"
		for i in range(self.num_classes):
			s += 'Class %d --------------------\n' % (i)
			s += 'Mean	: ' + str(self.class_means[i,:]) + "\n"
			s += 'Var	: ' + str(self.class_vars[i,:]) + "\n"
			s += 'Scales: ' + str(self.class_scales[i,:]) + "\n"

		s += "\n"
		return s
		
	def write(self, filename):
		'''Writes the Bayes classifier to a file.'''
		# extension
		return

	def read(self, filename):
		'''Reads in the Bayes classifier from the file'''
		# extension
		return

	
class KNN(Classifier):

	def __init__(self, dataObj=None, headers=[], categories=None, K=None):
		'''Take in a Data object with N points, a set of F headers, and a
		matrix of categories, with one category label for each data point.'''
		Classifier.__init__(self, 'KNN Classifier')
		
		self.headers = headers
		self.classes = None
		self.features = None		
		self.class_labels = None
		self.exemplars = []
		if dataObj != None:
			self.headers = dataObj.get_headers()
			A = dataObj.get_all_data()
			A = A[:,-1]
			if categories == None:
				categories = A
				self.headers.remove(self.headers[-1])
			A = dataObj.get_data(self.headers)
			self.build(A, categories)
							

	def build( self, A, categories, K = None ):
		'''Builds the classifier give the data points in A and the categories'''

		unique, mapping = np.unique( np.array(categories.T), return_inverse=True)
		self.unique1, self.mapping1 = np.unique( np.array(categories.T), return_inverse=True)
		self.num_classes = len(unique)
		self.class_labels = unique[mapping]
		C = len(unique)
		# for each category i, build the set of exemplars
		for i in range(0, C):
			if K == None:
				indexes = np.where(categories==unique[i])[0]
				data = A[indexes.tolist()[0],:]
				self.exemplars.append(data)
			else:
				# run K-means on the rows of A where the category/mapping is i
				codebook, codes, error = an.kmeans(A[(unique[mapping]==unique[i]),:], self.headers, K, whiten=False, categories='')
				self.exemplars.append(codebook)
		return

	def classify(self, A, K=3, return_distances=False):
		'''Classify each row of A into one category. Return a matrix of
		category IDs in the range [0..C-1], and an array of class
		labels using the original label values. If return_distances is
		True, it also returns the NxC distance matrix.

		The parameter K specifies how many neighbors to use in the
		distance computation. The default is three.'''

		# error check to see if A has the same number of columns as the class means
		N = A.shape[0]
		C = self.num_classes 
		
		D = np.matrix(np.zeros((N, C)))
				
		for i in range(0, C):
			temp = np.asmatrix(ssd.cdist(A, self.exemplars[i], 'seuclidean'))
			temp.sort(axis=1)
			D[:,i] = temp[:,:K].sum(axis=1)

		# calculate the most likely class for each data point
		cats = np.argmin(D, axis=1)

		unique_cats, mapping_cats = np.unique( np.array(cats.T), return_inverse=True)
		# use the class ID as a lookup to generate the original labels
		labels = self.class_labels[cats]
		if return_distances:
			return cats, labels, D
		return cats, labels


	def __str__(self):
		'''Make a pretty string that prints out the classifier information.'''
		s = "\nKNN Classifier\n"
		for i in range(self.num_classes):
			s += 'Class %d --------------------\n' % (i)
			s += 'Number of Exemplars: %d\n' % (self.exemplars[i].shape[0])
			s += 'Mean of Exemplars	 :' + str(np.mean(self.exemplars[i], axis=0)) + "\n"

		s += "\n"
		return s


	def write(self, filename):
		'''Writes the KNN classifier to a file.'''
		# extension
		return

	def read(self, filename):
		'''Reads in the KNN classifier from the file'''
		# extension
		return
	
