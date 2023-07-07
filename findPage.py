import PyPDF2
import keyword
import re
import numpy as np

#objective: find the page that relates the most to the question
#This is mostly finished, need to tailor a bit more and need to find a way to connect python to js
def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)

        text = []
        for page_num in range(num_pages):
            text.append(pdf_reader.pages[page_num].extract_text())

        return text

def keyword_list(word_list):
    ret = []
    for word in word_list:
        word = word.lower()
        if (not keyword.iskeyword(word)) and (word not in ret):
            ret.append(word)
    return ret

def to_list(text):
    ret = re.findall(r"[\w']+", text)
    return ret

def cvt_text(text):
    word_list = to_list(text)
    key_list = keyword_list(word_list)
    return key_list

def grading(question, page):
    ret = 0
    for word in question:
        if word in page:
            ret = ret + 1
    return ret

def grade_all(question, extracted_text):
    text_len = len(extracted_text)
    cvt_question = cvt_text(question)
    grade = []
    for i in range(text_len):
        cvt_extracted_text = cvt_text(extracted_text[i])
        grade.append(grading(cvt_question, cvt_extracted_text))
    return grade

# Example usage
pdf_file_path = './dokumen.pub_close-relations-an-introduction-to-the-sociology-of-families-6th-edition-6nbsped-9780134830636.pdf'
print("Enter your quiz question (I mean all the choices and also the question):")
question = """4.	What aspect of the Live-in Caregiver Program causes social inequality?
A.	It provides women from foreign countries such as the Philippines to work in Canada as nannies.
B.	It provides women from foreign countries such as the Philippines the opportunity to receive permanent resident status after two years of caregiving.
C.	It can leave workers to be exploited and abused by their employers but unable to do anything about their situation because of their immigration and economic status.
D.	It prevents workers from being exploited and abused by their employers as, after two years, their nanny would leave if exploited or abused
"""




extracted_text = extract_text_from_pdf(pdf_file_path)

grade = grade_all(question, extracted_text)
np_grade = np.array(grade)

print(np_grade)
print(np.argmax(np_grade)+1)
print("This page is the pdf file page (which include the opening and the content pages)")



