# file: analysis.py
# author: Luc Yuki Marrie
# date: 4/6/2015
# class: CS251

import sys
import data
import scipy.stats
import numpy as np
import random
import scipy.cluster.vq as vq
import scipy.spatial.distance as ssd


# All analysis functions will take lists of strings (column headers) to specify what (numeric) data to analyze.

# Takes in a list of column headers and the Data object and returns a list of 2-element 
# lists with the minimum and maximum values for each column. The function is required to work
# only on numeric data types.
def data_range(headers, data):
	values = [] 
	min = np.min(data)
	max = np.max(data)
	values.append([min, max])
	return values


# Takes in a list of column headers and the Data object and returns a list
# of the mean values for each column. Use the built-in numpy functions to execute this calculation.
def mean(headers, data):
	output = []
	mean = np.average(data)
	output.append(mean)
	return output


# Takes in a list of column headers and the Data object and returns a list of
# the standard deviation for each specified column. Use the built-in numpy functions
# to execute this calculation.
def stdev(headers, data):
	output = []
	stdev = np.std(data)
	output.append(stdev)
	return output
	

# Takes in a list of column headers and the Data object and returns a matrix with
# each column normalized so its minimum value is mapped to zero and its 
# maximum value is mapped to 1.
def normalize_columns_separately(d, headers):
	data = d.get_data(headers)
	dmax = np.max(data, axis=0)
	dmin = np.min(data, axis=0)
	return (data - dmin)/(dmax-dmin)
	


# Takes in a list of column headers and the Data object and returns a matrix
# with each entry normalized so that the minimum value (of all the data in this set of columns)
# is mapped to zero and its maximum value is mapped to 1.
def normalize_columns_together(headers, data):
	
	matrix = np.matrix(np.zeros((np.matrix.size(data,len(headers)))))
	for header in headers:
		min = np.min(header)
		max = np.max(header)
		for i in range(0, len(data)):
			norm_value = ((data[i, header]-min)/(max-min))
			matrix[i, header] = norm_value
	return matrix


def linear_regression(d, ind, dep):
	rows = d.get_raw_num_rows()
	y = d.get_column(dep)
	newA = np.matrix(np.zeros((rows, len(ind)+1)))
	index = 0
	for header in ind:
		oldA = d.get_column(header)
		for j in range(0,rows):
			newA[j,index+1] = oldA[j]
		index += 1
	A = newA
	A[:,0] = 1
	
	AAinv = np.linalg.inv(np.dot(A.T, A))
	
	x = np.linalg.lstsq( A, y )
	b = x[0]
	N = len(y)
	C = len(b)
	df_e = N - C
	df_r = C-1

	error = y - np.dot(A, b)

	sse = np.dot(error.T, error) / df_e

	stderr = np.sqrt( np.diagonal( sse[0, 0] * AAinv) )
	
	t = b.T / stderr
	
	p = (1 - scipy.stats.t.cdf(abs(t), df_e))
	
	r2 = 1 - error.var() / y.var()
	
	return [b, sse, r2, t, p]



# This version calculates the eigenvectors of the covariance matrix
def pca(d, headers, normalize=True):

	if normalize == True:
		A = normalize_columns_separately(d, headers)
	else:
		A = d.get_data(headers)
	C = np.cov(A, rowvar=False)
	W, V = np.linalg.eig(C)

	W = np.real(W)
	V = np.real(V)
	idx = W.argsort()
	idx = idx[::-1]
	W = W[idx]
	V = V[:,idx]
	V = V.T
	
	means = []
	for header in headers:
		cd = d.get_column(header)
		cd = np.mean(cd)
		means.append(cd)
	m = means
	
	D = A - m

	A = np.dot(V, D.T).T

	pcad = data.PCAData( headers, A, W, V, m )
	return pcad
	
	
# '''Takes in a Data object, a set of headers, and the number of clusters to create
# Computes and returns the codebook, codes, and representation error.'''	
def kmeans_numpy( d, headers, K, whiten = True):

	A = d.get_data(headers)
	W = vq.whiten(A)
	codebook, bookerror = vq.kmeans(W, K)
	codes, error = vq.vq(W, codebook)
	return codebook, codes, error



# The kmeans_init should take in the data, the number of clusters K, and an optional
#  set of categories and return a numpy matrix with K rows, each one repesenting a cluster mean. 
#  If no categories are given, a simple way to select the means is to randomly choose K data points 
#  (rows of the data matrix) to be the first K cluster means.
def kmeans_init( d, K, categories = '', metric=None):
	if metric == None:
		metric = "Euclidean"
	rows = d.shape[0]
	columns = d.shape[1]
	if categories == '':
		print "No categories in kmeans_init"
		# create a list of lists, each list contains a row of data
		data_rows = []
		for i in range(0, rows):
			data_points = []
			for j in range(0, columns):
				data_point = d[i,j]
				data_points.append(data_point)
			data_rows.append(data_points)
		
		# list for indexes, used for assigning a random index
		list = []
		for i in range(0, rows):
			list.append(i)
		
		# put rows from lists into matrix at random - remove index from list once used
		matrix = np.matrix(np.zeros((K, columns)))
		for i in range(0, K):
			random_num = random.choice(list)
			for j in range(0, columns):
				matrix[i,j] = data_rows[random_num][j]
			list.remove(random_num)
				
		return matrix, data_rows
		
	else:
		print "Categories in kmeans_init"	
		# create list of category indexes
		indexes = []
		cat_rows = categories.shape[0]
		for i in range(0, cat_rows):
			index = categories[i,0]
			indexes.append(index)
		
		# create a list of lists, each list contains a row of data
		data_rows = []
		for i in range(0, rows):
			data_points = []
			for j in range(0, columns):
				data_point = d[i,j]
				data_points.append(data_point)
			data_rows.append(data_points)
		
		# creates matrix with rows of the matching category, calculates mean, store means in list	
		means = []
		for i in range(0,K):
			indexes = np.where(categories==i)[0]
			data = d[indexes.tolist()[0],:]
			mean = np.mean(np.array(data), axis=0)
			means.append(mean)
		
		# output means into matrix
		matrix = np.matrix(np.zeros((K, columns)))
		for i in range(0, K):
			for j in range(0, columns):
				matrix[i,j] = means[i][j]
		
		return matrix, data_rows			

	

