import numpy as np 
import matplotlib.pyplot as plt
import networkx as nx
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import math

# xв = x/2 + rcosa ; yв = y/2 + rsina ; a = 360*k/n

class Graph:
    G = nx.DiGraph()
    type = ""
    nov = {}
    n = 0
    def __init__(self,path):
        with open(path) as file:
            lines = file.read().splitlines()
            self.type = (lines[0].split())[0]
            self.n = int((lines[0].split())[1])
            if(self.type == "t1"):
                self.G = nx.DiGraph()
                lines.remove(lines[0])
                k=0
                for line in lines:
                    line_list = list(line.split())
                    self.nov[line_list[0]] = True
                    self.G.add_node(line_list[0],pos=(500/2+100*math.cos(2*math.pi * k /self.n),500/2+100*math.sin(2*math.pi * k /self.n)))
                    k+=1
                    for _ in range(1,len(line_list)):
                        self.G.add_edge(line_list[0],line_list[_])
            if(self.type == "t2"):
                self.G = nx.DiGraph()
                lines.remove(lines[0])
                k=0
                for line in lines:
                    line_list = list(line.split())
                    self.nov[line_list[0]] = True
                    self.G.add_node(line_list[0],pos=(500/2+100*math.cos(2*math.pi * k /self.n),500/2+100*math.sin(2*math.pi * k /self.n)))
                    k+=1
                    for _ in range(1,len(line_list),2):
                        self.G.add_edge(line_list[0],line_list[_],weight = float(line_list[_+1]))            
            if(self.type == "t3"):
                self.G = nx.DiGraph(directed = True)
                lines.remove(lines[0])
                k=0
                for line in lines:
                    line_list = list(line.split())
                    self.nov[line_list[0]] = True
                    self.G.add_node(line_list[0],pos=(500/2+100*math.cos(2*math.pi * k /self.n),500/2+100*math.sin(2*math.pi * k /self.n)))
                    k+=1
                    for _ in range(1,len(line_list)):
                        self.G.add_edge(line_list[0],line_list[_])
            if(self.type == "t4"):
                self.G = nx.DiGraph(directed = True)
                lines.remove(lines[0])
                k=0
                for line in lines:
                    line_list = list(line.split())
                    self.nov[line_list[0]] = True
                    self.G.add_node(line_list[0],pos=(500/2+100*math.cos(2*math.pi * k /self.n),500/2+100*math.sin(2*math.pi * k /self.n)))
                    k+=1
                    for _ in range(1,len(line_list),2):
                        self.G.add_edge(line_list[0],line_list[_],weight = float(line_list[_+1]))
    def ClearNov(self):
        for _ in self.nov.keys():
            self.nov[_] = True
    def Dfs(self,v,list1,list2,g_dfs,k):
        if k==0:
            self.nov[v] = False 
            list2.append(v)
            list1.remove(v)
            g_dfs.add_node(v,pos = (500,50+50*k))
            self.DrawGraph(list1,list2,g_dfs)
            plt.pause(3)
            for _ in nx.neighbors(self.G,v):
                if self.nov[_] == True:
                    k+=1
                    g_dfs.add_node(_,pos = (500,50+50*k))
                    g_dfs.add_edge(v,_,weight = int(k))
                    self.Dfs(_,list1,list2,g_dfs,k)
                    k+=1
        else:
            self.nov[v] = False 
            list2.append(v)
            list1.remove(v)
            g_dfs.add_node(v,pos = (500,50+50*k))
            self.DrawGraph(list1,list2,g_dfs)
            plt.pause(3)
            for _ in nx.neighbors(self.G,v):
                if self.nov[_] == True:
                    k+=1
                    g_dfs.add_node(_,pos = (500,50+50*k))
                    g_dfs.add_edge(v,_,weight = int(k))
                    self.Dfs(_,list1,list2,g_dfs,k)
                    k+=1
    def DrawGraph(self,list1,list2,g_dfs):
        pos=nx.get_node_attributes(self.G,'pos')
        pos2=nx.get_node_attributes(g_dfs,'pos')
        nx.draw_networkx_nodes(self.G,pos,list1, node_color = "tab:blue")
        nx.draw_networkx_nodes(self.G,pos,list2,node_color = "tab:red")
        nx.draw_networkx_labels(self.G,pos)
        nx.draw_networkx_edges(self.G,pos)
        labels = nx.get_edge_attributes(self.G,'weight')
        nx.draw_networkx_edge_labels(self.G,pos,edge_labels=labels)
        nx.draw(g_dfs,pos2)
        nx.draw_networkx_labels(g_dfs,pos2)
        nx.draw_networkx_edges(g_dfs,pos2)

def open_file():
    g = Graph(filedialog.askopenfilename())
    label = ttk.Label(text="Выберете вершину начала обхода в глубину")
    label.pack(expand=True)
    combobox = ttk.Combobox(values=list(g.G.nodes))
    combobox.pack(expand=True)
    h = ttk.Button(text = "Описание работы визуализатора обхода в глубину", command = lambda:h_window())
    h.pack(expand=True)
    start_button = ttk.Button(text="Начать обход в глубину",command= lambda:start_dfs(g))
    start_button.pack(side=BOTTOM,fill = X)
    def start_dfs(g):
        plt.title("Визуализация обхода в глубину")
        v = str(combobox.get())
        list1 = list(g.G.nodes)
        list2 = list()
        g_dfs = nx.DiGraph()
        k=0
        g.Dfs(v,list1,list2,g_dfs,k)
        g.ClearNov()
    def h_window():
        window = Tk()
        window.title("Справка")
        window.geometry("500x500")
        label2 = ttk.Label(window,text = "Описание визуализатора обхода в глубину")
        label2.pack()
        label3 = ttk.Label(window,wraplength=500,text = "Алгоритм обхода в глубину: Алгоритм поиска описан рекурсивно. Перебираем все исходящие из рассматриваемой вершины рёбра. Если ребро ведёт в вершину, которая не была рассмотрена ранее, то запускаем алгоритм от этой нерассмотренной вершины, а после возвращаемся и продолжаем перебирать рёбра. Возврат происходит в том случае, если в рассматриваемой вершине не осталось рёбер, которые ведут в нерассмотренную вершину. \n \n \nПсевдокод: G - граф, u - вершина начала обхода, Adj[u] - смежные вершины с u, .visited - параметр посещенности вершины(true - посещена, false - непосещена) \n \n DFS(G,u)\n \t u.visited = true \n \t for each v ∈ G.Adj[u] \n \t \t if v.visited == false \n \t \t \t DFS(G,v) \n\n\nВ окне визуализации слева показывается граф: синие вершины - ещё не просмотренные, красные - просмотренные. Справа выводится последовательность посещенных вершин.")
        label3.pack(anchor="nw",pady=20)


root = Tk()
root.title("Визуализация обхода в глубину")
root.geometry("400x400")
open_button = ttk.Button(text ="Заполнить граф из файлу", command = open_file)
open_button.pack(side=TOP,fill=X)

root.mainloop()
