# file: machine_learning_naivebayes.py
# author: Luc Yuki Marrie
# date: 4/21/2015
# class: CS251

import csv
import sys
import data
import classifiers
import writeToCSV


def main(argv):
	''' Reads in a training set and its category labels, possibly as a separate file.
	Reads a test set and its category labels, possibly as a separate file.
	Builds a classifier using the training set.
	Classifies the training set and prints out a confusion matrix.
	Classifies the test set and prints out a confusion matrix.
	Writes out a new CSV data file with the test set data and the categories as an extra column. 
	Your application should be able to read this file and plot it with the categories as colors.
	
	THIS FILE IS FOR NAIVEBAYES'''
	
	if len(argv) < 3:
		print 'Usage: python %s <training data file> <test data file> <optional training category file> <optional test category file>' % (argv[0])
		exit(-1)

	# read in training set and test set
	dtrain = data.Data(argv[1])
	dtest = data.Data(argv[2])
	
	if len(argv) > 4:
		traincatdata = data.Data(argv[3])
		testcatdata = data.Data(argv[4])
		traincats = traincatdata.get_data(traincatdata.get_headers())
		testcats = testcatdata.get_data(testcatdata.get_headers())
		A = dtrain.get_all_data()
		B = dtest.get_all_data()
		rows = B.shape[0]
		columns = B.shape[1] + 1
	else:
		# assume the categories are the last column
		t = dtrain.get_all_data()
		traincats = t[:,-1]
		t1 = dtest.get_all_data()
		testcats = t1[:,-1]
		headers = dtrain.get_headers()[:-1]
		A = dtrain.get_data( dtrain.get_headers()[:-1] )
		B = dtest.get_data( dtest.get_headers()[:-1] )
		rows = B.shape[0]
		columns = B.shape[1] + 1
		
	C = classifiers.NaiveBayes()

	C.build( A, traincats )
	
	ctraincats, ctrainlabels = C.classify( A )
	
	ctestcats, ctestlabels = C.classify( B )
	
	confusion_matrix1, unique = C.confusion_matrix(traincats, ctraincats)
	confusion_matrix2, unique = C.confusion_matrix(testcats, ctestcats)
	
	C.confusion_matrix_str(confusion_matrix1, unique)
	C.confusion_matrix_str(confusion_matrix2, unique)
	
# 	if len(argv) > 4:
# 		print "Now converting to CSV file"
# 		dtest.add_column("class","numeric",ctestcats)
# 		headers = dtest.get_headers()
# 		types = dtest.get_raw_types()
# 		A = dtest.get_all_data()
# 		writeToCSV.writeToCSV(rows, columns, headers, types, A, "machine_learning_naivebayes.csv")
# 	else:
# 		print "Now converting to CSV file"
# 		B = dtest.get_all_data()
# 		B[:,-1] = ctestcats
# 		headers = dtest.get_headers()
# 		types = dtest.get_raw_types()
# 		writeToCSV.writeToCSV(rows, columns, headers, types, B, "machine_learning_naivebayes.csv")

if __name__ == "__main__":
	main(sys.argv)	  
	
	
	
	
	