# The kmeans_classify should take in the data and cluster means and 
# return a list or matrix (your choice) of ID values and distances. 
# The IDs should be the index of the closest cluster mean to the data point. 
# The distances should be the Euclidean distance to the nearest cluster mean.
def kmeans_classify( d, means, metric):
	rows = d.shape[0]
	columns = d.shape[1]
	mean_rows = means.shape[0]
	
	# create a list of lists, each list contains a row of data
	data_rows = []
	for i in range(0, rows):
		data_points = []
		for j in range(0, columns):
			data_point = d[i,j]
			data_points.append(data_point)
		data_rows.append(data_points)
	
	# calculate euclidean distance, append lowest distance and corresponding j value ( also ID)
	IDs = []
	distances = []
	for i in range(0, len(data_rows)):
		dist = None
		ID = None
		for j in range(0, mean_rows):
			if j == 0:
				dist = np.linalg.norm(np.array(data_rows[i])-np.array(means[j]))
				ID = j
			else:
				dist2 = np.linalg.norm(np.array(data_rows[i])-np.array(means[j]))
				if dist > dist2:
					dist = dist2
					ID = j
				else:
					pass
		IDs.append(ID)
		distances.append(dist)	
						
	# create matrix of ID's and distances
	IDmatrix = np.matrix(np.zeros((rows,1)))
	distanceMatrix = np.matrix(np.zeros((rows,1)))
	for i in range(0,rows):
		IDmatrix[i,0] = IDs[i]
		distanceMatrix[i,0] = distances[i]

	return IDmatrix, distanceMatrix

	

def kmeans_algorithm(A, means, metric=None):
# set up some useful constants
	MIN_CHANGE = 1e-7
	MAX_ITERATIONS = 100
	D = means.shape[1]
	K = means.shape[0]
	N = A.shape[0]

# iterate no more than MAX_ITERATIONS
	for i in range(MAX_ITERATIONS):
		# calculate the codes
		codes, errors = kmeans_classify( A, means, metric )
# 		print codes, errors
		# calculate the new means
		newmeans = np.zeros_like( means )
		counts = np.zeros( (K, 1) )
		for j in range(N):
			newmeans[codes[j,0],:] += A[j,:]
			counts[codes[j,0],0] += 1.0

		# finish calculating the means, taking into account possible zero counts
		for j in range(K):
			if counts[j,0] > 0.0:
				newmeans[j,:] /= counts[j, 0]
			else:
				newmeans[j,:] = A[random.randint(0,A.shape[0]),:]

		# test if the change is small enough
		diff = np.sum(np.square(means - newmeans))
		means = newmeans
		if diff < MIN_CHANGE:
			break

# call classify with the final means
	codes, errors = kmeans_classify( A, means, metric )
	
# return the means, codes, and errors
	return (means, codes, errors)


def kmeans(d, headers, K, whiten=True, categories = '', metric=None):
	'''Takes in a Data object, a set of headers, and the number of clusters to create
	Computes and returns the codebook, codes and representation errors. 
	If given an Nx1 matrix of categories, it uses the category labels 
	to calculate the initial cluster means.
	'''
	if metric==None:
		metric="Euclidean"
 	if isinstance(d, np.matrixlib.defmatrix.matrix) == True:
 		A = d
 		if whiten == True:
 			W = vq.whiten(A)
 		else:
 			W = A
 	else:
		A = d
		if whiten == True:
			W = vq.whiten(A.get_data(headers))
		else:
			W = A.get_data(headers)
		
	codebook, data_rows = kmeans_init(W, K, categories, metric)
	codebook, codes, errors = kmeans_algorithm(W, codebook, metric)
	return codebook, codes, errors

	
# used to return clustering clusters, means, IDmatrix, data_rows
def cluster(d, headers, K, categories = '', metric=None):
	metric = "Euclidean"
	means, data_rows = kmeans_init( d.get_data(headers), K, categories, metric)
	IDmatrix, distanceMatrix = kmeans_classify( d.get_data(headers), means, metric)
	codebook, codes, errors = kmeans(d, headers, K, True, categories, metric)
	cluster = data.ClusterData( d.get_data(headers), headers, K, means, IDmatrix, data_rows, metric)
	return cluster


