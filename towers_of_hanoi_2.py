from time import sleep

n = 8  # int(input("Number of disks: ")) # number of disks
moves_count = 0
move_delay = 0  # delay between moves. in seconds
towers = []


def start():
    """ sets up the board """
    global n, towers, move_count

    # fill first tower with disks, and other towers with zeros
    towers = tuple([row + 1 if tower == 0 else 0 for row in range(n)]
                   for tower in range(3))

    move_count = 0  # reset move count


def print_towers():
    """ helper method to visualize the board """
    global n, towers

    for i in range(n):
        print('%s\t%s\t%s'
              % (towers[0][i] or '', towers[1][i] or '', towers[2][i] or ''))
    print('=' * 18)  # separator


def top(src):
    """ gets the index and value of the disk at the top of a tower """
    global n, towers

    # check that the tower is valid
    assert src in range(3)
    # the top element is the first non-zero element in the towers array.
    return next(((i, towers[src][i])
                 for i in range(n) if towers[src][i]), (n, 0))


def move(src, dst):
    """
    moves the top disk in 'src' tower to the dst tower

    src: index of the source tower (0, 1, or 2)
    dst: index of the destination tower (0, 1, or 2)
    """
    global n, towers, moves_count, move_delay

    src_i, src_v = top(src)
    dst_i = top(dst)[0] - 1
    towers[dst][dst_i] = src_v
    towers[src][src_i] = 0
    moves_count += 1

    print_towers()
    sleep(move_delay)


def legal_move(src, dst):
    """
    performs the legal move between 2 towers
    """
    src_i, src_v = top(src)
    dst_i, dst_v = top(dst)

    '''
    if 'src' isn't empty and it's top disk is less than the top disk of 'dst',
    (or if dst is empty)
    then a move is made from 'src' to 'dst'
    otherwise, a move is made from 'dst' to 'src'
    '''
    if src_i < n and (src_v < dst_v or dst_i == n):
        move(src, dst)
    else:
        move(dst, src)


def solve_recur(ind, src, dst, tmp):
    """
    solves the game recursively

    ind: index of disk in the 'src' tower to move
    src: index of the source tower to move the disk from (0, 1, or 2)
    dst: index of the destination tower to move the disk to (0, 1, or 2)
    tmp: index the other tower to aid in the movement (0, 1, or 2)

    algorithm:
    1. if the disk to move is at the top, just move it directly
    2. if the disk isn't at the top:
       2.1. move the disks above to 'tmp', it is done by recursing from step 1
       2.2. move the disk, which is now at the top to 'dst'
       2.3. move the disks you move to 'tmp' to 'dst'
    """
    top_i, top_v = top(src)
    # 1. move disk to destination if it's at the top
    if ind == top_i:
        move(src, dst)
    else:
        tmp_i = top(tmp)[0] - 1
        # move disks at the top to the 'tmp' tower
        solve_recur(ind - 1, src, tmp, dst)
        # move current disk which is at the top to the 'dst' tower
        move(src, dst)
        # move the disks at 'tmp' to the 'dst' tower to complete migration
        solve_recur(tmp_i, tmp, dst, src)


def solve_iter_recur(ind, src, dst, tmp):
    """
    solves the game iteratively. it's similar to the recursive method,
    but the 'track' variable keeps track of the next move to make.

    ind: index of disk in the 'src' tower to move
    src: index of the source tower to move the disk from (0, 1, or 2)
    dst: index of the destination tower to move the disk to (0, 1, or 2)
    tmp: index the other tower to aid in the movement (0, 1, or 2)
    """
    moves_stack = [(ind, src, dst, tmp)]
    while moves_stack:
        # pick the move at the last position and remove it from the moves stack
        (ind, src, dst, tmp) = moves_stack.pop()

        top_i, top_v = top(src)  # get value at the top
        if ind == top_i:
            move(src, dst)
        else:
            tmp_i = top(tmp)[0] - 1
            '''
            because the parameters taking from 'track' is taken from the back,
            we have to add parameters this way:
            append this move A: [MOVE DISKS IN 'tmp' TO 'dst']
            append this move B: [MOVE DISK WHICH IS NOT AT TOP TO 'dst']
            append this move C: [MOVE DISK ABOVE TO 'tmp']
            so 'track' would look like:  [..., MOVE_A, MOVE_B, MOVE_C]

            because the moves are read from the back,
            it means MOVE_C is done first, then MOVE_B, then MOVE_A,
            which is the right order
            '''
            moves_stack.append((tmp_i, tmp, dst, src))
            moves_stack.append((ind, src, dst, tmp))
            moves_stack.append((ind - 1, src, tmp, dst))


def solve_iter(ind, src, dst, tmp):
    """
    pure iterative method without the need of a stack
    """
    # m is the total moves needed to solve the puzzle
    m = 2 ** n - 1

    if n % 2 == 0:
        _dst = dst
        dst = tmp
        tmp = _dst
    for i in range(1, m + 1):
        if i % 3 == 1:
            legal_move(src, dst)
        elif i % 3 == 2:
            legal_move(src, tmp)
        elif i % 3 == 0:
            legal_move(tmp, dst)


start()
print_towers()
solve_iter(n - 1, 0, 2, 1)  # n-1 is the index of the bottom disk
print("\nFinished with %d moves" % moves_count)
