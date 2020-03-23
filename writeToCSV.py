import csv

def writeToCSV(rows, columns, headers, types, data, file_name):
	rows = rows
	columns = columns
	f = file(file_name, 'w' )
	headerstring = ''
	idx = 0
	for header in headers:
		if idx == len(headers)-1:
			headerstring += header
		else:
			headerstring += header+","
		idx += 1
	typesString = ''
	idx = 0
	for type in types:
		if idx == len(headers)-1:
			typesString += type
		else:
			typesString += type+','
		idx += 1
	f.write(headerstring + '\n')
	f.write(typesString + '\n')
	for i in range(0, rows):
		string = ''
		for j in range(0, columns):
			if j == columns-1:
				string+=str(int(data[i,j]))
			else:
				string += str(float(data[i,j]))
				string += ","
		f.write( string + '\n')
	f.close()

