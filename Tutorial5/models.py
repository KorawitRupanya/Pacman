import arcade.key

DIR_STILL = 0
DIR_UP = 1
DIR_RIGHT = 2
DIR_DOWN = 3
DIR_LEFT = 4
MOVEMENT_SPEED = 4

KEY_MAP = { arcade.key.UP: DIR_UP,
            arcade.key.DOWN: DIR_DOWN,
            arcade.key.LEFT: DIR_LEFT,
            arcade.key.RIGHT: DIR_RIGHT, }
 
DIR_OFFSETS = { DIR_STILL: (0,0),
                DIR_UP: (0,1),
                DIR_RIGHT: (1,0),
                DIR_DOWN: (0,-1),
                DIR_LEFT: (-1,0) }

class Pacman:
    def __init__(self, world, x, y, maze, block_size):
        self.world = world
        self.x = x
        self.y = y
        self.direction = DIR_STILL
        self.maze = maze
 
        self.block_size = block_size
        self.next_direction = DIR_STILL
    
    def is_at_center(self):
        half_size = self.block_size // 2
        return (((self.x - half_size) % self.block_size == 0) and
                ((self.y - half_size) % self.block_size == 0))
 
    def move(self, direction):
        self.x += MOVEMENT_SPEED * DIR_OFFSETS[direction][0]
        self.y += MOVEMENT_SPEED * DIR_OFFSETS[direction][1]

    def check_walls(self,direction):
        new_r = DIR_OFFSETS[direction][1]+self.get_row()
        new_c = DIR_OFFSETS[direction][0]+self.get_col()
        return not self.maze.has_wall_at(new_r, new_c)
 
    def check_dots(self):
        if self.maze.has_dot_at(self.get_row(),self.get_col()) :
            self.maze.remove_dot_at(self.get_row(),self.get_col())
            self.world.increase_score()
 
    def update(self, delta):
        if self.is_at_center():
            if self.check_walls(self.next_direction):
                self.direction = self.next_direction
            else:
                self.direction = DIR_STILL
 
        self.move(self.direction)
 
        if self.is_at_center():
            self.check_dots()
    
    def get_row(self):
        return (self.y - self.block_size) // self.block_size
 
    def get_col(self):
        return self.x // self.block_size

class World:
    def __init__(self, width, height, block_size):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.maze = Maze(self)
 
        self.pacman = Pacman(self, 60, 100,
                             self.maze,
                             self.block_size)
        
        self.score = 0

    def on_key_press(self, key, key_modifiers):
        if key in KEY_MAP:
            self.pacman.next_direction = KEY_MAP[key]

    def increase_score(self):
        self.score += 1

    def update(self, delta):
        self.pacman.update(delta)
    
class Maze:
    def __init__(self, world):
        self.map = [ '####################',
                     '#..................#',
                     '#.###.###..###.###.#',
                     '#.#...#......#...#.#',
                     '#.#.###.####.###.#.#',
                     '#.#.#..........#.#.#',
                     '#.....###..###.....#',
                     '#.#.#..........#.#.#',
                     '#.#.###.####.###.#.#',
                     '#.#...#......#...#.#',
                     '#.###.###..###.###.#',
                     '#..................#',
                     '####################' ]
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.init_dot_data()
 
    def init_dot_data(self):
        has_dot = {}
        for r in range(self.height):
            has_dot[r] = {}
            for c in range(self.width):
                has_dot[r][c] = self.map[r][c] == '.'
        self.has_dot = has_dot
 
    def has_wall_at(self, r, c):
        return self.map[r][c] == '#'
    
    def has_dot_at(self, r, c):
        return self.has_dot[r][c]
    
    def remove_dot_at(self, r, c):
        self.has_dot[r][c] = False
 
    def update(self, delta):
        self.pacman.update(delta)