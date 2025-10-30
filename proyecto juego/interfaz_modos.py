import tkinter as tk
from tkinter import messagebox
import json
import uuid  # Importamos la librería para generar IDs únicos

# Nombre del archivo para guardar los modos de juego
MODOS_FILE = "modos.json"

class InterfazModos:
    """
    Clase principal para la interfaz gráfica del gestor de modos de juego.
    Permite agregar, editar, cargar y guardar modos de juego en un archivo JSON.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Modos de Juego (v2)")
        self.root.geometry("750x550")
        self.modos = []
        self.modo_seleccionado_index = None # Índice del modo que se está editando

        # Configuración de Grid
        root.columnconfigure(1, weight=1)

        # --- Interfaz de Entrada (Labels y Entries) ---
        tk.Label(root, text="ID (UUID):", padx=10, pady=5).grid(row=0, column=0, sticky="w")
        tk.Label(root, text="Nombre:", padx=10, pady=5).grid(row=1, column=0, sticky="w")
        tk.Label(root, text="Descripción:", padx=10, pady=5).grid(row=2, column=0, sticky="w")
        tk.Label(root, text="Dificultad:", padx=10, pady=5).grid(row=3, column=0, sticky="w")
        tk.Label(root, text="Enemigos (Número):", padx=10, pady=5).grid(row=4, column=0, sticky="w")
        tk.Label(root, text="Recursos:", padx=10, pady=5).grid(row=5, column=0, sticky="w")

        # Campo ID (Solo lectura)
        self.id_entry = tk.Entry(root, state='readonly') 
        self.nombre = tk.Entry(root)
        self.descripcion = tk.Entry(root)
        self.dificultad = tk.Entry(root)
        self.enemigos = tk.Entry(root)
        self.recursos = tk.Entry(root)

        self.id_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.nombre.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.descripcion.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.dificultad.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        self.enemigos.grid(row=4, column=1, padx=10, pady=5, sticky="ew")
        self.recursos.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

        # --- Botones de Acción ---
        frame_botones = tk.Frame(root)
        frame_botones.grid(row=6, column=0, columnspan=2, pady=15)

        self.btn_guardar_crear = tk.Button(frame_botones, text="Crear Nuevo Modo", command=self.guardar_crear_modo, width=20, bg="#4CAF50", fg="white")
        self.btn_guardar_crear.pack(side=tk.LEFT, padx=10)
        tk.Button(frame_botones, text="Guardar JSON", command=self.guardar_modos, width=15, bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(frame_botones, text="Eliminar Seleccionado", command=self.eliminar_modo, width=20, bg="#F44336", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(frame_botones, text="Limpiar y Nuevo", command=self.limpiar_y_restablecer, width=15).pack(side=tk.LEFT, padx=10)


        # --- Lista de Modos con Scrollbar ---
        tk.Label(root, text="Lista de Modos (Doble clic para editar):", padx=10, pady=5).grid(row=7, column=0, columnspan=2, sticky="w")
        
        list_frame = tk.Frame(root)
        list_frame.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        root.rowconfigure(8, weight=1)

        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
        self.lista = tk.Listbox(list_frame, height=15, yscrollcommand=scrollbar.set, font=("Arial", 10))
        scrollbar.config(command=self.lista.yview)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Cargar los modos al inicio
        self.cargar_modos()
        
        # Vincular el doble click para cargar en edición
        self.lista.bind('<Double-Button-1>', self.cargar_modo_para_edicion)
        self.limpiar_y_restablecer() # Inicializar campos al arrancar

    def set_id_entry(self, value):
        """Función helper para escribir en el Entry de ID (que es 'readonly')."""
        self.id_entry.config(state='normal')
        self.id_entry.delete(0, tk.END)
        self.id_entry.insert(0, value)
        self.id_entry.config(state='readonly')

    def limpiar_y_restablecer(self):
        """Limpia los campos y prepara la interfaz para crear un nuevo modo."""
        self.nombre.delete(0, tk.END)
        self.descripcion.delete(0, tk.END)
        self.dificultad.delete(0, tk.END)
        self.enemigos.delete(0, tk.END)
        self.recursos.delete(0, tk.END)
        
        self.set_id_entry(str(uuid.uuid4()))
        self.modo_seleccionado_index = None
        self.btn_guardar_crear.config(text="Crear Nuevo Modo", bg="#4CAF50")
        self.lista.selection_clear(0, tk.END)


    def guardar_crear_modo(self):
        """Guarda un modo existente (edición) o crea uno nuevo."""
        try:
            nombre = self.nombre.get().strip()
            descripcion = self.descripcion.get().strip()
            dificultad = self.dificultad.get().strip()
            enemigos_str = self.enemigos.get().strip()
            recursos = self.recursos.get().strip()
            
            # Validación básica de campos no vacíos
            if not all([nombre, descripcion, dificultad, enemigos_str, recursos]):
                messagebox.showwarning("Advertencia", "Todos los campos (excepto ID) son obligatorios.")
                return

            # Conversión de enemigos a entero
            enemigos = int(enemigos_str)
            
            # ID no puede estar vacío (aunque es readonly, se verifica el valor)
            current_id = self.id_entry.get()
            if not current_id:
                 messagebox.showerror("Error", "El ID no puede estar vacío. Limpia y restablece la interfaz.")
                 return

            modo = {
                "id": current_id,
                "nombre": nombre,
                "descripcion": descripcion,
                "dificultad": dificultad,
                "enemigos": enemigos,
                "recursos": recursos
            }

            if self.modo_seleccionado_index is not None:
                # Caso de Edición
                self.modos[self.modo_seleccionado_index] = modo
                messagebox.showinfo("Éxito", f"Modo '{nombre}' (ID: {current_id[:8]}...) guardado.")
            else:
                # Caso de Creación
                self.modos.append(modo)
                messagebox.showinfo("Éxito", f"Modo '{nombre}' creado con ID: {current_id[:8]}...")
            
            self.actualizar_lista()
            self.limpiar_y_restablecer()
            
        except ValueError:
            messagebox.showerror("Error de Entrada", "El campo 'Enemigos' debe ser un número entero.")

    def cargar_modo_para_edicion(self, event):
        """Carga los datos del modo seleccionado en los campos para edición."""
        try:
            seleccion = self.lista.curselection()
            if seleccion:
                self.modo_seleccionado_index = seleccion[0]
                modo = self.modos[self.modo_seleccionado_index]
                
                # Limpiar y rellenar campos
                self.nombre.delete(0, tk.END)
                self.descripcion.delete(0, tk.END)
                self.dificultad.delete(0, tk.END)
                self.enemigos.delete(0, tk.END)
                self.recursos.delete(0, tk.END)

                self.set_id_entry(modo['id'])
                self.nombre.insert(0, modo['nombre'])
                self.descripcion.insert(0, modo['descripcion'])
                self.dificultad.insert(0, modo['dificultad'])
                self.enemigos.insert(0, str(modo['enemigos']))
                self.recursos.insert(0, modo['recursos'])
                
                # Cambiar el texto del botón a "Guardar Cambios"
                self.btn_guardar_crear.config(text="Guardar Cambios", bg="#FF9800")
                self.lista.selection_set(self.modo_seleccionado_index) # Asegura que siga seleccionado
                messagebox.showinfo("Modo Cargado", f"Modo '{modo['nombre']}' cargado para edición.")
        except IndexError:
            self.limpiar_y_restablecer()
        except Exception as e:
            messagebox.showerror("Error de Carga", f"Error al cargar el modo: {e}")


    def eliminar_modo(self):
        """Elimina el modo de juego seleccionado en la lista."""
        try:
            seleccion = self.lista.curselection()
            if seleccion:
                index = seleccion[0]
                nombre_eliminado = self.modos[index]['nombre']
                
                # Confirmación antes de eliminar
                if messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de que quieres eliminar el modo '{nombre_eliminado}'?"):
                    del self.modos[index]
                    self.actualizar_lista()
                    self.limpiar_y_restablecer() # Limpiar la interfaz de edición
                    messagebox.showinfo("Eliminado", f"Modo '{nombre_eliminado}' eliminado. ¡Recuerda GUARDAR JSON!")
            else:
                messagebox.showwarning("Advertencia", "Selecciona un modo para eliminar.")
        except IndexError:
            messagebox.showerror("Error", "No se pudo encontrar el modo seleccionado.")

    def actualizar_lista(self):
        """Limpia la Listbox y la rellena con los modos de la lista 'self.modos'."""
        self.lista.delete(0, tk.END)
        for modo in self.modos:
            # Mostrar el ID truncado para referencia rápida
            id_corto = modo['id'][:8] if 'id' in modo else 'N/A'
            self.lista.insert(tk.END, f"[ID: {id_corto}] {modo['nombre']} - Dificultad: {modo['dificultad']}")

    def guardar_modos(self):
        """Guarda la lista completa de modos en el archivo JSON."""
        try:
            with open(MODOS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.modos, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("Guardado", "Modos guardados correctamente en " + MODOS_FILE)
        except Exception as e:
            messagebox.showerror("Error de Guardado", f"Ocurrió un error al guardar: {e}")

    def cargar_modos(self):
        """Carga los modos desde el archivo JSON si existe."""
        try:
            with open(MODOS_FILE, "r", encoding="utf-8") as f:
                self.modos = json.load(f)
                
                # Asegurar que todos los modos cargados tengan un ID (para compatibilidad)
                for i, modo in enumerate(self.modos):
                    if 'id' not in modo:
                        self.modos[i]['id'] = str(uuid.uuid4())
                        
                self.actualizar_lista()
            
            if self.modos:
                 messagebox.showinfo("Carga Exitosa", f"Se cargaron {len(self.modos)} modos de juego.")
            
        except FileNotFoundError:
            self.modos = []
            messagebox.showwarning("Archivo no encontrado", "No se encontró el archivo de modos. Se ha iniciado una lista vacía.")
        except json.JSONDecodeError:
            self.modos = []
            messagebox.showwarning("Error de Lectura", "El archivo de modos está corrupto o vacío. Se ha iniciado una lista vacía.")

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazModos(root)
    root.mainloop()
