from typing import Generator, Tuple, Optional, Callable, Set

from functools import cache

FILLED = '#'
EMPTY = ' '
UNKNOWN = '?'

@cache
def generate_valid_guesses(current_row: str, row_hint: Tuple[int, ...]) -> Generator[str, None, None]:

    def recurse(guess: str, count_trailing: int, unused_hints: Tuple[int, ...])\
        -> Generator[str, None, None]:
        i = len(guess)-1
        current_hint = unused_hints[0] if unused_hints else None

        if guess and current_row[i] == FILLED and guess[i] == EMPTY:
            return
        if guess and current_row[i] == EMPTY and guess[i] == FILLED:
            return
        
        if len(current_row) == len(guess):
            if len(unused_hints) == 0 or \
                len(unused_hints) == 1 and (count_trailing == current_hint):
                yield guess
            return

        # optimization: exit early if the remaining hints take more space than is available
        if sum(unused_hints[1:]) + len(unused_hints) - 1 > len(current_row) - len(guess):
            return
        
        if current_hint is not None and (count_trailing < current_hint):
            yield from recurse(guess+FILLED, count_trailing+1, unused_hints)
        if current_hint is None or count_trailing == 0 or (count_trailing == current_hint):
            yield from recurse(guess+EMPTY, 0,
                               unused_hints[1:] if count_trailing == current_hint else unused_hints)

    return recurse('', 0, row_hint)

@cache
def update_row(current_row: str, row_hint: Tuple[int, ...]) -> str:
    
    # optimization: exit early in trivial case and cases where no progress can be made
    if len(row_hint) == 0: return EMPTY*len(current_row)
    if (current_row.count(UNKNOWN) == len(current_row)) and \
        (len(row_hint) + sum(row_hint) < len(current_row)/2):
        return current_row
    
    valid_guesses = generate_valid_guesses(current_row, row_hint)

    def generate_cell_state(cell_values: Tuple[str, ...]) -> str:
        if all(value == FILLED for value in cell_values):
            return FILLED
        if all(value == EMPTY for value in cell_values):
            return EMPTY
        return UNKNOWN

    return ''.join(generate_cell_state(cell) for cell in zip(*valid_guesses))

@cache
def rotate(current_rows: Tuple[str, ...]) -> Tuple[str, ...]:
    return tuple(''.join(row) for row in zip(*current_rows))

def update_rows(current_rows: Tuple[str, ...], 
                row_hints: Tuple[Tuple[int, ...], ...],
                rows_to_explore: Optional[Set[int]] = None,
                on_update: Optional[Callable[[Tuple[str, ...], int], None]] = None) -> Tuple[Tuple[str, ...], Set[int]]:

    updated_cols = set()
    for i, [row, hints] in enumerate(zip(current_rows, row_hints)):
        if rows_to_explore and (not i in rows_to_explore):
            continue

        new_row = update_row(row, hints)
        current_rows = current_rows[:i] + (new_row,) + current_rows[i+1:]
        if on_update: on_update(current_rows, i)
        updated_cols.update({i for i in range(len(new_row)) if row[i] != new_row[i]})

    return current_rows, updated_cols

def solve_grid(row_hints: Tuple[Tuple[int, ...], ...],
               col_hints: Tuple[Tuple[int, ...], ...],
               initial_rows: Optional[Tuple[str, ...]] = None, 
               on_update: Optional[Callable[[Tuple[str, ...], Optional[int], Optional[int]], None]] = None) -> Tuple[str, ...]:
    width = len(col_hints)
    height = len(row_hints)

    current_rows = initial_rows or tuple(UNKNOWN * width for _ in range(height))
    
    def on_update_row(current_rows: Tuple[str, ...], i: int):
        if on_update: on_update(current_rows, i, None)

    def on_update_col(current_rows: Tuple[str, ...], i: int):
        if on_update: on_update(rotate(current_rows), None, i)

    cols_to_explore = set(range(width))
    first_round = True

    for _ in range(width * height):
        if len(cols_to_explore) == 0: break
        current_cols = rotate(current_rows)
        current_cols, rows_to_explore = update_rows(current_cols, col_hints, cols_to_explore, on_update_col)
        current_rows = rotate(current_cols)
        if first_round: rows_to_explore = set(range(height))
        if len(rows_to_explore) == 0: break
        current_rows, cols_to_explore = update_rows(current_rows, row_hints, rows_to_explore, on_update_row)
    
        first_round = False

    if on_update: on_update(current_rows, None, None)
    return current_rows

def search(row_hints: Tuple[Tuple[int, ...], ...],
           col_hints: Tuple[Tuple[int, ...], ...],
           initial_rows: Optional[Tuple[str, ...]] = None,
           on_update: Optional[Callable[[Tuple[str, ...], Optional[int], Optional[int]], None]] = None)\
            -> Generator[Tuple[str, ...], None, None]:

    current_rows = solve_grid(row_hints, col_hints, initial_rows, on_update)
    if not current_rows:
        return

    def replace_at(current_rows: Tuple[str, ...], x: int, y: int, new_state: str)\
        -> Tuple[str, ...]:
        new_row = current_rows[x][:y] + new_state + current_rows[x][y+1:]
        return current_rows[:x] + (new_row,) + current_rows[x+1:]

    def find_first_unknown() -> Optional[Tuple[int, int]]:
        for i, row in enumerate(current_rows):
            j = row.find(UNKNOWN)
            if j != -1:
                return i,j
        return None

    unknown = find_first_unknown()
    if unknown is None:
        yield current_rows
        return

    i, j = unknown

    empty_guess_state = replace_at(current_rows, i, j, EMPTY)
    if on_update: on_update(empty_guess_state, i, j)
    yield from search(row_hints, col_hints, empty_guess_state, on_update)

    filled_guess_state = replace_at(current_rows, i, j, FILLED)
    if on_update: on_update(filled_guess_state, i, j)
    yield from search(row_hints, col_hints, filled_guess_state, on_update)
