
import gridfs
from bson.objectid import ObjectId
from pymongo import MongoClient
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import io
import fitz  # PyMuPDF
from PIL import ImageTk, Image

# Configuración de MongoDB
MONGO_URI = "mongodb://localhost:27017/Actas_Arintia"
client = MongoClient(MONGO_URI)
db = client.get_database()
fs = gridfs.GridFS(db, collection='pdf_files')

# Cargar PDF desde el explorador de archivos
def upload_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("Archivos PDF", "*.pdf")])
    if file_path:
        with open(file_path, 'rb') as f:
            data = f.read()
        file_id = fs.put(data, filename=file_path.split('/')[-1])
        messagebox.showinfo("Subir PDF", f"PDF cargado con ID: {file_id}")
    update_list()

# Obtener y mostrar PDF automáticamente
def get_pdf():
    pdfs = list(db.pdf_files.files.find())
    if pdfs:
        file_data = fs.get(pdfs[-1]['_id']).read()
        with open("output.pdf", 'wb') as f:
            f.write(file_data)
        show_pdf("output.pdf")
    else:
        messagebox.showwarning("Obtener PDF", "No hay PDFs disponibles")

# Mostrar PDF en pantalla
def show_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    page = doc[0]
    pix = page.get_pixmap()
    
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    img = img.resize((250, 350))
    img_tk = ImageTk.PhotoImage(img)

    img_label.config(image=img_tk)
    img_label.image = img_tk

# Actualizar (Modificar PDF)
def update_pdf():
    pdfs = list(db.pdf_files.files.find())
    if pdfs:
        fs.delete(pdfs[-1]['_id'])
    upload_pdf()

# Eliminar PDF
def delete_pdf():
    selected_id = pdf_listbox.get(tk.ACTIVE)
    if selected_id:
        fs.delete(ObjectId(selected_id.split(" - ")[0]))
        img_label.config(image="")
        messagebox.showinfo("Eliminar PDF", f"PDF con ID {selected_id} eliminado")
        update_list()
    else:
        messagebox.showwarning("Eliminar PDF", "No hay PDFs para eliminar")

# Listar PDFs guardados y mostrarlos en pantalla
def update_list():
    pdfs = list(db.pdf_files.files.find())
    pdf_listbox.delete(0, tk.END)
    for pdf in pdfs:
        pdf_listbox.insert(tk.END, f"{pdf['_id']} - {pdf['filename']}")

def show_selected_pdf(event):
    selected_id = pdf_listbox.get(tk.ACTIVE).split(" - ")[0]
    if selected_id:
        file_data = fs.get(ObjectId(selected_id)).read()
        with open("output.pdf", 'wb') as f:
            f.write(file_data)
        show_pdf("output.pdf")

# Creación de la interfaz gráfica con imagen en la parte superior izquierda
root = tk.Tk()
root.title("Gestión de PDFs con GridFS")
root.geometry("550x600")
root.configure(bg="#FFFFFF")  # Fondo blanco

frame = ttk.Frame(root, padding=10)
frame.pack(fill="both", expand=True)

# Cargar imagen desde la ruta especificada
image_path = r"C:\Users\jairo.vargas\Pictures\Screenshots\logo .png"  # Reemplaza 'imagen.png' con tu archivo real
try:
    logo_img = Image.open(image_path)
    logo_img = logo_img.resize((400,100))  # Ajusta el tamaño
    logo_tk = ImageTk.PhotoImage(logo_img)

    logo_label = tk.Label(frame, image=logo_tk, bg="#FFFFFF")
    ##logo_label.pack(anchor="nw", padx=10, pady=10)
    logo_label.pack(pady=10)
except Exception as e:
    messagebox.showwarning("Error", f"No se pudo cargar la imagen: {e}")

ttk.Label(frame, text="Cargue PDFs Arintia TI", font=("Arial", 16, "bold"), foreground="black", background="#FFFFFF").pack(pady=10)

# Configuración de estilos de botones con mejor contraste
style = ttk.Style()
style.configure("TButton", font=("Arial", 10), padding=5, background="#3498DB", foreground="black")

upload_button = ttk.Button(frame, text="📂 Cargar PDF", style="TButton", command=upload_pdf, width=20)
upload_button.pack(pady=3)

get_button = ttk.Button(frame, text="📄 Obtener PDF", style="TButton", command=get_pdf, width=20)
get_button.pack(pady=3)

update_button = ttk.Button(frame, text="✏️ Actualizar PDF", style="TButton", command=update_pdf, width=20)
update_button.pack(pady=3)

delete_button = ttk.Button(frame, text="🗑️ Eliminar PDF", style="TButton", command=delete_pdf, width=20)
delete_button.pack(pady=3)

ttk.Label(frame, text="Lista de PDFs Guardados:", font=("Arial", 12, "bold"), foreground="black", background="#FFFFFF").pack(pady=5)
pdf_listbox = tk.Listbox(frame, height=6, width=50)
pdf_listbox.pack(pady=5)
pdf_listbox.bind("<<ListboxSelect>>", show_selected_pdf)

exit_button = ttk.Button(frame, text="🚪 Salir", style="TButton", command=root.quit, width=20)
exit_button.pack(pady=10)

# Espacio para mostrar el PDF visualmente
img_label = ttk.Label(frame)
img_label.pack(pady=10)

update_list()
root.mainloop()
