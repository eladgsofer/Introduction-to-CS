__author__ = 'Elad Sofer <elad.sofe@bgu.post.ac.il>'


import game_of_life_interface
import numpy as np
from matplotlib import pyplot as plt


class GameOfLife(game_of_life_interface.GameOfLife):
    FIGNUM = 0
    DEAD_BOOL = 0
    ALIVE_BOOL = 1
    ALIVE_VAL = 255
    DEAD_OR_ALIVE = [DEAD_BOOL, ALIVE_BOOL]
    PROB_MAPPER = {1: [0.5, 0.5], 2: [0.2, 0.8], 3: [0.8, 0.2]}

    def __init__(self, board_size, starting_position=1, rules='B3/S23'):
        #
        self.board_size = board_size
        self.nxn = tuple([self.board_size] * 2)
        self.edges = [0, self.board_size-1]
        # self.offset = tuple([(r,c) for c in r for r in range(3)])

        self.starting_position = starting_position
        self.position_mapper = {'1': self.__init_random_board,
                                '2': self.__init_random_board,
                                '3': self.__init_random_board,
                                '4': self.__init_gosper_glide,
                                '5': self.__init_pulsar,
                                '6': self.__init_grin,
                                '7': self.__init_test}

        self.rules = rules
        born, survive = self.rules.split('/')
        self.born = np.array([int(b) for b in born[1:]])
        self.survive = np.array([int(s) for s in survive[1:]])

        self.board  = np.zeros(shape=self.nxn, dtype=int)
        # board init
        self.position_mapper[str(self.starting_position)]()

    def neighbors_calc(self):
        neighbors_sum = np.zeros(
            shape=(self.board_size + 2, self.board_size + 2), dtype=int)

        for r_offset in range(3):
            for c_offset in range(3):
                if r_offset == 1 and c_offset == 1:
                    continue
                tmp_board = np.zeros((self.board_size + 2, self.board_size + 2),
                                     dtype=int)
                tmp_board[r_offset:r_offset + self.board_size,
                c_offset:c_offset + self.board_size] = self.board
                neighbors_sum += tmp_board

        return neighbors_sum[1:-1, 1:-1]

    def update(self):
        ''' This method updates the board game by the rules of the game.
        Input None.
        Output None.
        '''
        neighbors_sum = self.neighbors_calc()
        dead_neigh_sum = (self.board == self.DEAD_BOOL) * neighbors_sum
        alive_neigh_sum = (self.board == self.ALIVE_BOOL) * neighbors_sum

        alive_tb = np.isin(alive_neigh_sum, self.survive)
        dead_tb = np.isin(dead_neigh_sum, self.born)

        alive_tb = alive_tb*self.board

        self.board = (alive_tb+dead_tb)



    def save_board_to_file(self, file_name):
        ''' This method saves the current state of the game to a file. You should use Matplotlib for this.
        Input img_name donates the file name. Is a string, for example file_name = '1000.png'
        Output a file with the name that donates filename.
        '''
        plt.imsave(file_name, arr=self.board)


    def display_board(self):
        ''' This method displays the current state of the game to the screen. You can use Matplotlib for this.
        Input None.
        Output a figure should be opened and display the board.
        '''
        # plt.interactive(True)
        plt.show(plt.matshow(self.board, fignum=self.FIGNUM))
        # plt.show()

    def return_board(self):
        ''' This method returns a list of the board position. The board is a two-dimensional list that every
        cell donates if the cell is dead or alive. Dead will be donated with 0 while alive will be donated with 255.
        Input None.
        Output a list that holds the board with a size of size_of_board*size_of_board.
        '''
        return (self.board*self.ALIVE_VAL).tolist()

    def __init_pulsar(self):

        center = self.board_size//2

        ver_lines_x_indexes = [center-6, center-1,center+1,center+6]*2
        ver_lines_y_indexes = [center-4]*4 +[center+2]*4
        ver_start_points = zip(ver_lines_y_indexes, ver_lines_x_indexes)

        hor_lines_x_indexes = [center-4, center+2]*4
        hor_lines_y_indexes = [center-6]*2 + [center-1]*2 +[center+1]*2 + [center+6]*2
        hor_start_points = zip(hor_lines_y_indexes, hor_lines_x_indexes)

        for y, x in ver_start_points:
            self.board[y:y+3, x] = self.ALIVE_BOOL

        for y, x in hor_start_points:
            self.board[y,x:x+3] = self.ALIVE_BOOL

    def __init_gosper_glide(self):
        GOSPER_GLIDER_INDEXS = [(14, 10), (14, 11), (15, 10), (15, 11), (14, 20),
                                (15, 20), (16, 20), (13, 21), (17, 21), (12, 22),
                                (18, 22), (12, 23), (18, 23), (15, 24), (13, 25),
                                (17, 25), (15, 27), (11, 32), (15, 32)]
        for r,c in GOSPER_GLIDER_INDEXS:
            self.board[r,c] = self.ALIVE_BOOL

        self.board[10:12, 34] = self.ALIVE_BOOL
        self.board[15:17, 34] = self.ALIVE_BOOL
        self.board[12:14, 44] = self.ALIVE_BOOL
        self.board[12:14, 45] = self.ALIVE_BOOL
        self.board[14:17, 26] = self.ALIVE_BOOL
        self.board[12:15, 30] = self.ALIVE_BOOL
        self.board[12:15, 31] = self.ALIVE_BOOL

    def __init_grin(self):
        GRIN_INDEXES = [(5, 5), (5, 8), (6, 6), (6, 7)]
        for r,c in GRIN_INDEXES:
            self.board[r,c] = self.ALIVE_BOOL

    def __init_test(self):
        np.zeros(self.nxn)
        GRIN_INDEXES = [(1, 1), (1, 2), (1, 3)]
        for r,c in GRIN_INDEXES:
            self.board[r,c] = self.ALIVE_BOOL


    def __init_random_board(self):
        self.board = np.random.choice(self.DEAD_OR_ALIVE, size=self.nxn,
                                      p=self.PROB_MAPPER[self.starting_position])





if __name__ == '__main__':
    import time
    t1= time.time()
    a = GameOfLife(board_size=200, starting_position=1,
                   rules='B2/S0')
    for i in range(5):
        a.update()
        a.display_board()
    print (time.time()-t1)
    a.save_board_to_file('1000.png')

