import tkinter as tk
import pickle

from profile import Profile
import items
import components.summary as summary


SAVE_LOC = './profiles/'
PROFILE_EXT = '.bbp' 

class BudgetBuddy(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self, master)
		self.master = master

		self.p = self.loadProfile('user')
		self.p.items = []
		self.p.items.append(items.Income(bal=500))
		self.p.items.append(items.Checking(bal=100.2))
		self.p.items.append(items.Credit(500, label="LOC", bal=140))
		self.p.items.append(items.Credit(500, label="Visa", bal=200))
		self.p.items.append(items.Goal(label="Credit Payoff", bal=100))
		self.p.items.append(items.Goal(label="Save", bal=580))
		self.p.items.append(items.Expense(label="Spending", bal=100))

		self.s = summary.Summary(self, self.p.items)
		self.s.pack()

		self.saveProfile(self.p)
		
	def saveProfile(self, profile):
		pickle.dump(profile, open(SAVE_LOC + profile.username + PROFILE_EXT, 'wb'))

	def loadProfile(self, username):
		return pickle.load(open(SAVE_LOC + username + PROFILE_EXT, 'rb'))
		

def main():
	root = tk.Tk()
	BudgetBuddy(root).pack(side="top", fill="both", expand=True)
	root.mainloop()

main()