import fireeye, blograpid7, securelist
import time
#https://www.fireeye.com/current-threats/apt-groups.html
#Doesn't actually cover continuous numbering
aptNumbers = [1, 3, 5, 10, 12, 16, 17, 18, 19, 28, 29, 30, 32, 33, 34, 37, 38]
for aptNum in aptNumbers:
    query = "APT%s" % aptNum
    print("Searching for {}".format(query))
    fireeye.parse_data_save(query)
    #Same query to find references?
    blograpid7.parse_data_save(query)
    securelist.parse_data_save(query)
    #Found there were fewer failures if I waited between searches
    time.sleep(30)
