def convert_move(field_x: int, field_y: int, target_x: int, target_y: int) -> int:
    diff_x = target_x - field_x
    diff_y = target_y - field_y

    if diff_x < 0:
        if diff_y < 0:
            if diff_x - diff_y == 0:
                move_type = 5 * 7 - diff_x - 1
            else:
                move_type = 62 + diff_y
        elif diff_y == 0:
            move_type = 6 * 7 - diff_x - 1
        else:
            if diff_y + diff_x == 0:
                move_type = 7 * 7 - diff_x - 1
            else:
                move_type = 61 + diff_y
    elif diff_x == 0:
        if diff_y < 0:
            move_type = 4 * 7 - diff_y - 1
        else:
            move_type = diff_y - 1
    else:
        if diff_y < 0:
            if diff_x + diff_y == 0:
                move_type = 3 * 7 + diff_x - 1
            else:
                move_type = 60 - diff_x
        elif diff_y == 0:
            move_type = 2 * 7 + diff_x - 1
        else:
            if diff_x - diff_y == 0:
                move_type = 7 + diff_x - 1
            else:
                move_type = 55 + diff_x

    return move_type


def move_type_to_diff(move_type: int) -> tuple[int, int]:
    if move_type < 7:
        diff_x = 0
        diff_y = move_type + 1
    elif move_type < 14:
        diff_x = move_type - 6
        diff_y = move_type - 6
    elif move_type < 21:
        diff_x = move_type - 13
        diff_y = 0
    elif move_type < 28:
        diff_x = move_type - 20
        diff_y = 20 - move_type
    elif move_type < 35:
        diff_x = 0
        diff_y = 27 - move_type
    elif move_type < 42:
        diff_x = 34 - move_type
        diff_y = 34 - move_type
    elif move_type < 49:
        diff_x = 41 - move_type
        diff_y = 0
    elif move_type < 56:
        diff_x = 48 - move_type
        diff_y = move_type - 48
    elif move_type < 58:
        diff_x = move_type - 55
        diff_y = 3 - diff_x
    elif move_type < 60:
        diff_y = 57 - move_type
        diff_x = 3 + diff_y
    elif move_type < 62:
        diff_x = 59 - move_type
        diff_y = - 3 - diff_x
    elif move_type < 64:
        diff_y = move_type - 61
        diff_x = diff_y - 3
    else:
        diff_y = 1
        if move_type < 67:
            diff_x = move_type - 65
        elif move_type < 70:
            diff_x = move_type - 68
        else:
            diff_x = move_type - 71

    return diff_x, diff_y
