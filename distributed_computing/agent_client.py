'''In this file you need to implement remote procedure call (RPC) client

* The agent_server.py has to be implemented first (at least one function is implemented and exported)
* Please implement functions in ClientAgent first, which should request remote call directly
* The PostHandler can be implement in the last step, it provides non-blocking functions, e.g. agent.post.execute_keyframes
 * Hints: [threading](https://docs.python.org/2/library/threading.html) may be needed for monitoring if the task is done
'''

import weakref
import threading
import xmlrpclib
import pickle
import sys
import os
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'joint_control'))
from keyframes import hello
import numpy as np

class PostHandler(object):
    '''the post hander wraps function to be excuted in paralle
    '''
    def __init__(self, obj):
        self.proxy = weakref.proxy(obj)

    def execute_keyframes(self, keyframes):
        '''non-blocking call of ClientAgent.execute_keyframes'''
        # YOUR CODE HERE
        thread = threading.Thread(target = ClientAgent.execute_keyframes, args=(ClientAgent(), keyframes))
        thread.start()

    def set_transform(self, effector_name, transform):
        '''non-blocking call of ClientAgent.set_transform'''
        # YOUR CODE HERE
        thread = threading.Thread(target = ClientAgent.set_transform, args=(ClientAgent(), effector_name, transform))
        thread.start()


class ClientAgent(object):
    '''ClientAgent request RPC service from remote server
    '''
    # YOUR CODE HERE
    
    def __init__(self):
        self.post = PostHandler(self)
        self.proxy = xmlrpclib.ServerProxy('http://localhost:8000')
    
    def get_angle(self, joint_name):
        '''get sensor value of given joint'''
        # YOUR CODE HERE
        angle = self.proxy.get_angle(joint_name)
        print angle
        return angle
    
    def set_angle(self, joint_name, angle):
        '''set target angle of joint for PID controller
        '''
        # YOUR CODE HERE
        print self.proxy.set_angle(joint_name, angle)

    def get_posture(self):
        '''return current posture of robot'''
        # YOUR CODE HERE
        posture = self.proxy.get_posture()
        posture_deserialized = pickle.loads(posture)
        print posture_deserialized
        return posture_deserialized
        
    def execute_keyframes(self, keyframes):
        '''excute keyframes, note this function is blocking call,
        e.g. return until keyframes are executed
        '''
        # YOUR CODE HERE
        response = self.proxy.execute_keyframes(pickle.dumps(keyframes))
        print response            

    def get_transform(self, name):
        '''get transform with given name
        '''
        # YOUR CODE HERE
        transform = self.proxy.get_transform(name)
        transform_deserialized = pickle.loads(transform)
        print transform_deserialized
        return transform_deserialized

    def set_transform(self, effector_name, transform):
        '''solve the inverse kinematics and control joints use the results
        '''
        # YOUR CODE HERE
        transform_serialized = pickle.dumps(transform)
        response = self.proxy.set_transform(effector_name, transform_serialized)
        print response

if __name__ == '__main__':
    agent = ClientAgent()
    # TEST CODE HERE
    print "setting LAnklePitch to 13.7"
    agent.set_angle('LAnklePitch', 13.7)
    print "get_angle returns:"
    agent.get_angle('LAnklePitch')
    print "get_posture returns:"
    agent.get_posture()
    print "executing keyframe hello"
    agent.execute_keyframes(hello())
    print "get_transform returns:"
    agent.get_transform('LAnklePitch')
    transform = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]])
    print "setting transform"
    agent.set_transform('LAnklePitch', transform)
    ph = PostHandler(agent)
    print "executing keyframe hello (non-blocking)"
    ph.execute_keyframes(hello())
    print "setting transform (non-blocking)"
    ph.set_transform('LAnklePitch', transform)

