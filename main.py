from email import message
import requests
from bs4 import BeautifulSoup


def fetchProgramInfo(result):
    uniInfo = result.h6.contents
    program = uniInfo[0]
    comment = "No Extra Information Was Included By The Author!"

    if(len(uniInfo[1].contents) > 0):
        comment = result.h6.contents[1].contents[0]
    
    return program, comment
        
def convertToMessageFormat(program, authorComment, dateAdded, includedDetails): 
    return "\n..........\n".join([program, authorComment, dateAdded, includedDetails])

def runMain(lastFetchedResult):
    CS_URL = "https://www.thegradcafe.com/survey/?program=Computer+Science"

    siteHTML = BeautifulSoup(requests.get(CS_URL).text, features = "lxml")

    for result in siteHTML.find_all("div", class_ = "row mb-2"):
        lastResultFlag = True
        finalMessage = ""
        if(result.find("h6")):
            program, authorComment = fetchProgramInfo(result)
            dateAdded = result.find("p", class_ = "mb-0 fst-italic").contents[0]
            includedDetails = ""
            for detail in result.find("div", class_ = "mt-3").findChildren("span", recursive = False):
                includedDetails += (" ".join(detail.text.split()) + "\n")
            
            message = convertToMessageFormat(
                program = program,
                authorComment = authorComment,
                dateAdded = dateAdded,
                includedDetails = includedDetails.strip()
            )

            if(message == lastFetchedResult):
                return finalMessage, lastFetchedResult

            if(lastResultFlag):
                lastFetchedResult = message
                lastResultFlag = False

            finalMessage += (message + "\n\n")
    
    return finalMessage, lastFetchedResult
        
        


