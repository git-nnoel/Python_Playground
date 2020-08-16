import tkinter, configparser, random, os, tkinter.messagebox, tkinter.simpledialog

window = tkinter.Tk()
window.title("Minesweeper")

rows = 10
cols = 10

field = []
buttons = []

colors = ['#FFFFFF', '#0000FF', '#008200', '#FF0000', '#000084', '#840000', '#008284', '#840084', '#000000']
default_backgroundcolor = 0

gameover = False
customsizes = []

def createMenu():
    menubar = tkinter.Menu(window)
    menusize = tkinter.Menu(window, tearoff=0)
    menusize.add_separator()
    menubar.add_command(label="restart", command=restartGame)
    menubar.add_command(label="exit", command=lambda: window.destroy())
    window.config(menu=menubar)

def restartGame():
    global gameover
    gameover = False
    setGame()
    prepareWindow()


def RightClick(x,y):
    global field, buttons, colors, gameover, rows, cols
    if gameover:
        return
    if buttons[x][y]['state']=='disabled':
        return
    if buttons[x][y]["text"] == "!":
        buttons[x][y]["text"] = " "
        buttons[x][y].config(background=default_backgroundcolor)
    else:
        if buttons[x][y]["text"] == " ":
            buttons[x][y]["text"] = "!"
            buttons[x][y].config(background='gray')

def Click(x,y):
    global field, buttons, colors, gameover, rows, cols
    if gameover:
        return
    if buttons[x][y]['state']=='disabled':
        return
    if buttons[x][y]["text"]=="!":
        RightClick(x,y)
    buttons[x][y]["text"] = str(field[x][y])
    if field[x][y] == -1:
        buttons[x][y]["text"] = "*"
        buttons[x][y].config(background='red', disabledforeground='black')
        gameover = True
        for j in range(0,cols):
            for i in range(0, rows):
                if field[i][j] == -1:
                    buttons[i][j]["text"] = "*"
        tkinter.messagebox.showinfo("Game Over", "You Lost.")
    else:
        buttons[x][y].config(disabledforeground=colors[field[x][y]])
    buttons[x][y]['state'] = 'disabled'
    buttons[x][y].config(relief=tkinter.SUNKEN)
    if field[x][y] == 0:
        for i in range(-1 ,2):
            for j in range(-1, 2):
                if i==0 and j==0:
                    continue
                elif x == 0 and j == -1:
                    continue
                elif y == 0 and i == -1:
                    continue
                else:
                    if x+j != rows + 1 and y+i != cols + 1:
                        try:
                            Click(x+j,y+i)
                        except IndexError:
                            pass
    win = True
    for i in range(0, rows):
        for j in range(0, cols):
            if buttons[i][j]['state']!='disabled' and field[i][j] != -1:
                win = False
    if win:
        for j in range(0,cols):
            for i in range(0, rows):
                if field[i][j] == -1:
                    buttons[i][j]["text"] = "*"
        tkinter.messagebox.showinfo("Game Over", "YOU WON!")

def setGame():
    global rows, cols, field
    field = []
    for x in range(0, rows):
        field.append([])
        for y in range(0, cols):
            #inicialização dos valores para field[col][linha]
            field[x].append(0)
    for x in range(0, (int((rows*cols)*0.15 + 1))):
        x = random.randint(0, rows-1)
        y = random.randint(0, cols-1)
        while field[x][y] == -1:
            x = random.randint(0, rows-1)
            y = random.randint(0, cols-1)
        field[x][y] = -1
        updateAdjacents(x, y, field)

def updateAdjacents(x, y, field):
    for a in range(-1, 2):
        for b in range(-1, 2):
            if x+a != -1 and x+a != rows + 1:
                if y+b != -1 and y+b != cols + 1:
                    try:
                        if field[x+a][y+b] != -1:
                            field[x+a][y+b] = int(field[x+a][y+b]) + 1
                    except IndexError:
                        pass

def prepareWindow():
    global rows, cols, buttons, default_backgroundcolor
    buttons = []
    for x in range(0, rows):
        buttons.append([])
        for y in range(0, cols):
            button = tkinter.Button(window, text=" ", width=2, command=lambda x=x,y=y: Click(x,y))
            button.bind("<Button-3>", lambda e, x=x, y=y:RightClick(x, y))
            button.grid(row=x+1, column=y, sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
            buttons[x].append(button)
            default_backgroundcolor = button.cget("background")


createMenu()

prepareWindow()
setGame()

window.mainloop()
