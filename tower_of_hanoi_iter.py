n = 0
towers = []


def build_tower():
    """ sets up the board """
    # fill first tower with disks, and other towers with zeros
    return tuple([row + 1 if tower == 0 else 0 for row in range(n)]
                 for tower in range(3))


def print_towers():
    """ helper method to visualize the towers """
    for i in range(n):
        print('%s\t%s\t%s'
              % (towers[0][i] or '', towers[1][i] or '', towers[2][i] or ''))
    print('=' * 18)  # separator


def top_disk(tower_index):
    """ gets the index and value of the disk at the top of a tower """
    # the top element is the first non-zero element in the towers array.
    tower = towers[tower_index]
    return next(((i, tower[i])
                 for i in range(n) if tower[i]), None)


def move(src_index, dest_index):
    """
    moves the top disk in 'src' tower to the 'dst' tower

    src_inex: index of the source tower (0, 1, or 2)
    dest_index: index of the destination tower (0, 1, or 2)
    """

    src_top = top_disk(src_index)
    dest_top = top_disk(dest_index)
    if src_top is None:
        return
    src_disk_index, src_disk_val = src_top
    dest_disk_index = dest_top[0] - 1 if dest_top is not None else n - 1

    towers[dest_index][dest_disk_index] = src_disk_val
    towers[src_index][src_disk_index] = 0

    print_towers()


def legal_move(tower_1, tower_2):
    """
    performs the legal move between 2 towers
    """
    t1_top_index, t1_top_val = top_disk(tower_1) or (None, None)
    t1_top_ind, t2_top_val = top_disk(tower_2) or (None, None)

    '''
    if 'tower_1' isn't empty and it's top disk is less than the top disk of 'tower_2',
    (or if 'tower_2' is empty)
    then a move is made from 'tower_1' to 'tower_2'
    otherwise, a move is made from 'towe_2' to 'tower_1'
    '''
    t1_top_ind, t1_top_val = top_disk(tower_1) or (None, 0)
    t2_top_ind, t2_top_val = top_disk(tower_2) or (None, 0)

    if t1_top_ind is not None and (t2_top_val == 0 or t1_top_val < t2_top_val):
        move(tower_1, tower_2)
    else:
        move(tower_2, tower_1)


def solve():
    """
    pure iterative method without the need of a stack
    """
    m = 2 ** n - 1  # the total moves needed to solve the puzzle
    disk_ind = n - 1  # bottom disk
    src_tower, dest_tower, tmp_tower = 0, 2, 1

    print_towers()
    if n % 2 == 0:
        _dest_tower = dest_tower
        dest_tower, tmp_tower = tmp_tower, _dest_tower
    for i in range(1, m + 1):
        print("Move %d:" % i)
        if i % 3 == 1:
            legal_move(src_tower, dest_tower)
        elif i % 3 == 2:
            legal_move(src_tower, tmp_tower)
        elif i % 3 == 0:
            legal_move(tmp_tower, dest_tower)
        else:
            print("Nothing")


n = max(0, int(input("Number of Disks: ")))
towers = build_tower()
solve()
