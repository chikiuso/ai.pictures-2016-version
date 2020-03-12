import wikipedia
import jieba
import jieba.posseg as pseg
import jieba.analyse
import urllib3
import urllib
import urllib.request
from urllib.parse import quote_plus
from googleapiclient.discovery import build
import requests
import base64
import csv
import os
import re
import time
import glob
import string
import socket
import math
import sys
from snownlp import SnowNLP
import itertools
from shutil import copyfile
from bs4 import BeautifulSoup
import numpy as np
from scipy import *
from PIL import Image
import pytesseract
import json
import xml.etree.ElementTree as etree
from langdetect import detect
from hanziconv import HanziConv
import subprocess
from gtts import gTTS
from subprocess import Popen, PIPE
from moviepy.editor import *
from moviepy.video import *
from urllib.request import unquote


def bing_search(query, search_type):

	# Your base API URL; change "Image" to "Web" for web results.
	url = "https://api.datamarket.azure.com/Bing/Search/v1/Image"

	# Query parameters. Don't try using urlencode here.
	# Don't ask why, but Bing needs the "$" in front of its parameters.
	# The '$top' parameter limits the number of search results.
	#url += "?$format=json&$top=1&ImageFilters=%27Color:Color%2BSize:Large%27&Query=%27{}%27".format(quote_plus(query))
	url += "?$format=json&$top=1&ImageFilters=%27Color:Color%27&Query=%27{}%27".format(quote_plus(query))

	# You can get your primary account key at https://datamarket.azure.com/account
	r = requests.get(url, auth=("",""))
	resp = json.loads(r.text)

	#result_list = resp['d']['results']
	#return resp['d']['results'][0]['MediaUrl']
	return resp['d']['results']

	#return(resp)

skipto = 0
havevideo = 0
socket.setdefaulttimeout(90)
wikipedia.set_lang("zh")

whattomake = '徐少強'
wikilist = re.split('\n== |\n=== |\n==== ',wikipedia.page(whattomake).content)
wikipage = wikipedia.page(whattomake).html()
if wikipage.find("<h2>目录</h2>")>-1:
	wikilistinhtml = re.split('<h2>|<h3>|<h4>',wikipage.split("<h2>目录</h2>")[1])
elif wikipage.find("<h2>目錄</h2>")>-1:
	wikilistinhtml = re.split('<h2>|<h3>|<h4>',wikipage.split("<h2>目錄</h2>")[1])
wikilist.pop(0)
wikilistinhtml.pop(0)
print(str(len(wikilist))+"="+str(len(wikilistinhtml)))

