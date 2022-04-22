# ---------------------------------------------------------------------
# Rocket Landing Simulator
# Gate Check: 1
# ---------------------------------------------------------------------
import random, math
from typing import Tuple
from pygame.constants import WINDOWHIDDEN
from pythonGraph import *

import rocket_ai_solution as rocket_ai

# CONSTANTS
WINDOW_WIDTH  = 1200
WINDOW_HEIGHT = 800

# Performance Variabless
global Max_Score, Time_Elapsed, Fuel_Consumed, Score
Max_Score = 0
Time_Elapsed = 0
Fuel_Consumed = 0
Crashes = 0
Landings = 0
Score = 0

# Simulation Variables
NUM_RUNS_PER_SCENARIO = 10
num_runs = 0

# Terrain
terrain_list = []
GROUND_HIEGHT = 100
GROUND_WIDTH = 200
WATER_HEIGHT = 300

# Rocket
global Rocket_X_Coordinate , Rocket_Y_Coordinate , Rocket_X_Velocity , Rocket_Y_Velocity
global Rocket_Height , Rocket_Width , Rocket_Boost , Rocket_Acceleration
global Rocket_Up_Thrust, Rocket_Left_Thrust, Rocket_Right_Thrust

Rocket_X_Coordinate = 0
Rocket_Y_Coordinate = 0
Rocket_X_Velocity = 0
Rocket_Y_Velocity = 0
Rocket_Height = 50
Rocket_Width = 50
Rocket_Boost = True
Rocket_Up_Thrust = 0.0
Rocket_Left_Thrust = 0.0
Rocket_Right_Thrust = 0.0
Rocket_Acceleration = 0.5
GRAVITY = 0.15

# Boat (i.e., Landing Pad)
global B_X_Coordinate , B_Y_Coordinate , B_Initial_X , B_Initial_Y , B_Velocity , B_Initial_V , B_Width , B_Height
B_X_Coordinate = 0
B_Y_Coordinate = 0
B_Initial_X = 0
B_Initial_Y = 0
B_Velocity = 0
B_Initial_V = 0
B_Width = 200
B_Height = 50

# --------------------------------------------------------------
# Initializes the Launch Pad
# --------------------------------------------------------------
global Pad_X_Coordinate , Pad_Y_Coordinate , Pad_Width , Pad_Height
Pad_X_Coordinate = 0
Pad_Y_Coordinate = 0
Pad_Width = 100
Pad_Height = 100


# --------------------------------------------------------------
# Initializes the Simulation
# --------------------------------------------------------------
def initialize_simulation(generate_new_scenario):
    global Time_Elapsed, Fuel_Consumed
    Time_Elapsed = 0
    Fuel_Consumed = 0
    initialize_terrain(generate_new_scenario)
    initialize_boat(generate_new_scenario)
    initialize_rocket(generate_new_scenario)


# --------------------------------------------------------------
# Initializes the Terrain
# --------------------------------------------------------------
def initialize_terrain(generate_new_scenario):
    global GROUND_HIEGHT , GROUND_WIDTH , WATER_WIDTH , WATER_HEIGHT , terrain_list
    if generate_new_scenario == True:
            terrain_list = []
            GROUND_WIDTH = random.randint(100,WINDOW_WIDTH*0.2)
            GROUND_HIEGHT = random.randint(100,WINDOW_HEIGHT*0.3)
            WATER_WIDTH = WINDOW_WIDTH - GROUND_WIDTH
            WATER_HEIGHT = random.randint(50,GROUND_HIEGHT-10)
            for x in range(0, WINDOW_WIDTH):
                if x > GROUND_WIDTH:
                    terrain_list.append(WATER_HEIGHT)
                else:
                    terrain_list.append(GROUND_HIEGHT)


# --------------------------------------------------------------
# Initializes the Boat
# --------------------------------------------------------------
def initialize_boat(generate_new_scenario):
    global B_X_Coordinate , B_Y_Coordinate , B_Initial_X , B_Initial_Y , B_Velocity , B_Initial_V , B_Width , B_Height
    if(generate_new_scenario):
        B_Initial_X = random.randint(GROUND_WIDTH,WINDOW_WIDTH-B_Width)
        B_Initial_Y = WINDOW_HEIGHT - WATER_HEIGHT - B_Height
        B_Initial_V = random.randint(-10,10)
    B_X_Coordinate = B_Initial_X
    B_Y_Coordinate = B_Initial_Y
    B_Velocity = B_Initial_V

