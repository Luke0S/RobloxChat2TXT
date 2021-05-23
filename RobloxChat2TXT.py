import requests
import os
import io

import os.path
from os import path

print("""
=======================================
|                                     |
|                                     |
|           RobloxChat2TXT            |
|            By Luke O.S.             |
|                                     |
|          ----- Info ------          |
|                                     |
|   Insure the ROBLOSECURITY key is   |
| correct before running the program. |
|                                     |
=======================================
""")
input("\n\nPress any key to start...")

# Check ROBLOSECURITY
print('\nChecking to see if ROBLOSECURITY.txt exists...')

if path.exists(f"{os.path.dirname(os.path.realpath(__file__))}\ROBLOSECURITY.txt"):
    ROBLOSECURITYFile = open(f"{os.path.dirname(os.path.realpath(__file__))}\ROBLOSECURITY.txt", "rt").read()
else:
    file = open(f"{os.path.dirname(os.path.realpath(__file__))}\ROBLOSECURITY.txt","w+")

    os.startfile(f"{os.path.dirname(os.path.realpath(__file__))}\ROBLOSECURITY.txt")

    input("ROBLOSECURITY.txt did not exist. The file was created automatically for you to fill in.")
    exit()

cookies = {'.ROBLOSECURITY': f'{str(ROBLOSECURITYFile)}'}

print("Checking if ROBLOXSECURITY may be valid...")

if len(ROBLOSECURITYFile) <= 0:
    input("ROBLOXSECURITY has not been filled in.")
    os.startfile(f"{os.path.dirname(os.path.realpath(__file__))}\ROBLOSECURITY.txt")
    exit()
else:
    r = requests.get("https://chat.roblox.com/v2/get-user-conversations?pageNumber=1&pageSize=200",cookies=cookies)
    if 'errors' in r.json():
        os.system('cls')
        os.startfile(f"{os.path.dirname(os.path.realpath(__file__))}\ROBLOSECURITY.txt")
        input("\nThe key in ROBLOXSECURITY.txt appears to be invalid or expired.\n\nEnsure there are no spaces, linebreaks, or other characters at the beginning or end of the key.\nIf that doesn't work, get a new key.")
        exit()

source = requests.get("https://chat.roblox.com/v2/get-user-conversations?pageNumber=1&pageSize=200",cookies=cookies).json()

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

while True:
        os.system('cls')

        for i in range(len(source)):
            print(f'{i}: {source[i]["title"]}')

        selected = input("Input coversation to download: ")

        if selected != '' and RepresentsInt(selected) != False:
            if int(selected) < len(source)+1 and int(selected) > -1:
                break

os.system('cls')

conversationID = source[int(selected)]['id']

ApiURL = f'https://chat.roblox.com/v2/get-messages?conversationId={conversationID}&pageSize=30'
lastMsgID = False
cachedResults = []
numberOfMsgs = 0

userNames = []

def listToString(s):
    str1 = ""
    for ele in s:
        str1 += ele
    return str1

def readableTimeAndDate(sentTime):
    rawDate, rawTime = sentTime.split('T')[0], sentTime.split('T')[1]
    Date, Time = False,False

    #By default it comes in YYYY/MM/DD
    DateY,DateM,DateD = rawDate.split('-')[0],rawDate.split('-')[1],rawDate.split('-')[2]
    Date = str(f'{DateM}/{DateD}/{DateY}')

    #By default the roblox chat time is 4 hours ahead of EST and in 24hr format
    hrs,min = rawTime.split(':')[0],rawTime.split(':')[1]
    Time = str(f'{hrs}:{min}')

    return f'{Date} at {Time} UTC'

def getReadableName(ID):
    global userNames
    for i in range (len(userNames)):
        if str(userNames[i][0]['id']) == str(ID):
            return str(userNames[i][0]['name'])

print("Working...")

jsonRawData = requests.get("https://chat.roblox.com/v2/get-user-conversations?pageNumber=1&pageSize=200",cookies=cookies).json()
for i in range(len(jsonRawData)):
    if str(jsonRawData[i]['id']) == str(conversationID):
        for x in range(len(jsonRawData[i]['participants'])):
            userNames.append( [ {'name':jsonRawData[i]['participants'][x]['name'],'id':jsonRawData[i]['participants'][x]['targetId']} ] )

os.system('cls')

print("""
=======================================
|              Working...             |
|               -------               |
|  (This may take a while depending   |
|      on the size of the chat...)    |
=======================================
""")

while lastMsgID != True:
    if lastMsgID == False:
        source = requests.get(ApiURL,cookies=cookies).json()
        for i in range(len(source)):
            completeString = str(f"\n{str(getReadableName(source[i]['senderTargetId']))}: {str(source[i]['content'])}\nSent {readableTimeAndDate(source[i]['sent'])}\n")
            numberOfMsgs = numberOfMsgs + 1
            cachedResults.append(completeString)
            lastMsgID = source[i]['id']
        ApiURL = ApiURL+'&exclusiveStartMessageId='
    else:
        source = requests.get(ApiURL+lastMsgID,cookies=cookies).json()
        if len(source) > 0:
            for i in range(len(source)):
                completeString = str(f"\n{str(getReadableName(source[i]['senderTargetId']))}: {str(source[i]['content'])}\nSent {readableTimeAndDate(source[i]['sent'])}\n")
                numberOfMsgs = numberOfMsgs + 1
                cachedResults.append(completeString)
                lastMsgID = source[i]['id']
        else:
            lastMsgID = True

cachedResults.insert(0,f"Number of messages: {format(numberOfMsgs,',d')}\n")
cachedResultsInString = listToString(cachedResults)

while True:
        os.system('cls')

        print("Before continuing, make sure you don't mind that Output.txt is overwritten...")

        overwrite = input("\nPress 'y' to continue: ")

        if overwrite not in ('y'):
            continue
        else:
            if overwrite != '':
                break

print("\nAttempting to write to Output.txt...")

with io.open(f"{os.path.dirname(os.path.realpath(__file__))}\Output.txt", "w", encoding="utf-8") as f:
    f.write(cachedResultsInString)

input("Complete!")