for idxitemlist, wiki in enumerate(wikilist):

	#service = build('translate', 'v2', developerKey='')


	if wiki.find('====',1)>0:
		whattomaketitle = wiki.split(' ====',1)[0]
		wiki = wiki.split(' ====',1)[1]
		print(whattomaketitle)
	elif wiki.find('===',1)>0:
		whattomaketitle = wiki.split(' ===',1)[0]
		wiki = wiki.split(' ===',1)[1]
		print(whattomaketitle)
	elif wiki.find('==',1)>0:
		whattomaketitle = wiki.split(' ==',1)[0]
		wiki = wiki.split(' ==',1)[1]
		print(whattomaketitle)

	wiki = wiki.replace('\n','')
	wiki = wiki.replace('〈','')
	wiki = wiki.replace('〉','')
	wiki = wiki.replace('=','')


	if len(wiki)<20:
		continue

	if skipto>idxitemlist:
		continue


	wiki_old = wiki

	wikitempwhole = ""

	wiki_old = wiki_old.split("$")
	for eachsentold in wiki_old:
		if len(eachsentold) > 1:
			wikitempwhole = wikitempwhole + HanziConv.toTraditional(eachsentold)
		else:
			wikitempwhole = wikitempwhole + eachsentold
		

	wiki = wikitempwhole
	print(wiki)

	#wiki = HanziConv.toTraditional(wiki)


	foldertoempty = glob.glob('/Users/chikiuso/Downloads/images/*')
	for f in foldertoempty:
		os.remove(f)

	wikilistinhtml[idxitemlist] = HanziConv.toTraditional(wikilistinhtml[idxitemlist])

	wikilistinhtml[idxitemlist] = '.'+wikilistinhtml[idxitemlist]

	soup = BeautifulSoup(wikilistinhtml[idxitemlist])
	link_text = []
	for link in soup.find_all('a'):
		linklinktext = link.text
		if (link.text.find("/")<0)&(link.get('href').find(":")<0)&(linklinktext != "")&(link.text[:1] != "[")&(link.get('href').find("#")<0)&(link.text.find("'")<0):
			link_text.append((linklinktext,link.get('href')))
			#print(link.get('href'))


	foldertoempty = glob.glob('/Users/chikiuso/Downloads/images/mp3/*')
	for f in foldertoempty:
		os.remove(f)

	if len(wiki) >= 100:
		n = 100
		ffmpegstring = "concat:"
		wikiarray = [wiki[i:i+n] for i in range(0, len(wiki), n)]
		for idxwiki, wikisent in enumerate(wikiarray):
			tts = gTTS(text=wikisent, lang='zh-yue')
			tts.save("/Users/chikiuso/Downloads/mp3/"+str(idxwiki)+".mp3")
			ffmpegstring += "mp3/"+str(idxwiki)+".mp3|"
		ffmpegstring = ffmpegstring[:-1]
		r = subprocess.Popen('ffmpeg -i "'+ffmpegstring+'" -c  copy -write_xing 0 -y /Users/chikiuso/Downloads/wiki.mp3',bufsize=2048,shell=True,close_fds=True,stdout=PIPE)
		with r.stdout:
			for line6 in iter(r.stdout.readline, b''):
				print (line6),
		r.wait()
			
	else:
		tts = gTTS(text=wiki, lang='zh-yue')
		tts.save("/Users/chikiuso/Downloads/wiki.mp3")

	e = subprocess.Popen('ffmpeg -i wiki.mp3 -filter:a "atempo=1.18" -vn -y -write_xing 0 wiki2.mp3', bufsize=2048,shell=True,close_fds=True,stdout=PIPE)
	with e.stdout:
		for line5 in iter(e.stdout.readline, b''):
			print (line5),
	e.wait()

	#k = subprocess.Popen('ffmpeg -i wiki2.mp3 -af silenceremove=0:0:0:-1:0.3:-90dB -write_xing 0 -y wiki3.mp3', bufsize=2048,shell=True,close_fds=True,stdout=PIPE)
	k = subprocess.Popen('ffmpeg -i wiki2.mp3 -af silenceremove=1:0:0:-1:0.01:-80dB -write_xing 0 -y wiki3.mp3', bufsize=2048,shell=True,close_fds=True,stdout=PIPE)
	with k.stdout:
		for line8 in iter(k.stdout.readline, b''):
			print (line8),
	k.wait()


	all_sent = []
	filtered_sent = []
	tag_sent = []
	imgclip = []
	global last_sent

	temp_sent = []
	temp_links = []
	last_sent = None

	print("wiki="+str(wiki))

	winniedoc = SnowNLP(wiki)

	for idxnoun, noun in enumerate(link_text):
		print("noun="+str(noun))
		prefixfix = ""

		if wiki.find(noun[0]) > -1:
		
			global linelineline
			if (whattomake.find("(")>0):
				#whattomake2 = whattomake[:whattomake.find("(")]
				whattomake2 = whattomake.replace("("," ").replace(")","")
			else:
				whattomake2 = whattomake

			videosearch1 = requests.get("http://suggestqueries.google.com/complete/search?client=firefox&ds=yt&q="+whattomake2+"%20"+noun[0])
			videosearch2 = videosearch1.json()
			if len(videosearch2[1]) > 0:

				prefixfix = "@"
				havevideo = 1
			else:

				if (len(noun[0])>3)&(prefixfix == ""):
					prefixfix = "#"
				elif prefixfix == "":
					ents = pseg.cut(HanziConv.toSimplified(wiki))
					for hotinso, flag in ents:
						if (HanziConv.toSimplified(wiki).find(str(hotinso))>-1)&(HanziConv.toSimplified(wiki).find(HanziConv.toSimplified(noun[0]))>-1):
							if (HanziConv.toSimplified(wiki).find(str(hotinso))<=(HanziConv.toSimplified(wiki).find(HanziConv.toSimplified(noun[0]))+len(HanziConv.toSimplified(noun[0]))))&(HanziConv.toSimplified(wiki).find(HanziConv.toSimplified(noun[0]))<=(HanziConv.toSimplified(wiki).find(str(hotinso))+len(str(hotinso)))):
								if flag in ('ns','nr','nz'):
									prefixfix = "#"
									print(noun[0]+"="+flag)
									break

			if prefixfix == "":
				prefixfix = "*"


			if (link_text[0][0] == noun[0])&(len(temp_sent)<1):
				word_start = wiki.find(noun[0])
				word_end = word_start + len(noun[0])
				temp_sent.append(wiki[:word_start])
				temp_sent.append(prefixfix+str(wiki[word_start:word_end]))
				tag_sent.append(str(wiki[word_start:word_end]))
				temp_sent.append(wiki[word_end:])
				print("first="+prefixfix+noun[0])
			
			elif link_text[-1][0] == noun[0]:
				last_sent = temp_sent[len(temp_sent)-1]
				if last_sent.find(noun[0]) > -1:
					temp_sent.pop()
					word_start = last_sent.find(noun[0])
					word_end = word_start + len(noun[0])
					temp_sent.append(last_sent[:word_start])
					temp_sent.append(prefixfix+str(last_sent[word_start:word_end]))
					tag_sent.append(str(last_sent[word_start:word_end]))
					temp_sent.append(last_sent[word_end:])
					print("last="+prefixfix+noun[0])
				
			else:
				last_sent = temp_sent[len(temp_sent)-1]
				if last_sent.find(noun[0]) > -1:
					#last_sent = temp_sent[len(temp_sent)-1]
					temp_sent.pop()
					word_start = last_sent.find(noun[0])
					word_end = word_start + len(noun[0])
					temp_sent.append(last_sent[:word_start])
					temp_sent.append(prefixfix+str(last_sent[word_start:word_end]))
					tag_sent.append(str(last_sent[word_start:word_end]))
					temp_sent.append(last_sent[word_end:])
					print("other="+prefixfix+noun[0])
				
			all_sent = temp_sent
			all_sent = filter(lambda a: a != "", filter(lambda a: a != " ", all_sent))


	all_sent2 = []

	jieba.set_dictionary('dict.txt.big')

	for idxsent, eachsent in enumerate(all_sent):
		temp_sent = []
		numberofkeywords = round(len(eachsent)/80)
		if (eachsent[:1] != "#") & (eachsent[:1] != "@") & (numberofkeywords > 0):
			#print(eachsent)
			numberofkeywords = round(len(eachsent)/80)
			blob = jieba.analyse.extract_tags(eachsent, topK=numberofkeywords)
			sentencearray = ""
			if len(blob) > 0:
				for sentence in blob:

					index = eachsent.find(sentence)
					endchar = index + len(sentence)
				

					videosearch1 = requests.get("http://suggestqueries.google.com/complete/search?client=firefox&ds=yt&q="+whattomake2+"%20"+sentence)
					videosearch2 = videosearch1.json()
					if len(videosearch2[1]) > 0:
						eachsent = eachsent[:index] + "$@" + eachsent[index:endchar] + "$" + eachsent[endchar:]
						havevideo = 1
					elif idxsent%7==0:
						eachsent = eachsent[:index] + "$&" + eachsent[index:endchar] + "$" + eachsent[endchar:]
						havevideo = 1
					else:
						eachsent = eachsent[:index] + "$*" + eachsent[index:endchar] + "$" + eachsent[endchar:]

				temp_sent = eachsent.split("$")

		if len(temp_sent) > 0:
			print(temp_sent)
			all_sent2.append(temp_sent)
			temp_sent = []
		else:
			print(eachsent)
			all_sent2.append([str(eachsent)])
	#print("all_sent2a"+str(all_sent2))
	all_sent2 = list(itertools.chain(*all_sent2))
	#print("all_sent2b"+str(all_sent2))


	filtered_sent = filter(lambda a: a != "「", filter(lambda a: a != "」", filter(lambda a: a != "《", filter(lambda a: a != "》", filter(lambda a: a != "，", filter(lambda a: a != "。", filter(lambda a: a != "、", filter(lambda a: a != "*", filter(lambda a: a != "#", filter(lambda a: a != "@",filter(lambda a: a != ", ",filter(lambda a: a != " ,",filter(lambda a: a != ",",filter(lambda a: a != ".", filter(lambda a: a != " ", filter(lambda a: a != "", all_sent2))))))))))))))))
	#print(filtered_sent)
	dataFile = open('/Users/chikiuso/Downloads/text.txt', 'w')
	for eachitem in filtered_sent:
		dataFile.write(str(eachitem)+'\n')
	dataFile.close()
	p = subprocess.Popen("python3 -m aeneas.tools.execute_task wiki3.mp3 text.txt 'task_language=zho|os_task_file_format=xml|is_text_type=plain' map.xml", bufsize=2048,shell=True,close_fds=True,stdout=PIPE)
	with p.stdout:
		for line in iter(p.stdout.readline, b''):
			print (line),
	p.wait()

	audioclip = AudioFileClip("/Users/chikiuso/downloads/wiki3.mp3")

	try:
		tree = etree.parse('map.xml')
	except:
		continue

	root = tree.getroot()
	for child in root:
		if (child[0].text[:1]!="#")&(child[0].text[:1]!="@")&(child[0].text[:1]!="*"):
			root.remove(child)
	for eachindex, eachjson in enumerate(root):

		if eachjson[0].text[:1]=="#":
			try:

				chikiuso = ""
				for linkgetback in link_text:
					if linkgetback[0]==eachjson[0].text[1:]:
						if linkgetback[1].find("?")<0:
							chikiuso = unquote(linkgetback[1][linkgetback[1].rfind("/")+1:].replace("_"," ").replace("("," ").replace(")",""))
							print("chikiuso="+chikiuso)
						else:
							chikiuso = linkgetback[0]
						
				aaa = bing_search(chikiuso, 'Image')
				aaaindex = 0
				while (not os.path.isfile("/Users/chikiuso/downloads/images/"+eachjson.attrib['id']+".jpg")):
					urllib.request.urlretrieve(str(aaa[aaaindex]['MediaUrl']), "images/"+str(eachjson.attrib['id'])+".jpg")
					aaaindex = aaaindex + 1


				imgtemp = ImageClip("/Users/chikiuso/downloads/images/"+eachjson.attrib['id']+".jpg")
				imgtemp = imgtemp.set_start(round(float(eachjson.attrib['begin']),2))
				imgtemp = imgtemp.set_end(round(float(eachjson.attrib['end']),2))
				try:
					imgtemp = imgtemp.set_end(round(float(root[eachindex+1].attrib['begin']),2))
				except:
					pass
				imgtemp = imgtemp.set_position(('center','center'))
				if havevideo == 1:
					imgtemp = imgtemp.set_fps(18)
				else:
					imgtemp = imgtemp.set_fps(6)

				imgtemp2 = imgtemp
				imgtemp = imgtemp.resize(width=1280)
				imgtemp = imgtemp.fx( vfx.painting, saturation = 0.36,black = 0.0006)
				imgclip.append(imgtemp)

				imgtemp = imgtemp2

				if (imgtemp.w<500)&(imgtemp.h<500):
					imgtemp = imgtemp.fx( vfx.painting, saturation = 1,black = 0.0006)

				if imgtemp.w > imgtemp.h*1.7:
					imgtemp = imgtemp.resize(width=1280)
				else:
					imgtemp = imgtemp.resize(height=720)
				imgclip.append(imgtemp)


			except:
				pass



		elif eachjson[0].text[:1]=="*":
			try:

				aaa = bing_search(whattomake2+" "+eachjson[0].text[1:], 'Image')
				aaaindex = 0
				while (not os.path.isfile("/Users/chikiuso/downloads/images/"+eachjson.attrib['id']+".jpg")):
					urllib.request.urlretrieve(str(aaa[aaaindex]['MediaUrl']), "images/"+str(eachjson.attrib['id'])+".jpg")
					aaaindex = aaaindex + 1

				imgtemp = ImageClip("/Users/chikiuso/downloads/images/"+eachjson.attrib['id']+".jpg")
				imgtemp = imgtemp.set_start(round(float(eachjson.attrib['begin']),2))
				imgtemp = imgtemp.set_end(round(float(eachjson.attrib['end']),2))
				try:
					imgtemp = imgtemp.set_end(round(float(root[eachindex+1].attrib['begin']),2))
				except:
					pass
				imgtemp = imgtemp.set_position(('center','center'))
				if havevideo == 1:
					imgtemp = imgtemp.set_fps(18)
				else:
					imgtemp = imgtemp.set_fps(6)

				imgtemp2 = imgtemp
				imgtemp = imgtemp.resize(width=1280)
				imgtemp = imgtemp.fx( vfx.painting, saturation = 0.36,black = 0.0006)
				imgclip.append(imgtemp)

				imgtemp = imgtemp2

				if (imgtemp.w<500)&(imgtemp.h<500):
					imgtemp = imgtemp.fx( vfx.painting, saturation = 1,black = 0.0006)

				if imgtemp.w > imgtemp.h*1.7:
					imgtemp = imgtemp.resize(width=1280)
				else:
					imgtemp = imgtemp.resize(height=720)
				imgclip.append(imgtemp)

			except:
				pass


		elif eachjson[0].text[:1]=="{":
			try:

				aaa = bing_search(eachjson[0].text[1:], 'Image')
				aaaindex = 0
				while (not os.path.isfile("/Users/chikiuso/downloads/images/"+eachjson.attrib['id']+".jpg")):
					urllib.request.urlretrieve(str(aaa[aaaindex]['MediaUrl']), "images/"+str(eachjson.attrib['id'])+".jpg")
					aaaindex = aaaindex + 1

				imgtemp = ImageClip("/Users/chikiuso/downloads/images/"+eachjson.attrib['id']+".jpg")
				imgtemp = imgtemp.set_start(round(float(eachjson.attrib['begin']),2))
				imgtemp = imgtemp.set_end(round(float(eachjson.attrib['end']),2))
				try:
					imgtemp = imgtemp.set_end(round(float(root[eachindex+1].attrib['begin']),2))
				except:
					pass
				imgtemp = imgtemp.set_position(('center','center'))
				if havevideo == 1:
					imgtemp = imgtemp.set_fps(18)
				else:
					imgtemp = imgtemp.set_fps(6)

				imgtemp2 = imgtemp
				imgtemp = imgtemp.resize(width=1280)
				imgtemp = imgtemp.fx( vfx.painting, saturation = 0.36,black = 0.0006)
				imgclip.append(imgtemp)

				imgtemp = imgtemp2

				if (imgtemp.w<500)&(imgtemp.h<500):
					imgtemp = imgtemp.fx( vfx.painting, saturation = 1,black = 0.0006)

				if imgtemp.w > imgtemp.h*1.7:
					imgtemp = imgtemp.resize(width=1280)
				else:
					imgtemp = imgtemp.resize(height=720)
				imgclip.append(imgtemp)

			except:
				pass

		elif eachjson[0].text[:1]=="}":
			try:

				aaa = bing_search(eachjson[0].text[1:], 'Image')
				aaaindex = 0
				while (not os.path.isfile("/Users/chikiuso/downloads/images/"+eachjson.attrib['id']+".jpg")):
					urllib.request.urlretrieve(str(aaa[aaaindex]['MediaUrl']), "images/"+str(eachjson.attrib['id'])+".jpg")
					aaaindex = aaaindex + 1

				imgtemp = ImageClip("/Users/chikiuso/downloads/images/"+eachjson.attrib['id']+".jpg")
				imgtemp = imgtemp.set_start(round(float(eachjson.attrib['begin']),2))
				imgtemp = imgtemp.set_end(round(float(eachjson.attrib['end']),2))
				try:
					imgtemp = imgtemp.set_end(round(float(root[eachindex+1].attrib['begin']),2))
				except:
					pass

				imgtemp = imgtemp.set_position(('center','center'))
				if havevideo == 1:
					imgtemp = imgtemp.set_fps(18)
				else:
					imgtemp = imgtemp.set_fps(6)

				imgtemp2 = imgtemp
				imgtemp = imgtemp.resize(width=1280)
				imgtemp = imgtemp.fx( vfx.painting, saturation = 0.36,black = 0.0006)
				imgclip.append(imgtemp)

				imgtemp = imgtemp2

				if (imgtemp.w<500)&(imgtemp.h<500):
					imgtemp = imgtemp.fx( vfx.painting, saturation = 1,black = 0.0006)

				if imgtemp.w > imgtemp.h*1.7:
					imgtemp = imgtemp.resize(width=1280)
				else:
					imgtemp = imgtemp.resize(height=720)
				imgclip.append(imgtemp)

			except:
				pass


		elif eachjson[0].text[:1]=="[":
			try:

				aaa = bing_search(eachjson[0].text[1:], 'Image')
				aaaindex = 0
				while (not os.path.isfile("/Users/chikiuso/downloads/images/"+eachjson.attrib['id']+".jpg")):
					urllib.request.urlretrieve(str(aaa[aaaindex]['MediaUrl']), "images/"+str(eachjson.attrib['id'])+".jpg")
					aaaindex = aaaindex + 1

				imgtemp = ImageClip("/Users/chikiuso/downloads/images/"+eachjson.attrib['id']+".jpg")
				imgtemp = imgtemp.set_start(round(float(eachjson.attrib['begin']),2))
				imgtemp = imgtemp.set_end(round(float(eachjson.attrib['end']),2))
				try:
					imgtemp = imgtemp.set_end(round(float(root[eachindex+1].attrib['begin']),2))
				except:
					pass
				imgtemp = imgtemp.set_position(('center','center'))
				if havevideo == 1:
					imgtemp = imgtemp.set_fps(18)
				else:
					imgtemp = imgtemp.set_fps(6)

				imgtemp2 = imgtemp
				imgtemp = imgtemp.resize(width=1280)
				imgtemp = imgtemp.fx( vfx.painting, saturation = 0.36,black = 0.0006)
				imgclip.append(imgtemp)

				imgtemp = imgtemp2

				if (imgtemp.w<500)&(imgtemp.h<500):
					imgtemp = imgtemp.fx( vfx.painting, saturation = 1,black = 0.0006)

				if imgtemp.w > imgtemp.h*1.7:
					imgtemp = imgtemp.resize(width=1280)
				else:
					imgtemp = imgtemp.resize(height=720)
				imgclip.append(imgtemp)

			except:
				pass

		elif eachjson[0].text[:1]=="]":
			try:

				aaa = bing_search(eachjson[0].text[1:]+" logo", 'Image')
				aaaindex = 0
				while (not os.path.isfile("/Users/chikiuso/downloads/images/"+eachjson.attrib['id']+".jpg")):
					urllib.request.urlretrieve(str(aaa[aaaindex]['MediaUrl']), "images/"+str(eachjson.attrib['id'])+".jpg")
					aaaindex = aaaindex + 1

				imgtemp = ImageClip("/Users/chikiuso/downloads/images/"+eachjson.attrib['id']+".jpg")
				imgtemp = imgtemp.set_start(round(float(eachjson.attrib['begin']),2))
				imgtemp = imgtemp.set_end(round(float(eachjson.attrib['end']),2))
				try:
					imgtemp = imgtemp.set_end(round(float(root[eachindex+1].attrib['begin']),2))
				except:
					pass

				imgtemp = imgtemp.set_position(('center','center'))
				if havevideo == 1:
					imgtemp = imgtemp.set_fps(18)
				else:
					imgtemp = imgtemp.set_fps(6)

				imgtemp2 = imgtemp
				imgtemp = imgtemp.resize(width=1280)
				imgtemp = imgtemp.fx( vfx.painting, saturation = 0.36,black = 0.0006)
				imgclip.append(imgtemp)

				imgtemp = imgtemp2

				if (imgtemp.w<500)&(imgtemp.h<500):
					imgtemp = imgtemp.fx( vfx.painting, saturation = 1,black = 0.0006)

				if imgtemp.w > imgtemp.h*1.7:
					imgtemp = imgtemp.resize(width=1280)
				else:
					imgtemp = imgtemp.resize(height=720)
				imgclip.append(imgtemp)

			except:
				pass



		elif (eachjson[0].text[:1]=="@")|(eachjson[0].text[:1]=="&"):

			try:

				if (eachjson[0].text[:1]=="@"):
					y = subprocess.Popen("python3 youtubesearch.py --q '"+whattomake2+" "+eachjson[0].text.replace("@","")+"'", bufsize=2048,shell=True,close_fds=True,stdout=PIPE)
				elif (eachjson[0].text[:1]=="&"):
					#if len(wiki)<200:
						#y = subprocess.Popen("python3 youtubesearch.py --q '"+whattomake2+"'", bufsize=2048,shell=True,close_fds=True,stdout=PIPE)
					#else:
					y = subprocess.Popen("python3 youtubesearch.py --q '"+whattomake2+" "+eachjson[0].text.replace("&","")+"'", bufsize=2048,shell=True,close_fds=True,stdout=PIPE)




				with y.stdout:
					for line in iter(y.stdout.readline, b''):
						linelineline = line
				y.wait()

				print(linelineline)
				linelineline = linelineline.decode("utf-8").replace('\n','')

				m = subprocess.Popen("youtube-dl --username --password --no-check-certificate --format mp4 -f worst --output 'images/"+eachjson.attrib['id']+".mp4' -- '"+linelineline.replace('\n','')+"'", bufsize=2048,shell=True,close_fds=True,stdout=PIPE)
				with m.stdout:
					for line2 in iter(m.stdout.readline, b''):
						print (line2),
				m.wait()

				n = subprocess.Popen("youtube-dl --username --password --no-check-certificate --format mp4 -f best --output 'images/"+eachjson.attrib['id']+"_hd.mp4' -- '"+linelineline.replace('\n','')+"'", bufsize=2048,shell=True,close_fds=True,stdout=PIPE)
				with n.stdout:
					for line3 in iter(n.stdout.readline, b''):
						print (line3),
				n.wait()

				w = subprocess.Popen("scenedetect --input images/"+eachjson.attrib['id']+".mp4 -d content -t 30 --output images/"+eachjson.attrib['id']+".csv", bufsize=2048,shell=True,close_fds=True,stdout=PIPE)
				with w.stdout:
					for line4 in iter(w.stdout.readline, b''):
						print (line4),
				w.wait()

				with open('images/'+eachjson.attrib['id']+'.csv', 'r') as fin:
					data = fin.read().splitlines(True)
				with open('images/'+eachjson.attrib['id']+'.csv', 'w') as fout:
					fout.writelines(data[2:])
				csvfile = open('images/'+eachjson.attrib['id']+'.csv', 'r')
				jsonfile = open('images/'+eachjson.attrib['id']+'.json', 'w')
				fieldnames = ("Scene Number","Frame Number (Start)","Timecode","Start Time (seconds)","Length (seconds)")
				reader = csv.DictReader( csvfile, fieldnames)
				result = []
				for idxrow2, row2 in enumerate(reader):
					print(idxrow2)
					if (idxrow2 < 20):
						#json.dump(row2, jsonfile)
						result.append(row2)
				json.dump(result, jsonfile)
				jsonfile.close()

				videotemp = VideoFileClip("/Users/chikiuso/downloads/images/"+eachjson.attrib['id']+"_hd.mp4")

				dataFile4 = open("/Users/chikiuso/downloads/images/"+eachjson.attrib['id']+".json","r")
				json_result4 = json.loads(dataFile4.read())
				for jackjack in json_result4:
					if (float(jackjack['Length (seconds)'])>5):
						
						f = subprocess.Popen("ffmpeg -i images/"+eachjson.attrib['id']+"_hd.mp4 -vcodec png -ss "+str(float(jackjack['Start Time (seconds)'])+1.2)+" -vframes 1 -an -f rawvideo -y images/"+eachjson.attrib['id']+".png",bufsize=2048,shell=True,close_fds=True,stdout=PIPE)
						with f.stdout:
							for line7 in iter(f.stdout.readline, b''):
								print (line7),
						f.wait()
						if len(pytesseract.image_to_string(Image.open("images/"+eachjson.attrib['id']+".png")))<5:
							videotemp = videotemp.subclip(float(jackjack['Start Time (seconds)'])+0.2,float(jackjack['Start Time (seconds)'])+float(jackjack['Length (seconds)']))
							russia = 1
							break

				if russia != 1:
					#print("russia not 1 start="+videotemp.start+"& end="+videotemp.end)
					#videotemp = videotemp.subclip(0.01,0.02)
					#videotemp = videotemp.set_start(0.01)
					#videotemp = videotemp.set_end(0.02)

					aaa = bing_search(whattomake2+" "+eachjson[0].text[1:], 'Image')
					print(eachjson[0].text[1:])
					aaaindex = 0
					while (not os.path.isfile("/Users/chikiuso/downloads/images/"+eachjson.attrib['id']+".jpg")):
						urllib.request.urlretrieve(str(aaa[aaaindex]['MediaUrl']), "images/"+str(eachjson.attrib['id'])+".jpg")
						print("loading="+str(eachjson.attrib['id']))
						aaaindex = aaaindex + 1

					imgtemp = ImageClip("/Users/chikiuso/downloads/images/"+eachjson.attrib['id']+".jpg")
					imgtemp = imgtemp.set_start(round(float(eachjson.attrib['begin']),2))
					imgtemp = imgtemp.set_end(round(float(eachjson.attrib['end']),2))
					try:
						imgtemp = imgtemp.set_end(round(float(root[eachindex+1].attrib['begin']),2))
					except:
						pass

					imgtemp = imgtemp.set_position(('center','center'))
					if havevideo == 1:
						imgtemp = imgtemp.set_fps(18)
					else:
						imgtemp = imgtemp.set_fps(6)

					imgtemp2 = imgtemp
					imgtemp = imgtemp.resize(width=1280)
					imgtemp = imgtemp.fx( vfx.painting, saturation = 0.36,black = 0.0006)
					imgclip.append(imgtemp)

					imgtemp = imgtemp2

					if (imgtemp.w<500)&(imgtemp.h<500):
						imgtemp = imgtemp.fx( vfx.painting, saturation = 1,black = 0.0006)

					if imgtemp.w > imgtemp.h*1.7:
						imgtemp = imgtemp.resize(width=1280)
					else:
						imgtemp = imgtemp.resize(height=720)
					imgclip.append(imgtemp)

				elif russia == 1:
					videotemp = videotemp.set_start(round(float(eachjson.attrib['begin']),2))
					timeout = time.time() + 60
					while ((float(eachjson.attrib['begin'])+4)>float(root[eachindex+1].attrib['begin'])):
						if time.time() > timeout:
							break
						del root[eachindex+1]
					videotemp = videotemp.set_end(round(float(root[eachindex+1].attrib['begin']),2))

					if videotemp.end - videotemp.start > 12:
						videotemp = videotemp.set_end(videotemp.start+12)
					
					if videotemp.w > videotemp.h*1.7:
						videotemp = videotemp.resize(width=1280)
					else:
						videotemp = videotemp.resize(height=720)
					videotemp = videotemp.set_position(('center','center'))
					if havevideo == 1:
						videotemp = videotemp.set_fps(18)
					else:
						videotemp = videotemp.set_fps(6)
					imgclip.append(videotemp)

			except IndexError:
				videotemp = videotemp.set_end(videotemp.start+6)
				print("last="+str(eachjson))
				pass
			except:
				try:
					videotemp = videotemp.subclip(0.01,0.02)
					videotemp = videotemp.set_start(0.01)
					videotemp = videotemp.set_end(0.02)
				except:
					print("ok")

				pass
			
			try:
				if videotemp.w > videotemp.h*1.7:
					videotemp = videotemp.resize(width=1280)
				else:
					videotemp = videotemp.resize(height=720)
		
				videotemp = videotemp.set_position(('center','center'))
				if havevideo == 1:
					videotemp = videotemp.set_fps(18)
				else:
					imgtemp = imgtemp.set_fps(6)
				imgclip.append(videotemp)
			except:
				pass



	imgtemp = ImageClip("/Users/chikiuso/downloads/bg.jpg")
	imgtemp = imgtemp.set_start(audioclip.duration-1)
	imgtemp = imgtemp.set_duration(1)
	imgtemp = imgtemp.set_position(('center','center'))
	if havevideo == 1:
		imgtemp = imgtemp.set_fps(18)
	else:
		imgtemp = imgtemp.set_fps(6)
	imgclip.append(imgtemp)


	imgtemp = ImageClip("/Users/chikiuso/downloads/caption.png")
	imgtemp = imgtemp.set_start(0.01)
	imgtemp = imgtemp.set_duration(audioclip.duration)
	imgtemp = imgtemp.set_position(('center','bottom'))
	if havevideo == 1:
		imgtemp = imgtemp.set_fps(18)
	else:
		imgtemp = imgtemp.set_fps(6)
	imgclip.append(imgtemp)


	print(imgclip[0].start)
	if imgclip[0].start > 0.1:

		try:
			aaa = bing_search(whattomake2, 'Image')
			aaaindex = 0
			timeout = time.time() + 60
			while (not os.path.isfile("/Users/chikiuso/downloads/images/f000000.jpg")):
				if time.time() > timeout:
					break

				urllib.request.urlretrieve(str(aaa[aaaindex]['MediaUrl']), "images/f000000.jpg")
				aaaindex = aaaindex + 1
		
			imgtemp = ImageClip("/Users/chikiuso/downloads/images/f000000.jpg")
			imgtemp = imgtemp.set_start(0.01)
			imgtemp = imgtemp.set_end(float(imgclip[0].start))
			imgtemp = imgtemp.set_position(('center','center'))
			if havevideo == 1:
				imgtemp = imgtemp.set_fps(18)
			else:
				imgtemp = imgtemp.set_fps(6)

			imgtemp2 = imgtemp
			imgtemp = imgtemp.resize(width=1280)
			imgtemp = imgtemp.fx( vfx.painting, saturation = 0.36,black = 0.0006)
			imgclip.append(imgtemp)

			imgtemp = imgtemp2

			if (imgtemp.w<500)&(imgtemp.h<500):
				imgtemp = imgtemp.fx( vfx.painting, saturation = 1,black = 0.0006)

			if imgtemp.w > imgtemp.h*1.7:
				imgtemp = imgtemp.resize(width=1280)
			else:
				imgtemp = imgtemp.resize(height=720)
			imgclip.append(imgtemp)

		except:
			pass


	# start of caption
	newwiki = []



	doc = SnowNLP(wiki)
	for sentence2 in doc.sentences:
		splitsent = str(sentence2).split("、")
		for splitsent2 in splitsent:
			if len(splitsent2)>30:
				splitsent2 = [splitsent2[:14],splitsent2[14:28],splitsent2[28:]]
			elif len(splitsent2)>15:
				splitsent2 = [splitsent2[:14],splitsent2[14:]]
			else:
				splitsent2 = [splitsent2]
			
			newwiki.append(splitsent2)

	newwiki = list(itertools.chain(*newwiki))
	dataFile2 = open('/Users/chikiuso/Downloads/text2.txt', 'w')
	for idxeacheach2, eachitem2 in enumerate(newwiki):
		dataFile2.write(str(eachitem2)+'\n')
	dataFile2.close()

	p2 = subprocess.Popen("python3 -m aeneas.tools.execute_task wiki3.mp3 text2.txt 'task_language=zho|os_task_file_format=xml|is_text_type=plain' map2.xml", bufsize=2048,shell=True,close_fds=True,stdout=PIPE)
	with p2.stdout:
		for line in iter(p2.stdout.readline, b''):
			print (line),
	p2.wait()

	tree2 = etree.parse('map2.xml')
	root2 = tree2.getroot()
	for eachindex2, eachjson2 in enumerate(root2):
		txttemp = TextClip(eachjson2[0].text,color='white', stroke_color='black', fontsize=50, method='caption', align='center', size=(1150,110), stroke_width=0.8, font="/library/fonts/儷黑 Pro.ttf")
		txttemp = txttemp.set_start(round(float(eachjson2.attrib['begin']),2))
		try:
			txttemp = txttemp.set_end(round(float(root2[eachindex2+1].attrib['begin']),2))
		except:
			txttemp = txttemp.set_end(audioclip.duration-1)
		txttemp = txttemp.set_position(('center','bottom'))
		if havevideo == 1:
			txttemp = txttemp.set_fps(18)
		else:
			txttemp = txttemp.set_fps(6)
		imgclip.append(txttemp)






	screensize = (1280,720)
	video = CompositeVideoClip(imgclip,size=screensize)
	video = video.set_audio(audioclip)
	if havevideo == 1:
		video = video.set_fps(18)
	else:
		video = video.set_fps(6)
	video = video.set_duration(audioclip.duration)

	try:
		video.write_videofile("videoupload.webm")
	except:
		continue


	tag_sent = filter(lambda a: len(a) < 25, tag_sent)
	print("string="+str(','.join(tag_sent)))
	q = subprocess.Popen("youtube-upload --title='"+str(whattomake)+" - "+str(whattomaketitle)+"' --description='Credits:Text from Wikipedia,video auto-generated by ai.pictures.' --category=Education --playlist='"+whattomake2+"' --tags='"+str(', '.join(tag_sent))+"' --default-language='zh-yue' --default-audio-language='zh-yue' --client-secrets=client_secrets.json videoupload.webm", bufsize=2048,shell=True,close_fds=True,stdout=PIPE)
	with q.stdout:
		for line in iter(q.stdout.readline, b''):
			print (line),
	q.wait()

	try:
		copyfile("videoupload.webm", "videos/"+whattomake+str(whattomaketitle)+".webm")
	except:
		continue
	
print("end")