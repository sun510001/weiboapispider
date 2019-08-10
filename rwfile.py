import csv

fileHeader = ['created_at', 'id', 'tweet', 'screen_name']


# write and create the file
#  fileHeader = ["name", "score"]

#  d1 = ["Zhang", "30"]

csvFile = open("weibo.csv", "w")
writer = csv.writer(csvFile)

writer.writerow(fileHeader)

csvFile.close()

# add to the file

#  add_info = ("sun", "90")
#  csvFile = open("data.csv", "a")
#  writer = csv.writer(csvFile)
#  writer.writerow(add_info)
#  csvFile.close()


# read the file
#  csvFile = open("data.csv", "r")

#  dict_reader = csv.DictReader(csvFile)
#  for each in dict_reader:
#  print(each)

#  a = open("test.csv", "r")
#  print len(a.readlines())
