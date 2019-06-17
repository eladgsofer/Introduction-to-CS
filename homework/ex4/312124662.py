import auv_interface
import numpy as np
import matplotlib.pyplot as plt


class HydroCamel(auv_interface.Auv):
    FIGNUM=1
    SONAR_HEAD = 5
    HIDDEN_MINE = 6
    MINE_FOUND = 7
    SONAR_RADAR = 8
    #TODO REPLACE FORMULA - BETWEEN A AND C POINTS
    #TODO 45 DEGREES ANGLE PROBLEM
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
        ''' Returns the position of all the mines that the AUV has found.
        Input None.
        Output A list of tuples. Each tuple holds the coordinates (Yi , Xi) of found mines. The list should be sorted.
        '''
        return self.quicksort(self.found_mines)

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
        a, b, c = self.initial_position, self.left_sonar_p, self.right_sonar_p
        a_y, a_x = a
        b_y, b_x = b
        c_y, c_x = c

        for p_y, row in enumerate(self.mines_map):
            for p_x, cell_val in enumerate(row):
                if self.is_point_in_triangle(a,b,c, (p_y,p_x)):
                    found_points[(p_y,p_x)] = True
                    self.current_map[p_y, p_x] = self.SONAR_RADAR
                    if self.mines_map[p_y,p_x] == 1:
                        self.current_map[p_y, p_x] = self.MINE_FOUND
                        if (p_y, p_x) not in self.found_mines:
                            self.found_mines.append((p_y,p_x))

        self.current_map[a_y, a_x] = self.SONAR_HEAD
        self.prev_head = (a_y, a_x)
        return found_points

    @staticmethod
    def is_point_in_triangle(a, b, c, p):
        """ Handles a case where the denominator is 0 in the 'is_point_in_triangle_internal' function"""
        if c[0] - a[0] == 0:
            tmp = b
            b = c
            c = tmp
        return HydroCamel.is_point_in_triangle_internal(a, b, c, p)

    @staticmethod
    def is_point_in_triangle_internal(a, b, c, p):
        """ Receives a,b,c as the triangle vertices and determines if point p is inside that triangle
            I'm using an algorithm that was found online. """
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
        angle = np.degrees(self.vel_angle)
        if angle < 0:
            angle += 360
        return angle

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
        vel_vec = np.array(self.curr_velocity)
        self.vel_angle = np.arctan2(*vel_vec)
        # Head of the sonar no needs to rotate
        self.initial_position += vel_vec

        self.rotate()
        self.get_sonar_fov()

    def rotate(self):
        y, x = self.initial_position

        # Left Sonar Calculation
        left_sonar_ang = self.vel_angle + self.sonar_angle

        # Advance in Y,X axises from head
        rcos = self.radius * np.cos(left_sonar_ang)
        rsin = self.radius * np.sin(left_sonar_ang)
        self.left_sonar_p = np.array([y+rsin, rcos + x])

        # Right Sonar Calculation
        right_sonar_ang = self.sonar_angle - self.vel_angle

        rcos = self.radius * np.cos(right_sonar_ang)
        rsin = self.radius * np.sin(right_sonar_ang)
        # Left sonar is minus - as result of inverse y axis
        self.right_sonar_p = np.array([y - rsin, rcos + x])

    def start(self):
        ''' Activate the simulation and run until duration has ended
        Input None.
        Output None.
        '''

        for step_number_per_velocity, vel_vec in zip(self.duration, self.velocity):
            self.curr_velocity = vel_vec
            self.display_map()
            for step in range(step_number_per_velocity):
                self.time_step()
                self.display_map()
    @staticmethod
    def quicksort(lst):
        '''
        This function impliments the quicksort algorithm that we have learned in the class fitted into this code's requirements
        :param lst: a list to be sorted
        :return: a sorted list
        '''
        if len(lst) <= 1:
            return lst
        else:
            pivot = lst[0]
            smaller = [e for e in lst if HydroCamel.smaller_than(e, pivot)]
            equal = [pivot]
            greater = [e for e in lst if HydroCamel.smaller_than(pivot, e)]
        return HydroCamel.quicksort(smaller) + equal + HydroCamel.quicksort(greater)

    @staticmethod
    def smaller_than(a, b):
        '''
        Determine if tuple a is smaller than tuple b
        '''
        if a[1] < b[1]:
            return True
        elif a[1] == b[1] and a[0] < b[0]:
            return True
        else:
            return False

if __name__ == "__main__":
    # example 1
    map_size = (20, 15)
    mines = np.zeros(map_size).tolist()
    mines[16][6] = 1
    mines[12][4] = 1
    mines[14][10] = 1
    mines[17][11] = 1
    velocity = list()
    velocity.append([0, 1])
    sonar_range = 6
    sonar_angle = 60
    initial_position = (14, 1)
    duration = [8]

    game1 = HydroCamel(sonar_range, sonar_angle, map_size, initial_position, velocity, duration, mines)
    for i in range(0,7):
        game1.time_step()
        game1.display_map()
    sonar_res = game1.get_sonar_fov()
    game1.display_map()
    print(game1.get_mines())
    print(game1.get_sonar_fov())

    # example 2
    sonar_range = 5
    sonar_angle = 30
    map_size = (25, 20)
    initial_position = (10, 10)
    velocity = list()
    velocity.append([2, 2])
    velocity.append([-2, -2])
    velocity.append([0, 2])
    velocity.append([2, 0])
    duration = [2, 2, 2, 2]
    mines = np.random.choice([1, 0], map_size, p=[0.05, 0.95]).tolist()

    game2 = HydroCamel(sonar_range, sonar_angle, map_size, initial_position, velocity, duration, mines)
    game2.start()
    print(game2.get_mines())
    print(game2.get_sonar_fov())
