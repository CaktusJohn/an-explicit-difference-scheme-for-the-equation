import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class eq_solution:
    
    left_x = 0   #атрибут класса
    right_x = 1
    left_t = 0
    right_t = 10  
        
    def __init__(self, N, M):   # n кол-во разбиений по x, m - по t
        
        self.n = N           #атрибут экземпляра
        self.node_x = self.n + 1  #кол - во узлов 
        self.h = (eq_solution.right_x  - eq_solution.left_x) / self.n #шаг по x
        self.xi = [eq_solution.left_x + i * self.h for i in range(self.node_x)] # x - узлы сетки по x
        
        
        self.m = M
        self.node_t = self.m + 1
        self.tau = (eq_solution.right_t  - eq_solution.left_t) / self.m #шаг по x
        self.tj = [eq_solution.left_t + j * self.tau for j in range(self.node_t)]# t - узлы сетки по времени
        
        self.gamma = np.sqrt(3) # gamma - коэф-т перед второй производной
        
        self.g = lambda x, t: np.cos(np.pi * x) * t/(t+1)  # g(x, t) - функция 
           
        self.phi = lambda x: 1 - x ** 2   
        
        self.mu1 = lambda t: np.cos(t) 
       
        self.mu2 = lambda t: np.sin(4 * t) 

        
        self.Vij = np.empty([self.node_x, self.node_t], dtype=np.double)# матрица [n + 1, m + 1] с узлами сетки с координатами (xi, tj), i=1,node_x-1; j=1,node_t

    def check_stability(self):
        # Вычисление коэффициента CFL
        if (self.tau < self.h**2 / (2 * self.gamma**2)):
            return True
        return False

    def solve(self):
        #заполнили нулевой слой
        for i in range(self.node_x):
            x = self.xi[i]
            self.Vij[i][0] = 1 - x**2
            
        for j in range(self.m):
            self.Vij[0][j] = self.mu1(self.tj[j])
            self.Vij[-1][j] = self.mu2(self.tj[j])
            for i in range(1, self.n):
                a1 = self.Vij[i + 1][j]
                a2 = self.Vij[i][j]
                a3 = self.Vij[i - 1][j]
                self.Vij[i][j + 1] = self.tau * (3 * ( a1 - 2 * a2  + a3) / self.h**2 + self.g(self.xi[i], self.tj[j])) + a2
        
        self.Vij[0][-1] = self.mu1(self.tj[-1])
        self.Vij[-1][-1] = self.mu2(self.tj[-1])

    
    def get_table(self):
      
        '''
        # Формируем индексы для таблицы
        time_layers = list(np.arange(self.node_t))  # arange создаёт массив чисел от 0 до числа
        space_nodes = list(np.arange(self.node_x))  # Индексы узлов по x (i)

        # Повторяем индексы для всех временных слоев и узлов
        time_indices = sorted(time_layers * self.node_x)  # умножение повторяет элементы какое то колво раз
        time_values = sorted(list(self.tj) * self.node_x)  # Повторяем t_j для каждого узла x
        space_indices = space_nodes * self.node_t         # Повторяем i для всех слоев

        df = pd.DataFrame({
            'j': time_indices,                         
            't': np.around(time_values, 7),            #around округляет до какого то знака после запятой
            'i': space_indices,                        
            'x': np.around(list(self.xi) * self.node_t, 7),  
            'U(x,t)': np.around(self.Vij.ravel(), 14)        #ravel создаёт одномерный массив из двумерного
        })
        '''
       
        # Формируем индексы для таблицы
        time_layers = list(range(self.node_t))  # Временные слои
        space_nodes = list(range(self.node_x))  # Узлы по x

        # Создаем списки с повторяющимися значениями
        time_indices = [int(j) for j in time_layers for _ in space_nodes]
        time_values = [self.tj[j] for j in time_layers for _ in space_nodes]
        space_indices = [int(i) for _ in time_layers for i in space_nodes]
        x_values = [self.xi[i] for _ in time_layers for i in space_nodes]
        u_values = [self.Vij[i, j] for j in time_layers for i in space_nodes]

        # Создаем DataFrame
        df = pd.DataFrame({
            'j': np.around(time_indices,1),
            't': np.around(time_values, 7),
            'i': space_indices,
            'x': np.around(x_values, 7),
            'U(x,t)': np.around(u_values, 14)
        })
        
        

        return df
    '''
    def get_table(self):
        data = []
        for j in range(self.node_t):
            for i in range(self.node_x):
                data.append([j, self.tj[j], i, self.xi[i], self.Vij[i, j]])
        return pd.DataFrame(data, columns=["j", "t", "i", "x", "U(x,t)"])   
    '''
    
    def plot_layer(self, layer):
        if 0 <= layer < self.node_t:
            plt.figure(figsize=(8, 5))
            plt.plot(self.xi, self.Vij[:, layer], marker='o', label=f'Слой t={self.tj[layer]:.2f}')
            plt.title(f'Решение на слое {layer}')
            plt.xlabel('x')
            plt.ylabel('U(x,t)')
            plt.legend()
            plt.grid()
            plt.show()
        else:
            raise ValueError("Invalid layer index.")
    
    
    '''
    # Создаем DataFrame с данными из Vij
    df = pd.DataFrame(self.Vij, 
                    index=[f"x = {x:.4f}" for x in self.xi],  # Индексы — узлы по x
                    columns=[f"t = {t:.4f}" for t in self.tj])  # Столбцы — слои по t
    print(df)

    '''
    '''
    df = pd.DataFrame(self.Vij, index=[f"x={round(x, 2)}" for x in self.xi],
                    columns=[f"t={round(t, 2)}" for t in self.tj])
    print(df)
    '''