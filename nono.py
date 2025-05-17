from typing import Generator, Tuple, Set, Optional

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

def rotate(current_rows: Tuple[str, ...]) -> Tuple[str, ...]:
    return tuple(''.join(row) for row in zip(*current_rows))

def update_grid(current_rows: Tuple[str, ...],
                row_hints: Tuple[Tuple[int, ...], ...],
                col_hints: Tuple[Tuple[int, ...], ...]) -> Tuple[str, ...]:
    updated_cols = tuple(update_row(col, hints)
                         for col, hints in zip(rotate(current_rows), col_hints))
    updated_rows = tuple(update_row(row, hints)
                         for row, hints in zip(rotate(updated_cols), row_hints))
    return updated_rows

def solve_grid(row_hints: Tuple[Tuple[int, ...], ...],
               col_hints: Tuple[Tuple[int, ...], ...],
               initial_rows: Optional[Tuple[str, ...]] = None) -> Tuple[str, ...]:
    width = len(col_hints)
    height = len(row_hints)

    current_rows = initial_rows or tuple(UNKNOWN * width for _ in range(height))
    unknown_count = width * height
    for _ in range(width * height):
        previous_unknown_count = unknown_count
        current_rows = update_grid(current_rows, row_hints, col_hints)
        unknown_count = sum(row.count(UNKNOWN) for row in current_rows)

        if unknown_count == previous_unknown_count:
            return current_rows
    return current_rows

def search(row_hints: Tuple[Tuple[int, ...], ...],
           col_hints: Tuple[Tuple[int, ...], ...],
           initial_rows: Optional[Tuple[str, ...]] = None)\
            -> Generator[Tuple[str, ...], None, None]:
    current_rows = solve_grid(row_hints, col_hints, initial_rows)
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
    yield from search(row_hints, col_hints, empty_guess_state)

    filled_guess_state = replace_at(current_rows, i, j, FILLED)
    yield from search(row_hints, col_hints, filled_guess_state)
