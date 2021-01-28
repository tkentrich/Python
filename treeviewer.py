import csv
import json
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

class TreeViewer:
    def __init__(self):
        self.root = tk.Tk()
        self.selectedFileString = tk.StringVar()
        self.jsonObject = {}
        self.subObjects = {}

        tk.Button(self.root, text="Load File", command=self.load).pack(anchor=tk.W)
        tk.Label(self.root, textvariable=self.selectedFileString).pack(anchor=tk.W)

        self.tree=ttk.Treeview(self.root)
        self.tree['columns']=("Value")
        self.tree.column("#0", width=150, minwidth=150, stretch=tk.NO)
        self.tree.column("Value", minwidth=300)
        self.tree.heading("#0", text="Key", anchor=tk.W)
        self.tree.heading("Value", text="Value", anchor=tk.W)

        self.tree.pack(fill=tk.BOTH, expand=1)

        tk.Button(self.root, text="Expand", command=self.expand).pack()

        self.root.mainloop()

    def load(self):
        fileResponse = filedialog.askopenfilename(title = 'Select File', filetypes=(("json files", "*.json"), ("csv files", "*.csv"), ("all files", "*.*")))
        if fileResponse == "":
            return
        self.selectedFileString.set(fileResponse)
        try:
            self.jsonObject = json.load(open(fileResponse, 'r'))
        except json.JSONDecodeError:
            self.jsonObject = []
            fileObj = open(fileResponse, 'r')
            lines = fileObj.readlines()
            columns = []
            for y, row in enumerate(csv.reader(lines)):
                if y == 0:
                    columns=row
                    continue
                obj={}
                for x, col in enumerate(columns):
                    obj[col] = row[x]
                self.jsonObject.append(obj)
        if type(self.jsonObject) == list:
            self.jsonObject = {"items": self.jsonObject}
        self.generateOutput(self.jsonObject, "")

    def generateOutput(self, d, parent):
        if parent == "":
            self.tree.delete(*self.tree.get_children())
        for key in sorted(d.keys()):
            if type(d[key]) == dict:
                folder = self.tree.insert(parent, tk.END, None, text=key, values=("MAP",))
                self.subObjects[folder] = d[key]
                self.generateOutput(d[key], folder)
            elif type(d[key]) == list:
                folder = self.tree.insert(parent, tk.END, None, text=key, values=("LIST",))
                self.subObjects[folder] = d[key]
                for index,item in enumerate(d[key]):
                    if type(item) == dict:
                        subFolder = self.tree.insert(folder, tk.END, None, text="listitem %d"%(index,), values=("MAP",))
                        self.subObjects[subFolder] = item
                        self.generateOutput(item, subFolder)
                    elif type(item) == list:
                        subFolder = self.tree.insert(parent, tk.END, None, values=("LIST",))
                        self.subObjects[subFolder] = item
                    else:
                        subFolder = self.tree.insert(parent, tk.END, None, values=(item,))
                        self.subObjects[subFolder] = item
            else:
                item=self.tree.insert(parent, tk.END, None, text=key, values=(d[key],))
                self.subObjects[item] = d[key]

    def expand(self):
        selection = self.tree.selection()
        if len(selection) == 0:
            return
        selected = selection[0]
        jsonObj = self.subObjects[selected]
        newFrame = tk.Toplevel(self.root)
        if type(jsonObj) == dict:
            tree = ttk.Treeview(newFrame)
            tree['columns']=("Value")
            tree.column("#0", width=150, minwidth=150, stretch=tk.NO)
            tree.column("Value", minwidth=300)
            tree.heading("#0", text="Key", anchor=tk.W)
            tree.heading("Value", text="Value", anchor=tk.W)
            for key in jsonObj.keys():
                tree.insert("", tk.END, None, text=key, values=(jsonObj[key],))
            tree.pack(fill=tk.BOTH, expand=1)
        elif type(jsonObj) == list:
            if len(jsonObj) == 0:
                tk.Label(newFrame, text="Empty List")
            elif type(jsonObj[0]) == dict:
                tree = ttk.Treeview(newFrame)
                columns=[]
                for item in jsonObj:
                    if type(item) == dict:
                        for key in item.keys():
                            if key not in columns:
                                columns.append(key)
                columns = sorted(columns)
                print(columns)
                tree['columns'] = columns
                for col in columns:
                    tree.heading(col, text=col)
                for i, row in enumerate(jsonObj):
                    if (type(row) != dict):
                        continue
                    vals = []
                    for col in columns:
                        vals.append(row.get(col, "-"))
                    tree.insert("", tk.END, None, text=i, values=vals)
                tree.pack(fill=tk.BOTH, expand=1)
            else:
                tk.Label(newFrame, text=", ".join(jsonObj))
        else:
            tk.Label(newFrame, text=str(jsonObj)).pack()

if __name__ == "__main__":
    tv = TreeViewer()
