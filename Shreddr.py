from tkinter import *
from tkinter import ttk
from ttkbootstrap import Style, widgets
from tkinter.filedialog import askdirectory, askopenfilename
from tkinter.messagebox import showerror, showinfo
import string, os

style = Style(theme = "darkly")
win = style.master
win.title("Shreddr")
win.geometry('300x300')
win.resizable(False, False)

def GUI():
	# global entry, entry2, passes, max_filename
	
	folder_frame= ttk.LabelFrame(win, text = "Select Folder", width = 248, height = 50)
	folder_frame.place(x = 25, y = 1)
	entry = Entry(folder_frame, width = 30)
	entry.place(x = 2)
	open_folder_btn = ttk.Button(folder_frame, text = "Open", style = "primary.Outline.TButton",
		command = lambda :[Open(entry)])
	open_folder_btn.place(x =190)
	file_frame= ttk.LabelFrame(win,text = "Select File", width = 248, height = 50)
	file_frame.place(x = 25, y = 70)
	entry2 = Entry(file_frame, width = 30)
	entry2.place(x = 2)
	open_file_btn = ttk.Button(file_frame, text = "Open", style = "primary.Outline.TButton",
		command = lambda :[Open_file(entry2)])
	open_file_btn.place(x =190)

	nums_frame = ttk.LabelFrame(win, width = 248, height = 70)
	nums_frame.place(x = 25, y= 141)
	passes = IntVar()
	passLabel = Label(nums_frame, text = "Passes:")
	passLabel.place(x=0,y=0)
	passSpin = Spinbox(nums_frame, from_ = 1, to = 150, width  = 10, textvariable = passes)
	passSpin.place(y=20)
	max_filename = IntVar()
	max_fileLabel = Label(nums_frame, text="max filename")
	max_fileLabel.place(x = 80)
	max_filename_spin = Spinbox(nums_frame, from_=1, to = 150, width = 10, textvariable=max_filename)
	max_filename_spin.place(x = 80, y = 20)

	Btn = ttk.Button(win, text = "Shred", style = "primary.Outline.TButton",
		command = lambda :[shred(entry, entry2, passes, max_filename)])
	Btn.place(x = 125, y = 230)


def shred(entry, entry2, passes, max_filename):
	if entry.get() == "":
		if entry2.get()=="":
			showerror("Error", "Fields are empty")
		else:
			shred_file(path=entry2.get(), passes = passes.get(), max_filename = max_filename.get())
			showinfo("Success", "The shred was Successful")			
	else:
		shred_file(path=entry.get(), passes = passes.get(), max_filename = max_filename.get())
		showinfo("Success", "The shred was Successful")

def Open(entry):
	entry.delete(0, END)
	entry.insert(END, askdirectory())

def Open_file(entry):
	entry.delete(0, END)
	entry.insert(END, askopenfilename())

def shred_file(path : str, passes : int, max_filename : int):
	print(f"[*] Current file: {path}")
	valid_chars = string.ascii_letters + string.digits
	valid_bytes = [chr(c) for c in range(0xFF+1)]
	raw_byte_encode = "latin1"
	filesize = os.path.getsize(path)
	if(os.path.isfile(path) == True and filesize > 0):
		for temp in range(passes):
			#Overwrite file with random raw bytes
			for i in range(filesize):
				fd = os.open(path, os.O_WRONLY|os.O_NOCTTY)
				os.pwrite(fd, random.choice(valid_bytes).encode(raw_byte_encode), i)
				os.close(fd)

			#Rename File
			new_name = "".join(random.choices(valid_chars, k=random.choice(range(1, max_filename + 1))))
			new_path = f"{dir_char}".join(path.split(f"{dir_char}")[0:-1]) + f"{dir_char}{new_name}"
			if(len(path.split(f"{dir_char}")) == 1):
				new_path = new_name
			os.rename(path, new_path)
			path = new_path
		
		#Remove file after completing all passes
		os.remove(path)

	else:
		showerror("An Error Occured", "something is wrong from the data you inputed")

# if __name__=='__main__':
GUI()
# print(entry)
win.mainloop()
