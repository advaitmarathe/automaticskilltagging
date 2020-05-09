import os
import requests
import docx2txt
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import PyPDF2
import xlwt 
from xlwt import Workbook 
import re
# import textract
url = "https://www.engageny.org/resource/algebra-i-module-1-topic-lesson-1"
folder_location = r'webscraping'
if not os.path.exists(folder_location):os.mkdir(folder_location)
response = requests.get(url)
print(response)
alphabet ="abcdefghijklmnopqrstuvwxyz"
wb = Workbook() 
sheet1 = wb.add_sheet('Sheet 1') 
sheet1.write(0,0, "Module")
sheet1.write(0,1,"Topic")
sheet1.write(0,2,"Skill Name")
sheet1.write(0,3,"Lesson")
sheet1.write(0,4,"Problem Text")
# function to download the pdfs
def downloadpdfs(url,filename):
	# folder_location = r'webscraping' + filename
	# if not os.path.exists(folder_location):os.mkdir(folder_location)
	#makes a path for the username, given filename, and url
	path = os.path.join(folder_location,filename)
	if not os.path.isdir(path):
		os.makedirs(path)
	response = requests.get(url)
	#beautifulsoup object
	soup = BeautifulSoup(response.text, "html.parser")    
	urls = []
	#function to filer out the token part
	def filter(s):
		#student.docz
		if("file" and "token" and "pdf" and "student.docx" in s):
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
			return filename
try:
	print(response.raise_for_status())
except:
	print("Error Caught")
# downloadpdfs(url,"Module 1")
def getQuestions(problem):
	pset = re.search("Problem Set",problem)
	problems_start = problem[pset.end():]
	problems = problems_start.split('\n\n\n\n')
	print("problem breakdown length: ", len(problems) )
	filter_object = filter(lambda x: x != "", problems)
	return list(filter_object)
topics = ["a","b","c","d","e","f"]
lessons = range(1,50)
sheet_row = 1
for i in range(1,6):
	module_filename = "Module " + str(i)
	init_url = "https://www.engageny.org/resource/algebra-i-"
	#creates the module url
	module_url = init_url+"module-"+str(i)
	lesson_counter = 1
	for topic in topics:
		topic_filename = os.path.join(module_filename, "Topic "+ topic)
		print(topic_filename)
		if (topic == "a"):
			topic_url = module_url+"-topic-"
		else:
			topic_url = module_url+"-topic-"+str(topic)+"-"
		print(topic_url)
		for lesson in lessons[lesson_counter-1:]:
			print("Lesson " + str(lesson))
			lesson_url = topic_url + "lesson-" + str(lesson)
			response = requests.get(lesson_url)
			try:
				if response.raise_for_status() == None:
					print(lesson_url)
					ab = downloadpdfs(lesson_url,topic_filename)
					print(ab)
					folder_path = os.path.join(folder_location,topic_filename)
					# pdf_path = os.path.join(folder_path,ab)
					lesson_string = "Lesson "+str(lesson)
					text = docx2txt.process(ab)
					text = str(text)
					print("here")
					search_string = "Lesson "+str(lesson) + ":" +"[^\n]+\n"
					match_obj = re.search(search_string,text)
					skill = text[match_obj.start()+len(lesson_string)+3:match_obj.end()]
					full_path = os.path.join(folder_path, lesson_string +".txt")
					file1 = open(full_path,"w+")
					file1.write(text)
					file1.close()
					problem_set_match = re.search("Problem Set",text)
					eureka = re.search("This work is derived from Eureka Math",text)
					problem_set_text = text[problem_set_match.start():eureka.start()]
					problems_list = getQuestions(problem_set_text)
					print("Filtered problem list length: ",len(problems_list))
					for problem in problems_list:
						problem = re.sub("\n","",problem)
						filter_bool = True
						if len(problem) == 0:
							filter_bool = False
						if filter_bool:
							percentage = float(problem.count(" ") + problem.count("\t"))/float(len(problem))

						if(len(problem)>20 and percentage < 0.3):
							sheet1.write(sheet_row,0, i)
							sheet1.write(sheet_row,1,topic)
							sheet1.write(sheet_row,2,skill)
							sheet1.write(sheet_row,3,lesson)
							sheet1.write(sheet_row,4,problem)
							sheet_row+=1
					print("Finished lesson")
			except:
				lesson_counter = lesson
				break
		# else:
		# 	topic_url = module_url+"-topic-"+str(topic)+"-"
		# 	print(topic_url)
		# 	for lesson in lessons[lesson_counter-1:]:
		# 		lesson_url = topic_url + "lesson-" + str(lesson)
		# 		response = requests.get(lesson_url)
		# 		try:
		# 			if response.raise_for_status() == None:
		# 				print(lesson_url)
		# 				ab = downloadpdfs(lesson_url,topic_filename)
		# 				folder_path = os.path.join(folder_location,topic_filename)
		# 				# pdf_path = os.path.join(folder_path,ab)
		# 				lesson_string = "Lesson "+str(lesson)
		# 				text = docx2txt.process(ab)
		# 				text = str(text)
		# 				print("here")
		# 				search_string = "Lesson "+str(lesson) + ":" +"[^\n]+\n"
		# 				match_obj = re.search(search_string,text)
		# 				skill = text[match_obj.start()+len(lesson_string)+3:match_obj.end()]
		# 				full_path = os.path.join(folder_path, lesson_string + ".txt")
		# 				file1 = open(full_path,"w+")
		# 				file1.write(text)
		# 				file1.close()
		# 				problem_set_match = re.search("Problem Set",text)
		# 				eureka = re.search("This work is derived from Eureka Math",text)
		# 				problem_set_text = text[problem_set_match.start():eureka.start()]
		# 				sheet1.write(sheet_row,0, i)
		# 				#topic
		# 				sheet1.write(sheet_row,1,topic)
		# 				sheet1.write(sheet_row,2,skill)
		# 				sheet1.write(sheet_row,3,problem_set_text)
		# 				sheet_row+=1
		# 		except:
		# 			print(lesson)
		# 			lesson_counter = lesson
		# 			break
wb.save('Data.xls') 







	# print ("Found the URL:", link)
# for link in soup.select("a[href$='.pdf']"):
#     #Name the pdf files using the last portion of each link which are unique in this case
#     # filename = os.path.join(folder_location,link['href'].split('/')[-1])
#     # with open(filename, 'wb') as f:
#     #     f.write(requests.get(urljoin(url,link['href'])).content)
#     print(link)
#     print("cool")