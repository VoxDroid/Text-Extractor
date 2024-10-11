import os
from tkinter import Tk, Listbox, StringVar, Scrollbar, messagebox, filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class FileExtractorApp:
    def __init__(self, master):
        self.master = master
        master.title("Text Extractor")

        style = ttk.Style("superhero")
        master.geometry("600x650")
        master.configure(bg=style.colors.bg)

        self.file_paths = []

        # Program Title
        self.program_title = ttk.Label(master, text="Text Extractor", font=("Poppins", 18, "bold"),
                                       bootstyle="info")
        self.program_title.pack(pady=10)

        self.frame = ttk.Frame(master, bootstyle="primary")
        self.frame.pack(pady=10, padx=10)

        self.listbox = Listbox(self.frame, width=55, height=10, selectmode='single',
                               font=("Poppins", 10), bd=0, relief="flat", highlightthickness=1,
                               highlightcolor=style.colors.primary)
        self.listbox.pack(side='left', fill='both')

        self.scrollbar = Scrollbar(self.frame)
        self.scrollbar.pack(side='right', fill='y')
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        self.output_label = ttk.Label(master, text="Output Filename:", font=("Poppins", 12), bootstyle="info")
        self.output_label.pack(pady=5)

        self.output_var = StringVar(value='merged_output.txt')  # Default value in case user doesn't input
        self.output_entry = ttk.Entry(master, textvariable=self.output_var, width=40, font=("Poppins", 10))
        self.output_entry.pack(pady=5)

        self.button_frame = ttk.Frame(master)
        self.button_frame.pack(pady=10)

        self.select_button = ttk.Button(self.button_frame, text="Select New Files", command=self.select_files,
                                        bootstyle="primary-outline", width=20)
        self.select_button.grid(row=0, column=0, padx=5, pady=5)

        self.add_button = ttk.Button(self.button_frame, text="Add More Files", command=self.add_more_files,
                                     bootstyle="secondary-outline", width=20)
        self.add_button.grid(row=0, column=1, padx=5, pady=5)

        self.remove_dupes_button = ttk.Button(self.button_frame, text="Remove Duplicates", command=self.remove_duplicates,
                                              bootstyle="danger-outline", width=20)
        self.remove_dupes_button.grid(row=1, column=0, padx=5, pady=5)

        self.sort_button = ttk.Button(self.button_frame, text="Sort Files", command=self.sort_files,
                                      bootstyle="info-outline", width=20)
        self.sort_button.grid(row=1, column=1, padx=5, pady=5)

        self.clear_button = ttk.Button(self.button_frame, text="Clear Selected Files", command=self.clear_files,
                                       bootstyle="warning-outline", width=20)
        self.clear_button.grid(row=2, column=0, padx=5, pady=5)

        self.save_as_button = ttk.Button(self.button_frame, text="Save As", command=self.save_as,
                                         bootstyle="success-outline", width=20)
        self.save_as_button.grid(row=2, column=1, padx=5, pady=5)

        self.about_button = ttk.Button(master, text="About", command=self.show_about, bootstyle="light-outline",
                                       width=15)
        self.about_button.pack(pady=5)

        self.help_button = ttk.Button(master, text="Help", command=self.show_help, bootstyle="info-outline",
                                      width=15)
        self.help_button.pack(pady=5)

    def select_files(self):
        file_paths = filedialog.askopenfilenames(title="Select Files", filetypes=[("All Files", "*.*")])
        self.file_paths = list(file_paths)
        self.update_listbox()

    def add_more_files(self):
        file_paths = filedialog.askopenfilenames(title="Add More Files", filetypes=[("All Files", "*.*")])
        self.file_paths.extend(file_paths)
        self.update_listbox()

    def clear_files(self):
        self.file_paths.clear()
        self.update_listbox()

    def update_listbox(self):
        self.listbox.delete(0, 'end')
        for file_path in self.file_paths:
            self.listbox.insert('end', os.path.basename(file_path))  # Display only the file name

    def remove_duplicates(self):
        seen_files = {}
        unique_files = []

        for file_path in self.file_paths:
            try:
                file_size = os.path.getsize(file_path)
                if file_size not in seen_files:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    seen_files[file_size] = content
                    unique_files.append(file_path)
                elif seen_files[file_size] != content:
                    unique_files.append(file_path)
            except Exception as e:
                messagebox.showerror("Error", f"Cannot process {file_path}: {str(e)}")

        self.file_paths = unique_files
        self.update_listbox()

    def sort_files(self):
        self.file_paths.sort(key=lambda x: os.path.basename(x))
        self.update_listbox()

    def save_as(self):
        output_filename = self.output_var.get()

        output_file_path = filedialog.asksaveasfilename(initialfile=output_filename,
                                                        defaultextension=".txt",
                                                        filetypes=[("Text files", "*.txt")])

        if output_file_path:
            self.extract_text(output_file_path)

    def extract_text(self, output_file):
        try:
            with open(output_file, 'w', encoding='utf-8') as outfile:
                for file_path in self.file_paths:
                    file_name = os.path.basename(file_path)
                    outfile.write(f"{file_name}:\n")
                    try:
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            content = infile.read()
                            outfile.write(content + "\n")
                    except Exception as e:
                        outfile.write(f"Error reading {file_name}: {str(e)}\n")

                    outfile.write("\n-----\n\n")

            messagebox.showinfo("Success", f"Text extracted and saved to {output_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving file: {str(e)}")

    def show_about(self):
        messagebox.showinfo("About", "Text Extractor \n\nCreated by Izeno")

    def show_help(self):
        help_text = (
            "Tutorial:\n"
            "1. Click 'Select New Files' to choose files to extract text from.\n"
            "2. Use 'Add More Files' to include additional files.\n"
            "3. You can remove duplicates, sort files, or clear the selection.\n"
            "4. Enter the desired output filename or leave the default.\n"
            "5. Click 'Save As' to choose where to save the extracted text.\n\n"
            "Example Output:\n"
            "File1.java:\n"
            "public class File1 {...}\n"
            "-----\n\n"
            "File2.txt:\n"
            "This is a sample text file.\n"
            "-----\n\n"
        )
        messagebox.showinfo("Help", help_text)


if __name__ == "__main__":
    root = Tk()
    app = FileExtractorApp(root)
    root.mainloop()
