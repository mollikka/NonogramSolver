from typing import Generator, Tuple, Set, Optional

FILLED = '#'
EMPTY = ' '
UNKNOWN = '?'

def validateGuess(currentState: str, guess: str) -> bool:
    if len(guess) > len(currentState): return False
    for guessCell, stateCell in zip(guess, currentState):
        if stateCell == FILLED and guessCell != FILLED: return False
        if stateCell == EMPTY and guessCell != EMPTY: return False
    return True

def generateValidGuesses(currentState: str, hints: Tuple[int, ...]) -> Set[str]:
    def recurse(gaps: Tuple[int, ...]) -> Generator[str, None, None]:
        guess = "".join(((EMPTY * gap) + (FILLED * hint) for gap, hint in zip(gaps, hints)))

        if not validateGuess(currentState, guess): return

        if len(gaps) == len(hints):
            fullGuess = guess + (len(currentState) - len(guess)) * EMPTY
            if validateGuess(currentState, fullGuess): yield fullGuess
        else:
            minimumGap = 0 if len(gaps) == 0 else 1
            maximumGap = len(currentState) - sum(hints)
            for gapLength in range(minimumGap, maximumGap + 1):
                yield from recurse(gaps + (gapLength,))

    return set(recurse(tuple()))

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
    updatedCols = tuple(updateState(col, hints) for col, hints in zip(rotate(currentRows), colHints))
    updatedRows = tuple(updateState(row, hints) for row, hints in zip(rotate(updatedCols), rowHints))
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
