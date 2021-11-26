from __future__ import print_function
# ------------------------------------------------------------------------------------------------
# Copyright (c) 2016 Microsoft Corporation
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ------------------------------------------------------------------------------------------------

# Tutorial sample #1: Run simple mission

from builtins import range
import MalmoPython
from past.utils import old_div
import os
import sys
import time
import json
import tkinter as tk
import math

CANVAS_WIDTH = 390
CANVAS_HEIGHT = 540
ZERO_X = 11
ZERO_Y = -2

visited_list = []

def blockX(x):
    act_x = math.floor(ZERO_X - x)
    return act_x * 30

def blockY(y):
    act_y = math.floor(y) - ZERO_Y
    return (CANVAS_HEIGHT - act_y * 30) - 30



root = tk.Tk()
root.wm_title("Agent Tracker")

canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, borderwidth=0, highlightthickness=0, bg="black")
canvas.pack()
root.update()

def updateBlocks(xpos, ypos, stone):
    canvas.delete('all')
    if stone:
        current_block = (blockX(xpos), blockY(ypos), blockX(xpos)+30, blockY(ypos)+30)
        if current_block not in visited_list:
            visited_list.append(current_block)
    for block in visited_list:
        canvas.create_rectangle(block[0], block[1], block[2], block[3], fill="grey")

    canvas.create_rectangle(180, 420, 210, 450, fill="yellow")
    canvas.create_rectangle(180, 90, 210, 120, fill="blue")
    real_x = (ZERO_X - x) * 30
    real_y = (CANVAS_HEIGHT - (y - ZERO_Y) * 30)
    canvas.create_oval(real_x - 10, real_y - 10, real_x + 10, real_y + 10, fill="red")
    #print("Block at: ", blockX(xpos), blockY(ypos), blockX(xpos)+30, blockY(ypos)+30)
    root.update()


if sys.version_info[0] == 2:
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
    import functools
    print = functools.partial(print, flush=True)

# Create default Malmo objects:

agent_host = MalmoPython.AgentHost()
try:
    agent_host.parse( sys.argv )
except RuntimeError as e:
    print('ERROR:',e)
    print(agent_host.getUsage())
    exit(1)
if agent_host.receivedArgument("help"):
    print(agent_host.getUsage())
    exit(0)

mission_file = './bridging.xml'
with open(mission_file, 'r') as f:
    print("Loading mission from %s" % mission_file)
    mission_xml = f.read()
    my_mission = MalmoPython.MissionSpec(mission_xml, True)
my_mission_record = MalmoPython.MissionRecordSpec()

# Attempt to start a mission:
max_retries = 3
for retry in range(max_retries):
    try:
        agent_host.startMission( my_mission, my_mission_record )
        break
    except RuntimeError as e:
        if retry == max_retries - 1:
            print("Error starting mission:",e)
            exit(1)
        else:
            time.sleep(2)

# Loop until mission starts:
print("Waiting for the mission to start ", end=' ')
world_state = agent_host.getWorldState()
while not world_state.has_mission_begun:
    print(".", end="")
    time.sleep(0.01)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print("Error:",error.text)

print()
print("Mission running ", end=' ')

policy = ["crouch 1", "turn 0.5 180", "pitch 0.25 83"]

for i in range(10):
    policy.append("move -1 1")
    policy.append("use")

policy.append("pitch -0.25 38")
policy.append("turn 0.5 180")
policy.append("crouch 0")
policy.append("move 1 1")

cmdIndex = 0
action_executing = False
initial = None
prev = None
crouching = False
rotations = 0
cycles = 0

