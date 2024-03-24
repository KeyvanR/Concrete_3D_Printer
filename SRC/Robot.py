# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 14:35:11 2024

@author: Keyvan
"""

class Robot:
    def __init__(self):
        self.name = "Robot"
        self.connected = True 
        self.Q_active = False
        self.m_robot_active_manually = False
        self.m = False