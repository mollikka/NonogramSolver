
from typing import Tuple, Optional
from definitions import EMPTY, FILLED, UNKNOWN, OnUpdateFunc
from functools import cache

@cache
def count_streaks(row):
    streaks = []
    count = 0
    for c in row:
        if c == FILLED:
            count += 1
        else:
            if count: streaks.append(count)
            count = 0
    if count:
        streaks.append(count)
    return tuple(streaks)

@cache
def is_valid_line(row: str, hint: Tuple[int, ...]) -> bool:
    return count_streaks(row) == hint

@cache
def is_partial_line_valid(row: str, hint: Tuple[int, ...], width: int) -> bool:
    blocks = count_streaks(row)

    if len(blocks) > len(hint):
        return False

    last_block_is_done = row[-1] == EMPTY

    for i, block in enumerate(blocks):
        if block > hint[i]:
            return False
        if last_block_is_done and block < hint[i]:
            return False

    blocks_left = hint[len(blocks):]

    if len(blocks_left) == 0:
        return True

    if width - len(row) < len(blocks_left)-1 + sum(blocks_left):
        return False
    
    return True

def search(row_hints: Tuple[Tuple[int, ...], ...],
                  col_hints: Tuple[Tuple[int, ...], ...],
                  initial_rows: Optional[Tuple[str, ...]] = None,
                  on_update: Optional[OnUpdateFunc] = None) -> Optional[Tuple[str, ...]]:
    width = len(col_hints)
    height = len(row_hints)

    if initial_rows:
        i = len(initial_rows)-1
        last_row = initial_rows[i]
        j = len(last_row)-1
        last_col = "".join(row[j] for row in initial_rows)

        if on_update: on_update(
                'UPDATE', 
                tuple("".join(initial_rows[i][j] if (len(initial_rows) > i and len(initial_rows[i]) > j) else UNKNOWN
                            for j in range(height)
                            ) for i in range(width)),
             i, j)

        row_hint = row_hints[i]
        col_hint = col_hints[j]

        if len(last_row) == width and not is_valid_line(last_row, row_hint): return None
        if len(last_col) == height and not is_valid_line(last_col, col_hint): return None

        if len(last_row) < width and not is_partial_line_valid(last_row, row_hint, width): return None
        if len(last_col) < height and not is_partial_line_valid(last_col, col_hint, height): return None

        if len(last_row) == width and len(last_col) == height:
            return initial_rows
        
        if len(last_row) == width:
            return search(row_hints, col_hints, initial_rows + (FILLED,), on_update) or search(row_hints, col_hints, initial_rows + (EMPTY,), on_update)
        else:
            return search(row_hints, col_hints, initial_rows[:-1] + (last_row+FILLED,), on_update) or search(row_hints, col_hints, initial_rows[:-1] + (last_row+EMPTY,), on_update)
    else:
        return search(row_hints, col_hints, (FILLED,), on_update) or search(row_hints, col_hints, (EMPTY,), on_update)
    
