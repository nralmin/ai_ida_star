import copy


class Node:
    def __init__(self, state, h, g=0, parent=None):
        self.state = state
        self.parent = parent
        self.g = g
        self.h = h

    def is_goal(self):
        return self.h == 0

    def has_same_config_with(self, node2):
        return self.state == node2.state

    def generate_successor_states(self):
        s_list = []

        sorted_state = self._sort_state_by_coordinate()
        blank_pos = find_blank_pos(sorted_state)

        self._check_below_tile(blank_pos, sorted_state, s_list)
        self._check_above_tile(blank_pos, sorted_state, s_list)
        self._check_right_tile(blank_pos, sorted_state, s_list)
        self._check_left_tile(blank_pos, sorted_state, s_list)

        return s_list

    def is_already_expanded(self, closed_list):
        for node in closed_list:
            if self.has_same_config_with(node):
                return True
        return False

    def _sort_state_by_coordinate(self):
        return sorted(self.state.items(), key=lambda v: v[1])

    def _check_below_tile(self, blank_pos, sorted_state, s_list):
        below_tile_pos = blank_pos + N
        if below_tile_pos < N * N:
            s_list.append(self._move_tile(sorted_state[below_tile_pos][0]))

    def _check_above_tile(self, blank_pos, sorted_state, s_list):
        above_tile_pos = blank_pos - N
        if above_tile_pos >= 0:
            s_list.append(self._move_tile(sorted_state[above_tile_pos][0]))

    def _check_right_tile(self, blank_pos, sorted_state, s_list):
        right_tile_pos = blank_pos + 1
        if right_tile_pos % N != 0:
            s_list.append(self._move_tile(sorted_state[right_tile_pos][0]))

    def _check_left_tile(self, blank_pos, sorted_state, s_list):
        left_tile_pos = blank_pos - 1
        if blank_pos % N != 0:
            s_list.append(self._move_tile(sorted_state[left_tile_pos][0]))

    def _move_tile(self, tile):
        new_state = copy.deepcopy(self.state)
        swap_tiles(new_state, tile)
        return new_state


def is_blank(tile):
    return tile == '_'


def find_blank_pos(sorted_state):
    try:
        return next(i for i in range(
            len(sorted_state)) if is_blank(sorted_state[i][0]))
    except StopIteration:
        print("board does not have a blank space.")
        raise


def swap_tiles(config, tile1, tile2='_'):
    config[tile1], config[tile2] = config[tile2], config[tile1]


def compute_manhattan_distance(c1, c2):
    return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])


def compute_h(config):
    heuristic = 0

    for c in config:
        if is_blank(c):
            continue
        heuristic += compute_manhattan_distance(GOAL_CONFIG[c], config[c])

    return heuristic


def print_config_2d_list(config):
    for i in range(N):
        print(*config[i])


def print_config(config):
    sorted_dict = sorted(config.items(), key=lambda v: v[1])
    board_2d_list = [[sorted_dict[j * N + i][0]
                      for i in range(N)] for j in range(N)]

    print_config_2d_list(board_2d_list)


def find_node_with_lowest_f(open_list):
    min_f = open_list[0].h + open_list[0].g
    index = 0

    for i in range(1, len(open_list)):
        curr_f = open_list[i].h + open_list[i].g
        if curr_f < min_f:
            index = i
            min_f = curr_f

    return index


def print_configs_along_path(goal_node):
    path = [goal_node]
    parent_node = goal_node.parent

    while parent_node:
        path.append(parent_node)
        parent_node = parent_node.parent

    for node in path[:0:-1]:
        print_config(node.state)
        print()
    print_config(path[0].state)


def violates_cost_limit(f):
    return f > MAX_COST


def generate_new_nodes(node, successors):
    new_nodes = []

    for s in successors:
        h = compute_h(s)
        g = node.g + 1
        if not violates_cost_limit(h + g):
            new_nodes.append(Node(s, h, g, node))

    return new_nodes


def a_star_search():
    h = compute_h(INIT_CONFIG)
    init_node = Node(INIT_CONFIG, h)

    explored = []
    frontier = [init_node]

    while frontier:
        min_f_index = find_node_with_lowest_f(frontier)
        curr_node = frontier.pop(min_f_index)

        if curr_node.is_goal():
            print("SUCCESS\n")
            print_configs_along_path(curr_node)
            return

        if curr_node.is_already_expanded(explored):
            continue

        successors_list = curr_node.generate_successor_states()
        frontier.extend(generate_new_nodes(curr_node, successors_list))

        explored.append(curr_node)

    print("FAILURE")
    return


def ida_star_search():
    fmax = compute_h(INIT_CONFIG)
    init_node = Node(INIT_CONFIG, fmax)

    path = [init_node]
    while True:
        t = search(path, fmax)
        if t == "SUCCESS":
            print(t + "\n")
            curr_node = path.pop()
            print_configs_along_path(curr_node)
            return
        if t > MAX_COST:
            print("FAILURE")
            return
        fmax = t


def search(path, fmax):
    node = path[-1]
    f = node.g + node.h

    if f > fmax or f > MAX_COST:
        return f
    if node.is_goal():
        return "SUCCESS"
    minf = MAX_COST + 1

    successor_states_list = node.generate_successor_states()

    for s in successor_states_list:
        node_successor = Node(s, compute_h(s), node.g + 1, node)

        if node_successor.is_already_expanded(path):
            continue

        path.append(node_successor)
        t = search(path, fmax)
        if t == "SUCCESS":
            return t
        if t < minf:
            minf = t
        path.pop()

    return minf


def read_config_from_stdin():
    # return [input().split(' ') for _ in range(N)]
    config = {}

    for i in range(N):
        tile_positions = [(i, y) for y in range(N)]
        tile_numbers = input().split(' ')
        new_row = zip(tile_numbers, tile_positions)

        config.update(new_row)

    return config


def solve_the_puzzle():
    if SEARCH_METHOD == "A*":
        a_star_search()
    else:
        ida_star_search()


if __name__ == "__main__":
    # read task parameters from standard input
    # their values remain constant throughout the program
    SEARCH_METHOD = input()
    MAX_COST = int(input())
    N = int(input())  # board dimension

    INIT_CONFIG = read_config_from_stdin()
    GOAL_CONFIG = read_config_from_stdin()

    solve_the_puzzle()
