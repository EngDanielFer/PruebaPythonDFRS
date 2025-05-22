import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import requests

def iniciar_db():
    conex = sqlite3.connect('usuarios.db')
    cursor = conex.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS usuarios (
                       usuario TEXT PRIMARY KEY,
                       clave TEXT
                   )
                   ''')
    
    # Crear usuario de ejemplo
    cursor.execute('SELECT * FROM usuarios WHERE usuario = ?', ('admin',))
    if not cursor.fetchone():
        cursor.execute('INSERT INTO usuarios (usuario, clave) VALUES (?, ?)', ('admin', '12345'))
    conex.commit()
    conex.close()
    
# Función para verificar usuario en base de datos
def verificar_usuario(usuario, clave):
    conex = sqlite3.connect('usuarios.db')
    cursor = conex.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE usuario = ? AND clave = ?', (usuario, clave))
    res = cursor.fetchone()
    conex.close()
    return res is not None

# Función para obtener personajes desde la API de Rick and Morty
def obtener_personajes_rm():
    try:
        res = requests.get('https://rickandmortyapi.com/api/character')
        datos = res.json()
        return datos['results']
    except Exception as e:
        return ["Hubo un error al obtener datos de la API de Rick and Morty"]

# Si el login es exitoso mostrar ventana con personajes
def mostrar_personajes_rm():
    personajes_rm = obtener_personajes_rm()
    ventana_personajes = tk.Toplevel(root)
    ventana_personajes.title("Persoanjes de Rick and Morty")
    
    tabla_rm = ttk.Treeview(ventana_personajes, columns=('ID', 'Nombre', 'Estado', 'Especie', 'Género'), show='headings')
    tabla_rm.heading('ID', text='ID')
    tabla_rm.heading('Nombre', text='Nombre')
    tabla_rm.heading('Estado', text='Estado')
    tabla_rm.heading('Especie', text='Especie')
    tabla_rm.heading('Género', text='Género')

    # Añadir filas
    for pers in personajes_rm:
        tabla_rm.insert('', tk.END, values=(pers['id'], pers['name'], pers['status'], pers['species'], pers['gender']))

    tabla_rm.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Verificar login en aplicación
def login():
    usuario = entrada_usuario.get()
    clave = entrada_clave.get()
    
    if verificar_usuario(usuario, clave):
        mostrar_personajes_rm()
    else:
        messagebox.showerror("Error", "Credenciales incorrectas")
    
# Crear interfaz de usuario
root = tk.Tk()
root.title("Login - Personajes Rick and Morty")

tk.Label(root, text="Usuario:").grid(row=0, column=0, padx=10, pady=5)
entrada_usuario = tk.Entry(root)
entrada_usuario.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Clave:").grid(row=1, column=0, padx=10, pady=5)
entrada_clave = tk.Entry(root, show="*")
entrada_clave.grid(row=1, column=1, padx=10, pady=5)

btn_entrar = tk.Button(root, text="Iniciar Sesión", command=login)
btn_entrar.grid(row=2, column=0, columnspan=2, pady=10)

# Inicializar la BD
iniciar_db()

# Ejecutar la aplicación
root.mainloop()