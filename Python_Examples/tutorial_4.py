from __future__ import print_function
from __future__ import division
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

# Tutorial sample #4: Challenge - get to the centre of the sponge

from builtins import range
from past.utils import old_div
import MalmoPython
import os
import sys
import time
import json
import math

if sys.version_info[0] == 2:
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
    import functools
    print = functools.partial(print, flush=True)

def Menger(xorg, yorg, zorg, size, blocktype, variant, holetype):
    #draw solid chunk
    genstring = GenCuboidWithVariant(xorg,yorg,zorg,xorg+size-1,yorg+size-1,zorg+size-1,blocktype,variant) + "\n"
    #now remove holes
    unit = size
    while (unit >= 3):
        w=old_div(unit,3)
        for i in range(0, size, unit):
            for j in range(0, size, unit):
                x=xorg+i
                y=yorg+j
                genstring += GenCuboid(x+w,y+w,zorg,(x+2*w)-1,(y+2*w)-1,zorg+size-1,holetype) + "\n"
                y=yorg+i
                z=zorg+j
                genstring += GenCuboid(xorg,y+w,z+w,xorg+size-1, (y+2*w)-1,(z+2*w)-1,holetype) + "\n"
                genstring += GenCuboid(x+w,yorg,z+w,(x+2*w)-1,yorg+size-1,(z+2*w)-1,holetype) + "\n"
        unit = w
    return genstring

def GenCuboid(x1, y1, z1, x2, y2, z2, blocktype):
    return '<DrawCuboid x1="' + str(x1) + '" y1="' + str(y1) + '" z1="' + str(z1) + '" x2="' + str(x2) + '" y2="' + str(y2) + '" z2="' + str(z2) + '" type="' + blocktype + '"/>'

def GenCuboidWithVariant(x1, y1, z1, x2, y2, z2, blocktype, variant):
    return '<DrawCuboid x1="' + str(x1) + '" y1="' + str(y1) + '" z1="' + str(z1) + '" x2="' + str(x2) + '" y2="' + str(y2) + '" z2="' + str(z2) + '" type="' + blocktype + '" variant="' + variant + '"/>'
    
missionXML='''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            
              <About>
                <Summary>Hello world!</Summary>
              </About>
              
            <ServerSection>
              <ServerInitialConditions>
                <Time>
                    <StartTime>1000</StartTime>
                    <AllowPassageOfTime>false</AllowPassageOfTime>
                </Time>
                <Weather>clear</Weather>
              </ServerInitialConditions>
              <ServerHandlers>
                  <FlatWorldGenerator generatorString="3;7,44*49,73,35:1,159:4,95:13,35:13,159:11,95:10,159:14,159:6,35:6,95:6;12;"/>
                  <DrawingDecorator>
                    <DrawSphere x="-27" y="70" z="0" radius="30" type="air"/>''' + Menger(-40, 40, -13, 27, "stone", "smooth_granite", "air") + '''
                    <DrawBlock x="-27" y="39" z="0" type="diamond_block"/>
                  </DrawingDecorator>
                  <ServerQuitFromTimeUp timeLimitMs="120000"/>
                  <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
              </ServerSection>
              
              <AgentSection mode="Survival">
                <Name>MalmoTutorialBot</Name>
                <AgentStart>
                    <Placement x="0.5" y="56.0" z="0.5" yaw="90"/>
                    <Inventory>
                        <InventoryBlock slot="8" type="cobblestone" quantity="64"/>
                    </Inventory>
                </AgentStart>
                <AgentHandlers>
                  <ObservationFromFullStats/>
                  <ContinuousMovementCommands/>
                  <InventoryCommands/>
                  <AgentQuitFromReachingPosition>
                    <Marker x="-26.5" y="40" z="0.5" tolerance="0.5" description="Goal_found"/>
                  </AgentQuitFromReachingPosition>
                </AgentHandlers>
              </AgentSection>
            </Mission>'''

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

my_mission = MalmoPython.MissionSpec(missionXML, True)
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

# ADD YOUR CODE HERE
# TO GET YOUR AGENT TO THE DIAMOND BLOCK

agent_host.sendCommand("hotbar.9 1")
agent_host.sendCommand("hotbar.9 0")

policy = ["crouch 1", "turn 0.3 180", "pitch 0.25 83", "move -1 2"]
#policy = ["crouch 1", "move -1 1"]
for i in range(51):
    policy.append("use")
    policy.append("move -1 1")

policy.append("pitch -0.25 83")

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

    for error in world_state.errors:
        print("Error:",error.text)

    if (world_state.observations):
        agent_info = json.loads(world_state.observations[0].text)
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
            agent_coordinates = [agent_info[u'XPos'], agent_info[u'ZPos']]
            
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
        

print()
print("Mission ended")
# Mission has ended.
