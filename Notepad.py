import tkinter as tk
from tkinter import filedialog, messagebox
import os

MAIN_PATH = os.path.dirname(os.path.abspath(__file__))

class Main():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.title("Notepad Editor")
        self.current_file = None  # Para rastrear o arquivo atual
        self.setup_ui()
        
    def setup_ui(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(column=0, row=0, sticky='nsew')
        
        self.main_editor = tk.Text(self.main_frame, font=("Consolas", 13))
        self.main_editor.grid(column=0, row=0, sticky='nsew')
        
        # Expandir o editor de texto para preencher a janela
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Barra de menu
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        
        self.root.mainloop()

    def new_file(self):
        if self.main_editor.get("1.0", tk.END).strip() != "":
            msg = messagebox.askyesnocancel("Warning", "The current text file is not saved. Do you want to save it?")
            if msg:
                self.save_file()
                self.main_editor.delete("1.0", tk.END)
                self.current_file = None
            elif msg is False:
                self.main_editor.delete("1.0", tk.END)
                self.current_file = None
        else:
            self.main_editor.delete("1.0", tk.END)
            self.current_file = None
        
    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                self.main_editor.delete("1.0", tk.END)
                self.main_editor.insert("1.0", content)
                self.current_file = file_path
                self.root.title(f"Notepad Editor - {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
    
    def save_file(self):
        if self.current_file:
            try:
                content = self.main_editor.get("1.0", tk.END)
                with open(self.current_file, 'w') as file:
                    file.write(content)
                messagebox.showinfo("Success", "File saved successfully")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            self.save_file_as()
    
    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            try:
                content = self.main_editor.get("1.0", tk.END)
                with open(file_path, 'w') as file:
                    file.write(content)
                self.current_file = file_path
                self.root.title(f"Notepad Editor - {os.path.basename(file_path)}")
                messagebox.showinfo("Success", "File saved successfully")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    app = Main()