# Loop until mission ends:
while world_state.is_mission_running:
    time.sleep(0.01)
    world_state = agent_host.getWorldState()
    if world_state.number_of_observations_since_last_state > 0: # Have any observations come in?
        msg = world_state.observations[-1].text                 # Yes, so get the text
        agent_info = json.loads(msg)                          # and parse the JSON
        grid = agent_info['floor3x3']
        distance = agent_info['distanceFromend']
        x = agent_info["XPos"]
        y = agent_info["ZPos"]

        updateBlocks(x, y, grid[4]=="stone")
        #print(distance)
        #print(grid)

        cmd = ['stall']
        if cmdIndex < len(policy):
            cmd = policy[cmdIndex].split() # Get next action in policy, otherwise stall
            if not action_executing:
                print("Executing command: " + policy[cmdIndex])
        elif not action_executing:
            action_executing = True
            print("End of policy execution, stalling...")
            agent_host.sendCommand("quit")

        type = cmd[0]
        if type == 'move':
            # Get info about the user's current position
            agent_coordinates = [x, y]
            
            # Get command parameters
            speed = cmd[1]
            dist = float(cmd[2])
            correction_factor = (1.186 if not crouching else 0.3696) * abs(float(speed))
            CYCLE_LIMIT = 20 * dist

            if not action_executing:
                action_executing = True
                initial = agent_coordinates
                agent_host.sendCommand("move " + speed)
                if (float(speed) == 0 and dist != 0):
                    raise Exception("Action \"" + policy[cmdIndex] + "\" is infeasible")
            else:
                cycles += 1
                if math.hypot(initial[0]-agent_coordinates[0], initial[1]-agent_coordinates[1]) >= dist or cycles > CYCLE_LIMIT:
                    agent_host.sendCommand("move 0")
                    action_executing = False
                    cycles = 0
                    initial = None
                    cmdIndex += 1
        elif type == 'crouch':
            param = cmd[1]
            agent_host.sendCommand("crouch " + param)
            crouching = True if 1 else False
            cmdIndex += 1
        elif type == 'pitch':
            pitch = agent_info[u'Pitch']
            speed = cmd[1]
            dist = float(cmd[2])
            correction_factor = 22.3576*0.05

            if not action_executing:
                action_executing = True
                initial = pitch
                agent_host.sendCommand("pitch " + speed)
                if (float(speed) == 0 and dist != 0):
                    raise Exception("Action \"" + policy[cmdIndex] + "\" is infeasible")
            else:
                if abs(pitch - initial + correction_factor) >= dist:
                    agent_host.sendCommand("pitch 0")
                    action_executing = False
                    initial = None
                    cmdIndex += 1
                elif abs(pitch - initial) >= dist - 15:
                    if pitch - initial > 0:
                        agent_host.sendCommand("pitch 0.05")
                    else:
                        agent_host.sendCommand("pitch -0.05")
                    
        elif type == 'turn':
            yaw = agent_info[u'Yaw']
            absYaw = yaw if yaw > 0 else yaw + 360
            speed = cmd[1]
            speed_num = float(speed)
            dist = float(cmd[2])
            correction_factor = 26.9576*0.1

            if not action_executing:
                action_executing = True
                agent_host.sendCommand("turn " + speed)
                if (speed_num == 0 and dist != 0):
                    raise Exception("Action \"" + policy[cmdIndex] + "\" is infeasible")
                initial = speed_num/abs(speed_num) * dist + absYaw
            else:
                if absYaw < prev and speed_num > 0:
                    rotations += 1
                if absYaw > prev and speed_num < 0:
                    rotations -= 1
                if (absYaw + rotations*360 + correction_factor >= initial and speed_num > 0) or (absYaw + rotations*360 + correction_factor <= initial and speed_num < 0):
                    agent_host.sendCommand("turn 0")
                    action_executing = False
                    initial = None
                    rotations = 0
                    cmdIndex += 1
                elif(absYaw + rotations*360 >= initial - 15 and speed_num > 0) or (absYaw + rotations*360 <= initial + 15 and speed_num < 0):
                    if speed_num > 0:
                        agent_host.sendCommand("turn 0.1")
                    else:
                        agent_host.sendCommand("turn -0.1")
            prev = absYaw
        elif type == 'use':
            agent_host.sendCommand("use 1")
            time.sleep(0.1)
            agent_host.sendCommand("use 0")
            cmdIndex += 1
        elif type == 'jump':
            agent_host.sendCommand("jump 1")
            time.sleep(0.1)
            agent_host.sendCommand("jump 0")
            cmdIndex = cmdIndex + 1
        elif type == 'stall':
            agent_host.sendCommand("move 0")
            agent_host.sendCommand("pitch 0")
            agent_host.sendCommand("turn 0")
            cmdIndex += 1
        else:
            raise ValueError('The action \"' + policy[cmdIndex] + '\" is unknown or invalid')
        
    for error in world_state.errors:
        print("Error:",error.text)

print()
print("Mission ended")
# Mission has ended.
