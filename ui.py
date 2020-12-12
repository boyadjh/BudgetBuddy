import tkinter as tk

class Summary(tk.Frame):
	def __init__(self, master, label, items, addF):
		tk.Frame.__init__(self, master)
		tk.Label(self, text=label).pack()
		self.items = items
		self.addF = addF
		
		self.makeItems(tk.Frame(self))
		self.makeForm(tk.Frame(self))
		

	def makeForm(self, master):
		self.e_newLabel = tk.Entry(master)
		self.e_newLabel.grid(column=0, row=0)
		self.e_newBal = tk.Entry(master)
		self.e_newBal.grid(column=2, row=0)
		self.b_add = tk.Button(master, text="Add Item", command=self.addF).grid(column=3, row=0)
		master.pack()

	def makeItems(self, master):
		for i in range(len(self.items)):

			tk.Label(master, text=self.items[i].label).grid(column=0, row=i)
			tk.Label(master, text=str(self.items[i].bal)).grid(column=2, row=i)
		master.pack()