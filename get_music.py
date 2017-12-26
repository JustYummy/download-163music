# -*- coding: utf-8 -*-
import requests
import re
import os
import sys
def getMusic(MID, MName, albumName):

	regex = re.compile(r'"url":"[^"]+')
	music_url="http://127.0.0.1:3000/music/url?id="
	url = music_url + MID
	content = requests.get(url).content

	downloadUrl = regex.findall(str(content))
	
	path = sys.path[0]  
	temp_path = os.path.join(path, albumName)
	if not os.path.exists(temp_path):
		os.chdir(path)
		os.mkdir(albumName)

	path = temp_path
	try:
		downloadUrl = re.sub('"url":"', '', str(downloadUrl[0]))
		###method one

		r = requests.get(downloadUrl)

		file_path = os.path.join(path, MName)
		with open(file_path + '.mp3', 'wb') as code:
			code.write(r.content)
	except IndexError:
		pass
	except FileNotFoundError:
		MName = MName.replace('/',' ')
		file_path = os.path.join(path, MName)
		with open(file_path + '.mp3', 'wb') as code:
			code.write(r.content)

def getList(LID):
	regex = re.compile(r'{"name":"[^"]+","id":\d+')
	list_url = "http://127.0.0.1:3000/playlist/detail?id="
	url = list_url + LID

	###转码
	content = requests.get(url)
	content.encoding='utf-8'
	content = content.text

	rawID = regex.findall(str(content))
	delRegex = re.compile(r'{"name":"[^"]+","id":')
	numID = []	#音乐ID
	for i in rawID:
		numID.append(delRegex.sub('', i))

	regex2 = re.compile(r'{"name":"[^"]+')
	nameRegex = re.compile(r'{"name":"')
	rawNameID = regex2.findall(str(content))

	nameList = []
	for i in rawNameID:	#歌名
		nameList.append(nameRegex.sub('', i))

	dic = {}
	for i in range(len(numID)):
		dic[numID[i]] = nameList[i]
	
	regex_text = r'[^"]+","id":' + str(LID)
	albumRegex = re.compile(regex_text)
	albumtext = albumRegex.findall(str(content))
	albumName = albumtext[0]
	# print(albumName)
	del_text = '","id":' + str(LID)
	albumName = re.sub(del_text, '', albumName)
	print(albumName)
	return dic, albumName

if __name__ == '__main__':

	### Open the NetMusicApi first node app.js
	listID = input('Pleaes input you Playlist ID:')
	dic, albumName = getList(str(listID))

	i = 1
	for ID, Name in dic.items():
		print('No.' + str(i) + ' Downloading ' + str(Name))
		getMusic(ID, Name, albumName)
		i += 1
	print('All Done!')







