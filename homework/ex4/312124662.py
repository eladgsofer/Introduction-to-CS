import auv_interface
import numpy as np
import matplotlib.pyplot as plt


class HydroCamel(auv_interface.Auv):
    FIGNUM=1
    SONAR_HEAD = 5
    HIDDEN_MINE = 6
    MINE_FOUND = 7
    SONAR_RADAR = 8

    def __init__(self, _sonar_range, _sonar_angle, _map_size,
                 _initial_position, _velocity, _duration, _mines_map):
        ''' init method for class Auv.
        Input _sonar_range - An integer with values between 3-9, denote the range of the sonar
        the distance between the 2 corners of the cells "opening distance"
        _sonar_angle - An integer with values between 15-85 in degrees, denote half of the field of view angle
        _map_size - a tuple (Height, Width) of the map
        _initial_position - a tuple (Py, Px). The starting point of the AUV.
        _velocity - a tuple of lists. each donates a velocity ([Vy1, Vx1], [Vy2, Vx2]...)
        _duration - a lists of integers. each denote the time to run the simulation
                                         with the matching velocity [t1, t2,...]
        _mines_map - a list of lists holding the location of all the mines.
        Output None.
        '''
        self.sonar_range = _sonar_range
        self.radius = _sonar_range

        self.sonar_angle = np.radians(_sonar_angle)
        self.map_size = _map_size
        self.initial_position = _initial_position

        # Assuming start Velocity angel is 0
        self.vel_angle = 0

        self.velocity = _velocity
        self.duration = _duration
        self.curr_velocity = self.velocity[0]
        self.mines_map = np.array(_mines_map)

        y, x = _initial_position
        self.prev_head = y, x
        rcos = self.radius*np.cos(self.sonar_angle)
        rsin = self.radius*np.sin(self.sonar_angle)

        # Left sonar is minus - as result of inverse y axis
        self.left_sonar_p = np.array([-1*rsin+y, rcos+x])
        self.right_sonar_p = np.array([rsin+y, rcos+x])

        self.found_mines = []
        self.current_map = self.mines_map[:]*self.HIDDEN_MINE
        self.get_sonar_fov()


    def get_mines(self):
        ''' Returns the head_position of all the mines that the AUV has found.
        Input None.
        Output A list of tuples. Each tuple holds the coordinates (Yi , Xi) of found mines. The list should be sorted.
        '''
        return self.bubble_sort(self.found_mines)

    def get_sonar_fov(self):
        ''' Returns all the current  (Yi , Xi) coordinates of the map which are in range for the sonar
        Input None.
        Output A dictionary. The keys of the dictionary are tuples of the (Yi , Xi) coordinates
        and the value should be Boolean True
        '''

        # Reset Sonar map
        self.current_map[self.current_map==self.SONAR_RADAR] = 0
        self.current_map[self.prev_head[0], self.prev_head[1]] = 0


        found_points = {}
        # Triangle Points
        a, b, c = self.initial_position, self.left_sonar_p, self.right_sonar_p

        # head point
        a_y, a_x = a

        for p_y, row in enumerate(self.mines_map):
            for p_x, cell_val in enumerate(row):
                if self.is_point_in_triangle(a,b,c, (p_y,p_x)):
                    # Insert the point into the dictionary & update map
                    found_points[(p_y,p_x)] = True
                    self.current_map[p_y, p_x] = self.SONAR_RADAR
                    if cell_val == 1:
                        # If a mine was found in the sonar, add it
                        self.current_map[p_y, p_x] = self.MINE_FOUND
                        if (p_y, p_x) not in self.found_mines:
                            self.found_mines.append((p_y,p_x))

        # head point update
        self.current_map[a_y, a_x] = self.SONAR_HEAD
        self.prev_head = (a_y, a_x)
        return found_points


    @staticmethod
    def is_point_in_triangle(a, b, c, p):
        """
        This algorithem is taken from youtube....
        :param a:
        :param b:
        :param c:
        :param p:
        :return:
        """

        # in case of zero division - while 90 degrees
        # np.close because - sometimes the number was diff between numbers was almost
        # 0, therfor wasn't 0
        if np.allclose((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]), 0)\
                or np.allclose(c[0] - a[0], 0):
            tmp = b
            b = c
            c = tmp


        w1 = (a[1] * (c[0] - a[0]) + (p[0] - a[0]) * (c[1] - a[1]) - p[1] * (
        c[0] - a[0])) / \
             ((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]))
        w2 = (p[0] - a[0] - w1 * (b[0] - a[0])) / (c[0] - a[0])

        return (np.allclose(w1, 0) or w1 >= 0) and (
        np.allclose(w2, 0) or w2 >= 0) and \
               (np.allclose(w1 + w2, 1) or (w1 + w2) <= 1)

    def display_map(self):
        ''' Display the current map.
        Input None.
        Output None
        '''
        plt.imshow(self.current_map)

    def get_heading(self):
        ''' Returns the Direction of movement of the AUV in Degrees. The heading will be between 0-360.
                    With respect to the x and y axes of the map.
        Input None.
        Output the Direction of movement of the AUV in Degrees.
        '''
        # taking care of negative angle
        angle = np.degrees(self.vel_angle)
        return angle + 360 if angle < 0 else angle

    def set_course(self, _velocity, _duration):
        ''' Receive new values for the velocity and duration properties. Append the new values to the current ones
        Input- Velocity as tuple of lists.
        Duration as list of integers
        Output None.
        '''
        self.velocity.extend(_velocity)
        self.duration.extend(_duration)


    def time_step(self):
        ''' Propagate the simulation by one step (one second) if duration >0
        Input None.
        Output None.
        '''

        self.curr_velocity = np.array(self.velocity[0])
        self.vel_angle = np.arctan2(*self.curr_velocity)

        if self.vel_angle <0:
            self.vel_angle+=2*np.pi

        # Head of the sonar no needs to rotate
        self.initial_position += self.curr_velocity

        # rotate via angles update
        self.rotate()
        # sonar search
        self.get_sonar_fov()
        # update duration
        self.duration[0]-=1

    def rotate(self):
        y, x = self.initial_position

        # Left Sonar Calculation
        left_sonar_ang = self.vel_angle + self.sonar_angle
        right_sonar_ang = self.vel_angle - self.sonar_angle

        # Advance in Y,X axises from head
        rcos = self.radius * np.cos(left_sonar_ang)
        rsin = self.radius * np.sin(left_sonar_ang)
        self.left_sonar_p = np.array([y + rsin, rcos + x])

        # Right Sonar Calculation
        rcos = self.radius * np.cos(right_sonar_ang)
        rsin = self.radius * np.sin(right_sonar_ang)
        # Left sonar is minus - as result of inverse y axis
        self.right_sonar_p = np.array([y + rsin, rcos + x])

    def start(self):
        ''' Activate the simulation and run until duration has ended
        Input None.
        Output None.
        '''
        #TODO Possible Problem - Substraction isn't in time_step
        # sum the duration and make a while loop with a couter
        # the update will happen inside the step !!!
        while len(self.duration) != 0:
            if self.duration[0]==0:
                self.duration.pop(0)
                self.velocity.pop(0)
            else:
                self.time_step()
                self.display_map()


    def bubble_sort(self, lst):
        '''
        bubble sort implementation
        '''
        for i in range(len(lst)):
            for j in range(len(lst) -1 -i):
                if self.is_bigger(lst[j], lst[j+1]):
                   tmp = lst[j+1]
                   lst[j+1] = lst[j]
                   lst[j] = tmp
        return lst

    @staticmethod
    def is_bigger(p1, p2):
        '''
        sub routine which sorts via 2 keys
        '''
        if p1[1] > p2[1]:
            return True
        elif p1[1] == p2[1] and p1[0] > p2[0]:
            return True

        return False


