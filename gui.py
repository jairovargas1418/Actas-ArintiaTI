import tkinter as tk
from tkinter import filedialog, messagebox
from crud import save_pdf, get_pdf, update_pdf, delete_pdf

class PDFManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Manager")
        
        
        self.create_widgets()

    def create_widgets(self):
        self.upload_button = tk.Button(self.root, text="Upload PDF", command=self.upload_pdf)
        self.upload_button.pack(pady=10)

        self.download_button = tk.Button(self.root, text="Download PDF", command=self.download_pdf)
        self.download_button.pack(pady=10)

        self.update_button = tk.Button(self.root, text="Update PDF", command=self.update_pdf)
        self.update_button.pack(pady=10)

        self.delete_button = tk.Button(self.root, text="Delete PDF", command=self.delete_pdf)
        self.delete_button.pack(pady=10)

    def upload_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            file_id = save_pdf(file_path)
            messagebox.showinfo("Success", f"PDF uploaded with ID: {file_id}")

    def download_pdf(self):
        file_id = filedialog.askstring("Enter File ID", "Enter the ID of the PDF to download:")
        if file_id:
            output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            if output_path:
                get_pdf(file_id, output_path)
                messagebox.showinfo("Success", "PDF downloaded successfully")

    def update_pdf(self):
        file_id = filedialog.askstring("Enter File ID", "Enter the ID of the PDF to update:")
        if file_id:
            new_file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
            if new_file_path:
                new_file_id = update_pdf(file_id, new_file_path)
                messagebox.showinfo("Success", f"PDF updated with new ID: {new_file_id}")

    def delete_pdf(self):
        file_id = filedialog.askstring("Enter File ID", "Enter the ID of the PDF to delete:")
        if file_id:
            delete_pdf(file_id)
            messagebox.showinfo("Success", "PDF deleted successfully")
