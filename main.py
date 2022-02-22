import requests
from bs4 import BeautifulSoup
import os

from dotenv import load_dotenv

load_dotenv()

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
    CS_URL = os.environ.get("TARGET_URL")
    siteHTML = BeautifulSoup(requests.get(CS_URL).text, features = "lxml")

    lastResultFlag = True
    messages = []

    for result in siteHTML.find_all("div", class_ = "row mb-2"):
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
                return messages, lastFetchedResult

            if(lastResultFlag):
                lastFetchedResult = message
                lastResultFlag = False

            messages.append(message)
    
    return messages, lastFetchedResult
        
