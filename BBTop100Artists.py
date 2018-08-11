# "Brute-force" program to retrieve and store pages from Billboard for artists who
# have a song in the All-time Top 100 list. The exact list of pages is found in
# an external file provided in this repository

import glob, os
import re
import pprint
from urllib.request import Request, urlopen
from os import listdir
from bs4 import BeautifulSoup

def retrievePages(htmlPage,targetFile):
    req = Request(htmlPage, headers={'User-Agent': 'Mozilla/5.0'})
    webByte = urlopen(req).read()
    webPage = webByte.decode('utf-8')
    outFile = open(targetFile, "w")
    outFile.write(webPage)
    outFile.close()
    
def extractData(tSectStr,findText,fieldArrayLoc,fieldLocStart,cnt):
    fieldNameStart = fieldArrayLoc + fieldLocStart
    fieldNameEnd = tSectStr.find(findText,fieldNameStart)
    fieldName = tSectStr[fieldNameStart:fieldNameEnd]
    fieldName = fieldName.replace('&amp;','and')
    fieldName = fieldName.replace(',',' ')
    fieldName = fieldName.strip(' ')
    return fieldName
    
def multi_find(s, r):
    return [pos for pos in range(len(s)) if s.startswith(r,pos)]

def createTopArtistNumCounts(listOfPages,outFile):
    for htmlPage in listOfPages:
        #print(htmlPage)
        htmlFilePath = pageDir + htmlPage
        with open(htmlFilePath, "rb", buffering=0) as f:
            htmlFile = f.read()
            soup = BeautifulSoup(htmlFile, 'html.parser')    
            aSection = soup.find('div',class_="artist-section artist-section--chart-history")
            if aSection != None:
                aNameDiv = aSection.find('div', class_='artist-header__info')
                aNameTxt = aNameDiv.get_text()
                aName = aNameTxt.strip('\r\n ')
                # ***** Statistics about Number of No. 1 Hits, of Top 10 Hits, of Top 100 Hits
                sStatDiv = aSection.find('div', class_='artist-section--chart-history__stats')
                strStatDiv = str(sStatDiv)
                locsOfStat = multi_find(strStatDiv,'stat--number">')
                lenS = len(locsOfStat)
                stats = ['0','0','0']
                if lenS > 0: #num 1s
                    stats[0] = strStatDiv[locsOfStat[0]:][14:strStatDiv[locsOfStat[0]:].find('<')]
                if lenS > 1: #top 10s
                    stats[1] = strStatDiv[locsOfStat[1]:][14:strStatDiv[locsOfStat[1]:].find('<')]
                if lenS > 2: #top 100s
                    stats[2] = strStatDiv[locsOfStat[2]:][14:strStatDiv[locsOfStat[2]:].find('<')]
                pStr = aName + ',' + stats[0] + ',' + stats[1] + ',' +  stats[2] + '\n'
                print(pStr)
                f = open(outFile, "a")
                f.write(pStr)
    f.close()
    
def createTopArtistsTop10SongStats(listOfPages, outFile):           
    for htmlPage in listOfPages:
        #print(htmlPage)
        htmlFilePath = pageDir + htmlPage
        with open(htmlFilePath, "rb", buffering=0) as f:
            htmlFile = f.read()
            soup = BeautifulSoup(htmlFile, 'html.parser')    
            aSection = soup.find('div',class_="artist-section artist-section--chart-history")
            if aSection != None:
                aNameDiv = aSection.find('div', class_='artist-header__info')
                aNameTxt = aNameDiv.get_text()
                aName = aNameTxt.strip('\r\n ')
                
                # ******** Data for Top 10 Songs by Artist
                tSection = aSection.find('div', class_='artist-section--chart-history__title-list')
                tSectStr = str(tSection)
                tSectStr = tSectStr.replace('\n','')
                tSectStr = tSectStr.replace('\r','')
                noOfTitles = 0
                titleLocs = multi_find(tSectStr,'data-title="')
                aNameLocs = multi_find(tSectStr,'text--artist-name">')
                pRankLocs = multi_find(tSectStr,'Peaked at #')
                pRankDateLocs = multi_find(tSectStr,'"date" href="/charts//')
                numSongs = len(titleLocs)
                for cnt in range(0,numSongs):
                    songTitle = extractData(tSectStr,'">',12,titleLocs[cnt],cnt)
                    artistName = extractData(tSectStr,'</div>',19,aNameLocs[cnt],cnt)
                    pRank = extractData(tSectStr,' on <a class=',11,pRankLocs[cnt],cnt)
                    pRankDate = extractData(tSectStr,'">',22,pRankDateLocs[cnt],cnt)
                    sep = ','
                    pStr = aName + sep + str(noOfTitles + 1) + sep + songTitle + sep + artistName + sep + pRank + sep + pRankDate + '\n'
                    print(pStr)
                    f = open(outFile, "a")
                    f.write(pStr)                
                    noOfTitles += 1 
    f.close()

# Pseudo Main

# Establish directories
analysisDir = 'C:/research/Hip Hop Rap/AugustAnalysis/'
listFile = analysisDir + "BB-Top_100_Artists_Chart_History_HTMLs.txt"
pageDir = analysisDir + "BBAlltimeTop100-2018/"
oFileCounts = analysisDir + 'BB-Top_100_Artist_Counts.txt'
oFileSongs = analysisDir + 'BB-Top_100_Artist_TopN_Songs.txt' # some artists have more than 10 and some less - but up to 10 are shown

# Retrieve pages and store in local directory

with open(listFile) as f:
    htmlData = f.read()
    htmlPages = htmlData.split("\n")

for htmlPage in htmlPages:
    print(htmlPage)
    artistName = htmlPage[32:len(htmlPage)-14]
    tFile = pageDir + artistName + ".html"
    # this next call retrieves pages from Billboard site
    retrievePages(htmlPage,tFile)
    print(tFile)

# Read and write Top 100 Artists Song Stats and Top 100 Top 10 Song data to local files

listOfPages = listdir(pageDir) #list of BB html files stored locally
createTopArtistNumCounts(listOfPages,oFileCounts)
createTopArtistsTop10SongStats(listOfPages,oFileSongs)
