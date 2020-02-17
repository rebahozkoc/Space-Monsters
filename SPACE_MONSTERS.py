import turtle
import math
import random
import platform
import os
# Determine platform type

plt_list = ["Linux", "Windows", "Darwin"]
plt = platform.system()
if plt == "Windows":
    import winsound


# Set up the screen
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Space Monsters")
wn.bgpic("space_monsters_background.gif")

# Register the shapes
turtle.register_shape("monster.gif")
turtle.register_shape("player.gif")

highest = open("highscore.txt", "r")
last_score = highest.readline()
highest.close()
# Draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300, -300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()

# Set the score to 0
score = 0

# Draw the score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 300)
scorestring = "Score: %s" % score
score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))

# Credits and gameover pen
gameover_pen = turtle.Turtle()
gameover_pen.speed(0)
gameover_pen.color("orange")
gameover_pen.penup()
gameover_pen.setposition(75, -320)
creditstring = "Developed by Rebahozkoc"
gameover_pen.write(creditstring, False, align="left", font=("Arial", 10, "bold"))
gameover_pen.hideturtle()


# Create the player turtle
player = turtle.Turtle()
player.color("blue")
player.shape("player.gif")
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)
playerspeed = 15


# Create the player's bullet
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()
bulletspeed = 20

# Define bullet state
# ready - ready to fire
# fire - bullet is firing
bulletstate = "ready"


# Create enemy


number_of_enemies = 5
enemies = []
for i in range(number_of_enemies):
    enemies.append(turtle.Turtle())

for enemy in enemies:
    enemy.color("red")
    enemy.shape("monster.gif")
    enemy.penup()
    enemy.speed(0)
    x = random.randint(-200, 200)
    y = random.randint(100, 250)
    enemy.setposition(x, y)

enemyspeed = 2
# Move the player the left and right


def move_left():
    x_c = player.xcor()
    x_c = x_c - playerspeed
    if x_c < -285:
        x_c = -285
    player.setx(x_c)


def move_right():
    x_c = player.xcor()
    x_c = x_c + playerspeed
    if x_c > +285:
        x_c = +285
    player.setx(x_c)


# Declare bulletstate as a global if it needs changed
def fire_bullet():
    global bulletstate
    # Move the bullet to just above the player
    if bulletstate == "ready":
        bulletstate = "fire"
        x_c = player.xcor()
        y_c = player.ycor() + 10
        bullet.setposition(x_c, y_c)
        bullet.showturtle()
        if plt == plt_list[0]:
            os.system("aplay laser.wav&")
        if plt == plt_list[1]:
            winsound.PlaySound("laser.wav", winsound.SND_ASYNC)
        if plt == plt_list[2]:
            os.system("aflay laser.wav&")


def isCollision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(), 2)+math.pow(t1.ycor()-t2.ycor(), 2))
    if distance < 15:
        return True
    else:
        return False


wn.onkey(lambda: move_left(), "Left")
wn.onkey(lambda: move_right(), "Right")
wn.onkey(lambda: fire_bullet(), "space")

wn.listen()

endcheck = 1
bordercheck = 0
speedchanger1 = 1
speedchanger2 = 1
# main game loop
while endcheck:

    if score == 3000 and speedchanger1:
        enemyspeed = 3
        speedchanger1 = 0
    if score == 6000 and not speedchanger1:
        enemyspeed = 4
        speedchanger1 = 1
    if score == 20000 and speedchanger2:
        enemyspeed = 5
        speedchanger2 = 0
    if score == 25000 and not speedchanger2:
        enemyspeed = 7
        speedchanger2 = 1
    for enemy in enemies:
        x = enemy.xcor()
        x += enemyspeed
        enemy.setx(x)
        if enemy.xcor() > 285:
            enemyspeed *= -1
            for i in enemies:
                y = i.ycor()
                y -= 40
                i.sety(y)
        if enemy.xcor() < -285:
            enemyspeed *= -1
            for j in enemies:
                y = j.ycor()
                y -= 40
                j.sety(y)
        if enemy.ycor() < -270:
            bordercheck = 1

        # Move the enemy back and down
        # Check for collision between the bullet and the enemy.
        if isCollision(bullet, enemy):
            bullet.hideturtle()
            bulletstate = "ready"
            bullet.setposition(0, -400)
            x = random.randint(-200, 200)
            y = random.randint(200, 250)
            enemy.setposition(x, y)
            if plt == plt_list[0]:
                os.system("aplay explosion.wav&")
            if plt == plt_list[1]:
                winsound.PlaySound("explosion.wav", winsound.SND_ASYNC)
            if plt == plt_list[2]:
                os.system("aflay explosion.wav&")
            # Update the score
            score += 1000
            scorestring = "Score: %s" % score
            score_pen.clear()
            score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))

        if isCollision(enemy, player) or bordercheck:
            if plt == plt_list[0]:
                os.system("aplay game_over.wav")
            if plt == plt_list[1]:
                winsound.PlaySound("gameover.wav", winsound.SND_ASYNC)
            if plt == plt_list[2]:
                os.system("aflay game_over.wav")

            if score > int(last_score):
                new_score = open("highscore.txt", "w")
                new_score.write(str(score))
                new_score.close()
            player.hideturtle()
            bullet.hideturtle()
            for k in enemies:
                k.hideturtle()
            score_pen.clear()
            score_pen.penup()
            gameover_pen.clear()
            gameover_pen.penup()
            gameover_pen.setposition(0, 0)
            creditstring = "       GAME OVER\n Your Score:%s\n Last High Score:%s" % (score, last_score)
            gameover_pen.write(creditstring, False, align="center", font=("Arial", 30, "bold"))
            gameover_pen.hideturtle()
            endcheck = 0
            break

    # Move the bullet
    if bulletstate == "fire":
        by = bullet.ycor()
        by += bulletspeed
        bullet.sety(by)
    # Check to see if the bullet has gone to the top
        if bullet.ycor() > 285:
            bullet.hideturtle()
            bulletstate = "ready"


wn.mainloop()
