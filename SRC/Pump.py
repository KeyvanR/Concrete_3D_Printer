# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 14:33:56 2024

@author: Keyvan
"""

class Pump:
    def __init__(self):
        self.name = "Pump"
        self.connected = True 
        self.Q_active = False 
        self.prev_pump_state = False  # Initially assuming pump is inactive
        self.m_pump_active_by_robot = False
        self.m_pump_active_manually = False
        self.m_pump_stoped = False
        self.m_pump = False