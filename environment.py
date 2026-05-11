class MazeEnv:

    def __init__(self):

        self.size = 10

        self.goal = (9, 9)

        # стены
        self.walls = [

            (1,0),(1,1),(1,2),(1,3),

            (3,1),(3,2),(3,3),(3,4),

            (5,5),(5,6),(5,7),

            (7,2),(7,3),(7,4),(7,5),

            (8,7),(8,8)

        ]

        # ловушки
        self.traps = [

            (2,7),
            (4,8),
            (6,1),
            (7,8)

        ]

        self.reset()

    def reset(self):

        self.agent_pos = [0, 0]

        return self.get_state()

    def get_state(self):

        return self.agent_pos[0] * self.size + self.agent_pos[1]

    def step(self, action):

        x, y = self.agent_pos

        new_x, new_y = x, y

        # 0 up
        # 1 down
        # 2 left
        # 3 right

        if action == 0:
            new_x -= 1

        elif action == 1:
            new_x += 1

        elif action == 2:
            new_y -= 1

        elif action == 3:
            new_y += 1

        # проверка границ и стен
        if (
            0 <= new_x < self.size and
            0 <= new_y < self.size and
            (new_x, new_y) not in self.walls
        ):
            x, y = new_x, new_y

        self.agent_pos = [x, y]

        reward = -1

        done = False

        # ловушка
        if (x, y) in self.traps:

            reward = -50

        # цель
        if (x, y) == self.goal:

            reward = 500

            done = True

        return self.get_state(), reward, done