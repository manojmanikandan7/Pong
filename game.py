from tkinter import Canvas, NW, Button, Label, messagebox
import random
import time
from PIL import ImageTk, Image
"""
The main game file.
Author: Manoj Manikandan
Student ID: 11409534
"""
"""
Boss Image source - Unsplash: https://unsplash.com/photos/magic-keyboard-beside-mug-and-click-pen-VieM9BdZKFo
Used under the Unsplash License: https://unsplash.com/license

"""

#Global variables declaration for use in the game.
paused=False
speed=5
#Class Paddle to define the functions and characteristics of the paddle.
class Paddle:
    def __init__(self, canvas, score, left_key, right_key, paddlesize):
        global speed
        speed=5+int(score/7)
        self.canvas = canvas
        self.id = canvas.create_rectangle(0,0, paddlesize, 10, fill="gray")
        self.canvas.move(self.id, 935, 880) #Initially placing the paddle in the mid-lower of the screen.
        self.speed_x = 0
        #Binding keys for the controls, selected by the user or using default configuration.
        self.canvas.bind_all(f'<KeyPress-{left_key}>', self.left) 
        self.canvas.bind_all(f'<KeyPress-{right_key}>', self.right)

    #A method to move the ball, according to its speed.
    def drawpaddle(self):
        self.canvas.move(self.id, self.speed_x, 0)
        position = self.canvas.coords(self.id)
        #Defining the bounds for the movement of the paddle.
        if position[0] <= 0:
            self.speed_x = 0
        if position[2] >= 1920:
            self.speed_x = 0
    
    #Defining the movement of the paddle to the left or right when the key is pressed.
    def left(self, event):
        global speed
        self.speed_x = -speed
    def right(self, event):
        global speed
        self.speed_x = speed

class Ball:
    def __init__(self, canvas, paddle, score, multiplier, slowball):
        global speed
        speed=5+int(score/7)
        self.ballspeed=speed-slowball #Creating a separate, class variable so that the "slowball" cheat does not effect the paddle speed.
        self.canvas = canvas
        self.paddle = paddle
        self.id = canvas.create_oval(10, 10, 30, 30, fill="white")
        self.canvas.move(self.id, 950, 100)
        self.speed_x = random.randrange(-speed,speed)   
        self.speed_y = -1
        self.hit_bottom = False
        self.score = score
        self.multiplier=multiplier
    
    #A method to move the ball, according to its speed.
    def drawball(self):
        global speed
        self.canvas.move(self.id, self.speed_x, self.speed_y)
        position = self.canvas.coords(self.id)
        if position[1] <= 0:
            self.speed_y = self.ballspeed
        if position[3] >= 1080:
            self.hit_bottom = True
        if position[0] <= 0:
            self.speed_x = self.ballspeed
        if position[2] >= 1920:
            self.speed_x = -self.ballspeed
        if self.hit_paddle(position):
            self.speed_y = -self.ballspeed
            self.speed_x = random.randrange(-self.ballspeed, self.ballspeed)
            self.score += self.multiplier*1
            if self.score%7==0:
                speed=speed+1
                self.ballspeed=self.ballspeed+1
            
    #A method to check for collision between the ball and the paddle.
    def hit_paddle(self, position):
        paddle_positions = self.canvas.coords(self.paddle.id)
        if position[2] >= paddle_positions[0] and position[0] <= paddle_positions[2] and position[3] >= paddle_positions[1] and position[3] <= paddle_positions[3]:
                return True
        return False
    
    

def game(window, init_score, left, right, paddlesize, multiplier, slowball):
    
    #A method to pause the game, either with the use of the pause button or the keyboard shortcut, Control-p.
    def pause_game(*event):
        global paused
        if not paused:
            pauseButton.configure(text="|>", command=pause_game)
            c.itemconfig(Pause, text="\tPaused \nGrab a cup of tea or coffee!")
            paused=True
        else:
            c.after(1000, c.itemconfig(Pause, text="Resuming"))
            window.update()
            time.sleep(1)
            c.itemconfig(Pause, text="")
            c.after(1000, pauseButton.configure(text="||", command=pause_game))
            paused=False


    #A function to flip to an image when the "Control-b" key is pressed (Boss Button)
    def BossButton(event):
        window.title("A Perfectly Normal Desktop")
        def resurrect(event):
            boss_label.destroy()
            window.title("Pong - Game")
            pause_game()
            window.bind("<Control-b>", BossButton)
        pause_game()
        boss_image = ImageTk.PhotoImage(Image.open("boss.jpg"))
        boss_label = Label(window, image=boss_image)
        boss_label.place(x=0, y=0)
        window.bind("<Control-b>", resurrect)
        global paused
        while paused:
            boss_label.update()
    
    
    # Creating the window and the canvas for the game
    window.title("Pong - Game")
    c = Canvas(window, width=1920, height=1080, bd=0, bg='black')
    c.pack()

    #The text that are displayed in the game screen.
    points = c.create_text(960, 20, anchor="n", text=f"POINTS: {init_score}", font=("Futura",25))
    levels = c.create_text(75, 20, anchor="n", text=f"LEVEL: {int(init_score/5)+1}", font=("Futura",25))
    
    c.create_line(0, 879, 1920, 879, dash=(6,2), fill="white") 
    c.create_line(0, 891, 1920, 891, dash=(6,2), fill="white") 
    
    pauseButton=Button(c, height=2, width=2, text="||", font=("Courier New", 15, "bold"), background="white", foreground="black", command=pause_game, justify='center', border=2)
    Pause=c.create_text(960, 150, anchor="n", text="", font=("Futura",35))
    pauseButton.place(x=1100, y=10)
    
    window.update()
    
    #Creating a paddle and a ball object for the game
    paddle = Paddle(c, init_score, left, right, paddlesize)
    ball = Ball(c, paddle, init_score, multiplier, slowball)

    #Embedding the keyboard shortcuts for the Boss button and the pause button.
    window.bind("<Control-b>", BossButton)
    window.bind("<Control-p>", pause_game)
    
    #A method to confirm to save the score, if the player decides to quit mid-game.
    def confirmclose():
        ball.hit_bottom=True
    window.protocol("WM_DELETE_WINDOW", confirmclose)

    #A loop to update the position of the ball and the paddle until the ball hits the bottom of the screen.
    while not ball.hit_bottom:
        if not paused:
            ball.drawball()
            paddle.drawpaddle()
            c.itemconfig(points, text=f"POINTS: {ball.score}")
            c.itemconfig(levels, text=f"LEVEL: {int(ball.score/7)+1}")
        window.after(10, window.update())

    #The commands to present the GAME OVER screen and later, prompting the user to save their progress.
    pauseButton.destroy()
    c.itemconfig(points, text="")
    c.create_text(960,440,text="GAME OVER",font=("Papyrus",40))
    c.create_text(960,540,text="POINTS SCORED: "+str(ball.score),font=("Papyrus",30))
    window.update()
    time.sleep(3)
    save=messagebox.askyesno(title="Save Game", message=f"Do you want to save your score of {ball.score}? If not, the score of {init_score} will be saved.")
    if not save:
        ball.score=init_score
    c.after(10, window.destroy)
    return ball.score
