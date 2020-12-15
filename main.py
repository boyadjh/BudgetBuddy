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

		self.master.protocol('WM_DELETE_WINDOW', self.close)

		self.profile_name = 'user'

		self.p = self.loadProfile(self.profile_name)

		self.s = summary.Summary(self, self.p.items, self.updateProfileItems)
		self.s.pack()

	def updateProfileItems(self, items):
		self.p.items = items
		
	def close(self):
		self.saveProfile()
		self.master.destroy()

	def saveProfile(self):
		pickle.dump(self.p, open(SAVE_LOC + self.p.username + PROFILE_EXT, 'wb'))

	def loadProfile(self, username):
		return pickle.load(open(SAVE_LOC + username + PROFILE_EXT, 'rb'))
		

def main():
	root = tk.Tk()
	BudgetBuddy(root).pack(side="top", fill="both", expand=True)
	root.mainloop()

main()