import turtle
import time
import random
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Function to play sound
def play_sound(sound_file):
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()

# Function to handle file operations
def handle_file(name):
    try:
        with open(name, 'r') as file:
            high_score = int(file.read())
    except FileNotFoundError:
        high_score = 0
        with open(name, 'w') as file:
            file.write('0')
    return high_score

# Function to create food
def create_food():
    food = turtle.Turtle()
    colors = random.choice(['red', 'green', 'black'])
    shapes = random.choice(['square', 'triangle', 'circle'])
    food.speed(0)
    food.shape(shapes)
    food.color(colors)
    food.penup()
    food.goto(0, 100)
    return food

# Function to update the high score
def update_high_score(name, score):
    with open(name, 'w') as file:
        file.write(str(score))

# Function to start the game
def start_game(name):
    # Initialize screen
    wn = turtle.Screen()
    wn.title("Snake Game")
    wn.bgcolor("blue")
    wn.setup(width=600, height=600)
    wn.tracer(0)

    # Initialize head of the snake
    head = turtle.Turtle()
    head.shape("square")
    head.color("green")
    head.penup()
    head.goto(0, 0)
    head.direction = "Stop"

    # Initialize score and high score
    high_score = handle_file(name)
    score = 0

    # Initialize food
    food = create_food()

    # Initialize pen for score display
    pen = turtle.Turtle()
    pen.speed(0)
    pen.shape("square")
    pen.color("white")
    pen.penup()
    pen.hideturtle()
    pen.goto(0, 250)
    pen.write(f"Score: 0  High Score: {high_score}", align="center", font=("comic sans", 24, "bold"))

    # Functions for changing direction
    def go_up():
        if head.direction != "down":
            head.direction = "up"

    def go_down():
        if head.direction != "up":
            head.direction = "down"

    def go_left():
        if head.direction != "right":
            head.direction = "left"

    def go_right():
        if head.direction != "left":
            head.direction = "right"

    # Keyboard bindings
    wn.listen()
    wn.onkeypress(go_up, "w")
    wn.onkeypress(go_down, "s")
    wn.onkeypress(go_left, "a")
    wn.onkeypress(go_right, "d")
    wn.onkeypress(wn.bye, "q")  

    # Initialize segments for snake body
    segments = []

    # Main Gameplay Loop
    delay = 0.1
    while True:
        wn.update()

        # Check for collision with the screen edges
        if (
            head.xcor() > 290
            or head.xcor() < -290
            or head.ycor() > 290
            or head.ycor() < -290
        ):
            time.sleep(1)
            head.goto(0, 0)
            head.direction = "Stop"

            # Reset segments
            for segment in segments:
                segment.goto(1000, 1000)
            segments.clear()

            # Reset score and update high score
            score = 0
            delay = 0.1
            pen.clear()
            pen.write(
                "Score: {}  High Score: {} ".format(score, high_score),
                align="center",
                font=("comic sans", 24, "bold"),
            )

        # Check for collision with food
        if head.distance(food) < 20:
            play_sound("short-success-sound-glockenspiel-treasure-video-game-6346.mp3")
            x = random.randint(-270, 270)
            y = random.randint(-270, 270)
            food.goto(x, y)
            if diff=='e':
                delay -= 0.00001
            elif diff=='m':
                delay -= 0.0001
            elif diff=='h':
                delay -= 0.001
            elif diff=='i':
                delay -= 0.01

            # Add a segment to the snake
            new_segment = turtle.Turtle()
            new_segment.speed(0)
            new_segment.shape("circle")
            new_segment.color("orange")
            new_segment.penup()
            segments.append(new_segment)

            # Increase score and update high score
            score += 10
            if score > high_score:
                high_score = score
                update_high_score(name, high_score)

            # Update score display
            pen.clear()
            pen.write(
                "Score: {}  High Score: {} ".format(score, high_score),
                align="center",
                font=("comic sans", 24, "bold"),
            )

        # Move the snake's body
        for index in range(len(segments) - 1, 0, -1):
            x = segments[index - 1].xcor()
            y = segments[index - 1].ycor()
            segments[index].goto(x, y)

        if len(segments) > 0:
            x = head.xcor()
            y = head.ycor()
            segments[0].goto(x, y)

        # Move the head
        if head.direction == "up":
            y = head.ycor()
            head.sety(y + 20)
        if head.direction == "down":
            y = head.ycor()
            head.sety(y - 20)
        if head.direction == "left":
            x = head.xcor()
            head.setx(x - 20)
        if head.direction == "right":
            x = head.xcor()
            head.setx(x + 20)

        # Check for collision with the snake's body
        for segment in segments:
            if segment.distance(head) < 20:
                play_sound("mixkit-unlock-game-notification-253.wav")
                time.sleep(1)
                head.goto(0, 0)
                head.direction = "Stop"

                # Reset segments
                for segment in segments:
                    segment.goto(1000, 1000)
                segments.clear()

                # Reset score and update high score
                score = 0
                delay = 0.1
                pen.clear()
                pen.write(
                    "Score: {}  High Score: {} ".format(score, high_score),
                    align="center",
                    font=("comic sans", 24, "bold"),
                )

        # Update the game speed
        time.sleep(delay)

# Get the player's name
diff = input("Enter diffiulty leve (Easy:e, Med:m, hard:h, insane:i) : ")
if diff != 'e' and diff != 'm' and diff != 'h' and diff != 'i':
    print("Invalid input")
    diff = 'm'
    print("Difficulty set to medium by default...")
name = input("Enter your name: ")

# Start the game after getting the player's name
start_game(name)