# --------------------------------------------------------------
# Initializes the Rocket
# --------------------------------------------------------------
def initialize_rocket(generate_new_scenario):
    global Rocket_X_Coordinate, Rocket_Y_Coordinate, Rocket_X_Velocity, Rocket_Y_Velocity, Rocket_Boost
    global Rocket_Height, Rocket_Width, Rocket_IX_Coordinate, Rocket_IY_Coordinate
    Rocket_X_Coordinate = (GROUND_WIDTH / 2) - (Rocket_Width / 2)
    Rocket_Y_Coordinate = WINDOW_HEIGHT - GROUND_HIEGHT - Rocket_Height - 20
    Rocket_X_Velocity = 0.0
    Rocket_Y_Velocity = 0.0
    Rocket_Boost = True
    Rocket_IX_Coordinate = Rocket_X_Coordinate
    Rocket_IY_Coordinate = Rocket_Y_Coordinate

# --------------------------------------------------------------
# Draws all of the in game objects
# --------------------------------------------------------------
def erase_objects():
    clear_window("BLACK")


# --------------------------------------------------------------
# Draws all of the in game objects
# --------------------------------------------------------------
def draw_objects():
    global Time_Elapsed
    Time_Elapsed += 1
    draw_terrain()
    draw_rocket()
    draw_hud()
    draw_boat()
    draw_pad()
  

# --------------------------------------------------------------
# Draws the Terrain
# --------------------------------------------------------------
def draw_terrain():
  for x in range(0, WINDOW_WIDTH):
        if x > GROUND_WIDTH:
            pythonGraph.draw_line(x, WINDOW_HEIGHT, x, WINDOW_HEIGHT - terrain_list[x], "light_blue")
        else:
            pythonGraph.draw_line(x, WINDOW_HEIGHT, x, WINDOW_HEIGHT - terrain_list[x], "green")

   
# --------------------------------------------------------------
# Draws the Launch Pad
# --------------------------------------------------------------
def draw_pad():
    global Pad_Width , Pad_Height , Pad_X_Coordinate , Pad_Y_Coordinate
    
    draw_image('files/launchpad.png',Rocket_IX_Coordinate-50,WINDOW_HEIGHT-GROUND_HIEGHT-Pad_Height,Pad_Width,Pad_Height)


# --------------------------------------------------------------
# Draws the Boat
# --------------------------------------------------------------
def draw_boat():
    draw_image('files/boat.png',B_X_Coordinate,B_Y_Coordinate,B_Width,B_Height)


# --------------------------------------------------------------
# Draws the Rocket (and Thrusters)
# --------------------------------------------------------------
def draw_rocket():
    global Rocket_Height, Rocket_Width, Rocket_Up_Thrust, Rocket_Left_Thrust, Rocket_Right_Thrust
    draw_image('files/rocket.png',Rocket_X_Coordinate,Rocket_Y_Coordinate,Rocket_Width,Rocket_Height)

    if Rocket_Up_Thrust > 0.0 :
        draw_ellipse((Rocket_X_Coordinate+Rocket_Width/2)-5,(Rocket_Y_Coordinate+Rocket_Height)-5,(Rocket_X_Coordinate+Rocket_Width/2)+5,(Rocket_Y_Coordinate+Rocket_Height)+10,'red',True)

    if Rocket_Right_Thrust > 0.0 :
        draw_ellipse((Rocket_X_Coordinate-5),(Rocket_Y_Coordinate+Rocket_Width/2)-3,(Rocket_X_Coordinate+10),(Rocket_Y_Coordinate+Rocket_Width/2)+3,'red',True)

    if Rocket_Left_Thrust > 0.0 :
        draw_ellipse((Rocket_X_Coordinate-5)+50,(Rocket_Y_Coordinate+Rocket_Width/2)-3,(Rocket_X_Coordinate+10)+50,(Rocket_Y_Coordinate+Rocket_Width/2)+3,'red',True)


# --------------------------------------------------------------
# Draws the On Screen Text
# --------------------------------------------------------------
def draw_hud():
    draw_text("Max Score: "+str(round(Max_Score)),0,0,'white')
    draw_text("Time Elapsed: "+str(round(Time_Elapsed)),0,30,'white')
    draw_text("Fuel Consumed: "+str(round(Fuel_Consumed)),0,60,'white')
    draw_text("X-Velocity: "+str(round(Rocket_X_Velocity,3)),0,90,'white')
    draw_text("Y-Velocity: "+str(round(Rocket_Y_Velocity,3)*-1),0,120,'white')
    draw_text("Crashes: "+str(round(Crashes))+" Landings: "+str(Landings),0,150,'white')
    draw_text("Score: "+str(round(Score)),0,180,'white')


# --------------------------------------------------------------
# Updates all animated objects
# --------------------------------------------------------------
def update_objects():
    update_boat()
    update_rocket()


