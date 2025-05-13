FILLED = '#'
EMPTY = ' '
UNKNOWN = '?'

def validateGuess(currentState, guess):

    if len(guess) > len(currentState): return False
    for guessCell,stateCell in zip(guess, currentState):
        if stateCell == FILLED and guessCell != FILLED: return False
        if stateCell == EMPTY and guessCell != EMPTY: return False
    return True

def generateValidGuesses(currentState, hints):

    def recurse(gaps):
        guess = "".join(((EMPTY*gap)+(FILLED*hint) for gap,hint in zip(gaps,hints)))

        if not validateGuess(currentState, guess): return

        if len(gaps) == len(hints):
            fullGuess = guess + (len(currentState)-len(guess))*EMPTY
            if validateGuess(currentState, fullGuess): yield fullGuess

        else:
            minimumGap = 0 if len(gaps) == 0 else 1
            maximumGap = len(currentState) - sum(hints)
            for gapLength in range(minimumGap, maximumGap+1):
                yield from recurse(gaps+(gapLength,))

    return set(recurse(tuple()))

def updateState(currentState, hints):

    validGuesses = generateValidGuesses(currentState, tuple(hints))

    def generateCellState(cellValues):
        if all(value == FILLED for value in cellValues): return FILLED
        if all(value == EMPTY for value in cellValues): return EMPTY
        return UNKNOWN
    
    return ''.join(generateCellState(cell) for cell in zip(*validGuesses))

def rotate(grid):
    return tuple(''.join(row) for row in zip(*grid))

def updateGrid(currentRows, rowHints, colHints):

    updatedCols = tuple(updateState(col, hints) for col,hints in zip(rotate(currentRows), colHints))
    updatedRows = tuple(updateState(row, hints) for row,hints in zip(rotate(updatedCols), rowHints))

    return updatedRows

def solveGrid(rowHints, colHints, currentRows = None):
    width = len(colHints)
    height = len(rowHints)

    currentRows = currentRows or tuple(UNKNOWN*width for row in range(height))
    unknownCount = width*height
    for i in range(width*height):
        previousUnknownCount = unknownCount
        currentRows = updateGrid(currentRows, rowHints, colHints)
        unknownCount = sum(row.count(UNKNOWN) for row in currentRows)
        
        if unknownCount == previousUnknownCount:
            return currentRows
        
    return currentRows

def search(rowHints, colHints, initialRows = None):
    currentRows = solveGrid(rowHints, colHints, initialRows)
    if len(currentRows) == 0: return currentRows

    def replaceAt(currentRows, x, y, newState):
        return tuple(
            tuple(currentRows[i][j] if (i!=x or j!=y) else newState for j in range(len(currentRows[i])) )
              for i in range(len(currentRows)))

    def findFirstUnknown():
        for i in range(len(currentRows)):
            for j in range(len(currentRows[i])):
                if currentRows[i][j] == UNKNOWN:
                    return i,j

    unknown = findFirstUnknown()

    if unknown is None:
        yield tuple(currentRows)
        return

    i,j = unknown

    emptyGuessState = replaceAt(currentRows, i, j, EMPTY)
    emptyGuessSolved = search(rowHints, colHints, emptyGuessState)

    yield from emptyGuessSolved
   
    filledGuessState = replaceAt(currentRows, i, j, FILLED)
    filledGuessSolved = search(rowHints, colHints, filledGuessState)
    
    yield from filledGuessSolved