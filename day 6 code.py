import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="polko0909",
            database="Variant8_Work"
        )
        return connection
    except Error as e:
        messagebox.showerror("Ошибка БД", f"Не удалось подключиться: {e}")
        return None

class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Управление школьной базой данных - все таблицы")
        self.root.geometry("1100x750")
        
        self.current_table = None
        self.current_columns = None
        self.entries = {}
        self.tree = None
        self.search_entry = None
        
        self.create_menu()
        self.create_table_selector()
        self.create_main_frame()
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        tables_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Таблицы", menu=tables_menu)
        
        tables = ["Students", "Subjects", "Teachers", "Teachers_Subjects", "Grades", "Attendance"]
        for table in tables:
            tables_menu.add_command(label=table, command=lambda t=table: self.load_table_by_name(t.lower()))
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.show_about)
    
    def create_table_selector(self):
        selector_frame = tk.Frame(self.root, bg="#f0f0f0", relief=tk.RAISED, bd=2)
        selector_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(selector_frame, text="Выберите таблицу:", font=("Arial", 12, "bold"), 
                bg="#f0f0f0").pack(side=tk.LEFT, padx=10)
        
        self.table_var = tk.StringVar()
        tables = ["students", "subjects", "teachers", "teachers_subjects", "grades", "attendance"]
        self.table_combo = ttk.Combobox(selector_frame, textvariable=self.table_var, 
                                        values=tables, width=20, font=("Arial", 11))
        self.table_combo.pack(side=tk.LEFT, padx=10)
        self.table_combo.bind("<<ComboboxSelected>>", self.on_table_selected)
        
        tk.Button(selector_frame, text="Загрузить таблицу", command=self.load_table,
                 bg="#4CAF50", fg="white", font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=10)
        
        self.info_label = tk.Label(selector_frame, text="", font=("Arial", 10), bg="#f0f0f0", fg="blue")
        self.info_label.pack(side=tk.RIGHT, padx=10)
    
    def create_main_frame(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.input_frame = tk.LabelFrame(self.main_frame, text="Ввод данных", padx=10, pady=10, font=("Arial", 10, "bold"))
        self.input_frame.pack(pady=10, fill="x")
        
        self.inputs_container = tk.Frame(self.input_frame)
        self.inputs_container.pack()
        
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(pady=10)
        
        self.search_frame = tk.Frame(self.main_frame)
        self.search_frame.pack(pady=5)
        
        self.tree_frame = tk.Frame(self.main_frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.status_label = tk.Label(self.main_frame, text="Готов к работе. Выберите таблицу.", font=("Arial", 9), fg="gray")
        self.status_label.pack(pady=5)
    
    def get_columns_config(self, table_name):
        configs = {
            "students": [
                {"name": "student_id", "label": "ID студента", "pk": True, "auto_increment": True},
                {"name": "full_name", "label": "ФИО", "required": True},
                {"name": "class_name", "label": "Класс", "required": True},
                {"name": "email", "label": "Email", "required": False}
            ],
            "subjects": [
                {"name": "subject_id", "label": "ID предмета", "pk": True, "auto_increment": True},
                {"name": "subject_name", "label": "Название предмета", "required": True}
            ],
            "teachers": [
                {"name": "teacher_id", "label": "ID учителя", "pk": True, "auto_increment": True},
                {"name": "full_name", "label": "ФИО учителя", "required": True}
            ],
            "teachers_subjects": [
                {"name": "teacher_id", "label": "ID учителя", "pk": True, "required": True},
                {"name": "subject_id", "label": "ID предмета", "pk": True, "required": True}
            ],
            "grades": [
                {"name": "grade_id", "label": "ID оценки", "pk": True, "auto_increment": True},
                {"name": "student_id", "label": "ID студента", "required": True},
                {"name": "subject_id", "label": "ID предмета", "required": True},
                {"name": "grade_value", "label": "Оценка", "required": True},
                {"name": "grade_date", "label": "Дата", "required": True}
            ],
            "attendance": [
                {"name": "attendance_id", "label": "ID записи", "pk": True, "auto_increment": True},
                {"name": "student_id", "label": "ID студента", "required": True},
                {"name": "attendance_date", "label": "Дата", "required": True},
                {"name": "status", "label": "Статус", "required": True}
            ]
        }
        return configs.get(table_name, [])
    
    def load_table_by_name(self, table_name):
        self.table_var.set(table_name)
        self.load_table()
    
    def on_table_selected(self, event):
        self.load_table()
    
    def load_table(self):
        self.current_table = self.table_var.get()
        if not self.current_table:
            messagebox.showwarning("Предупреждение", "Выберите таблицу")
            return
        
        self.current_columns = self.get_columns_config(self.current_table)
        if not self.current_columns:
            messagebox.showerror("Ошибка", f"Конфигурация для таблицы {self.current_table} не найдена")
            return
        
        self.clear_inputs()
        self.create_input_fields()
        self.create_buttons()
        self.create_search()
        self.create_treeview()
        self.refresh_table()
        
        table_names = {
            "students": "Ученики",
            "subjects": "Предметы",
            "teachers": "Учителя",
            "teachers_subjects": "Связь учителей и предметов",
            "grades": "Оценки",
            "attendance": "Посещаемость"
        }
        self.info_label.config(text=f"Таблица: {table_names.get(self.current_table, self.current_table)}")
        self.status_label.config(text=f"Загружена таблица: {self.current_table}")
    
    def clear_inputs(self):
        for widget in self.inputs_container.winfo_children():
            widget.destroy()
        self.entries = {}
    
    def create_input_fields(self):
        row = 0
        col = 0
        
        for column in self.current_columns:
            if column.get('pk') and column.get('auto_increment'):
                continue
            
            label = tk.Label(self.inputs_container, text=f"{column['label']}:", 
                           font=("Arial", 10, "bold"))
            label.grid(row=row, column=col, padx=5, pady=5, sticky="e")
            
            if column['name'] in ['status']:
                entry = ttk.Combobox(self.inputs_container, width=23, font=("Arial", 10))
                entry['values'] = ('Присутствовал', 'Отсутствовал', 'Опоздал')
                entry.set('Присутствовал')
            elif column['name'] in ['grade_value']:
                entry = ttk.Combobox(self.inputs_container, width=23, font=("Arial", 10))
                entry['values'] = ('2', '3', '4', '5')
                entry.set('5')
            elif column['name'] in ['student_id', 'subject_id', 'teacher_id']:
                entry = tk.Entry(self.inputs_container, width=25, font=("Arial", 10))
                self.add_foreign_key_help(entry, column['name'])
            else:
                entry = tk.Entry(self.inputs_container, width=25, font=("Arial", 10))
            
            entry.grid(row=row, column=col+1, padx=5, pady=5)
            self.entries[column['name']] = entry
            
            col += 2
            if col >= 6:
                col = 0
                row += 1
    
    def add_foreign_key_help(self, entry, field_name):
        help_text = {
            'student_id': " (ID из таблицы students: 1-5)",
            'subject_id': " (ID из таблицы subjects: 1-3)",
            'teacher_id': " (ID из таблицы teachers: 1-2)"
        }
        if field_name in help_text:
            hint = tk.Label(self.inputs_container, text=help_text[field_name], 
                          font=("Arial", 8), fg="gray")
            hint.grid(row=self.get_current_row(), column=self.get_current_col()+2, padx=2)
    
    def get_current_row(self):
        for widget in self.inputs_container.winfo_children():
            info = widget.grid_info()
            if 'row' in info:
                return info['row']
        return 0
    
    def get_current_col(self):
        for widget in self.inputs_container.winfo_children():
            info = widget.grid_info()
            if 'column' in info:
                return info['column']
        return 0
    
    def create_buttons(self):
        for widget in self.button_frame.winfo_children():
            widget.destroy()
        
        buttons = [
            ("➕ Добавить", self.add_record, "#90EE90"),
            ("✏️ Обновить", self.update_record, "#FFD700"),
            ("🗑️ Удалить", self.delete_record, "#FF6347"),
            ("🧹 Очистить", self.clear_entries, "#D3D3D3"),
            ("🔄 Обновить", self.refresh_table, "#ADD8E6"),
            ("📊 Показать статистику", self.show_statistics, "#FFB6C1")
        ]
        
        for i, (text, command, bg) in enumerate(buttons):
            btn = tk.Button(self.button_frame, text=text, command=command, 
                           bg=bg, width=14, font=("Arial", 10))
            btn.grid(row=0, column=i, padx=3)
    
    def create_search(self):
        for widget in self.search_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.search_frame, text="🔍 Поиск:", font=("Arial", 10)).pack(side=tk.LEFT)
        self.search_entry = tk.Entry(self.search_frame, width=40, font=("Arial", 10))
        self.search_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(self.search_frame, text="Найти", command=self.search,
                 bg="#87CEEB", width=10).pack(side=tk.LEFT)
        tk.Button(self.search_frame, text="Сброс", command=self.refresh_table,
                 bg="#D3D3D3", width=10).pack(side=tk.LEFT, padx=5)
    
    def create_treeview(self):
        for widget in self.tree_frame.winfo_children():
            widget.destroy()
        
        scroll_y = tk.Scrollbar(self.tree_frame, orient=tk.VERTICAL)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scroll_x = tk.Scrollbar(self.tree_frame, orient=tk.HORIZONTAL)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        columns_display = [col['name'] for col in self.current_columns]
        self.tree = ttk.Treeview(self.tree_frame, columns=columns_display, show="headings",
                                 yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        for col in self.current_columns:
            self.tree.heading(col['name'], text=col['label'])
            if col['name'] in ['full_name', 'subject_name']:
                self.tree.column(col['name'], width=200, anchor="w")
            else:
                self.tree.column(col['name'], width=100, anchor="center")
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
    
    def refresh_table(self):
        if not self.tree:
            return
        
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        conn = connect_db()
        if not conn:
            return
        
        cursor = conn.cursor()
        columns_names = [col['name'] for col in self.current_columns]
        query = f"SELECT {', '.join(columns_names)} FROM {self.current_table}"
        
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                self.tree.insert("", tk.END, values=row)
            self.status_label.config(text=f"Загружено записей: {len(rows)}")
        except Error as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")
        finally:
            cursor.close()
            conn.close()
    
    def search(self):
        if not self.search_entry:
            return
        
        keyword = self.search_entry.get().strip()
        if not keyword:
            self.refresh_table()
            return
        
        conn = connect_db()
        if not conn:
            return
        
        cursor = conn.cursor()
        
        exclude_fields = ['student_id', 'teacher_id', 'subject_id', 'grade_id', 'attendance_id']
        text_columns = [col['name'] for col in self.current_columns 
                       if col['name'] not in exclude_fields]
        
        if not text_columns:
            self.refresh_table()
            return
        
        conditions = " OR ".join([f"{col} LIKE %s" for col in text_columns])
        query = f"SELECT * FROM {self.current_table} WHERE {conditions}"
        
        try:
            params = tuple([f"%{keyword}%"] * len(text_columns))
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            for row in self.tree.get_children():
                self.tree.delete(row)
            
            for row in rows:
                self.tree.insert("", tk.END, values=row)
            
            if not rows:
                messagebox.showinfo("Поиск", "Ничего не найдено")
                self.status_label.config(text="Результатов не найдено")
            else:
                self.status_label.config(text=f"Найдено записей: {len(rows)}")
                
        except Error as e:
            messagebox.showerror("Ошибка", str(e))
        finally:
            cursor.close()
            conn.close()
    
    def on_select(self, event):
        if not self.tree or not self.entries:
            return
        
        selected = self.tree.selection()
        if not selected:
            return
        
        values = self.tree.item(selected[0])['values']
        
        for i, col in enumerate(self.current_columns):
            col_name = col['name']
            if col_name in self.entries:
                self.entries[col_name].delete(0, tk.END)
                self.entries[col_name].insert(0, str(values[i]) if values[i] is not None else "")
    
    def get_pk_name(self):
        for col in self.current_columns:
            if col.get('pk'):
                return col['name']
        return None
    
    def get_pk_values(self, row_values):
        pk_indices = []
        pk_names = []
        for i, col in enumerate(self.current_columns):
            if col.get('pk'):
                pk_indices.append(i)
                pk_names.append(col['name'])
        
        if len(pk_indices) == 1:
            return {pk_names[0]: row_values[pk_indices[0]]}
        else:
            pk_values = {}
            for idx, name in zip(pk_indices, pk_names):
                pk_values[name] = row_values[idx]
            return pk_values
    
    def add_record(self):
        if not self.current_table or not self.entries:
            messagebox.showwarning("Предупреждение", "Загрузите таблицу")
            return
        
        values = {}
        for col_name, entry in self.entries.items():
            values[col_name] = entry.get().strip()
        
        for col in self.current_columns:
            col_name = col['name']
            if col.get('required') and col_name in self.entries and not values[col_name]:
                messagebox.showwarning("Ошибка", f"Поле '{col['label']}' обязательно для заполнения")
                return
        
        conn = connect_db()
        if not conn:
            return
        
        cursor = conn.cursor()
        columns_names = list(values.keys())
        placeholders = ", ".join(["%s"] * len(columns_names))
        query = f"INSERT INTO {self.current_table} ({', '.join(columns_names)}) VALUES ({placeholders})"
        
        try:
            cursor.execute(query, list(values.values()))
            conn.commit()
            messagebox.showinfo("Успех", "Запись добавлена")
            self.clear_entries()
            self.refresh_table()
        except Error as e:
            if "Duplicate entry" in str(e):
                messagebox.showerror("Ошибка БД", "Такая запись уже существует (дубликат ключа)")
            else:
                messagebox.showerror("Ошибка БД", str(e))
        finally:
            cursor.close()
            conn.close()
    
    def update_record(self):
        if not self.tree or not self.entries:
            messagebox.showwarning("Предупреждение", "Загрузите таблицу")
            return
        
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите запись для обновления")
            return
        
        values_current = self.tree.item(selected[0])['values']
        pk_values = self.get_pk_values(values_current)
        
        if not pk_values:
            messagebox.showerror("Ошибка", "Не удалось определить первичный ключ")
            return
        
        new_values = {}
        for col_name, entry in self.entries.items():
            new_values[col_name] = entry.get().strip()
        
        conn = connect_db()
        if not conn:
            return
        
        cursor = conn.cursor()
        
        where_clause = " AND ".join([f"{k} = %s" for k in pk_values.keys()])
        set_clause = ", ".join([f"{col} = %s" for col in new_values.keys()])
        query = f"UPDATE {self.current_table} SET {set_clause} WHERE {where_clause}"
        
        try:
            params = list(new_values.values()) + list(pk_values.values())
            cursor.execute(query, params)
            conn.commit()
            messagebox.showinfo("Успех", "Запись обновлена")
            self.refresh_table()
        except Error as e:
            messagebox.showerror("Ошибка БД", str(e))
        finally:
            cursor.close()
            conn.close()
    
    def delete_record(self):
        if not self.tree:
            messagebox.showwarning("Предупреждение", "Загрузите таблицу")
            return
        
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите запись для удаления")
            return
        
        if not messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить запись?\nВНИМАНИЕ: Могут быть удалены связанные данные!"):
            return
        
        values_current = self.tree.item(selected[0])['values']
        pk_values = self.get_pk_values(values_current)
        
        if not pk_values:
            messagebox.showerror("Ошибка", "Не удалось определить первичный ключ")
            return
        
        conn = connect_db()
        if not conn:
            return
        
        cursor = conn.cursor()
        
        where_clause = " AND ".join([f"{k} = %s" for k in pk_values.keys()])
        query = f"DELETE FROM {self.current_table} WHERE {where_clause}"
        
        try:
            cursor.execute(query, list(pk_values.values()))
            conn.commit()
            messagebox.showinfo("Успех", "Запись удалена")
            self.clear_entries()
            self.refresh_table()
        except Error as e:
            if "foreign key constraint" in str(e).lower():
                messagebox.showerror("Ошибка БД", "Невозможно удалить запись, так как на нее есть ссылки в других таблицах")
            else:
                messagebox.showerror("Ошибка БД", str(e))
        finally:
            cursor.close()
            conn.close()
    
    def clear_entries(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
    
    def show_statistics(self):
        if not self.current_table:
            messagebox.showinfo("Статистика", "Сначала выберите таблицу")
            return
        
        conn = connect_db()
        if not conn:
            return
        
        cursor = conn.cursor()
        
        stats_window = tk.Toplevel(self.root)
        stats_window.title(f"Статистика - {self.current_table}")
        stats_window.geometry("600x400")
        
        stats_text = tk.Text(stats_window, wrap=tk.WORD, font=("Arial", 10))
        stats_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(stats_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        stats_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=stats_text.yview)
        
        stats_text.insert(tk.END, f"📊 СТАТИСТИКА ДЛЯ ТАБЛИЦЫ: {self.current_table.upper()}\n")
        stats_text.insert(tk.END, "="*50 + "\n\n")
        
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {self.current_table}")
            count = cursor.fetchone()[0]
            stats_text.insert(tk.END, f"📌 Общее количество записей: {count}\n\n")
            
            if self.current_table == "students":
                cursor.execute("SELECT class_name, COUNT(*) FROM students GROUP BY class_name")
                stats_text.insert(tk.END, "📌 Ученики по классам:\n")
                for row in cursor.fetchall():
                    stats_text.insert(tk.END, f"   - {row[0]}: {row[1]} учеников\n")
            
            elif self.current_table == "grades":
                cursor.execute("SELECT AVG(grade_value) FROM grades")
                avg_grade = cursor.fetchone()[0]
                stats_text.insert(tk.END, f"📌 Средний балл по всем оценкам: {round(avg_grade, 2) if avg_grade else 0}\n\n")
                
                cursor.execute("""
                    SELECT sub.subject_name, AVG(g.grade_value) 
                    FROM grades g 
                    JOIN subjects sub ON g.subject_id = sub.subject_id 
                    GROUP BY sub.subject_name
                """)
                stats_text.insert(tk.END, "📌 Средний балл по предметам:\n")
                for row in cursor.fetchall():
                    stats_text.insert(tk.END, f"   - {row[0]}: {round(row[1], 2) if row[1] else 0}\n")
            
            elif self.current_table == "attendance":
                cursor.execute("""
                    SELECT status, COUNT(*) 
                    FROM attendance 
                    GROUP BY status
                """)
                stats_text.insert(tk.END, "📌 Статистика посещаемости:\n")
                for row in cursor.fetchall():
                    stats_text.insert(tk.END, f"   - {row[0]}: {row[1]} раз\n")
            
            elif self.current_table == "teachers_subjects":
                cursor.execute("""
                    SELECT t.full_name, COUNT(ts.subject_id) 
                    FROM teachers t
                    JOIN teachers_subjects ts ON t.teacher_id = ts.teacher_id
                    GROUP BY t.teacher_id
                """)
                stats_text.insert(tk.END, "📌 Количество предметов у учителей:\n")
                for row in cursor.fetchall():
                    stats_text.insert(tk.END, f"   - {row[0]}: {row[1]} предметов\n")
            
        except Error as e:
            stats_text.insert(tk.END, f"Ошибка получения статистики: {e}")
        
        stats_text.config(state=tk.DISABLED)
        
        cursor.close()
        conn.close()
    
    def show_about(self):
        about_text = "Школьная база данных v2.0"
        messagebox.showinfo("О программе", about_text)

def main():
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()