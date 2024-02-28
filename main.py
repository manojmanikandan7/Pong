from tkinter import Tk, Label, Text, END, Toplevel, Frame, N, NSEW, Text, StringVar, messagebox
from game import *  #A seperate file containing the game

"""Recommended Screen Resolution: 1920x1080"""
"""
The homepage for the game. 
Author: Manoj Manikandan
Student ID: 11409534
"""


Leaderboard={} #The Leaderboard dictionary to load the score of each user

#Global variables to be used in the home page.
left="Left"
right="Right"
paddlesize=100
multiplier=1
slowball=0

#Method to load the home page frame
def start_frame(frame, window, paddlesize, multiplier, slowball):

    #To load the players' info to the Leaderboard dictionary from the .txt file
    def load_Leaderboard(event):
        global Leaderboard
        #Exception handling in the case of unavailablity of save file.
        try:
            with open("Leaderboard.txt","r") as file:
                lines=file.readlines()
            for line in lines:
                name, score=line.rsplit(", ")
                Leaderboard[name.strip()]=int(score)
        except:
            Leaderboard={}
        finally:
            messagebox.showinfo(title="Scores Load", message="Player information loaded successfully!")

    #To re-display the home page after displaying another page
    def start_screen(cframe):
            cframe.destroy() #Closing the current frame
            frame=Frame(window, width=1920, height=1080, background="black")
            global paddlesize, multiplier, slowball
            start_frame(frame, window, paddlesize, multiplier, slowball)
    
    #To change the keybindings for the controls
    def keybindings(event):
        
        def check_left(event):
            global left
            left_label.configure(text=f"Paddle Left ({event.keysym})")
            left=event.keysym
        def check_right(event):
            global right
            right_label.configure(text=f"Paddle Right ({event.keysym})")
            right=event.keysym
        def reset():
            global left, right
            left="Left"
            right="Right"
            left_label.configure(text=f"Paddle Left (Default: Left)")
            right_label.configure(text=f"Paddle Right (Default: Right)")
        frame.destroy()
        #Creating the elements for the Frame
        kb_frame=Frame(window, width=1080, height=1080, background="black")
        kb_frame.pack(pady=200)
        name_label=Label(kb_frame,text="KEYBINDINGS", font=("Courier New", 75, "bold"),foreground="white", background="black")
        name_label.grid(row=0, sticky=NSEW, columnspan=10, pady=40)
        type_label=Label(kb_frame,text="Enter your keybindings", font=("Courier New", 45),foreground="white", background="black")
        type_label.grid(row=1, sticky=NSEW, columnspan=10, pady=40)

        left_label=Label(kb_frame,text="Paddle Left (Default: Left)", font=("Courier New", 35),foreground="white", background="black")
        left_label.grid(row=2, column=0, sticky=NW, columnspan=25)
        
        left_entry=Text(kb_frame, width=10, height=1, background="white", borderwidth=1, foreground="black", font=("Courier New", 30) )
        left_entry.grid(row=2, column=1, columnspan=10, sticky=NSEW)
        left=StringVar()

        left_entry.bind("<KeyPress>", check_left)

        right_label=Label(kb_frame,text="Paddle Right (Default: Right)", font=("Courier New", 35),foreground="white", background="black")
        right_label.grid(row=3, column=0, sticky=NW, columnspan=25)

        right_entry=Text(kb_frame, width=10, height=1, background="white", borderwidth=1, foreground="black", font=("Courier New", 30), )
        right_entry.grid(row=3, column=1, columnspan=10, sticky=NSEW)
        right=StringVar()

        right_entry.bind("<KeyPress>", check_right)

        backbutton=Button(kb_frame, text="Back", width=30, height=1,background="white", command=lambda:start_screen(kb_frame), font=("Courier New", 30))
        backbutton.grid(row=4, column=0, sticky=NSEW, pady=30)
        resetbutton=Button(kb_frame, text="Reset to Default", width=30, height=1,background="white", command=reset, font=("Courier New", 30))
        resetbutton.grid(row=4, column=1, sticky=NSEW, pady=30)
        
    #To display the Leaderboard in a seperate frame
    def display_Leaderboard(event):
        def backhp(event):
            start_screen(lb_frame)

        frame.destroy() #Closing the homepage frame
        lb_frame=Frame(window, width=960, height=540, background="black")
        lb_frame.pack()
        pong_label=Label(lb_frame, text="PONG", font=("Papyrus", 100), background="black", foreground="teal")
        pong_label.pack(pady=50)
        Title=Label(lb_frame, text="LEADERBOARD", font=("Courier New", 40), foreground='white', background="black")
        Title.pack(padx=40, pady=40)
        header=Label(lb_frame, text=" POSITION \t\t NAME \t\t\t SCORE ", font=("Courier New", 30), foreground='white', background="black")
        header.pack(padx=40, anchor=N)
        seperator=Label(lb_frame, text=" -------- \t\t ---- \t\t\t ----- ", font=("Courier New", 30), foreground='white', background="black")
        seperator.pack(padx=20, anchor=N)
        back=Label(lb_frame, text="Back to Home Page", font=("Courier New", 25), foreground="gray", background="black")

        for i, name in enumerate(dict(sorted(Leaderboard.items(), key=lambda x:x[1], reverse=True))): #Sorting the 'Leaderboard' dictionary by the players' scores
            label=Label(lb_frame, text=f"  {i+1} \t\t\t  {name} \t\t\t\t{Leaderboard[name]:02}", font=("Courier New",25), foreground='white', background="black")
            label.pack(padx=30, pady=10, anchor=N)
            if i==9:
                break
        back.pack(padx=40, pady=40,anchor=N)
        back.bind("<Button-1>", backhp)
    
    #To start a new game or reset an existing score for a player
    def new_game(*event):
        #To extract the name of the player
        def get_name(): 
            name=name_entry.get("1.0", END).strip()
            if Leaderboard.get(name, 0)==0:
                Leaderboard[name]=0
                start_screen(us_frame) 
                y=start_game(Leaderboard[name]) #Starting the game 
                scorewrite(name, y) #Passing in the name and the final score of the player to write to the save file
                
                
            else:
                rewrite=messagebox.askyesno(title="Confirmation", message=f"Do you want to reset the score of {name} back to '0'? \nIf No, you shall proceed with the existing score of: {Leaderboard[name]}")
                if rewrite:
                    Leaderboard[name]=0
                    start_screen(us_frame)
                    y=start_game(Leaderboard[name]) #Starting the game 
                    scorewrite(name, y) #Passing in the name and the final score of the player to write to the save file
                    
                else:
                    new_game()

        #To check if the "Enter" key is pressed in the text box.
        def check(event):
            if event.keysym=="Return":
                get_name()
        
        frame.destroy()

        #Creating the elements for the Frame
        us_frame=Frame(window, width=1080, height=1080, background="black")
        us_frame.pack(pady=200)
        name_label=Label(us_frame,text="NEW GAME", font=("Courier New", 75, "bold"),foreground="white", background="black")
        name_label.grid(row=0, sticky=NSEW, columnspan=10, pady=40)
        type_label=Label(us_frame,text="Enter your name", font=("Courier New", 45),foreground="white", background="black")
        type_label.grid(row=1, sticky=NSEW, columnspan=10, pady=40)
        name_entry=Text(us_frame, width=40, height=1, background="white", borderwidth=1, foreground="black", font=("Courier New", 30), )
        name_entry.grid(row=2, columnspan=20, sticky=NSEW)
        name_entry.bind_all("<KeyPress>", check)
        name=StringVar()
        backbutton=Button(us_frame, text="Back", width=20, height=1,background="white", command=lambda:start_screen(us_frame), font=("Courier New", 30))
        backbutton.grid(row=3, column=0, sticky=NSEW, pady=30)
        nextbutton=Button(us_frame, text="Next", width=20, height=1,background="white", command=get_name, font=("Courier New", 30))
        nextbutton.grid(row=3, column=1, sticky=NSEW, pady=30)

    #To continue where the player left of
    def continue_game(*event):
        def get_name():
            name=name_entry.get("1.0", END).strip()
            if Leaderboard.get(name, 0)==0:
                Leaderboard[name]=0
                
            continue_as=messagebox.askyesno(title="Confirmation", message=f"Do you want to continue as {name}? \nIf Yes, you shall proceed with the existing score of: {Leaderboard[name]}")
            if continue_as:
                start_screen(cg_frame)
                y=start_game(Leaderboard[name]) #Starting the game 
                scorewrite(name, y) #Passing in the name and the final score of the player to write to the save file
                
            else:
                continue_game()
        
        #To check if the "Enter" key is pressed in the text box.
        def check(event):
            if event.keysym=="Return":
                get_name()

        frame.destroy()
        #Creating the elements for the Frame
        cg_frame=Frame(window, width=1080, height=1080, background="black")
        cg_frame.pack(pady=200)
        name_label=Label(cg_frame,text="CONTINUE GAME", font=("Courier New", 75, "bold"),foreground="white", background="black")
        name_label.grid(row=0, sticky=NSEW, columnspan=10, pady=40)
        type_label=Label(cg_frame,text="Enter your name", font=("Courier New", 45),foreground="white", background="black")
        type_label.grid(row=1, sticky=NSEW, columnspan=10, pady=40)
        name_entry=Text(cg_frame, width=40, height=1, background="white", borderwidth=1, foreground="black", font=("Courier New", 30), )
        name_entry.grid(row=2, columnspan=20, sticky=NSEW)
        name_entry.bind_all("<KeyPress>", check)
        name=StringVar()
        backbutton=Button(cg_frame, text="Back", width=20, height=1,background="white", command=lambda:start_screen(cg_frame), font=("Courier New", 30))
        backbutton.grid(row=3, column=0, sticky=NSEW, pady=30)
        nextbutton=Button(cg_frame, text="Next", width=20, height=1,background="white", command=get_name, font=("Courier New", 30))
        nextbutton.grid(row=3, column=1, sticky=NSEW, pady=30)

    #The method to start a game of PONG
    def start_game(init_score):  
        game_window=Toplevel(window)
        game_window.geometry("1920x1080")
        global paddlesize, multiplier, slowball
        return game(game_window, init_score, left, right, paddlesize, multiplier, slowball)

    #To save the final score to the .txt file for future games
    def scorewrite(name, y):
        Leaderboard[name]=y
        with open("Leaderboard.txt", 'w') as file:
            for player in Leaderboard:
                file.write(f"{player}, {Leaderboard[player]}\n")

    frame.pack() #Packing the frame to the window
    
    #Labels for the home page menu
    pong_label=Label(frame, text="PONG", font=("Papyrus", 100), background="black", foreground="teal")
    label1=Label(frame, text="Start a new game", font=("Futura", 25), background="black", foreground="white")
    label2=Label(frame, text="Continue game", font=("Futura", 25), background="black", foreground="white")
    label3=Label(frame, text="View Leaderboard", font=("Futura", 25), background="black", foreground="white")
    label4=Label(frame, text="Load Scores", font=("Futura", 25), background="black", foreground="white")
    label5=Label(frame, text="KeyBindings", font=("Futura", 25), background="black", foreground="white")
    
    #Packing the different labels to the frame
    pong_label.pack(pady=75)
    label1.pack(pady=50)
    label2.pack(pady=50)
    label3.pack(pady=50)
    label4.pack(pady=50)
    label5.pack(pady=50)

    #Binding for the Labels to perform different functions
    label1.bind("<Button-1>", new_game)
    label2.bind("<Button-1>", continue_game)
    label3.bind("<Button-1>", display_Leaderboard)
    label4.bind("<Button-1>", load_Leaderboard)
    label5.bind("<Button-1>", keybindings)


    #Adding Hover effects to the labels/buttons
    label1.bind("<Enter>",lambda event: label1.config(foreground = "lightgreen"))
    label1.bind("<Leave>",lambda event: label1.config(foreground = "white"))


    label2.bind("<Enter>",lambda event: label2.config(foreground = "lightblue"))
    label2.bind("<Leave>",lambda event: label2.config(foreground = "white"))



    label3.bind("<Enter>",lambda event: label3.config(foreground = "lightyellow"))
    label3.bind("<Leave>",lambda event: label3.config(foreground = "white"))


    label4.bind("<Enter>",lambda event: label4.config(foreground = "salmon"))
    label4.bind("<Leave>",lambda event: label4.config(foreground = "white"))

    label5.bind("<Enter>",lambda event: label5.config(foreground = "gray"))
    label5.bind("<Leave>",lambda event: label5.config(foreground = "white"))    

