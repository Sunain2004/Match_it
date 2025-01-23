import tkinter as tk
from tkinter import *
import random
from tkinter import messagebox
from tkinter.simpledialog import askstring
import time


def startgame(root):
    global grid_size
    playbutton.destroy()  
    create_grid(root,grid_size)

def new_game():
    global grid_size,count_dict
    root.destroy()
    grid_size = 4
    count_dict['moves'] = 0
    for row in grid_buttons:
        for button in row:
            button.destroy()
    create_grid(root, grid_size)


def create_grid(master, n):
    global grid_buttons,mainframe

    grid_buttons = [[None for _ in range(n)] for _ in range(n)]

    mainframe = LabelFrame(root, bg = '#990662', bd = 10)
    mainframe.pack(padx = 10, pady = 50)

    for i in range(n):
        for j in range(n):
            random_object = random.choice(objects[:n])
            btn = tk.Button(mainframe, text = random_object, width = 4, height = 2, bg = '#010117', fg = 'white', font = custom_font, bd = 10, command = lambda x = i, y = j: move_obj(x, y))
            btn.grid(row = i, column = j)
            grid_buttons[i][j] = btn
    print(grid_buttons)


def move_obj(x, y):
    global count_dict, mainframe, grid_size

    direction = askstring('Move', 'Where do you want it to move [up, down, left, right]: ').lower()

    if direction == 'up' and x - 1 >= 0:
        source_text = grid_buttons[x][y].cget('text')
        grid_buttons[x][y].config(text = grid_buttons[x-1][y].cget('text'))
        grid_buttons[x - 1][y].config(text = source_text)
    elif direction == 'down' and x + 1 <= grid_size - 1:
        source_text = grid_buttons[x][y].cget('text')
        grid_buttons[x][y].config(text = grid_buttons[x+1][y].cget('text'))
        grid_buttons[x + 1][y].config(text = source_text)
    elif direction == 'left' and y - 1 >= 0:
        source_text = grid_buttons[x][y].cget('text')
        grid_buttons[x][y].config(text = grid_buttons[x][y - 1].cget('text'))
        grid_buttons[x][y - 1].config(text = source_text)
    elif direction == 'right' and y + 1 <= grid_size - 1:
        source_text = grid_buttons[x][y].cget('text')
        grid_buttons[x][y].config(text = grid_buttons[x][y + 1].cget('text'))
        grid_buttons[x][y + 1].config(text = source_text)
    else:
        messagebox.showerror('Invalid Move', 'Invalid Move')

    movesbutton.config(text=f'moves:{1 + count_dict["moves"]}')
    scorebutton.config(text=f'Score:{count_dict["score"] - count_dict["moves"] - 1}')
    count_dict["moves"] += 1
    count_dict["score"] = count_dict['score'] - count_dict['moves']
    
    if count_dict["score"]< 0:
        messagebox.showinfo('You lose!')
        root.after(20000, reset_game)
    
    
    if checkwin():
        print(count_dict['moves'])
        messagebox.showinfo('Congratulations', f'You won!\nYou scored: {count_dict["score"]}\nYou moved {count_dict["moves"]}')
        count_dict['level'] += 1

        if count_dict['level'] >3:
                messagebox.showinfo('Game end')
                root.destroy()

        grid_size += 1
        levelbutton.config(text=f'level:{count_dict["level"]}')
        mainframe.destroy()
        root.after(20, reset_game)

def reset_game():
    global count_dict
    count_dict['moves'] = 0
    create_grid(root, grid_size)  

def checkwin():
    global grid_size, count_dict

    for i in range(grid_size):
        # Horizontal check
        if all(grid_buttons[i][j].cget('text') == grid_buttons[i][j + 1].cget('text') for j in range(grid_size - 1)):
            
            return True

        # Vertical check
        if all(grid_buttons[j][i].cget('text') == grid_buttons[j + 1][i].cget('text') for j in range(grid_size - 1)):
            
            return True

    # Diagonal check
    if all(grid_buttons[i][i].cget('text') == grid_buttons[i + 1][i + 1].cget('text') for i in range(grid_size - 1)):
        
        return True

    # Anti-Diagonal check
    if all(grid_buttons[i][grid_size - i - 1].cget('text') == grid_buttons[i + 1][grid_size - i - 2].cget('text') for i in range(grid_size - 1)):
        
        return True

    return False



# Start the GUI main loop
objects = ['A', 'B', 'C', 'D', 'E', 'F']
grid_size = 4
# moves = 0
# score = 100
# level = 1
count_dict = {'moves':0, 'score':100, 'level':1}


root = tk.Tk()
root.title("MATCH IT")
root.geometry("1440x810")

custom_font = ("Helvetica", 20, "bold")


#Define BG Image
background_image = tk.PhotoImage(file = 'Background.png', width = 1440, height = 810)
canvas = Label(root, image = background_image)
canvas.place(x = 0, y = 0, relwidth = 1, relheight = 1)

playbutton = tk.Button(root, text = "PLAY!", bg = "Black", font = custom_font, fg = "White", relief = "solid", command = lambda:startgame(root)) 
playbutton.place(relx = 0.5, rely = 0.86, anchor = "center")

exitbutton = tk.Button(root, text="EXIT", bg="Black", font=custom_font, fg ="RED", relief="solid", command=root.destroy) 
exitbutton.place(relx = 0.08, rely = 0.92, anchor = "center")


movesbutton = tk.Label(root, text=f'moves:{count_dict["moves"]}',bg="Black", font=custom_font, fg='white',border=10)  
movesbutton.place(relx = 0.92, rely = 0.1, anchor = "n")

scorebutton = tk.Label(root, text=f'Score:{count_dict["score"]}', bg="Black", font=custom_font, fg='white',border=10) 
scorebutton.place(relx = 0.08, rely = 0.1, anchor = "n")

levelbutton = tk.Label(root, text=f'Level:{count_dict["level"]}', bg="Black", font=custom_font, fg='white',border=10) 
levelbutton.place(relx = 0.92, rely = 0.87, anchor = "n")
 

root.mainloop()

 