# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 12:11:27 2024

@author: Keyvan

    Naming the input addresses:
        Input addresses begin with the letter 'I', followed by the specific component or device responsible for generating the signal. 
        The subsequent details pertain to the functionality of the input address. For example 'I_Switch_valve_keep_open' begins with 
        'I' indicating input address. Switch indicates that this input address belongs to a switch. The rest (valve_keep_open) explain 
        what this switch is used for.
        
    ..................................................................................................................................
    .                                               List of inputs
    ..................................................................................................................................
    .   .  Address                  .  Signal Source .                                   Comment
    ..................................................................................................................................
    . 1 . I_Swith_Pump             . Operating Panel . On-Off switch to turn the pump on and off .
    ..................................................................................................................................
    . 2 . I_UI_Pump                . User Interface  . On-Off switch to turn the pump on and off 
    ..................................................................................................................................
    . 3 . I_Swith_Valve            . Operating Panel . On-Off switch to turn the valve on and off 
    ..................................................................................................................................
    . 4 . I_UI_Valve               . User Interface  . On-Off switch to turn the valve on and off
    ..................................................................................................................................
    . 5 . I_Robot_Start_Pump       . Robot           . Command the pump to start
    ..................................................................................................................................
    . 6 . I_Robot_Stop_Pump        . Robot           . Command the pump to stop
    ..................................................................................................................................
    . 7 . I_Robot_Start_Valve      . Robot           . Command the valve to start
    ..................................................................................................................................
    . 8 . I_Robot_Stop_Valve       . Robot           . Command the valve to stop
    ..................................................................................................................................
    . 9 . I_Swith_Robot            . Operating Panel .  On-Off switch to turn the robot on and off 
    ..................................................................................................................................
    . 10. I_UI_Robot               . User Interface  .  On-Off switch to turn the robot on and off 
    ..................................................................................................................................
    . 11. I_Switch_valve_keep_open . Operating Panel .  On-Off switch to keep the valve open. his signal overrides any other command. 
    ..................................................................................................................................

 
 """
 
import numpy as np
from ControlPLC import ControlPLC
from Pump import Pump
from Valve import Valve
from Robot import Robot


# Creating components
pump = Pump()
valve = Valve()
robot = Robot()

# Creating control PLC
plc = ControlPLC(robot, pump, valve)

def str_to_bool(s):
    return s.lower() == 'true'

# Simulation loop
while True:
    
    input_matrix_str_connection_test = input("\n Determine which components are connected and which are not connected? In order pump, valve, robot (e.g., [1,0,0]): ")
    input_matrix_connection_test = eval(input_matrix_str_connection_test)  # Convert input string to list
    pump.connected= bool(input_matrix_connection_test[0])
    valve.connected = bool(input_matrix_connection_test[1])
    robot.connected = bool(input_matrix_connection_test[2])
    
    
    while not plc.check_connection():
        input_matrix_str_connection_test = input("\n Determine which components are connected and which are not connected? In order pump, valve, robot (e.g., [1,0,0]): ")
        input_matrix_connection_test = eval(input_matrix_str_connection_test)  # Convert input string to list
        pump.connected= bool(input_matrix_connection_test[0])
        valve.connected = bool(input_matrix_connection_test[1])
        robot.connected = bool(input_matrix_connection_test[2])
       
        pass  # Keep looping until all components are connected
   
    # -------------------------------------------------------------------------------------------------------
    
    #Get input matrix from user
    input_matrix_str = input("Enter the array of inputs (e.g., [1,0,0,0,0,0,0,0,0,0,0]): ")
    input_matrix = eval(input_matrix_str)  # Convert input string to list
    
    #input_matrix = np.array([1,0,0,0,0,0,0,0,0,0,0])
       
    # Assign values from input array to variables
    plc.I_Swith_Pump = bool(input_matrix[0])
    plc.I_UI_Pump = bool(input_matrix[1])
    plc.I_Swith_Valve = bool(input_matrix[2])
    plc.I_UI_Valve = bool(input_matrix[3])
    plc.I_Robot_Start_Pump = bool(input_matrix[4])
    plc.I_Robot_Stop_Pump = bool(input_matrix[5])
    plc.I_Robot_Start_Valve = bool(input_matrix[6])
    plc.I_Robot_Stop_Valve = bool(input_matrix[7])
    plc.I_Swith_Robot = bool(input_matrix[8])
    plc.I_UI_Robot = bool(input_matrix[9])
    plc.I_Switch_valve_keep_open = bool(input_matrix[10])
    # -------------------------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------------
    # #If you want to enter the variables one by one uncomment this section:
    
    # plc.I_Swith_Pump = str_to_bool(input("Enter I_Swith_Pump (True/False): "))
    # plc.I_UI_Pump = str_to_bool(input("Enter I_UI_Pump (True/False): "))
    # plc.I_Swith_Valve = str_to_bool(input("Enter I_Swith_Valve (True/False): "))
    # plc.I_UI_Valve = str_to_bool(input("Enter I_UI_Valve (True/False): "))
    # plc.I_Robot_Start_Pump = str_to_bool(input("Enter I_Robot_Start_Pump (True/False): "))
    # plc.I_Robot_Stop_Pump = str_to_bool(input("Enter I_Robot_Stop_Pump (True/False): "))
    # plc.I_Robot_Start_Valve = str_to_bool(input("Enter I_Robot_Start_Valve (True/False): "))
    # plc.I_Robot_Stop_Valve = str_to_bool(input("Enter I_Robot_Stop_Valve (True/False): "))
    # plc.I_Swith_Robot = str_to_bool(input("Enter I_Swith_Robot (True/False): "))
    # plc.I_UI_Robot = str_to_bool(input("Enter I_UI_Robot (True/False): "))
    # plc.I_Switch_valve_keep_open = str_to_bool(input("Enter I_Switch_valve_keep_open (True/False): "))
    
    # -------------------------------------------------------------------------------------------------------
    
    
    # process pump 
    plc.Pump_Logic()
    
    # process valve Pump_Stopped_Logic
    plc.Pump_Stopped_Logic()
    
    # process valve
    plc.Valve_Logic()
    
    # process robot
    plc.Robot_Logic()
      
    # Generate the outputs
    plc.Generate_Outputs() 
    
    print("\n Pump:", pump.Q_active)
    print("\n Valve:", valve.Q_active)
    print("\n robot:", robot.Q_active)
   

 