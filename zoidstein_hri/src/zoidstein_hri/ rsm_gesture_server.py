__author__ = 'alex'

from hri_framework import GestureActionServer
from zoidstein_hri.zoidstein import ZoidGesture
from rsm_serial_node import RSMSerialNode
from threading import Timer
import rospy



#!/usr/bin/env python

class GestureHandle():
    def __init__(self, goal_handle, timer):
        self.goal_id = goal_handle.get_goal_id().id
        self.goal_handle = goal_handle
        self.timer = timer

class RSMGestureActionServer(GestureActionServer):
    NODE_NAME = "RSMGestureServer"
    serialPort = None

    def __init__(self):
        GestureActionServer.__init__(self, ZoidGesture)
        self.gesture_handle_lookup = {}


    def gesture_finished(self, goal_handle):
        super(RSMGestureActionServer, self).gesture_finished(goal_handle)
        self.remove_gesture_handle(goal_handle)

    def start_gesture(self, goal_handle):
        self.rsm_serial_node = RSMSerialNode()
        goal = goal_handle.get_goal()

        if self.has_gesture(goal.gesture):
            gesture = ZoidGesture[goal.gesture]
            duration = ZoidGesture.get_duration(gesture) # TODO: implement this function in ZoidGesture
            
            #TODO: make call to self.rsm_serial_node to start the gesture

            timer = Timer(goal_duration, self.gesture_finished, goal_handle)
            gesture_handle = GestureHandle(goal_handle, timer)
            self.add_gesture_handle(gesture_handle)
            timer.start()

        else:
            self.action_server.set_aborted()

    def get_gesture_handle(self, goal_handle):
        return self.gesture_handle_lookup[goal_handle.get_goal_id().id]

    def add_gesture_handle(self, gesture_handle):
        self.gesture_handle_lookup[gesture_handle.goal_id] = gesture_handle

    def remove_gesture_handle(self, goal_handle):
        self.gesture_handle_lookup.pop(goal_handle.get_goal_id().id)

if __name__ == '__main__':
    rospy.init_node('gesture_action_server')
    gesture_server = RSMGestureActionServer()
    gesture_server.start()
    rospy.spin()
