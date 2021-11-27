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
from MalmoPython import MissionRecordSpec
import malmoutils
from past.utils import old_div
import os
import sys
import time
import json
import tkinter as tk
import math
from tabular_q_learning import TabQAgent

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

# # Create default Malmo objects:

# agent_host = MalmoPython.AgentHost()
# try:
#     agent_host.parse( sys.argv )
# except RuntimeError as e:
#     print('ERROR:',e)
#     print(agent_host.getUsage())
#     exit(1)
# if agent_host.receivedArgument("help"):
#     print(agent_host.getUsage())
#     exit(0)

# mission_file = './bridging.xml'
# with open(mission_file, 'r') as f:
#     print("Loading mission from %s" % mission_file)
#     mission_xml = f.read()
#     my_mission = MalmoPython.MissionSpec(mission_xml, True)
# my_mission_record = MalmoPython.MissionRecordSpec()

# # Attempt to start a mission:
# max_retries = 3
# for retry in range(max_retries):
#     try:
#         agent_host.startMission( my_mission, my_mission_record )
#         break
#     except RuntimeError as e:
#         if retry == max_retries - 1:
#             print("Error starting mission:",e)
#             exit(1)
#         else:
#             time.sleep(2)

# # Loop until mission starts:
# print("Waiting for the mission to start ", end=' ')
# world_state = agent_host.getWorldState()
# while not world_state.has_mission_begun:
#     print(".", end="")
#     time.sleep(0.01)
#     world_state = agent_host.getWorldState()
#     for error in world_state.errors:
#         print("Error:",error.text)

# print()
# print("Mission running ", end=' ')

# policy = ["crouch 1", "turn 0.5 180", "pitch 0.25 83"]

# for i in range(10):
#     policy.append("move -1 1")
#     policy.append("use")

# policy.append("pitch -0.25 38")
# policy.append("turn 0.5 180")
# policy.append("crouch 0")
# policy.append("move 1 1")

agent_host = MalmoPython.AgentHost()
mission_file = "./bridging.xml"
# add some args
agent_host.addOptionalStringArgument('mission_file',
    'Path/to/file from which to load the mission.', mission_file)
agent_host.addOptionalFloatArgument('alpha',
    'Learning rate of the Q-learning agent.', 0.1)
agent_host.addOptionalFloatArgument('epsilon',
    'Exploration rate of the Q-learning agent.', 0.01)
agent_host.addOptionalFloatArgument('gamma', 'Discount factor.', 1.0)
agent_host.addOptionalFlag('load_model', 'Load initial model from model_file.')
agent_host.addOptionalStringArgument('model_file', 'Path to the initial model file', '')
agent_host.addOptionalFlag('debug', 'Turn on debugging.')


# -- set up the agent -- #
actionSet = ["crouch 1","crouch 0", "move -1 1", "use"]

agent = TabQAgent(
    actions=actionSet,
    epsilon=0.01, #agent_host.getFloatArgument('epsilon'),
    alpha=0.1, #agent_host.getFloatArgument('alpha'),
    gamma=1.0, #agent_host.getFloatArgument('gamma'),
    debug = True, #agent_host.receivedArgument("debug"),
    canvas = canvas,
    root = root)

# -- set up the mission -- #
mission_file = "./bridging.xml"
with open(mission_file, 'r') as f:
    print("Loading mission from %s" % mission_file)
    mission_xml = f.read()
    my_mission = MalmoPython.MissionSpec(mission_xml, True)
my_mission.removeAllCommandHandlers()
my_mission.allowAllDiscreteMovementCommands()
#my_mission.requestVideo( 320, 240 )
my_mission.setViewpoint( 1 )

my_clients = MalmoPython.ClientPool()
my_clients.add(MalmoPython.ClientInfo('127.0.0.1', 10000)) # add Minecraft machines here as available

max_retries = 3
agentID = 0
expID = 'tabular_q_learning'

num_repeats = 150
cumulative_rewards = []
for i in range(num_repeats):
    
    print("\nMission %d of %d:" % ( i+1, num_repeats )) #print("\nMap %d - Mission %d of %d:" % ( imap, i+1, num_repeats ))

    my_mission_record = MissionRecordSpec() #malmoutils.get_default_recording_object(agent_host, "./save_%s-rep%d" % (expID, i))

    for retry in range(max_retries):
        try:
            agent_host.startMission( my_mission, my_clients, my_mission_record, agentID, "%s-%d" % (expID, i) )
            break
        except RuntimeError as e:
            if retry == max_retries - 1:
                print("Error starting mission:",e)
                exit(1)
            else:
                time.sleep(2.5)

    print("Waiting for the mission to start", end=' ')
    world_state = agent_host.getWorldState()
    while not world_state.has_mission_begun:
        print(".", end="")
        time.sleep(0.1)
        world_state = agent_host.getWorldState()
        for error in world_state.errors:
            print("Error:",error.text)
    print()

    # -- run the agent in the world -- #
    cumulative_reward = agent.run(agent_host)
    print('Cumulative reward: %d' % cumulative_reward)
    cumulative_rewards += [ cumulative_reward ]

    # -- clean up -- #
    time.sleep(0.5) # (let the Mod reset)

print("Done.")

print()
print("Cumulative rewards for all %d runs:" % num_repeats)
print(cumulative_rewards)






























# Loop until mission ends:
# while world_state.is_mission_running:
#     time.sleep(0.01)
#     world_state = agent_host.getWorldState()
#     if world_state.number_of_observations_since_last_state > 0: # Have any observations come in?
#         msg = world_state.observations[-1].text                 # Yes, so get the text
#         agent_info = json.loads(msg)                          # and parse the JSON
#         grid = agent_info['floor3x3']
#         distance = agent_info['distanceFromend']
#         x = agent_info["XPos"]
#         y = agent_info["ZPos"]

#         updateBlocks(x, y, grid[4]=="stone")
#         #print(distance)
#         #print(grid)


        
#     for error in world_state.errors:
#         print("Error:",error.text)

# print()
# print("Mission ended")
# Mission has ended.
