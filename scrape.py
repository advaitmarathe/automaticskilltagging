import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
url = "https://www.engageny.org/resource/algebra-i-module-1-topic-"
folder_location = r'webscraping'
if not os.path.exists(folder_location):os.mkdir(folder_location)
response = requests.get(url)
print(response)
alphabet ="abcdefghijklmnopqrstuvwxyz"
def downloadpdfs(url,filename):
	# folder_location = r'webscraping' + filename
	# if not os.path.exists(folder_location):os.mkdir(folder_location)
	path = os.path.join(folder_location,filename)
	if not os.path.isdir(path):
		os.makedirs(path)
	response = requests.get(url)
	soup = BeautifulSoup(response.text, "html.parser")    
	urls = []
	def filter(s):
		if("file" and "token" and "pdf" in s):
			slist = s.split("?token")
			return slist[0]
		else:
			return ""

	for a in soup.find_all('a', href=True):
		url = "https://www.engageny.org/"
		link = a["href"]
		use = filter(link)
		if(use != ""):
			filename = os.path.join(path,use.split('/')[-1])
			with open(filename, 'wb') as f:
				f.write(requests.get(urljoin(url,use)).content)
downloadpdfs(url,"Module 1")
for i in range(1,6):
	init_url = "https://www.engageny.org/resource/algebra-i-"
	module_url = init_url+"module-"+str(i)
	counter = 0
	for topic in range(1,27):
		if counter == 0:
			topic_url = module_url + "-topic"
			for lesson in range(1,100):
				lesson_url = topic_url +"-lesson-" + str(lesson)
				response = requests.get(lesson_url)
				if not response.status_code == 404:
					downloadpdfs(lesson_url,)
			counter = 1
		else:
			topic_url = module_url + "-topic-" + str







	# print ("Found the URL:", link)
# for link in soup.select("a[href$='.pdf']"):
#     #Name the pdf files using the last portion of each link which are unique in this case
#     # filename = os.path.join(folder_location,link['href'].split('/')[-1])
#     # with open(filename, 'wb') as f:
#     #     f.write(requests.get(urljoin(url,link['href'])).content)
#     print(link)
#     print("cool")