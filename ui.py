import tkinter as tk
import random
import webbrowser

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Matchups')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.geometry('750x750')
        self.resizable(True, True)
        self.config(bg='#ffffff')
        self.font = ('Arial', 14)
        self.labelPick = tk.Label(self, text='Enter the names of the players below:', font=self.font, bg='#ffffff')
        self.labelPick.pack(pady=10)
        self.text = tk.Text(self, width=50, height=10, font=self.font)
        self.text.pack(pady=10)
        self.button = tk.Button(self, text='Create Matchups', font=self.font, command=self.click)
        self.button.pack()
        self.labels = []
        self.frame = tk.Frame(self, bg='#ffffff')
        self.frame.pack(pady=10)
        self.canvas = tk.Canvas(self.frame, bg='#ffffff')
        self.canvas.config(width=500)
        self.scrollbar = tk.Scrollbar(self.frame, orient='vertical', command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='#ffffff')
        self.scrollable_frame.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side='left', fill='both', expand=True)
        self.scrollbar.pack(side='right', fill='y')
        
    def shuffle(self):
        for label in self.labels:
            label.destroy()
        self.labels = []

        self.lista = self.text.get('1.0', 'end-1c').split('\n')
        random.shuffle(self.lista)
        for i in range(int(len(self.lista)/2)):
            self.labels.append(tk.Label(self.scrollable_frame, text='', font=self.font, bg='#ffffff'))
            # we want the labels to be aligned to the left
            self.labels[i].pack(anchor='w', pady=10)


        
        self.matchups = []
        try:
            for i in range(0, len(self.lista), 2):
                self.matchups.append(self.lista[i] + ' vs ' + self.lista[i+1])
        except IndexError:
            self.matchups.append(self.lista[i] + ' vs ' + 'no one lol')
            
    def pick(self):
        self.n = random.randint(0, len(self.lista)-1)

    def update(self):
        for i in range(len(self.matchups)):
            try:
                self.labels[i].config(text=self.matchups[i])
            except IndexError:
                pass
        self.labelPick.config(text='The player will play with: ' + self.lista[self.n])
    
    def sendToText(self):
        with open('matchups.txt', 'w') as f:
            for matchup in self.matchups:
                f.write(matchup + '\n')
            f.write('The player will play with: ' + self.lista[self.n])
        
    def click(self):
        self.shuffle()
        self.pick()
        self.update()
        self.sendToText()
        
    def run(self):
        self.mainloop()
    

def popup():
    popup = tk.Tk()
    popup.title('Credits')
    popup.geometry('300x200')
    popup.resizable(False, False)
    popup.config(bg='#ffffff')
    popup.update_idletasks()
    width = popup.winfo_width()
    height = popup.winfo_height()
    x = (popup.winfo_screenwidth() // 2) - (width // 2)
    y = (popup.winfo_screenheight() // 2) - (height // 2)
    popup.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    popup.grid_columnconfigure(0, weight=1)
    popup.grid_rowconfigure(0, weight=1)
    popup.label = tk.Label(popup, text='Made by LuigiTrevisan 😉', font=('Arial', 14), bg='#ffffff')
    popup.label.pack(pady=10)
    popup.button = tk.Button(popup, text='Close', font=('Arial', 14), command=(lambda: [popup.destroy(), App().run()]))
    popup.button.pack(pady=10)
    popup.button = tk.Button(popup, text='Github', font=('Arial', 14), command=lambda: webbrowser.open('https://github.com/LuigiTrevisan'))
    popup.button.pack(pady=10)
    popup.mainloop()
def main():
    popup()

main()

# now we want to convert this script into a executable file
# we can do this with pyinstaller
# pyinstaller --onefile --windowed ui.py
# to set the icon:
# pyinstaller --onefile --windowed --icon=icon.ico ui.py