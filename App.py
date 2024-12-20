from Eq_sol import eq_solution
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt

class App:

    def __init__(self, root):
        self.root = root
        self.root.title("Задача №10 (вариант 1) Иванов Кирилл. Команда - Иванов, Зацепин, Хамков, Максимович. 3822Б1ПМоп2")
        self.create_widgets()
    
    def create_widgets(self):
        # Поля ввода
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Разбиения по x (N):").grid(row=0, column=0, padx=5)
        self.n_entry = tk.Entry(frame, width=10)
        self.n_entry.grid(row=0, column=1, padx=5)
        self.n_entry.insert(0, "10")

        tk.Label(frame, text="Разбиения по t (M):").grid(row=1, column=0, padx=5)
        self.m_entry = tk.Entry(frame, width=10)
        self.m_entry.grid(row=1, column=1, padx=5)
        self.m_entry.insert(0, "10")
        
        # Добавляем текстовое поле для проверки устойчивости
        self.stability_label = tk.Label(self.root, text="", fg="blue")
        self.stability_label.pack()
        
        #текст критерия
        self.criterion_label = tk.Label(self.root, text="Критерий устойчивости: m > 60 * n^2", fg="green", font=("Arial", 10))
        self.criterion_label.pack(side="right", pady=5)

        # Кнопки
        tk.Button(frame, text="Решить", command=self.solve_equation).grid(row=0, column=2, padx=10, rowspan=2)

        # Таблица с прокруткой
        self.tree_frame = tk.Frame(self.root)
        self.tree_frame.pack(pady=10)

        self.tree = ttk.Treeview(self.tree_frame, columns=("j", "t", "i", "x", "U(x,t)"), show="headings", height=25)
        self.tree.pack(side=tk.LEFT)

        # Прокрутка
        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

        for col in ("j", "t", "i", "x", "U(x,t)"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200,  anchor="center")

        # Поле для вывода графика
        graph_frame = tk.Frame(self.root)
        graph_frame.pack(pady=10)

        tk.Label(graph_frame, text="Номер слоя t (j):").grid(row=0, column=0, padx=5)
        self.layer_entry = tk.Entry(graph_frame, width=10)
        self.layer_entry.grid(row=0, column=1, padx=5)

        tk.Button(graph_frame, text="Построить график", command=self.plot_graph).grid(row=0, column=2, padx=10)

    def solve_equation(self):
        N = int(self.n_entry.get())
        M = int(self.m_entry.get())
        solver = eq_solution(N, M)
        solver.solve()
       

        self.solution = solver
        self.update_table()
        
        # Проверяем устойчивость
        is_stable = solver.check_stability()
        self.stability_label.config(
            text="Схема устойчива" if is_stable else "Схема неустойчива",
            fg="green" if is_stable else "red"
        )

    def update_table(self):
        # Очистка текущей таблицы
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Обновление таблицы
        df = self.solution.get_table()
        for _, row in df.iterrows():
            self.tree.insert("", tk.END, values=list(row))
    
        

    def plot_graph(self):
        try:
            layer = int(self.layer_entry.get())
            if 0 <= layer < self.solution.node_t:
                x_values = self.solution.xi
                y_values = self.solution.Vij[:, layer]
                plt.figure(figsize=(8, 5))
                plt.plot(x_values, y_values, marker='o', label=f"Слой {layer}")
                plt.title(f"График слоя {layer} (t = {self.solution.tj[layer]:.2f})")
                plt.xlabel("x")
                plt.ylabel("U(x,t)")
                plt.legend()
                plt.grid()
                plt.show()
            else:
                tk.messagebox.showerror("Ошибка", f"Слой {layer} вне диапазона (0-{self.solution.node_t - 1})!")
        except ValueError:
            tk.messagebox.showerror("Ошибка", "Введите корректный номер слоя!")