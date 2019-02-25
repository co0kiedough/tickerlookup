import os, sys, csv, requests, glob

print 'loaded'

#   ***************************************
#   **                                   **
#   **   This tool is used to look-up    **
#   **   historical prices of stocks.    **
#   **                                   **
#   **   It will read any .csv in the    **
#   **   directory (currently) and       **
#   **   using alphavantage.co api look  **
#   **   up the ticker symbol for the    **
#   **   date provided and return the    **
#   **   historical price.               **
#   **                                   **
#   ***************************************

#  Use the example CSV to setup your files


theFiles = glob.glob('*.csv')
for items in theFiles:
    csvSymbols = dict()
    currentFile = open(items, 'r')
    currentCSV = csv.DictReader(currentFile)
    for rows in currentCSV:
        if len(rows['Symbol']) == 0:
            print 'no symbol'
        else:
            csvSymbols[rows['Symbol']] = rows['Date']
    closepriceDict = dict()
    for stocks in csvSymbols:
        apicall = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="+stocks+"&outputsize=full&apikey=NVW2O5ESEB8SJOZR"
        r = requests.get(apicall)
        if r.status_code == 200:
            x = r.json()
            try:
                closepriceDict[stocks] = x['Time Series (Daily)'][csvSymbols[stocks]]['4. close']
    # print(csvSymbols)
            except KeyError:
                closepriceDict[stocks] = 'Missing Date'
                print ('Price not available')
    newFile = theFiles[0].split('.')
    newCSV = open(newFile[0] + '_new.csv', 'wb')
    fieldnames = ['Date', 'Stock', 'Price']
    actualCSV = csv.DictWriter(newCSV, fieldnames)
    actualCSV.writeheader()
    csvDict = dict()
    
    for stocks in closepriceDict:
        csvDict[stocks] = {'Date':csvSymbols[stocks], 'Stock':stocks, 'Price':closepriceDict[stocks]}
    for stocks in csvDict:
        print "writing"
        actualCSV.writerow(csvDict[stocks])
    newCSV.close()
    
    
        