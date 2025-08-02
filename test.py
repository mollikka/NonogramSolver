import unittest

from nono import generate_valid_guesses, update_row, solve_grid, search, merge_results
from greedy import greedy_search
import fixtures

class TestHelperFunctions(unittest.TestCase):

    def test_generate_valid_guesses(self):
        self.assertEqual(set(generate_valid_guesses('???????????????', (10,))), 
                         {  '##########     ',' ##########    ',
                            '  ##########   ','   ##########  ',
                            '    ########## ', '     ##########'
                         })
        self.assertEqual(set(generate_valid_guesses('#####   ?????', (5,4))), 
                         {  '#####   #### ',
                            '#####    ####'
                         })
        self.assertEqual(set(generate_valid_guesses('?????', tuple())), {'     '})

    def test_update_row(self):
        self.assertEqual(update_row('??????????',tuple()), '          ')
        self.assertEqual(update_row('??????????',(10,)), '##########')
        self.assertEqual(update_row('??????????',(5,4)), '##### ####')
        self.assertEqual(update_row('??????????',(6,)), '????##????')
        self.assertEqual(update_row('???#?????#',(3,1,2)), ' ?##??? ##')
        self.assertEqual(update_row('???? #?????????',(2,3,4)), '???? ### ??##??')
        self.assertEqual(update_row('???? #??????????????',(2,3,4)), '???? ##?????????????')

class Testsolve_grid(unittest.TestCase):

    def test_solve_grid(self):

        self.assertEqual(solve_grid(fixtures.simple.rows, fixtures.simple.cols), fixtures.simple.solution)

        self.assertEqual(solve_grid(((5,),(2,1,),(5,),), ((3,),(3,),(1,1,),(1,1,),(3,),)), (
            '#####',
            '##  #',
            '#####'
        ))

        self.assertEqual(solve_grid(fixtures.apple.rows, fixtures.apple.cols), fixtures.apple.solution)

        self.assertEqual(solve_grid(fixtures.wikipedia.rows, fixtures.wikipedia.cols), fixtures.wikipedia.solution)

        self.assertEqual(solve_grid(fixtures.rose.rows, fixtures.rose.cols), fixtures.rose.solution)

        self.assertEqual(solve_grid(fixtures.duck.rows, fixtures.duck.cols), fixtures.duck.solution)
 
    def test_solve_grid_faulty(self):

        row_hints = ((5,),(1,1,),(1,1,),(1,),(5,),)
        col_hints = ((5,),(1,1,),(1,1,),(1,1,),(5,),)
        
        self.assertEqual(solve_grid(row_hints, col_hints), tuple())

    def test_solve_grid_first_round_finds_nothing(self):

        row_hints = ((),(5,),(),(),(),)
        col_hints = ((1,),(1,),(1,),(1,),(1,),)
        
        self.assertEqual(solve_grid(row_hints, col_hints), ('     ', '#####',  '     ', '     ', '     '))        
        self.assertEqual(solve_grid(col_hints, row_hints), (' #   ', ' #   ',  ' #   ', ' #   ', ' #   '))

    def test_solve_grid_indeterminate(self):

        row_hints = ((5,),(1,),(1,1,),(1,),(1,1,),)
        col_hints = ((5,),(1,),(1,1,),(1,),(1,1,),)
        
        self.assertEqual(solve_grid(row_hints, col_hints), (
            '#####',
            '#    ',
            '# ? ?',
            '#    ',
            '# ? ?'
        ))
    
    def test_solve_grid_multiline_reasoning(self):
        # https://puzzling.stackexchange.com/questions/129849/nonograms-that-require-more-than-single-line-logic
        # This is a case that requires multiline reasoning. Thus solve_grid will fail to solve it.
        self.assertEqual(solve_grid((
            (1,),(1,),(1,),(1,)
        ,), (
            (1,1,),
            (2,)
        ,)), 
        (
            '??',
            '??',
            '??',
            '??'
        ))

        self.assertEqual(solve_grid(
            fixtures.multiline.rows, 
            fixtures.multiline.cols), 
        ('?? ??',
         '?? ??',
         '     ',
         '?? ??',
         '?? ??'))
        
        self.assertEqual(solve_grid( (
            (1,),(2,),(2,),(2,1,),(1,1,)
        ,),
        (
            (2,),(2,),(2,),(2,),(2,)
        ,)), 
        ('  ?? ',
         '  ## ',
         '???? ',
         '##  #',
         '??  #'
        ))

