#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import json
import numpy as np
from lxml import html
import re
import requests
import time


# In[2]:


def get_data(writingSample):
    try:
        s = requests.Session()
        starter = s.get('http://141.225.41.245/cohmetrixgates/Home.aspx', timeout=120)
        tree = html.fromstring(starter.text)

        cookies = {
            'ASP.NET_SessionId': 'nhobvdrzvutqzq45cjkb3w45'
        }

        headers = {
            'Host': '141.225.41.245',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'http://141.225.41.245/cohmetrixgates/Home.aspx',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }
        viewstate = tree.xpath('//input[@id="__VIEWSTATE"]/@value')[0]
        validation = tree.xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value')[0]
        view = tree.xpath('//input[@id="__EVENTVALIDATION"]/@value')[0]

        data = {
            '__VIEWSTATE': viewstate,
            '__VIEWSTATEGENERATOR': validation,
            '__EVENTVALIDATION': view,
            'ctl00$ContentPlaceHolder1$txtUserName': 'rb',
            'ctl00$ContentPlaceHolder1$btnLogin': 'Enter',
        }
        l = s.post('http://141.225.41.245/cohmetrixgates/Home.aspx', headers=headers, data=data, cookies=cookies, timeout=120)

        headers = {
            'Host': '141.225.41.245',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'http://141.225.41.245/cohmetrixgates/Design1.aspx',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }
        viewstate = "/wEPDwULLTE2NzE0NTQyNzgPZBYCZg9kFgICAw9kFgQCAw9kFgICBQ8PFgIeBFRleHQFAnJiZGQCBQ9kFgICBQ8WAh4HVmlzaWJsZWhkZD9kZprglf5/H4YayQZiNiUeKwke"
        validation = '/wEWBQKQ5ID8AgKMjYnCAwK/86lLAoWF7b8NAsW5+oAEYy+Z8IQxtc+PyX5/TU0QntRW9dU='

        sampleData = {
            '__VIEWSTATE': viewstate,
            '__VIEWSTATEGENERATOR': '1F2DA56D',
            '__EVENTVALIDATION': validation,
            'ctl00$ContentPlaceHolder1$txtMultiLine': writingSample,
            'ctl00$ContentPlaceHolder1$btnAnalyse': 'Analyze',
        }

        t = s.post('http://141.225.41.245/cohmetrixgates/Design1.aspx', headers=headers, cookies=cookies, data=sampleData, timeout=120)
        matches= re.findall(r'\"font-size:x-small;">([0-9]+)%', t.text)
        matches= np.array(matches, np.int)
        return matches
    except Exception as e:
        print (e)
        return np.zeros(5)
    


# In[3]:


def get_score(matches):
    try:
        return (matches[3]+matches[4]-matches[0]-matches[1]-matches[2])/500
    except Exception as e:
        print(e)
        return 0
    


# In[ ]:


def parse_data(text, writingSampleId, outputFileName):
    tree = html.fromstring(text)
    rows = tree.xpath('//tr')
    workbook = get_result_file(outputFileName)

    worksheet = workbook.active
    worksheet.title = "Coh Results"

    add_excel_header(rows, worksheet)

    # Read all the rows and check to make sure we haven't put this value in before
    add_parsed_results_to_spreadsheet(rows, worksheet, writingSampleId)

    workbook.save(outputFileName)


# In[4]:


def process_file(filename):
    fullname= '/home/bansal/Downloads/' + filename + '.json'
    print (fullname)
    scores= []
    count= 1
    for comment in open(fullname, 'r'):
        text= json.loads(comment)['body']
        matches= get_data(text)
        print (text)
        score= get_score(matches)
        print (score)
        scores.append(score)
        print (count)
        count+= 1
    
    scores= np.array(scores)
    print ("Number of comments analyzed:" + str(len(scores)))
    print ("Mean of comments analyzed:" + str(np.mean(scores)))
    print ("Median of comments analyzed:" + str(np.median(scores)))
    outname= "/home/bansal/Desktop/" + filename + '.txt'
    np.savetxt(outname, scores, newline=" ")
    print ("DONE!!!")
    


# In[7]:


def read_json():
    loc= '/home/bansal/Downloads/discourse_reddit.json'
    appreciationvirality= []
    humorvirality= []
    questionvirality= []
    announcementvirality= []
    appreciationscores= []
    humorscores= []
    questionscores= []
    announcementscores= []
    count= 1
    for comment in open(loc, 'r'):
        text= json.loads(comment)
        for post in text['posts']:
            if('virality' in post and 'body' in post):
                if(post['majority_type']== 'appreciation'):
                    appreciationvirality.append(post['virality'])
                    matches= get_data(post['body'])
                    score= get_score(matches)
                    print (count)
                    count+= 1
                    print (score)
                    appreciationscores.append(score)
                elif(post['majority_type']== 'humor'):
                    humorvirality.append(post['virality'])
                    matches= get_data(post['body'])
                    score= get_score(matches)
                    print (count)
                    count+= 1
                    print (score)
                    humorscores.append(score)
                elif(post['majority_type']== 'question'):
                    questionvirality.append(post['virality'])
                    matches= get_data(post['body'])
                    score= get_score(matches)
                    print (count)
                    count+= 1
                    print (score)
                    questionscores.append(score)
                elif(post['majority_type']== 'announcement'):
                    announcementvirality.append(post['virality'])
                    matches= get_data(post['body'])
                    score= get_score(matches)
                    print (count)
                    count+= 1
                    print (score)
                    announcementscores.append(score)
    
    np.savetxt("/media/data_dump_1/Rajat/appreciationdiscourse.txt", appreciationscores, newline=" ")
    np.savetxt("/media/data_dump_1/Rajat/humordiscourse.txt", humorscores, newline=" ")
    np.savetxt("/media/data_dump_1/Rajat/questiondiscourse.txt", questionscores, newline=" ")
    np.savetxt("/media/data_dump_1/Rajat/announcementdiscourse.txt", announcementscores, newline=" ")
    np.savetxt("/media/data_dump_1/Rajat/appreciationdiscoursevirality.txt", appreciationvirality, newline=" ")
    np.savetxt("/media/data_dump_1/Rajat/humordiscoursevirality.txt", humorvirality, newline=" ")
    np.savetxt("/media/data_dump_1/Rajat/questiondiscoursevirality.txt", questionvirality, newline=" ")
    np.savetxt("/media/data_dump_1/Rajat/announcementdiscoursevirality.txt", announcementvirality, newline=" ")
    print ("The mean of appreciation scores: " + str(np.mean(appreciationscores)))
    print ("The mean of humor scores: " + str(np.mean(humorscores)))
    print ("The mean of question scores: " + str(np.mean(questionscores)))
    print ("The mean of announcement scores: " + str(np.mean(announcementscores)))
    print ("The median of appreciation scores: " + str(np.median(appreciationscores)))
    print ("The median of humor scores: " + str(np.median(humorscores)))
    print ("The median of question scores: " + str(np.median(questionscores)))
    print ("The median of announcement scores: " + str(np.median(announcementscores)))
    print ("Appreciation Correlation Scores: " + str(np.corrcoef(appreciationscores, appreciationvirality)[0][1]))
    print ("Humor Correlation Scores: " + str(np.corrcoef(humorscores, humorvirality)[0][1]))
    print ("Question Correlation Scores: " + str(np.corrcoef(questionscores, questionvirality)[0][1]))
    print ("Announcement Correlation Scores: " + str(np.corrcoef(announcementscores, announcementvirality)[0][1]))
    


# In[8]:


read_json()


# In[ ]:




