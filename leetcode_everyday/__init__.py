from nonebot import get_driver

from .config import Config
from nonebot import on_command
global_config = get_driver().config
config = Config.parse_obj(global_config)

from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11 import Message
from nonebot.adapters.onebot.v11.message import MessageSegment

from selenium import webdriver
import time
import os.path
import multiprocessing as mp

import requests
from datetime import datetime
import json
import smtplib
from email.mime.text import MIMEText


def activeShotHtml():
    # 首先创建一个保存截图的文件夹
    filename = "C:/CodePython/Bot_leetcode/bot_leetcode/plugins/leetcode_everyday/data/"
    if not os.path.isdir(filename):
            # 判断文件夹是否存在，如果不存在就创建一个
            os.makedirs(filename)
    
    
    with open('C:/CodePython/Bot_leetcode/bot_leetcode/plugins/leetcode_everyday/data/urls.txt', 'r') as f:
            lines = f.readlines()
    urls = []
        # thelist = {"1.png", "file:///C:/Users/Administrator/Desktop/leetcodeTmp.html"}
    for line in lines:
            thelist = line.strip().split(",")
            if len(thelist) == 2 and thelist[0] and thelist[1]:
                urls.append((thelist[0], thelist[1]))
    
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')  # 不知为啥只能在无头模式执行才能截全屏
            options.add_argument('--disable-gpu')
            driver = webdriver.Chrome(options=options)
            driver.maximize_window()
            # 返回网页的高度的js代码
            js_height = "return document.body.clientHeight"
            picname = str(thelist[0])
            link = thelist[1]
            print(link)
    
            driver.get(link)
            k = 1
            height = driver.execute_script(js_height)
            while True:
                    if k * 500 < height:
                        js_move = "window.scrollTo(0,{})".format(k * 500)
                        print(js_move)
                        driver.execute_script(js_move)
                        time.sleep(0.2)
                        height = driver.execute_script(js_height)
                        k += 1
                    else:
                        break
            scroll_width = driver.execute_script('return document.body.parentNode.scrollWidth')
            scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')
            driver.set_window_size(scroll_width, scroll_height + 100)
            driver.get_screenshot_as_file("C:/CodePython/Bot_leetcode/bot_leetcode/plugins/leetcode_everyday/data/" + picname)
            print("Process {} get one pic !!!".format(os.getpid()))
            driver.quit()

leetcode_get_html = on_command("leetcode_update")

leetcodeShot = on_command("leetcode")

Helpcommand = on_command("lc_hp")

@leetcode_get_html.handle()
async def leetcode_get_handle():
    try:
        base_url = 'https://leetcode-cn.com'
    # 获取今日每日一题的题名(英文)
        response = requests.post(base_url + "/graphql", json={
            "operationName": "questionOfToday",
            "variables": {},
            "query": "query questionOfToday { todayRecord {   question {     questionFrontendId     questionTitleSlug     __typename   }   lastSubmission {     id     __typename   }   date   userStatus   __typename }}"
        })
        leetcodeTitle = json.loads(response.text).get('data').get('todayRecord')[0].get("question").get('questionTitleSlug')
        # 获取今日每日一题的所有信息
        url = base_url + "/problems/" + leetcodeTitle
        response = requests.post(base_url + "/graphql",
                                json={"operationName": "questionData", "variables": {"titleSlug": leetcodeTitle},
                                    "query": "query questionData($titleSlug: String!) {  question(titleSlug: $titleSlug) {    questionId    questionFrontendId    boundTopicId    title    titleSlug    content    translatedTitle    translatedContent    isPaidOnly    difficulty    likes    dislikes    isLiked    similarQuestions    contributors {      username      profileUrl      avatarUrl      __typename    }    langToValidPlayground    topicTags {      name      slug      translatedName      __typename    }    companyTagStats    codeSnippets {      lang      langSlug      code      __typename    }    stats    hints    solution {      id      canSeeDetail      __typename    }    status    sampleTestCase    metaData    judgerAvailable    judgeType    mysqlSchemas    enableRunCode    envInfo    book {      id      bookName      pressName      source      shortDescription      fullDescription      bookImgUrl      pressImgUrl      productUrl      __typename    }    isSubscribed    isDailyQuestion    dailyRecordStatus    editorType    ugcQuestionId    style    __typename  }}"})
        # 转化成json格式
        jsonText = json.loads(response.text).get('data').get("question")
        # 题目题号
        no = jsonText.get('questionFrontendId')
        # 题名（中文）
        leetcodeTitle = jsonText.get('translatedTitle')
        # 题目难度级别
        level = jsonText.get('difficulty')
        # 题目内容
        context = jsonText.get('translatedContent')

        # print(context)
        #print(leetcodeTitle)
        file_html = open("C:/CodePython/Bot_leetcode/bot_leetcode/plugins/leetcode_everyday/data/leetcodeTmp.html", "r+")
        file_html.write(context)
        file_html.close()

        print("Leetcode writing is done!")
        activeShotHtml()
        await leetcode_get_html.send("Bot_Plugin_Test[LeecodeUpdate]: update failed!")
    except:
        await leetcode_get_html.send("Bot_Plugin_Test[LeecodeUpdate]: update complete!")

@Helpcommand.handle()
async def help_cemu(bot: Bot, event:Event):
     await Helpcommand.send("Bot_Plugin_Test[HELP]:\n/leetcode_update: 更新每日一题\n/leetcode: 输出当前保存的每日一题")
 
 
# def webshot(tup):
#     print("当前进程%d已启动" %os.getpid())
 
#     options = webdriver.ChromeOptions()
#     options.add_argument('--headless')  # 不知为啥只能在无头模式执行才能截全屏
#     options.add_argument('--disable-gpu')
#     driver = webdriver.Chrome(options=options)
#     driver.maximize_window()
#     # 返回网页的高度的js代码
#     js_height = "return document.body.clientHeight"
#     picname = str(tup[0])
#     link = tup[1]
#     print(link)
 
#     try:
#         driver.get(link)
#         k = 1
#         height = driver.execute_script(js_height)
#         while True:
#             if k * 500 < height:
#                 js_move = "window.scrollTo(0,{})".format(k * 500)
#                 print(js_move)
#                 driver.execute_script(js_move)
#                 time.sleep(0.2)
#                 height = driver.execute_script(js_height)
#                 k += 1
#             else:
#                 break
#         scroll_width = driver.execute_script('return document.body.parentNode.scrollWidth')
#         scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')
#         driver.set_window_size(scroll_width, scroll_height + 100)
#         driver.get_screenshot_as_file("D:/pics/" + picname)
#         print("Process {} get one pic !!!".format(os.getpid()))
#         driver.quit()
#     except Exception as e:
#         print(picname, e)
 
 

# "C:\CodePython\Bot_leetcode\bot_leetcode\plugins\leetcode_everyday\data\leetcodeTmp.html"
@leetcodeShot.handle()
async def leetcodeShotFunc(bot:Bot, event: Event):
    cq = "[CQ:image,file=file:///C:\CodePython\Bot_leetcode\\bot_leetcode\plugins\leetcode_everyday\data\\1.png]"
    await leetcodeShot.send(Message(cq))

        # cq = "[[CQ:image,file=file:///D:\pics\1.png,id=40000]]"