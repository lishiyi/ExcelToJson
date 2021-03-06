# This code is used to convert excel file to JSON file which is in UTF-8 format. 
# lastdate:2015-6-18 17:11 version 1.1 
import os
import sys
import codecs
import xlrd #http://pypi.python.org/pypi/xlrd
if len(sys.argv) != 2 :
    print "argv count != 2, program exit"
    print "USAGE: exceltojson.py excelfilename"
    exit(0)
print "excel to json"
excelFileName = sys.argv[1]
def FloatToString (aFloat):
    if type(aFloat) != float:
        return ""
    strTemp = str(aFloat)
    strList = strTemp.split(".")
    if len(strList) == 1 :
        return strTemp
    else:
        if strList[1] == "0" :
            return strList[0]
        else:
            return strTemp
    
def table2jsn(table, jsonfilename):
    nrows = table.nrows
    ncols = table.ncols
    f = codecs.open(jsonfilename,"w","utf-8")

    f.write(u"{\n\t\"list\":[\n")
    for r in range(nrows-1):    
        f.write(u"\t\t{\"nutrientTargets\": { ")
        #f.write(u"\t\t{ ")
        for c in range(ncols):
            strCellValue = u""
            CellObj = table.cell_value(r+1,c)
            if type(CellObj) == unicode:
                strCellValue = CellObj
            elif type(CellObj) == float:
                strCellValue = FloatToString(CellObj)
            else:
                strCellValue = str(CellObj)
                #strCellValue = u"\"" + strCellValue + u"\""
            if(table.cell_value(0,c)=="name" or table.cell_value(0,c)=="gender"):
                strTmp = u"\""  + table.cell_value(0,c) + u"\": "+ u"\"" + strCellValue + u"\""
            else:
                strTmp = u"\""  + table.cell_value(0,c) + u"\": "+ strCellValue
            
            if c< ncols-1:
                strTmp += u", "
            f.write(strTmp)
        f.write(u" }}")
        if r < nrows-2:
            f.write(u",")
        f.write(u"\n")
    f.write(u"\t]\n}\n")
    f.close()
    print "Create ",jsonfilename," OK"
    return

data = xlrd.open_workbook(excelFileName)
table = data.sheet_by_name(u"tablelist")
rs = table.nrows
for r in range(rs-1):
    print table.cell_value(r+1,0), "==>", table.cell_value(r+1,2)
    desttable = data.sheet_by_name(table.cell_value(r+1,0))
    destfilename = table.cell_value(r+1,2)
    table2jsn(desttable,destfilename)

print "All OK"