#Cheat Codes!
#Cheat 1: Doubles the length of the player's paddle.
def cheatcode1(event):
    messagebox.showinfo(title="Cheat Code Unlock", message="Congratulations! \nYou unlocked a cheat! \nCheat Unlocked: Enlarge Paddle")
    global paddlesize
    paddlesize=200

#Cheat 2: Activates the point multiplier.
def cheatcode2(event):
    messagebox.showinfo(title="Cheat Code Unlock", message="Congratulations! \nYou unlocked a cheat! \nCheat Unlocked: Points Multiplier(x2)")
    global multiplier
    multiplier=2

#Cheat 3: Slows down the ball in the game.
def cheatcode3(event):
    messagebox.showinfo(title="Cheat Code Unlock", message="Congratulations! \nYou unlocked a cheat! \nCheat Unlocked: Slower Ball")
    global slowball
    slowball=1

#Creation of the main window and calling the start_frame method to create the home page frame
def main():
    window=Tk()
    window.geometry("1920x1080")
    window.configure(background="black")
    window.title("Pong - Welcome Page")

    #Implementing the keybindings for the cheats (A.K.A. the "cheat codes")
    window.bind("bigboy", cheatcode1)
    window.bind("<Control-Shift-M>", cheatcode2)
    window.bind("slowpoke", cheatcode3)

    frame=Frame(window, width=1920, height=1080, background="black")
    start_frame(frame=frame, window=window, paddlesize=paddlesize, multiplier=multiplier, slowball=slowball)
    window.mainloop()



if __name__=="__main__":
    main()