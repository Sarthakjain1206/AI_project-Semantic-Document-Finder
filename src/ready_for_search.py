import sqlite3
import pickle

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from gensim.parsing.preprocessing import STOPWORDS
import re

class MakeDataForSearch:
    def __init__(self, data, titles, documents):
        self.data, self.titles, self.documents = self.get_all_texts_titles_documents()

    def fetch_all_texts(self):
        conn = sqlite3.connect(r"DataBase/Document_finder_db2.db")
        c = conn.cursor()
        c.execute("SELECT text from document_info")
        tup = c.fetchall()
        conn.close()
        return tup

    def fetch_all_titles(self):
        conn = sqlite3.connect(r"DataBase/Document_finder_db2.db")
        c = conn.cursor()
        c.execute("SELECT title from document_info")
        tup = c.fetchall()
        conn.close()
        return tup

    def fetch_all_documentsWithExtensions(self):
        conn = sqlite3.connect(r"DataBase/Document_finder_db2.db")
        c = conn.cursor()
        c.execute("SELECT document,extension from document_info")
        tup = c.fetchall()
        conn.commit()
        conn.close()
        return tup

    def get_all_texts_titles_documents(self):
        svos_file = []
        texts = self.fetch_all_texts()
        titles = self.fetch_all_titles()
        tup = self.fetch_all_documentsWithExtensions()

        data_file = [text[0] for text in texts]
        title_file = [title[0] for title in titles]

        blob_list = [tup[k][0] for k in range(len(tup))]
        entension_list = [tup[k][1] for k in range(len(tup))]
        index_list = [i for i in range(len(tup))]

        dictionary = {k: {"document": x, "extension": y} for (k, x, y) in zip(index_list, blob_list, entension_list)}

        return data_file, title_file, dictionary


def get_corpus(text):
    """
    Function to clean text
    """
    pattern = r"((\S+)?(http(s)?)(\S+))|((\S+)?(www)(\S+))|((\S+)?(\@)(\S+)?)"
    text = str(text)

    text = re.sub('[[a-zA-Z0-9]+]|[\n[\nedit\n]+]', ' ', text)      # as in our dataset(wikipedia articles) [/n edit /n] is present many times in a article

    text = re.sub(pattern, " ", text)
    text = re.sub("[^a-zA-Z]", " ", text)
    text = text.lower()
    text = word_tokenize(text)
    # return text
    text = [word for word in text if word not in STOPWORDS]
    lemmed = [WordNetLemmatizer().lemmatize(word) for word in text if len(word) > 2]
    lemmed = [WordNetLemmatizer().lemmatize(word, pos='v') for word in lemmed]
    return lemmed


def get_latest_text_title():
    conn = sqlite3.connect(r"DataBase/Document_finder_db2.db")
    c = conn.cursor()
    c.execute("SELECT title,text from document_info where rowid = (SELECT MAX(rowid) FROM document_info)")
    tup = c.fetchall()
    conn.close()
    return tup


def maintaining_all_files():
    data = []
    titles = []
    documents = {}
    obj = MakeDataForSearch(data, titles, documents)

    titles_list = pickle.load(open(r"DataBase/wiki_title_file.pkl", "rb"))
    text_list = pickle.load(open(r"DataBase/wiki_text_file.pkl", "rb"))

    full_text = text_list + obj.data
    full_titles = titles_list + obj.titles

    pickle.dump(full_text, open(r"DataBase/data_file.pkl", "wb"))
    pickle.dump(full_titles, open(r"DataBase/title_file.pkl", "wb"))

    pickle.dump(obj.documents, open(r"DataBase/document_file.pkl", "wb"))

    # appending to the main corpus
    corpus = pickle.load(open(r"DataBase/wiki_corpus_file.pkl", "rb"))

    print("Files are updated")
    temp = get_latest_text_title()
    text = temp[0][1]
    title = temp[0][0]
    corpus.append(get_corpus(text)+get_corpus(title))

    pickle.dump(corpus, open(r"DataBase\wiki_corpus_file.pkl", "wb"))

    print("corpus is updated")
