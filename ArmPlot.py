'''
Copyright (C) 2013 Travis DeWolf

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import numpy as np
import pyglet

import Arm
# from Arm import def_test


def plot():
    """A function for plotting an arm, and having it calculate the
    inverse kinematics such that given the mouse (x, y) position it
    finds the appropriate joint angles to reach that point."""

    # create an instance of the arm
    arm = Arm.Arm3Link(L=np.array([300, 200, 100]))

    # make our window for drawin'
    window = pyglet.window.Window(500, 500, 'Arm')
     

    label = pyglet.text.Label(
        'Mouse (x,y)', font_name='Times New Roman',
        font_size=36, x=window.width//2, y=window.height//2,
        anchor_x='center', anchor_y='center')

    def get_joint_positions():
        """This method finds the (x,y) coordinates of each joint"""

        x = np.array([
            0,
            arm.L[0]*np.cos(arm.q[0]),
            arm.L[0]*np.cos(arm.q[0]) + arm.L[1]*np.cos(arm.q[0]+arm.q[1]),
            arm.L[0]*np.cos(arm.q[0]) + arm.L[1]*np.cos(arm.q[0]+arm.q[1]) +
            arm.L[2]*np.cos(np.sum(arm.q))]) + window.width/2

        y = np.array([
            0,
            arm.L[0]*np.sin(arm.q[0]),
            arm.L[0]*np.sin(arm.q[0]) + arm.L[1]*np.sin(arm.q[0]+arm.q[1]),
            arm.L[0]*np.sin(arm.q[0]) + arm.L[1]*np.sin(arm.q[0]+arm.q[1]) +
            arm.L[2]*np.sin(np.sum(arm.q))])

        return np.array([x, y]).astype('int')

    window.jps = get_joint_positions()

    @window.event
    def on_draw():
        window.clear()
        label.draw()
        for i in range(3):
            pyglet.graphics.draw(
                2,
                pyglet.gl.GL_LINES,
                ('v2i', (window.jps[0][i], window.jps[1][i],
                         window.jps[0][i+1], window.jps[1][i+1])))

    @window.event
    def on_mouse_motion(x, y, dx, dy):
        # call the inverse kinematics function of the arm
        # to find the joint angles optimal for pointing at
        # this position of the mouse
        label.text = '(x,y) = (%.3f, %.3f)' % (x, y)
        arm.q = arm.inv_kin([x - window.width/2, y])  # get new arm angles
        window.jps = get_joint_positions()  # get new joint (x,y) positions
        # print('angles',arm.q,   'coordinates',(x,y))
        list = arm.q.tolist()
        # print(list)

        # for i in list:

        input_number = list[0]
        input_min = 0
        input_max = 3
        output_min = 100
        output_max = 500
        result = (input_number-input_min)*(output_max-output_min)/(input_max-input_min)+output_min
        # print('a==',result)

        input_number2 = list[1]
        input_min2 = 0
        input_max2 = 3
        output_min2 = 100
        output_max2 = 500
        result2 = (input_number2-input_min2)*(output_max2-output_min2)/(input_max2-input_min2)+output_min2
        # print('b==',result2)

        input_number3 = list[2]
        input_min3 = 0
        input_max3 = 3
        output_min3 = 100
        output_max3 = 500
        result3 = (input_number3-input_min3)*(output_max3-output_min3)/(input_max3-input_min3)+output_min3
        print(result,result2,result3)
      
    pyglet.app.run()
    

    print()

plot()
