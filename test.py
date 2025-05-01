import unittest

from nono import validateGuess, generateValidGuesses, updateState, solveGrid

class TestHelperFunctions(unittest.TestCase):

    def test_validateGuess_valid(self):
        self.assertTrue(validateGuess('### ### ###', '### ### ###'))
        self.assertTrue(validateGuess('### ### ###', '### ##'))
        self.assertTrue(validateGuess('#????## ###', '### ### ###'))

    def test_validateGuess_invalid(self):
        self.assertFalse(validateGuess('### ### ###', ' ## ### ###'))
        self.assertFalse(validateGuess('### ### ###', ' ### ###'))
        self.assertFalse(validateGuess('#????## ###', '### ### ## '))

    def test_generateGuesses(self):
        self.assertEqual(generateValidGuesses('???????????????', [10]), 
                         {  '##########     ',' ##########    ',
                            '  ##########   ','   ##########  ',
                            '    ########## ', '     ##########'
                         })
        self.assertEqual(generateValidGuesses('#####   ?????', [5,4]), 
                         {  '#####   #### ',
                            '#####    ####'
                         })
        self.assertEqual(generateValidGuesses('?????', []), {'     '})

    def test_generateNewState(self):
        self.assertEqual(updateState('??????????',[]), '          ')
        self.assertEqual(updateState('??????????',[10]), '##########')
        self.assertEqual(updateState('??????????',[5,4]), '##### ####')
        self.assertEqual(updateState('??????????',[6]), '????##????')
        self.assertEqual(updateState('???#?????#',[3,1,2]), ' ?##??? ##')
        self.assertEqual(updateState('???? #?????????',[2,3,4]), '???? ### ??##??')
        self.assertEqual(updateState('???? #??????????????',[2,3,4]), '???? ##?????????????')

class TestUpdateGrid(unittest.TestCase):

    def test_updateGrid(self):

        self.assertEqual(solveGrid([[5],[1,1],[1,1],[1,1],[5]], [[5],[1,1],[1,1],[1,1],[5]]), [
            '#####',
            '#   #',
            '#   #',
            '#   #',
            '#####'
        ])

        self.assertEqual(solveGrid([[5],[2,1],[5]], [[3],[3],[1,1],[1,1],[3]]), [
            '#####',
            '##  #',
            '#####'
        ])

        # Japanilaiset Nonogram-ristikot 1/2025, sivu 4, "2. Lääkärin hedelmä"
        self.assertEqual(solveGrid([
            [1,5],
            [2,5],
            [6],
            [4,1],
            [6,4],
            [1,9],
            [2,11],
            [2,5,5],
            [2,1,6,2],
            [3,7,3],
            [11,3],
            [7,1,2],
            [8,2],
            [10],
            [6]
        ], [
            [5],
            [9],
            [2,5],
            [2,3,4],
            [5,6],
            [12],
            [2,11],
            [3,10],
            [1,3,3,3],
            [2,8,2],
            [3,7,1],
            [3,4,2],
            [3,8],
            [2,6],
            [1,2]
        ]), [
            '      #   #####',
            '      ## ##### ',
            '       ######  ',
            '  #### #       ',
            ' ###### ####   ',
            ' #  #########  ',
            '## ########### ',
            '## ##### ##### ',
            '## # ###### ## ',
            '### ####### ###',
            '########### ###',
            ' ####### #  ## ',
            ' ########  ##  ',
            '  ##########   ',
            '    ######     '
        ])

        # https://en.wikipedia.org/wiki/File:Nonogram_wiki.svg
        # Nonogram puzzle of the Wikipedia icon by Gus Polly at English Wikipedia
        self.assertEqual(solveGrid([
            [8,7,5,7],
            [5,4,3,3],
            [3,3,2,3],
            [4,3,2,2],
            [3,3,2,2],
            [3,4,2,2],
            [4,5,2],
            [3,5,1],
            [4,3,2],
            [3,4,2],
            [4,4,2],
            [3,6,2],
            [3,2,3,1],
            [4,3,4,2],
            [3,2,3,2],
            [6,5],
            [4,5],
            [3,3],
            [3,3],
            [1,1]
        ], [
            [1],
            [1],
            [2],
            [4],
            [7],
            [9],
            [2,8],
            [1,8],
            [8],
            [1,9],
            [2,7],
            [3,4],
            [6,4],
            [8,5],
            [1,11],
            [1,7],
            [8],
            [1,4,8],
            [6,8],
            [4,7],
            [2,4],
            [1,4],
            [5],
            [1,4],
            [1,5],
            [7],
            [5],
            [3],
            [1],
            [1]
        ]), [
            '######## ####### ##### #######',
            '  #####   ####    ###    ###  ',
            '   ###     ###    ##     ###  ',
            '   ####     ###   ##     ##   ',
            '    ###     ###  ##      ##   ',
            '    ###     #### ##     ##    ',
            '    ####     #####      ##    ',
            '     ###     #####      #     ',
            '     ####     ###      ##     ',
            '      ###     ####     ##     ',
            '      ####    ####    ##      ',
            '       ###   ######   ##      ',
            '       ###   ## ###   #       ',
            '       #### ### #### ##       ',
            '        ### ##   ### ##       ',
            '        ######   #####        ',
            '         ####    #####        ',
            '         ###      ###         ',
            '         ###      ###         ',
            '          #        #          '
        ])

    def test_updateGrid_faulty(self):

        rowHints = [[5],[1,1],[1,1],[1],[5]]
        colHints = [[5],[1,1],[1,1],[1,1],[5]]
        
        self.assertEqual(solveGrid(rowHints, colHints), [])

    def test_updateGrid_indeterminate(self):

        rowHints = [[5],[1],[1,1],[1],[1,1]]
        colHints = [[5],[1],[1,1],[1],[1,1]]
        
        self.assertEqual(solveGrid(rowHints, colHints), [
            '#####',
            '#    ',
            '# ? ?',
            '#    ',
            '# ? ?'
        ])