from typing import Generator, Tuple, Set, Optional

from functools import cache

FILLED = '#'
EMPTY = ' '
UNKNOWN = '?'

@cache
def generateValidGuesses(currentState: str, hints: Tuple[int, ...]) -> Set[str]:

    def recurse(guess: str, countTrailing: int, unusedHints: Tuple[int, ...]) -> Generator[str, None, None]:
        i = len(guess)-1
        currentHint = unusedHints[0] if unusedHints else None
        
        if guess and currentState[i] == FILLED and guess[i] == EMPTY: 
            return
        if guess and currentState[i] == EMPTY and guess[i] == FILLED: 
            return

        if len(currentState) == len(guess):
            if len(unusedHints) == 0 or len(unusedHints) == 1 and (countTrailing == currentHint):
                yield guess
            return

        if currentHint is not None and (countTrailing < currentHint):
            yield from recurse(guess+FILLED, countTrailing+1, unusedHints)
        if currentHint is None or countTrailing == 0 or (countTrailing == currentHint):
            yield from recurse(guess+EMPTY, 0, unusedHints[1:] if countTrailing == currentHint else unusedHints)

    return set(recurse('', 0, hints))

def updateState(currentState: str, hints: Tuple[int, ...]) -> str:
    validGuesses = generateValidGuesses(currentState, hints)

    def generateCellState(cellValues: Tuple[str, ...]) -> str:
        if all(value == FILLED for value in cellValues): return FILLED
        if all(value == EMPTY for value in cellValues): return EMPTY
        return UNKNOWN

    return ''.join(generateCellState(cell) for cell in zip(*validGuesses))

def rotate(grid: Tuple[str, ...]) -> Tuple[str, ...]:
    return tuple(''.join(row) for row in zip(*grid))

def updateGrid(currentRows: Tuple[str, ...], rowHints: Tuple[Tuple[int, ...], ...], colHints: Tuple[Tuple[int, ...], ...]) -> Tuple[str, ...]:
    updatedCols = tuple(updateState(col, tuple(hints)) for col, hints in zip(rotate(currentRows), colHints))
    updatedRows = tuple(updateState(row, tuple(hints)) for row, hints in zip(rotate(updatedCols), rowHints))
    return updatedRows

def solveGrid(rowHints: Tuple[Tuple[int, ...], ...], colHints: Tuple[Tuple[int, ...], ...], currentRows: Optional[Tuple[str, ...]] = None) -> Tuple[str, ...]:
    width = len(colHints)
    height = len(rowHints)

    currentRows = currentRows or tuple(UNKNOWN * width for _ in range(height))
    unknownCount = width * height
    for _ in range(width * height):
        previousUnknownCount = unknownCount
        currentRows = updateGrid(currentRows, rowHints, colHints)
        unknownCount = sum(row.count(UNKNOWN) for row in currentRows)

        if unknownCount == previousUnknownCount:
            return currentRows
    return currentRows

def search(rowHints: Tuple[Tuple[int, ...], ...], colHints: Tuple[Tuple[int, ...], ...], initialRows: Optional[Tuple[str, ...]] = None) -> Generator[Tuple[str, ...], None, None]:
    currentRows = solveGrid(rowHints, colHints, initialRows)
    if not currentRows: return

    def replaceAt(currentRows: Tuple[str, ...], x: int, y: int, newState: str) -> Tuple[str, ...]:
        return tuple(
            ''.join(currentRows[i][j] if (i != x or j != y) else newState for j in range(len(currentRows[i])))
            for i in range(len(currentRows))
        )

    def findFirstUnknown() -> Optional[Tuple[int, int]]:
        for i, row in enumerate(currentRows):
            for j, cell in enumerate(row):
                if cell == UNKNOWN:
                    return i, j
        return None

    unknown = findFirstUnknown()
    if unknown is None:
        yield currentRows
        return

    i, j = unknown

    emptyGuessState = replaceAt(currentRows, i, j, EMPTY)
    yield from search(rowHints, colHints, emptyGuessState)

    filledGuessState = replaceAt(currentRows, i, j, FILLED)
    yield from search(rowHints, colHints, filledGuessState)
