import sqlite3
import tkinter as tk
from tkinter import messagebox
import re
from PIL import Image, ImageTk


# Crear o conectar a la base de datos
def conectar_db():
    conexion = sqlite3.connect("contactos_db.db")
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre VARCHAR(100) NOT NULL,
            telefono VARCHAR(20) NOT NULL,
            email VARCHAR(100) NOT NULL
        )
    """)
    conexion.commit()
    conexion.close()

# Función para validar el email
def validar_email(email):
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email)

# Función para validar el número de teléfono
def validar_telefono(telefono):
    patron = r'^\+?\d{9,15}$'
    return re.match(patron, telefono)

# Función para validar que el número de teléfono sea único
def validar_telefono_unico(telefono):
    conexion = sqlite3.connect("contactos_db.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM contacts WHERE telefono = ?", (telefono,))
    contacto = cursor.fetchone()
    conexion.close()
    return contacto is None

# Función para validar que el número de teléfono sea único
def validar_email_unico(email):
    conexion = sqlite3.connect("contactos_db.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM contacts WHERE email = ?", (email,))
    contacto = cursor.fetchone()
    conexion.close()
    return contacto is None



# Función para agregar contacto
def agregar_contacto():
    nombre = entry_nombre.get()
    telefono = entry_telefono.get()
    email = entry_email.get()
    if nombre and telefono and email:
        if not validar_telefono(telefono):
            messagebox.showerror("Error", "Número de teléfono no válido. Debe contener entre 9 y 15 dígitos.")
            return
        if not validar_email(email):
            messagebox.showerror("Error", "Email no válido.")
            return
        if not validar_telefono_unico(telefono):
            messagebox.showerror("Error", "El número de teléfono ya existe.")
            return
        if not validar_email_unico(email):
            messagebox.showerror("Error", "El email ya existe.")
            return
        

        conexion = sqlite3.connect("contactos_db.db")
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO contacts (nombre, telefono, email) VALUES (?, ?, ?)", (nombre, telefono, email))
        conexion.commit()
        conexion.close()
        entry_nombre.delete(0, tk.END)
        entry_telefono.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        actualizar_lista()
    else:
        messagebox.showerror("Error", "Todos los campos son obligatorios")

# Función para eliminar contacto
def eliminar_contacto(contacto_id):
    respuesta = messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas eliminar este contacto?")
    if respuesta:
        conexion = sqlite3.connect("contactos_db.db")
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM contacts WHERE id = ?", (contacto_id,))
        conexion.commit()
        conexion.close()
        actualizar_lista()

# Función para actualizar un contacto seleccionado
def actualizar_contacto():
    global contacto_seleccionado
    if contacto_seleccionado:
        nombre = entry_nombre.get()
        telefono = entry_telefono.get()
        email = entry_email.get()
        if nombre and telefono and email:
            if not validar_telefono(telefono):
                messagebox.showerror("Error", "Número de teléfono no válido. Debe contener entre 10 y 15 dígitos.")
                return
            if not validar_email(email):
                messagebox.showerror("Error", "Email no válido.")
                return
            conexion = sqlite3.connect("contactos_db.db")
            cursor = conexion.cursor()
            cursor.execute("UPDATE contacts SET nombre = ?, telefono = ?, email = ? WHERE id = ?",
                           (nombre, telefono, email, contacto_seleccionado))
            conexion.commit()
            conexion.close()
            entry_nombre.delete(0, tk.END)
            entry_telefono.delete(0, tk.END)
            entry_email.delete(0, tk.END)
            actualizar_lista()
            btn_actualizar.config(state=tk.DISABLED)
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
    else:
        messagebox.showerror("Error", "Seleccione un contacto para actualizar")

# Función para seleccionar un contacto y cargar sus datos en el formulario
def seleccionar_contacto(contacto_id, nombre, telefono, email):
    global contacto_seleccionado
    contacto_seleccionado = contacto_id
    entry_nombre.delete(0, tk.END)
    entry_nombre.insert(0, nombre)
    entry_telefono.delete(0, tk.END)
    entry_telefono.insert(0, telefono)
    entry_email.delete(0, tk.END)
    entry_email.insert(0, email)
    btn_actualizar.config(state=tk.NORMAL)

# Función para actualizar la lista de contactos
def actualizar_lista():
    global contacto_seleccionado, delete_icon, selectedit_icon
    contacto_seleccionado = None
    for widget in lista_contactos.winfo_children():
        widget.destroy()
    
    # Load delete icon image
    delete_icon_img = Image.open("img/delete-user.png")
    delete_icon_img = delete_icon_img.resize((40, 40), Image.Resampling.LANCZOS)
    delete_icon = ImageTk.PhotoImage(delete_icon_img)
    
    selectedit_icon_img = Image.open("img/colored-pencil.png")
    selectedit_icon_img = selectedit_icon_img.resize((40, 40), Image.Resampling.LANCZOS)
    selectedit_icon = ImageTk.PhotoImage(selectedit_icon_img)


    
    tk.Label(lista_contactos, text="Nombre", bg="white", font=("Arial", 10, "bold"), width=18, anchor="w").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(lista_contactos, text=" | Teléfono", bg="white", font=("Arial", 10, "bold"), width=18, anchor="w").grid(row=0, column=1, padx=5, pady=5)
    tk.Label(lista_contactos, text=" | Email", bg="white", font=("Arial", 10, "bold"), width=18, anchor="w").grid(row=0, column=2, padx=5, pady=5)
    tk.Label(lista_contactos, text="", bg="white", width=5).grid(row=0, column=3, padx=5, pady=5)
    
    conexion = sqlite3.connect("contactos_db.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM contacts")
    for index, contacto in enumerate(cursor.fetchall(), start=1):
        tk.Label(lista_contactos, text=contacto[1], bg="white", width=18, anchor="w").grid(row=index, column=0, padx=5, pady=5)
        tk.Label(lista_contactos, text=contacto[2], bg="white", width=18, anchor="w").grid(row=index, column=1, padx=5, pady=5)
        tk.Label(lista_contactos, text=contacto[3], bg="white", width=18, anchor="w").grid(row=index, column=2, padx=5, pady=5)
        
        btn_seleccionar = tk.Button(lista_contactos, image=selectedit_icon, command=lambda c=contacto: seleccionar_contacto(c[0], c[1], c[2], c[3]))
        btn_seleccionar.grid(row=index, column=3, padx=2, pady=5)
        btn_eliminar = tk.Button(lista_contactos, image=delete_icon, command=lambda c_id=contacto[0]: eliminar_contacto(c_id))
        btn_eliminar.grid(row=index, column=4, padx=2, pady=5)

    conexion.close()

# Interfaz gráfica
root = tk.Tk()
root.title("Gestor de Contactos")
root.iconbitmap("img/icono.ico")
root.geometry("860x500")
root.resizable(0, 0)
root.configure(bg="#45D8BB")

conectar_db()

# Crear el marco principal
main_frame = tk.Frame(root, bg="#f3f3ed")
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Añadir título
header_frame = tk.Frame(main_frame, bg="#43C6AB")
header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=30)
tk.Label(header_frame, text="🖊 Agenda de Contactos 📖", font=("Arial", 24, "bold"), bg="#43C6AB", fg="white", pady=10).pack()

# Crear el marco del formulario
form_frame = tk.Frame(main_frame, bg="#ffffff", padx=5, pady=10 ,relief=tk.RIDGE, borderwidth=2)
form_frame.grid(row=1, column=0, padx=10, pady=30, sticky="n")

# Campos de entrada
entry_nombre = tk.Entry(form_frame, width=30, bg="#e0e0e0")
entry_telefono = tk.Entry(form_frame, width=30, bg="#e0e0e0")
entry_email = tk.Entry(form_frame, width=30, bg="#e0e0e0")

# Etiquetas
tk.Label(form_frame, text="Nombre:", bg="#ffffff").grid(row=0, column=0, sticky="w", padx=5)
entry_nombre.grid(row=1, column=0, pady=5, padx=5)
tk.Label(form_frame, text="Teléfono:", bg="#ffffff").grid(row=2, column=0, sticky="w", padx=5)
entry_telefono.grid(row=3, column=0, pady=5, padx=5)
tk.Label(form_frame, text="Email:", bg="#ffffff").grid(row=4, column=0, sticky="w", padx=5)
entry_email.grid(row=5, column=0, pady=5, padx=5)

# Botones
btn_frame = tk.Frame(form_frame, bg="#ffffff")
btn_frame.grid(row=6, column=0, pady=10)

global edit_icon, add_icon
edit_icon_img = Image.open("img/edit-user.png")
edit_icon_img = edit_icon_img.resize((40, 40), Image.Resampling.LANCZOS)
edit_icon = ImageTk.PhotoImage(edit_icon_img)
    
add_icon_img = Image.open("img/add-user.png")
add_icon_img = add_icon_img.resize((40, 40), Image.Resampling.LANCZOS)
add_icon = ImageTk.PhotoImage(add_icon_img)
    
tk.Button(btn_frame, text="Agregar", command=agregar_contacto, image=add_icon ).pack(side=tk.LEFT, padx=5)
btn_actualizar = tk.Button(btn_frame, text="Actualizar", command=actualizar_contacto, image=edit_icon, state=tk.DISABLED, disabledforeground="black")
btn_actualizar.pack(side=tk.LEFT, padx=5)

# Lista de contactos
lista_contactos = tk.Frame(main_frame, bg="white", relief=tk.RIDGE, borderwidth=2)
lista_contactos.grid(row=1, column=1, padx=5, pady=30, sticky="n")

contacto_seleccionado = None
actualizar_lista()

root.mainloop()