#! venv/bin/python3
import tkinter as tk
from tkinter import ttk, Toplevel, messagebox
from tkcalendar import Calendar
import datetime
import json

class ToDoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lista de Tareas")
        self.configure(bg="#1e1e1e")
        self.geometry("600x500")
        self.task_list = []
        self.load_tasks()  # Cargar tareas al iniciar la aplicación

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self, text="Lista de Tareas", fg="white", bg="#1e1e1e", font=("Arial", 20, "bold"))
        title.pack(pady=10)
        
        self.task_frame = tk.Frame(self, bg="#1e1e1e")
        self.task_frame.pack(fill=tk.BOTH, expand=True)
        
        self.update_task_list()
        
        add_button = tk.Button(self, text="Agregar Tarea +", command=self.add_task_window, fg="black", bg="#4CAF50", font=("Arial", 12, "bold"))
        add_button.pack(pady=10)

    def add_task_window(self):
        self.new_window = Toplevel(self)
        self.new_window.title("Agregar Tarea")
        self.new_window.configure(bg="#2c2c2c")
        self.new_window.geometry("400x350")
        
        tk.Label(self.new_window, text="Agregar Tarea!", fg="white", bg="#2c2c2c", font=("Arial", 18, "bold")).pack(pady=10)
        
        tk.Label(self.new_window, text="Nombre de la tarea:", fg="white", bg="#2c2c2c", font=("Arial", 12)).pack()
        self.task_name_entry = tk.Entry(self.new_window, font=("Arial", 14))
        self.task_name_entry.pack(pady=5)
        
        tk.Label(self.new_window, text="Fecha de finalización:", fg="white", bg="#2c2c2c", font=("Arial", 12)).pack()
        self.date_button = tk.Button(self.new_window, text="Seleccionar Fecha", command=self.pick_date, fg="black", bg="#007AFF", font=("Arial", 12, "bold"))
        self.date_button.pack(pady=5)
        
        self.selected_date_label = tk.Label(self.new_window, text="No seleccionada", fg="white", bg="#2c2c2c", font=("Arial", 12))
        self.selected_date_label.pack()
        
        save_button = tk.Button(self.new_window, text="Guardar", command=self.save_task, fg="black", bg="#4CAF50", font=("Arial", 12, "bold"))
        save_button.pack(pady=10)

    def pick_date(self):
        top = Toplevel(self.new_window)
        top.title("Seleccionar Fecha")
        top.configure(bg="#2c2c2c")
        
        today = datetime.date.today()
        self.cal = Calendar(top, selectmode="day", year=today.year, month=today.month, day=today.day, locale='es')
        self.cal.pack(pady=20)
        
        select_button = tk.Button(top, text="Seleccionar", command=lambda: self.set_date(top), fg="black", bg="#007AFF", font=("Arial", 12, "bold"))
        select_button.pack()
    
    def set_date(self, top):
        date = self.cal.get_date()
        date_obj = datetime.datetime.strptime(date, "%d/%m/%y")
        formatted_date = date_obj.strftime("%A %d de %B").capitalize()
        self.selected_date_label.config(text=formatted_date)
        top.destroy()
    
    def save_task(self):
        task_name = self.task_name_entry.get().strip()
        task_date = self.selected_date_label.cget("text")
        
        if not task_name:
            messagebox.showerror("Error", "El nombre de la tarea no puede estar vacío.")
            return
        
        # Establecer el estado por defecto como "Por iniciar"
        task_status = "Por iniciar"
        
        # Crear una nueva tarea con estado por defecto
        new_task = {"name": task_name, "date": task_date, "status": task_status}
        self.task_list.append(new_task)
        self.save_tasks()
        self.update_task_list()
        self.new_window.destroy()
    
    def update_task_list(self):
        for widget in self.task_frame.winfo_children():
            widget.destroy()
        
        # Mostrar las tareas en la interfaz
        for index, task in enumerate(self.task_list, start=1):
            frame = tk.Frame(self.task_frame, bg="#1e1e1e")
            frame.pack(fill=tk.X, padx=10, pady=5)
            
            tk.Label(frame, text=f"{index}. {task['name']}", fg="white", bg="#1e1e1e", font=("Arial", 18, "bold")).grid(row=0, column=0, sticky="w")
            tk.Label(frame, text=task["date"], fg="#BBBBBB", bg="#1e1e1e", font=("Arial", 12)).grid(row=0, column=1, padx=10)
            
            # Mostrar el estado como un Combobox editable
            status_var = tk.StringVar(value=task["status"])
            status_label = ttk.Combobox(frame, textvariable=status_var, values=["Por iniciar", "En progreso", "Completada"], state="normal", font=("Arial", 10))
            status_label.grid(row=0, column=2, padx=10)
            status_label.bind("<<ComboboxSelected>>", lambda event, t=task, var=status_var: self.update_status(event, t, var))
            
            delete_button = tk.Button(frame, text="Eliminar", command=lambda t=task: self.delete_task(t), fg="black", bg="#FF3B30", font=("Arial", 10, "bold"))
            delete_button.grid(row=0, column=3, padx=10)
    
    def update_status(self, event, task, status_var):
        new_status = status_var.get()
        task["status"] = new_status
        self.save_tasks()
    
    def delete_task(self, task):
        self.task_list.remove(task)
        self.save_tasks()
        self.update_task_list()
    
    def save_tasks(self):
        with open("tasks.json", "w") as file:
            json.dump(self.task_list, file, indent=4)
    
    def load_tasks(self):
        try:
            with open("tasks.json", "r") as file:
                self.task_list = json.load(file)
        except FileNotFoundError:
            self.task_list = []

if __name__ == "__main__":
    app = ToDoApp()
    app.mainloop()
