import sqlite3
import os
import pickle
from final_script_fulldb import load_word_embeddings
from final_script_fulldb import PreProcess
from ready_for_search import *
print('imported')

def convertToBinaryData(file):
    #Convert digital data to binary format
    with open(file, 'rb') as file:
        blobData = file.read()
    return blobData


def insert_data_to_database(doc_id, title, text, file, extension):
    try:
        conn = sqlite3.connect(r"DataBase\Document_finder_db2.db")
        c = conn.cursor()

        sqlite_insert_blob_query = """ INSERT INTO document_info
                                              (doc_id, title, text, document,extension) VALUES (?, ?, ?, ?, ?)"""

        document = convertToBinaryData(file)
        # Convert data into tuple format
        data_tuple1 = (doc_id, title, text, document, extension)
        c.execute(sqlite_insert_blob_query, data_tuple1)
        conn.commit()
        # call maintaining_all_files() fn for updating all files for search.
        maintaining_all_files()

    except sqlite3.Error as error:
        conn.rollback()
        print("Failed to insert data into sqlite table", error)
        raise Exception
    finally:
        if (conn):
            conn.close()
            # print("the sqlite connection is closed")

def get_last_inserted_rowid():
    try:
        conn = sqlite3.connect(r"DataBase\Document_finder_db2.db")
        c = conn.cursor()
        c.execute('''SELECT MAX(rowid) FROM document_info''')
        tup = c.fetchone()
        conn.close()
        return tup[0]
    except Exception:
        print('Cannot access the database right now')

def main(file_upload, title):

    # load_word_embeddings()
    # print('loaded')
    global word_embeddings
    word_embeddings = pickle.load(open(r"DataBase\word_embeddings.json", "rb"))
    # file_upload = r"C:\Users\Asus\PycharmProjects\Intelligent_Document_Finder\Data\Population Explosion.docx"
    # file_upload = r"sarthak.docx"

    preprocess_obj = PreProcess(file_upload)

    if preprocess_obj.check_extension():

        extension = preprocess_obj.get_extension()

        if extension == 'docx':
            text = preprocess_obj.get_text_from_docx_document()
            text = preprocess_obj.remove_escape_sequences(text)
            print('I m in')
        elif extension == 'pptx':
            text = preprocess_obj.get_text_from_pptx_document()
            text = preprocess_obj.remove_escape_sequences(text)

        elif extension == 'pdf':
            text = preprocess_obj.get_text_from_pdf_document()
            text = preprocess_obj.remove_escape_sequences(text)

        else:
            text = preprocess_obj.get_text_from_txt_document()
            text = preprocess_obj.remove_escape_sequences(text)

        #doc_id = str(file_upload.split('\\')[-1]).replace('.' + extension, "")  # name of file(in local directory) as doc_id

        # title = data.title[int(re.findall("_[0-9]+",doc_id)[0][1:])-1]
        try:
            doc_id = f'news_{get_last_inserted_rowid()+1}'
        except TypeError:
            doc_id = 'news_1'

        print(doc_id)

        print(text)

        assert type(title) == type(text) == str, r"Data cannot be inserted into table as data type of text and title doesn't match the database's data type"

        insert_data_to_database(doc_id, title, text, file_upload, extension)

    else:
        print('Invalid Extension')

# main()


