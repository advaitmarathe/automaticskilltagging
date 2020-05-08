from docx import Document
# import docx.parts.Numbering
import os
main_file = r'webscraping'
module_filename = os.path.join(main_file, "Module " + str(1))
topic_filename = os.path.join(module_filename, "Topic " + "a")
doc_filename = os.path.join(topic_filename,"Lesson 1.txt")
file1 = open(doc_filename,"r")
array = file1.readlines()
print(array)
file1.close()
# def getQuestions(problem):
# /Users/advaitmarathe/Documents/GitHub/automaticskilltagging/webscraping/Module 2/Topic b
# 	re.search("Problem Set")

# from docx2python import docx2python
# doc2 = docx2python(doc_filename, html=True)
