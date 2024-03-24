# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 14:34:41 2024

@author: Keyvan
"""

class Valve:
    def __init__(self):
        self.name = "Valve"
        self.connected = True
        self.Q_active = False
        self.m_valve_active_by_robot = False
        self.m_valve_keep_open = False
        self.m_valve_active_pump_active = False
        self.m_valve_active_manually = False