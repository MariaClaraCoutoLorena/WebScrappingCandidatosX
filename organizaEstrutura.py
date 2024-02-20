import os
import pandas as pd
url_images_path = "2018"
candidatosArq = os.listdir(url_images_path)
candidatosInfo = {}
# estrutura que quero:
# {Haddad: {codIm: url, codIm2:url2}, Bolsonaro: {codIm: url, codIm2:url2}}
for cand in candidatosArq:
    candidatosInfo[cand[:-12]] = {}
    #pagando um arquivp csv:
    dateCandidate = pd.read_csv("2018/"+cand, sep=",")
    tweetID = dateCandidate["Tweet ID"]
    tweetUrl = dateCandidate["URL"]
    i=0
    for id in tweetID:
        id = id[3:]
        candidatosInfo[cand[:-12]][id] = tweetUrl[i]
        i+=1
print(candidatosInfo)
