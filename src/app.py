from flask import Flask, flash, request, redirect, render_template
from Search import search_by_BM25
# from multiprocessing import Process
from nltk.tokenize import word_tokenize,sent_tokenize
import subprocess
from spellchecker import SpellChecker
import os
from final_script_fulldb import writeTofile
from ready_for_search import *
import webbrowser
from multiprocessing import Process

from flaskwebgui import FlaskUI

# def get_text_from_docx_document(file):
#     try:
#         doc = Document(file)
#         temp = ''
#         for para in doc.paragraphs:
#             temp += para.text
#         return temp
#     except Exception:
#         print('Raising......')
#         raise Exception
def clean_query(query):
    '''
    Function to perform lemmatization and cleaning on query
    '''
    query = re.sub("'s", "", query)
    query = re.sub("s'", "", query)
    query = re.sub("n't", " not", query)
    lemmed = [WordNetLemmatizer().lemmatize(word) for word in word_tokenize(query) if word not in STOPWORDS]
    lemmed = [WordNetLemmatizer().lemmatize(word, pos='v') for word in lemmed]
    lemmed = list(set(lemmed))

    # applying spell checker on tags
    spell = SpellChecker()
    misspelled = spell.unknown(lemmed)
    new_query = query
    if len(misspelled) == 0:
        return lemmed, query, new_query
    else:
        correct_words = list(set(lemmed) - misspelled)
        correction = []

        for word in misspelled:
            # Get the one `most likely` answer
            correction.append(spell.correction(word))

        for i in range(len(correction)):
            new_query = new_query.replace(list(misspelled)[i], correction[i])


        # cleaned auto_tags
        lemmed = correct_words + correction
        print(f"Searching for {new_query} instead of {query}")
        return lemmed, query, new_query


app = Flask(__name__)
ui = FlaskUI(app)
app.config['SECRET_KEY'] = 'Apna Time Aaega'


app.config['MAX_CONTENT_LENGTH	'] = 1024 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'docx', 'pptx'])



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/searchByText', methods=['POST', 'GET'])
def viewSearchbyText():
    if request.method == 'POST':
        mystring = "Text"
        query = request.form['namesearchbytext']
        # query = "Corona Virus"
        data = pickle.load(open(r"DataBase\data_file.pkl", "rb"))
        titles = pickle.load(open(r"DataBase\title_file.pkl", "rb"))

        corpus = pickle.load(open(r"DataBase\wiki_corpus_file.pkl", "rb"))
        bm25 = search_by_BM25(corpus)

        tokenized_query, old_query, new_query = clean_query(query.lower())

        indexes, results = bm25.get_top_n(tokenized_query, data, n=5)
        results_titles = []

        for i in indexes:
            results_titles.append(titles[i])
        text = []
        for i in results:
            text_to_show = " ".join(sent_tokenize(i)[:2])
            if text_to_show != '':
                text.append(text_to_show + '....')
            else:
                text.append(i)

        title = results_titles
        title_len = len(title)

        document_file = pickle.load(open(r"DataBase\document_file.pkl", "rb"))
        extension_list = []
        for i in indexes:
            if i < 10909:
                extension_list.append('wikipedia')
            else:
                extension_list.append(document_file[i - 10909]["extension"])

        return render_template('searchbyText.html', text=text, tag=query, title=title,
                           type=mystring, title_len=title_len, old_query=old_query, new_query=new_query, extension_list=extension_list)


#
# @app.route('/nopage')
# def noaccountpagefunction():
#     return render_template('nopage.html')
#
#
# # tempdiv = ""

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

myclassname = ""

var_path = None

@app.route('/filenameonclick', methods=['GET', 'POST'])
def filenameonclick():
    if request.method == 'POST':
        with open("path.txt", "r") as file:
            var_path = file.read()

        if os.path.exists(var_path):

            myclassname = request.form['myclassname']
            print(myclassname)
            titles = pickle.load(open(r"DataBase\title_file.pkl", "rb"))
            for i in range(len(titles)):
                if titles[i] == myclassname:
                    index = i
                    break
            if index > 10909:
                document_file = pickle.load(open(r"DataBase\document_file.pkl", "rb"))

                blob_data = document_file[index-10909]["document"]
                extension = document_file[index-10909]["extension"]

                if len(myclassname) > 80:
                    myclassname = myclassname[:80]

                punctuations = '!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~'
                for x in myclassname:
                    if x in punctuations:
                        myclassname = myclassname.replace(x, "")

                print(myclassname)
                file_name = myclassname + '.' + extension
                file_name = os.path.join(var_path, file_name)

                writeTofile(blob_data, file_name)
            else:
                extension = 'wikipedia'

            return render_template('redirect.html', myclassname=myclassname, extension=extension)
        else:
            mymessage = "Please enter the working directory for current session."
            return render_template('checkworking.html', mymessage=mymessage)


def main_func():
    p2 = Process(target=ui.run)
    p2.run()

    p2.join()


# main_func()

if __name__ == '__main__':
    # app.run(debug=True)
    ui = FlaskUI(app)
    ui.run()
