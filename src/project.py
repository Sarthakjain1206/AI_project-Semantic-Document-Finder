from tkinter import filedialog
import tkinter as tk
import tkinter.messagebox
from app import *
from main import *
import multiprocessing


def on_click(event):
    filepath.configure(state=tk.NORMAL)
    filepath.delete(0, tk.END)

    # make the callback only work once
    filepath.unbind('<Button-1>', on_click_id)


def first_window():
    global window0
    window0 = tk.Tk()
    text2 = tk.Text(window0, height=25, width=150,)
    scroll = tk.Scrollbar(window0, command=text2.yview)
    text2.configure(yscrollcommand=scroll.set)
    text2.tag_configure('bold_italics', font=('Arial', 20, 'bold', 'italic'))
    text2.tag_configure('big', font=('Verdana', 20, 'bold'))
    text2.tag_configure('color',
                        foreground='#476042',
                        font=('Tempus Sans ITC', 12, 'bold'))


    text2.insert(tk.END, '\nDocument Search Manager\n', 'big')
    quote = """
    How easy do you find it to remember the exact location of a document that you created last year?
    Not very easy, right?
    Big Organizations/people deal with hundreds of documents daily and forget about them, most of the time. 
    But what if we want that old documentation again for some work,
    but unfortunately you do not remember the name or the actual content of that document to retrieve it from the large storage of your computer. 
    In such cases, use of a Intelligent document finder can really make a huge difference.
    """
    text2.insert(tk.END, quote, 'color')
    labelfont = ('times', 40, 'bold')
    text2.config(bg='black', fg='yellow')
    text2.config(font=labelfont)
    text2.config(height=10, width=40)
    text2.pack(expand=True, fill=tk.BOTH)

    text2.pack(fill=tk.BOTH, anchor="e")
    scroll.pack(fill=tk.Y)

    contentfont = ('times', 20, 'bold')
    contentframe = tk.Label(window0, text="Do you want to upload a file or search for a file?")
    contentframe.config(font=contentfont)
    contentframe.config(bg='black', fg='aqua')
    contentframe.pack(expand=True, fill=tk.BOTH)
    contentframe.pack()

    uploadbutton=tk.Button(window0, text="Upload file", relief=tk.GROOVE, borderwidth=5, command=upload_window)
    uploadfont = ('times', 25, 'bold')
    uploadbutton.config(font=uploadfont)
    uploadbutton.config(bg='black', fg='aqua')
    uploadbutton.pack(side= tk.LEFT, expand=True, fill=tk.BOTH, padx=15, pady=15)

    searchbutton=tk.Button(window0, text="Search file", relief=tk.GROOVE, borderwidth=5, command=main_func)
    searchfont = ('times', 25, 'bold')
    searchbutton.config(font=searchfont)
    searchbutton.config(bg='black', fg='aqua')
    searchbutton.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=15, pady=15)

    window0.mainloop()
def print_path():
    global title, f
    f = tk.filedialog.askopenfilename(
        parent=window, initialdir='C:/Tutorial',
        title='Choose file',
        filetypes=[('txt files', '.txt'),
                   ('all files', '*')]
    )

    filename = os.path.basename(f)
    fileupload.config(state=tk.NORMAL)
    fileupload.insert(0, filename)
    fileupload.config(state=tk.DISABLED)
    print(f)
    title = ".".join(filename.split('.')[:-1])
    print(title)




def delete_path():
    fileupload.config(state=tk.NORMAL)
    fileupload.delete(0, tk.END)
    fileupload.config(state=tk.DISABLED)



def upload_file():

    var_path = filepath.get()
    flag = True
    if not os.path.exists(var_path):
        tk.messagebox.showerror(title='Path Error', message='Entered Directory does not exists!! Please Enter Valid Path')
        filepath.delete(0, tk.END)
        flag = False
    try:
        if not os.path.exists(f):
            print('f: ',f)
            tk.messagebox.showerror(title='File Not Found', message='Please Upload Correct File on System first!! By click on upload file button')
            flag = False
        else:
            if f.split('.')[-1] not in ALLOWED_EXTENSIONS:
                print(f)
                tk.messagebox.showerror(title='Error', message='File Format is not Supported!! Please upload files of only docx,txt,pdf or pptx format')
                flag = False
    except NameError:
        tk.messagebox.showerror(title='Error',
                                message='You have not choosen any file yet!!')
        flag = False

    if flag == True:
        with open("path.txt", "w") as file:
            file.write(var_path)

        main(f, title)
        tk.messagebox.showinfo("Successful", "File Successfully uploaded!")


# def main_func2():
#     # p1 = subprocess.run(['python', 'app.py'], shell=True)
#     # p1.terminate()
#     # p1.kill()
#     p2 = multiprocessing.Process(target=main_func())
#     p2.run()
#     # p2.start()
#     # sleep(5)
#     # p2.terminate()
#
#     # p2.join()
#
placeholder = "Enter Working Directory of this System"


def upload_window():
    global window
    window = tk.Toplevel(window0)
    # window = tk.Tk()
    # window0.withdraw()
    window.title("Upload File")

    titleframe = tk.Label(window, text="Click on the Upload file button and browse the file that you want to upload.",
                          relief=tk.RAISED)
    labelfont = ('times', 20, 'bold')
    titleframe.config(bg='black', fg='yellow')
    titleframe.config(font=labelfont)
    titleframe.config(height=10, width=80)
    titleframe.pack(expand=True, fill=tk.BOTH)
    titleframe.pack()

    fp = tk.Frame(window)
    fp.pack()

    global filepath, on_click_id, var_path
    filepath = tk.Entry(fp, font=("Times New Roman", 15, "bold"), justify='center')
    filepath.config(width=120, bd=5, relief=tk.SUNKEN)
    filepath.insert(0, placeholder)
    filepath.config(state=tk.DISABLED)

    on_click_id = filepath.bind('<Button-1>', on_click)
    # path = filepath.get()
    filepath.pack(side=tk.LEFT)

    # var_path = path

    buttons = tk.Frame(window)
    buttons.pack(side=tk.LEFT)

    uploadbutton2 = tk.Button(buttons, text='Upload file', command=print_path, width=20)
    buttonfont = ('times', 25, 'bold')
    uploadbutton2.config(font=buttonfont)
    uploadbutton2.config(bg='black', fg='aqua')
    uploadbutton2.pack(expand=True, fill=tk.BOTH, padx=15, pady=15)

    removefile = tk.Button(buttons, text="Remove file", command=delete_path, relief=tk.GROOVE, borderwidth=5, width=20)
    removefont = ('times', 25, 'bold')
    removefile.config(font=removefont)
    removefile.config(bg='black', fg='aqua')
    removefile.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=15, pady=15)

    upent = tk.Frame(window)
    upent.pack()
    global fileupload
    fileupload = tk.Entry(upent, width=60, bd=5, font=("Times New Roman", 14, "bold"), justify='center',
                          state=tk.DISABLED)
    fileupload.config(fg='brown')
    fileupload.pack(side=tk.LEFT)

    upbutton = tk.Button(upent, text="Upload", command=upload_file, relief=tk.GROOVE, borderwidth=5)
    uploadfont2 = ('times', 25, 'bold')
    upbutton.config(font=uploadfont2)
    upbutton.config(bg='black', fg='aqua')
    upbutton.pack(expand=True, fill=tk.BOTH, padx=15, pady=15)

    # window.mainloop()




# p1 = multiprocessing.Process(target=first_window())
# # p2 = multiprocessing.Process(target=app.run)
# #
# p1.start()
# #
# # # p2. join()
# p1.join()
first_window()
# upload_window()