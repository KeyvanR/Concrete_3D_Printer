# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 20:07:17 2024

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

class ControlPLC:
    def __init__(self, robot, pump, valve):
        self.robot = robot
        self.pump = pump
        self.valve = valve
        # list of inputs
        self.I_Swith_Robot = False
        self.I_UI_Robot = False
        self.I_Swith_Pump = False
        self.I_UI_Pump = False
        self.I_Swith_Valve = False
        self.I_UI_Valve = False
        self.I_Robot_Start_Pump = False
        self.I_Robot_Stop_Pump = False
        self.I_Robot_Start_Valve = False
        self.I_Robot_Stop_Valve = False
        self.I_Switch_valve_keep_open = False
        


# if any of the components is not connected to the control PLC, all other components should
# be disabled until the connection state is restored
# Ba or ham mishe nevesht

    def check_connection(self):
        if not all([self.robot.connected, self.pump.connected, self.valve.connected]):
            self.diactive_components()
            if not self.robot.connected:
                print("\n Warning: Robot not connected") 
            if not self.pump.connected:
                print("\n Warning: Pump not connected") 
            if not self.valve.connected:
                print("\n Warning: Valve not connected")
            print("\n Pump:", self.pump.active)
            print("\n Valve:", self.valve.active)
            print("\n robot:", self.robot.active)
            return False
        return True
        
    def diactive_components(self): #deactivate components
            self.robot.active = False
            self.pump.active = False
            self.valve.active = False

    def Pump_Logic(self):
        
        # Control the pump manually through switch or UI
        
        if ( self.I_Swith_Pump or self.I_UI_Pump ):
                self.pump.m_pump_active_manually = True
        else:
                self.pump.m_pump_active_manually = False
        
        # Pump is controlled by the robot
        
        if self.I_Robot_Start_Pump:
            self.pump.m_pump_active_by_robot = True

        if self.I_Robot_Stop_Pump:
            self.pump.m_pump_active_by_robot = False
            self.pump.m_pump_active_manually = False
        
        if (self.pump.m_pump_active_by_robot or self.pump.m_pump_active_manually):
            self.pump.m_pump = True
            
        else:
            self.pump.m_pump = False
            
        
    
    def Pump_Stopped_Logic(self):
        
        if self.pump.prev_pump_state and not self.pump.m_pump:  
            self.pump.m_pump_stoped = True
            
        
        if not self.pump.prev_pump_state and self.pump.m_pump:  
            self.pump.m_pump_stoped = False
        
        self.pump.prev_pump_state = self.pump.m_pump
        
    
    def Valve_Logic(self):
        
        # the valve have the option of being kept open by a signal that overrides any other command
        
        if self.I_Switch_valve_keep_open:
            self.valve.m_valve_keep_open = True
        else:
            self.valve.m_valve_keep_open = False
        
        
        # the valve should always be open if the pump is active, even if the robot commands it to close
        
        if (self.pump.m_pump_active_by_robot or self.pump.m_pump_active_manually):
            self.valve.m_valve_active_pump_active = True
        else:
            self.valve.m_valve_active_pump_active = False
        
        # the pump and the valve should have an option of being activated and deactivated manually 
        #(for example, using a physical switch or signal from a UI), 
        
            
        if ( self.I_Swith_Valve or self.I_UI_Valve ):
                self.valve.m_valve_active_manually = True
        else:
                self.valve.m_valve_active_manually = False
        
                
        # Valve is controlled by robot - command from the robot 
        #should have precedence over the manual operation signals
        
        if self.I_Robot_Start_Valve:
            self.valve.m_valve_active_by_robot = True
        
        if self.I_Robot_Stop_Valve:
            self.valve.m_valve_active_by_robot = False
            self.valve.m_valve_active_manually = False
        
    
    def Robot_Logic(self):
        

        # Control the robot manually through switch or UI
        
        if ( self.I_Swith_Robot or self.I_UI_Robot ):
                self.robot.m_robot_active_manually = True
        else:
                self.robot.m_robot_active_manually = False
        

                
    
    def Generate_Outputs(self):
        
        # Pump
        
        if self.pump.m_pump:
            self.pump.Q_active = True
        else:
            self.pump.Q_active = False
            
       
    
        # Valve
        if (self.valve.m_valve_keep_open  or self.valve.m_valve_active_pump_active or 
            self.valve.m_valve_active_by_robot or self.valve.m_valve_active_manually):
            
            self.valve.Q_active = True
        else:
            self.valve.Q_active = False
        
        # Robot
        
        if self.robot.m_robot_active_manually and not self.pump.m_pump_stoped: 
                self.robot.Q_active = True
        else:
                self.robot.Q_active = False
                
        if self.pump.m_pump_stoped:
            self.robot.Q_active = False
            print('The robot stopped because the pump stopped.Switch on the pump if you wish to proceed ')
        