# --------------------------------------------------------------
# Updates the Rocket
# --------------------------------------------------------------
def update_rocket():
    global Rocket_X_Coordinate, Rocket_Y_Coordinate
    global Rocket_Left_Thrust, Rocket_Right_Thrust, Rocket_Up_Thrust
    global Rocket_X_Velocity, Rocket_Y_Velocity
    global Rocket_Boost, GRAVITY, Fuel_Consumed

    if Rocket_Boost == True:
        Rocket_Up_Thrust = Rocket_Left_Thrust = Rocket_Right_Thrust = 0.0
        
        if Rocket_Y_Coordinate >= (WINDOW_HEIGHT)/2 :
            Rocket_Up_Thrust = 0.35
        else:
            Rocket_Right_Thrust = 0.25
        if Rocket_X_Coordinate >= (WINDOW_WIDTH - WATER_WIDTH):
            Rocket_Up_Thrust = 0.0
            Rocket_Boost = False
    
    Rocket_X_Velocity = Rocket_X_Velocity - Rocket_Left_Thrust
    Rocket_X_Velocity = Rocket_X_Velocity + Rocket_Right_Thrust
    Rocket_Y_Velocity = Rocket_Y_Velocity - Rocket_Up_Thrust + GRAVITY

    Rocket_X_Coordinate += Rocket_X_Velocity
    Rocket_Y_Coordinate += Rocket_Y_Velocity

    Fuel_Consumed += Rocket_Left_Thrust + Rocket_Right_Thrust + Rocket_Up_Thrust

# --------------------------------------------------------------
# Updates the Landing Pad / Boat
# --------------------------------------------------------------
def update_boat():
    global B_X_Coordinate, B_Velocity
    if(B_X_Coordinate <= GROUND_WIDTH or B_X_Coordinate >= (WINDOW_WIDTH-B_Width)):
        B_Velocity *= -1
    B_X_Coordinate = B_X_Coordinate + B_Velocity


# --------------------------------------------------------------
# Checks for Manual (oreventually) AI Input
# --------------------------------------------------------------
def get_input():
    global Rocket_Height, Rocket_Width, Rocket_Up_Thrust, Rocket_Left_Thrust, Rocket_Right_Thrust
    Rocket_Up_Thrust = Rocket_Left_Thrust = Rocket_Right_Thrust = 0
   
            
    if Rocket_Boost == False:
        ai_decision = rocket_ai.run_autopilot(num_runs, Rocket_X_Coordinate - Rocket_Width/2, Rocket_Y_Coordinate, Rocket_X_Velocity, Rocket_Y_Velocity, Rocket_Width, B_X_Coordinate, B_Y_Coordinate, B_Width)
        Rocket_Left_Thrust = ai_decision[0]
        Rocket_Right_Thrust = ai_decision[1]
        Rocket_Up_Thrust = ai_decision[2]
        
        if pythonGraph.key_down("left"):
            Rocket_Left_Thrust = 0.1
            
        if pythonGraph.key_down("right"):
            Rocket_Right_Thrust = 0.1
                
        if pythonGraph.key_down("up"):
            Rocket_Up_Thrust = 0.5

      


# --------------------------------------------------------------
# Detects if the Rocket has hit the ground or a boundry
# --------------------------------------------------------------
def is_simulation_over():
     if Rocket_Boost == False:
            rocket_left = int(Rocket_X_Coordinate - Rocket_Width/2)
            rocket_right = int(Rocket_X_Coordinate + Rocket_Width/2)
        
        # Checks for Collisions with the Sides
            if rocket_left < 0 or rocket_right >= WINDOW_WIDTH:
                return True
        
        # Checks for Collisions with the Ground
            for x in range(rocket_left, rocket_right):
                if (Rocket_Y_Coordinate >= WINDOW_HEIGHT - terrain_list[x]):
                    return True

 
     return False
    


# --------------------------------------------------------------
# Analyzes the Results of the Simulation
# --------------------------------------------------------------
def analyze_results():
    global Score, Landings, Crashes, Max_Score, B_X_Coordinate, Rocket_X_Coordinate, B_Width , Rocket_Width
    if B_X_Coordinate <= Rocket_X_Coordinate and B_X_Coordinate+B_Width >= Rocket_X_Coordinate+Rocket_Width:
        Score = 5000 - (Fuel_Consumed + Time_Elapsed)
        Landings += 1
        if (Score > Max_Score):
            Max_Score = Score
    else:
        Score = 1000 - (Fuel_Consumed + Time_Elapsed)
        Crashes += 1

# -----------------------------------------------------
# "Main Program"
# -----------------------------------------------------
pythonGraph.open_window(WINDOW_WIDTH, WINDOW_HEIGHT)
pythonGraph.set_window_title("CMPS445 Rocket Simulator")  

# Initializes the Simulation At Least Once
initialize_simulation(True)
    
# Main "Game Loop"
while pythonGraph.window_not_closed():
    if is_simulation_over() == False:
        erase_objects()
        draw_objects()
        get_input()
        update_objects()
    else:
        analyze_results()
        num_runs = num_runs + 1
        if num_runs == NUM_RUNS_PER_SCENARIO:
            num_runs = 0
            initialize_simulation(True)
        else:
            initialize_simulation(False)
        
    pythonGraph.update_window()