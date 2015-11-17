#===============================================================================
# My Genes(front-end) V1.2  26/October/2015
# coded by: Daniel Vilar (dvjorge@fc.ul.pt)
# 15/October/2013
#===============================================================================

#Python modules import
from Tkinter import *
from os import system

class Application(Frame):
	def __init__(self, master=None):
		Frame.__init__(self,master)
		self.grid()
		self.createWidgets()
		self.createMenu()
		
	def createWidgets(self):
	
		self.nameLabel = Label(self, text="ID")
		self.nameLabel.grid(row=1, column=0)
		self.nameEntry = Entry(self, state=NORMAL)
		self.nameEntry.grid(row=1, column=1)
		
		self.ncellsLabel = Label(self, text="Population size")
		self.ncellsLabel.grid(row=2, column=0)
		self.ncellsEntry = Entry(self, state=NORMAL)
		self.ncellsEntry.grid(row=2, column=1)
		
		self.ngenerationsLabel = Label(self, text="Number of Generations")
		self.ngenerationsLabel.grid(row=3, column=0)
		self.ngenerationsEntry = Entry(self, state=NORMAL)
		self.ngenerationsEntry.grid(row=3, column=1)
		
		self.probduplicLabel = Label(self, text="Duplication Probability")
		self.probduplicLabel.grid(row=4, column=0)
		self.probduplicEntry = Entry(self, state=NORMAL)
		self.probduplicEntry.grid(row=4, column=1)
		
		self.probelimLabel = Label(self, text="Elimination Probability")
		self.probelimLabel.grid(row=5, column=0)
		self.probelimEntry = Entry(self, state=NORMAL)
		self.probelimEntry.grid(row=5, column=1)
		
		self.probdeltaLabel = Label(self, text="Delta Probability")
		self.probdeltaLabel.grid(row=6, column=0)
		self.probdeltaEntry = Entry(self, state=NORMAL)
		self.probdeltaEntry.grid(row=6, column=1)
		
		self.probalphaLabel = Label(self, text="Alpha Probability")
		self.probalphaLabel.grid(row=7, column=0)
		self.probalphaEntry = Entry(self,state=NORMAL)
		self.probalphaEntry.grid(row=7, column=1)

		self.itstepsLabel = Label(self, text= "Iteration Steps")
		self.itstepsLabel.grid(row=8, column=0)
		self.itstepsEntry = Entry(self, state=NORMAL)
		self.itstepsEntry.grid(row=8, column=1)
		
		self.replicasLabel = Label(self, text="Number of replicas")
		self.replicasLabel.grid(row=9, column=0)
		self.replicasEntry = Entry(self, state=NORMAL)
		self.replicasEntry.grid(row=9, column=1)
		
		self.envLabel = Label(self, text="Environment")
		self.envLabel.grid(row=10, column=0)
		self.envEntry = Entry(self, state=NORMAL)
		self.envEntry.grid(row=10, column=1)
		
		self.quitButton = Button(self,text='Run',command=self.onRun)		
		self.quitButton.grid(row=11, column=0)
		self.quitButton = Button(self,text='Quit',command=self.quit)		
		self.quitButton.grid(row=11, column=1)
		
		
	def createMenu(self):
		pass
	
	def onRun(self):
		query = 'python main.py %s %s %s %s %s %s %s %s %s %s 1' %(self.nameEntry.get(), self.ncellsEntry.get(), self.ngenerationsEntry.get(), self.probduplicEntry.get(), self.probelimEntry.get(), self.probdeltaEntry.get(), self.probalphaEntry.get(), self.itstepsEntry.get(), self.replicasEntry.get(), self.envEntry.get())
		system(query)
		
app = Application()
app.master.title("My Genes")
#app.master.geometry("604x630+150+50") 
app.master.resizable(width=FALSE, height=FALSE)
#app.wm_iconbitmap('data/a.ico') #importa um icon
app.mainloop()
