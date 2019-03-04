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

class lookup:
    
    def __init__(self):
  
        self.csvSymbols = dict()
        self.closepriceDict = dict()
        
         
    def iterateRows(csvFile):
        
        for rows in csvFile:
            if len(rows['Symbol']) == 0:
                print 'no symbol'
            else:
                self.csvSymbols[rows['Symbol']] = rows['Date']
        return self.csvSymbols
    
    def composeCall(symboltoCall):
        
        apiCall = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="+symboltoCall+"&outputsize=full&apikey=NVW2O5ESEB8SJOZR"
        return apicall
    
    def getPrice(symbolDict):
        for stocks in symbolDict:
            requestUrl = composeCall(stocks)
            r = request.get(requestUrl)
            if r.status_code == 200:
                x = r.json()
                try:
                    self.closepriceDict[stocks] = x['Time Series (Daily)'][symbolDict[stocks]]['4. close']
                except KeyError:
                    self.closepriceDict[stocks]= 'Missing Date'
                    print 'Price not available'
        return self.closepriceDict
    
    def iterateFiles(self):
        theFiles = glob.glob('*.csv')
        for files in theFiles:
            x = self.iterateRows(files)
            y = self.getPrice(x)
            newFile = theFiles[0].split('.')
            newCSV = open(newFile[0] + '_new.csv', 'wb')
            fieldnames = ['Date', 'Stock', 'Price']
            actualCSV = csv.DictWriter(newCSV, fieldnames)
            actualCSV.writeheader()
            csvDict = dict()
            
            for stocks in y:
                csvDict[stocks] = {'Date':y[stocks], 'Stock':stocks, 'Price':y[stocks]}
            for stocks in csvDict:
                print "writing"
                actualCSV.writerow(csvDict[stocks])
            newCSV.close()
               
                
doit = lookup()
keepdoing = doit.iterateFiles()
    
        