class TestMergeResults(unittest.TestCase):
    def test_merge_results(self):
        result_a = ('###  ', '# ###', '#####', '#####', '#####')
        result_b = ('#### ', '#  ##', '#####', '# # #', '#####')
        combined = ('###? ', '# ?##', '#####', '#?#?#', '#####')
        self.assertEqual(tuple(merge_results([result_a,result_b])), combined)

        result_a = ('     ', '    #', '   ##', '  ###', ' ####')
        result_b = ('#####', ' ####', '  ###', '   ##', '    #')
        combined = ('?????', ' ???#', '  ?##', '  ?##', ' ???#')
        self.assertEqual(tuple(merge_results([result_a,result_b])), combined)

class TestSearch(unittest.TestCase):

    def test_search_multiline_reasoning(self):
        self.assertEqual(set(search( (
            (1,),(1,),(1,),(1,)
        ,), (
            (1,1,),
            (2,)
        ,))), 
        {(    
            '# ',
            ' #',
            ' #',
            '# ',)
        })

        self.assertEqual(set(search(
            fixtures.multiline.rows, 
            fixtures.multiline.cols)), 
        {fixtures.multiline.solution
        })
        
        self.assertEqual(set(search( (
            (2,2,),(2,2,),(3,),(3,),(3,),(2,2,),(2,2,)
        ,), (
            (2,2,),(2,2,),(3,),(3,),(3,),(2,2,),(2,2,)
        ,))), 
        {('##   ##', 
          '##   ##',
          '  ###  ', 
          '  ###  ',
          '  ###  ', 
          '##   ##', 
          '##   ##')
        })
        
        self.assertEqual(set(search( (
            (1,),(2,),(2,),(2,1,),(1,1,)
        ,),
        (
            (2,),(2,),(2,),(2,),(2,)
        ,))), 
        {('   # ',
          '  ## ', 
          ' ##  ', 
          '##  #', 
          '#   #')
        })

    def  test_search_multiline_reasoning_big(self):
        self.assertEqual(next(search( fixtures.galaxy.rows, fixtures.galaxy.cols)), fixtures.galaxy.solution)

    def test_search_indeterminate(self):
        # if the grid is indeterminate, search returns a set of more than one solution
        self.assertEqual(set(search(((1,),(1,),), ((1,),(1,),))), {(' #', '# '), ('# ', ' #')})
        
        self.assertEqual(set(search(((3,),(),(1,),(1,),(1,),), ((1,1,),(1,1,),(1,1,),))), 
                         {
                            ('###', '   ', '#  ', ' # ', '  #'), 
                            ('###', '   ', '#  ', '  #', ' # '),
                            ('###', '   ', ' # ', '#  ', '  #'),
                            ('###', '   ', ' # ', '  #', '#  '),
                            ('###', '   ', '  #', '#  ', ' # '),
                            ('###', '   ', '  #', ' # ', '#  '), 
                        })
        
        self.assertEqual(set(search(((1,1,),(1,1,),(1,1,),(1,1,),), ((1,1,),(1,1,),(1,1,),(1,1,),))), {
            (' # #', 
             '# # ',
             ' # #',
             '# # '), 

            ('# # ',
             ' # #',
             '# # ',
             ' # #')})
    
    def test_search_faulty(self):
        # if the grid is faulty, search returns an empty set
        
        self.assertEqual(set(search(fixtures.faulty.rows, fixtures.faulty.cols)), set())

class Testsolve_greedy(unittest.TestCase):

    def test_greedy_search(self):
        
        self.assertEqual(greedy_search(fixtures.simple.rows, fixtures.simple.cols), fixtures.simple.solution)

        self.assertEqual(greedy_search(fixtures.apple.rows, fixtures.apple.cols), fixtures.apple.solution)

        self.assertEqual(greedy_search(fixtures.duck.rows, fixtures.duck.cols), fixtures.duck.solution)
    def test_greedy_faulty(self):
        # if the grid is faulty, search returns None
        self.assertEqual(greedy_search(fixtures.faulty.rows, fixtures.faulty.cols), None)