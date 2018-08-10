# "Brute-force" program to retrieve and store pages from Billboard for artists who
# have a song in the All-time Top 100 list

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
    
def multi_find(s, r):
    return [pos for pos in range(len(s)) if s.startswith(r,pos)]
        
listPath = "c:/billboard_top_artists_chart_history/"
listFile = listPath + "BBTop100Artists.txt"
tPath = listPath + "BBAlltimeTop100-2018/"

#Code to retrieve pages -- run once!
with open(listFile) as f:
    htmlData = f.read()
    htmlPages = htmlData.split("\n")

for htmlPage in htmlPages[0:]:
    print(htmlPage)
    artistName = htmlPage[32:len(htmlPage)-14]
    tFile = tPath + artistName + ".html"
    retrievePages(htmlPage,tFile)
    print(tFile)

listOfPages = listdir(tPath)

for htmlPage in listOfPages[0:]:
    #print(htmlPage)
    htmlFilePath = tPath + htmlPage
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
            #print(aName, lenS, locsOfStat)
            stats = ['0','0','0']
            if lenS > 0:
                stats[0] = strStatDiv[locsOfStat[0]:][14:strStatDiv[locsOfStat[0]:].find('<')]
            if lenS > 1:
                stats[1] = strStatDiv[locsOfStat[1]:][14:strStatDiv[locsOfStat[1]:].find('<')]
            if lenS > 2:
                stats[2] = strStatDiv[locsOfStat[2]:][14:strStatDiv[locsOfStat[2]:].find('<')]
            pStr = aName + ',' + stats[0] + ',' + stats[1] + ',' +  stats[2]
            print(pStr)
            
for htmlPage in listOfPages[0:]:
    #print(htmlPage)
    htmlFilePath = tPath + htmlPage
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
                sTitleStart = titleLocs[cnt] + 12
                sTitleEnd = tSectStr.find('">',sTitleStart)
                songTitle = tSectStr[sTitleStart:sTitleEnd]
                songTitle = songTitle.replace('&amp;','and')
                songTitle = songTitle.replace(',',' ')
                songTitle = songTitle.strip(' ')
                
                aNameStart = aNameLocs[cnt] + 19
                aNameEnd = tSectStr.find('</div>',aNameStart)
                artistName = tSectStr[aNameStart:aNameEnd]
                artistName = artistName.replace('&amp;','and')
                artistName = artistName.replace(',',' ')
                artistName = artistName.strip(' ')
                
                pRankStart = pRankLocs[cnt] + 11
                pRankEnd = tSectStr.find(' on <a class=',pRankStart)
                pRank = tSectStr[pRankStart:pRankEnd]
                pRank = pRank.strip(' ')
    
                pRankDateStart = pRankDateLocs[cnt] + 22
                pRankDateEnd = tSectStr.find('">',pRankDateStart)
                pRankDate = tSectStr[pRankDateStart:pRankDateEnd]
                pRankDate = pRankDate.strip(' ')
 
                sep = ','
                pStr = aName + sep + str(noOfTitles + 1) + sep + songTitle + sep + artistName + sep + pRank + sep + pRankDate
                print(pStr)
                noOfTitles += 1          
