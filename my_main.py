from Eq_sol import eq_solution
from App import App
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

'''
solution = eq_solution(10,100) #n m
solution.solve()
solution.show_tab()
'''