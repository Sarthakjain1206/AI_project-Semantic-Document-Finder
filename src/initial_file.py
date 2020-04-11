import sqlite3

conn = sqlite3.connect(r"DataBase\Document_finder_db2.db")
c = conn.cursor()

sqlite_insert_blob_query = """ CREATE TABLE document_info(doc_id text PRIMARY KEY, title text, text text, document blob, extension text)"""

c.execute(sqlite_insert_blob_query)
conn.commit()
conn.close()

# # import sqlite3
# # conn = sqlite3.connect(r"DataBase/Document_finder_db2.db")
# # c = conn.cursor()
# # # c.execute('''SELECT * from document_summary''')
# # c.execute('''
# # SELECT sql
# # FROM sqlite_master
# # WHERE name = 'document_info' ''')
# # print(c.fetchone())
# #
# # conn.close()

# import tkinter as tk
# from tk_html_widgets import HTMLLabel
#
# root = tk.Tk()
# html_label = HTMLLabel(root, html='<h1 style="color: red; text-align: center"> Hello World </H1>')
# html_label.pack(fill="both", expand=True)
# html_label.fit_height()
# root.mainloop()

# import pickle
# titles = pickle.load(open(r"DataBase/wiki_title_file.pkl", "rb"))
# print(len(titles))