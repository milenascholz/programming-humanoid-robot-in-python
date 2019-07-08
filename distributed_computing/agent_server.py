'''In this file you need to implement remote procedure call (RPC) server

* There are different RPC libraries for python, such as xmlrpclib, json-rpc. You are free to choose.
* The following functions have to be implemented and exported:
 * get_angle
 * set_angle
 * get_posture
 * execute_keyframes
 * get_transform
 * set_transform
* You can test RPC server with ipython before implementing agent_client.py
'''

# add PYTHONPATH
import os
import sys
import pickle
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'kinematics'))
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'joint_control'))

from SimpleXMLRPCServer import SimpleXMLRPCServer
from recognize_posture import PostureRecognitionAgent
from inverse_kinematics import InverseKinematicsAgent


class ServerAgent(PostureRecognitionAgent, InverseKinematicsAgent):
    '''ServerAgent provides RPC service
    '''
    # YOUR CODE HERE
    
    
    def get_angle(self, joint_name):
        '''get sensor value of given joint'''
        # YOUR CODE HERE
        return self.perception.joint[joint_name]
    
    def set_angle(self, joint_name, angle):
        '''set target angle of joint for PID controller
        '''
        # YOUR CODE HERE
        self.perception.joint[joint_name] = angle
        return "set_angle complete"

    def get_posture(self):
        '''return current posture of robot'''
        # YOUR CODE HERE
        recognized_posture = self.recognize_posture(self.perception)
        return pickle.dumps(recognized_posture)

    def execute_keyframes(self, keyframes):
        '''excute keyframes, note this function is blocking call,
        e.g. return until keyframes are executed
        '''
        # YOUR CODE HERE
        self.keyframes = pickle.loads(keyframes)
        return "execute_keyframes complete"

    def get_transform(self, name):
        '''get transform with given name
        '''
        # YOUR CODE HERE
        local_trans = self.local_trans(name, self.perception.joint[name])
        return pickle.dumps(local_trans)

    def set_transform(self, effector_name, transform):
        '''solve the inverse kinematics and control joints use the results
        '''
        # YOUR CODE HERE
        self.set_transforms(effector_name, pickle.loads(transform))
        return "set_transform complete"

        
server = SimpleXMLRPCServer(("localhost", 8000))
print "Listening on port 8000..."
server.register_introspection_functions()
server.register_instance(ServerAgent())
server.serve_forever()

if __name__ == '__main__':
    agent = ServerAgent()
    agent.run()

