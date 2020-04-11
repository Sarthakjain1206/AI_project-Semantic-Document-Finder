import warnings
warnings.filterwarnings('ignore')

import re
# from nltk.cluster.util import cosine_distance
import numpy as np
# import networkx as nx
# from nltk.tokenize import word_tokenize, sent_tokenize
# from sklearn.metrics.pairwise import cosine_similarity


import PyPDF2
# from docx import Document
from docx import Document

import textract


def writeTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
    print("Stored blob data into: ", filename, "\n")

valid_extensions = {'docx', 'pptx', 'txt', 'pdf'}

class PreProcess:

    def __init__(self, file):
        self.file = file

    def check_extension(self):
        if self.file.split('.')[-1] in valid_extensions:
            return True
        else:
            return False


    def get_extension(self):
        return self.file.split('.')[-1]


    def get_text_from_docx_document(self):
        try:
            doc = Document(self.file)
            temp = ''
            for para in doc.paragraphs:
                temp += para.text
            return temp
        except Exception:
            print('Raising......')
            raise Exception

    #     text = textract.process(file)
    #     text = str(text)[2:]
    #     return text

    def get_text_from_pdf_document(self):
        file_obj = open(self.file, "rb")
        pdf_reader = PyPDF2.PdfFileReader(file_obj)
        page_numbers = pdf_reader.numPages
        temp = ''

        for i in range(page_numbers):
            page_obj = pdf_reader.getPage(i)
            temp += page_obj.extractText()
        file_obj.close()
        return temp


    def get_text_from_txt_document(self):
        #     text = textract.process(file)
        #     text = str(text)[2:]
        try:
            f = open(self.file, "r")
            temp = f.read()

        except UnicodeDecodeError:
            #         print("\n\nI am in except block\n\n")
            try:
                f = open(self.file, "r", encoding="utf-8")
                temp = f.read()
            except:
                print("Sorry! can't decode encodings!")
                raise Exception("Sorry! can't decode bytes")
        # except Exception:
        #     print('Another exception occured')
        #     raise Exception
        finally:
            f.close()
            return temp



    def get_text_from_pptx_document(self):
        text = textract.process(self.file)
        text = str(text)[2:]
        return text


    def remove_escape_sequences(self, text):
        pattern = r"\\[a-z]"
        text = re.sub(pattern, " ", text)
        return text


def load_word_embeddings():
    global word_embeddings
    word_embeddings = {}
    f = open(r'\DataBase\glove.6B.100d.txt', encoding="utf-8")
    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        word_embeddings[word] = coefs
    f.close()

