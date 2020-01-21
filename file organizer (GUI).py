import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

class NoFileInDirectory(Exception):
	pass

window = tk.Tk()

file_path = str()

entry = tk.Entry(window, textvariable=file_path, state='readonly')

def browse_folder():
	global file_path

	global entry

	file_path = filedialog.askdirectory()

	entry.config(state='normal')

	entry.delete(0, tk.END)

	entry.insert(0, file_path)

	entry.config(state='readonly')

def get_files(directory):
	return [file for file in os.listdir(directory) 
			if os.path.isfile(os.path.join(directory, file))]

def organize():
	try:
		files = get_files(file_path)

		if len(files) == 0:
			raise NoFileInDirectory

		for file in files:
			extension = os.path.splitext(file)[1]

			folder_name = os.path.join(file_path, extension[1:])

			if not os.path.exists(folder_name):
				os.makedirs(folder_name)

			if os.path.exists(os.path.join(folder_name, file)):
				raise shutil.SameFileError

			else:	
				shutil.move(os.path.join(file_path, file), os.path.join(folder_name, file))
	except shutil.SameFileError:
		messagebox.showerror(title='Error', message='One or more file has the same name')
	except NoFileInDirectory:
		messagebox.showerror(title='Error', message='There is no file in the selected directory')
	except:
		messagebox.showerror(title='Error', message='Unknown error has occured!')
	else:
		messagebox.showinfo(title='Success', message='All files in the selected directory is now organized')

def setup():
	global file_path

	window.iconbitmap('C:\\Users\\Syarifah Dzulhikmah\\Downloads\\Folder.ico')

	window.title('File Organizer')

	window.geometry('360x55')

	entry.pack(fill=tk.BOTH)

	tk.Frame(window, relief=tk.RAISED, borderwidth=1).pack(fill=tk.BOTH, expand=True)

	tk.Button(window, command=organize, text='Organize').pack(side=tk.RIGHT, padx=5, pady=5)

	tk.Button(window, command=browse_folder, text='Browse Folder').pack(side=tk.LEFT, padx=5, pady=5)

	window.mainloop()

def main():
	setup()

if __name__ == '__main__':
	main()
