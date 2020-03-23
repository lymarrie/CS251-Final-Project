# file: anova.py
# author: Luc Yuki Marrie
# date: 5/5/2015
# Happy cinco de mayo
# class: CS251

import sys
import data
import scipy.stats
import numpy as np
import random
import scipy.cluster.vq as vq
import scipy.spatial.distance as ssd
import matplotlib.pyplot as plt


# Used scipy stats function for this called f_oneway

# The one-way ANOVA tests the null hypothesis that two or more groups have the same population mean. 
# The test is applied to samples from two or more groups, possibly with differing sizes.

# http://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.f_oneway.html


# takes in data file, creates columns of data, conducts ANOVA and outputs F & P values
def ANOVA(argv):
	d = data.Data(argv[1])
	d.read(argv[1])
	
	Medu = d.get_column("Medu")
	Fedu = d.get_column("Fedu")
	higher = d.get_column("higher")
	grades = d.get_column("G3")
	romantic = d.get_column("romantic")
	
	rows = Medu.shape[0]

	col1 = []
	col2 = []
	
	# ANOVA for mother's education
	for i in range(0, rows):
		if Medu[i,0] == 4:
			col1.append(grades[i,0])
		elif Medu[i,0] == 2:
			col2.append(grades[i,0])
	
	result = scipy.stats.f_oneway(col1, col2)
	print "\n", result[0], "Mother edu F-value"
	print result[1], "Mother edu P-value", "\n"
	
	col3 = []
	
	for i in range(0, len(col2)):
		col3.append(col1[i])	
	
	# creates 3 histogram plots
	# 1 for results with most educated mothers
	# 2 for results with 2nd least educated mothers
	# 3 for scatterplot of first vs second
	create_histogram(col3, col2)
	
# 	col1 = []
# 	col2 = []
# 	
# 	# ANOVA for father's education
# 	for i in range(0, rows):
# 		if Fedu[i,0] == 4:
# 			col1.append(grades[i,0])
# 		elif Fedu[i,0] == 1:
# 			col2.append(grades[i,0])
# 	
# 	result = scipy.stats.f_oneway(col1, col2)
# 	print result[0], "Father edu F-value"
# 	print result[1], "Father edu P-value", "\n"
# 	
# 	col1 = []
# 	col2 = []
# 	
# 	# ANOVA for whether or not a child wants to pursue a higher education by the education index of the mother
# 	for i in range(0, rows):
# 		if higher[i,0] == 1:
# 			col1.append(Medu[i,0])
# 		elif higher[i,0] == 0:
# 			col2.append(Medu[i,0])
# 	
# 	result = scipy.stats.f_oneway(col1, col2)
# 	print result[0], "Higher education F-value"
# 	print result[1], "Higher education P-value", "\n"
# 	
# 	col1 = []
# 	col2 = []
# 	
# 	# ANOVA for being in a relationship
# 	for i in range(0, rows):
# 		if romantic[i,0] == 1:
# 			col1.append(grades[i,0])
# 		elif romantic[i,0] == 0:
# 			col2.append(grades[i,0])
# 	
# 	result = scipy.stats.f_oneway(col1, col2)
# 	print result[0], "Dating F-value"
# 	print result[1], "Dating P-value", "\n"
	

def create_histogram(col1, col2):
	# coding for plotting just one
	fig = plt.figure()
	plt.hist( col1, bins=1000, normed=0 )

	fig = plt.figure()
	plt.hist( col2, bins=1000, normed=0 )

	fig = plt.figure()
	both = np.vstack( (col1, col2 ) )
	plt.hist( both.T )
	plt.show()
	exit()

	fig = plt.figure()
	plt.scatter( col1, col2 )

	plt.show()



ANOVA(sys.argv)

