from PIL import Image, ImageDraw
from typing import Tuple, Optional, List
from definitions import EMPTY, FILLED, UNKNOWN, Event
from solve import search, merge_results
from dfs import search as dfs_search
import fixtures

CELL_SIZE = 20
GRID_COLOR = (40, 40, 40)
ERROR_COLOR = (100, 0, 0)

COLORS_NORMAL = {
                FILLED: (0, 0, 0),
                EMPTY: (255, 255, 255),
                UNKNOWN: (100, 100, 100)
            }


COLORS_HIGHLIGHT = {
                FILLED: (50, 0, 0),
                EMPTY: (255, 200, 200),
                UNKNOWN: (200, 100, 100)
            }

def draw_frame(grid: Tuple[str, ...], highlightRow: Optional[int] = None, highlightCol: Optional[int] = None) -> Image.Image:
    height = len(grid)
    width = len(grid[0]) if height else 0
    image = Image.new('RGB', (max(1,width * CELL_SIZE), max(1,height * CELL_SIZE)), ERROR_COLOR)
    draw = ImageDraw.Draw(image)

    for j, row in enumerate(grid):
        for i, cell in enumerate(row):
            top_left = (i * CELL_SIZE, j * CELL_SIZE)
            bottom_right = ((i+1) * CELL_SIZE - 1, (j+1) * CELL_SIZE - 1)
            if (highlightRow == j or highlightCol == i):
                draw.rectangle([top_left, bottom_right], fill=COLORS_HIGHLIGHT[cell])
            else:
                draw.rectangle([top_left, bottom_right], fill=COLORS_NORMAL[cell])


    for j in range(0, height+1, 5):
        draw.line(((0, j * CELL_SIZE -1 ),(width*CELL_SIZE, j * CELL_SIZE-1)), GRID_COLOR, 2)

    for i in range(0, width+1, 5):
        draw.line(((i * CELL_SIZE-1, 0),(i * CELL_SIZE -1,height*CELL_SIZE)), GRID_COLOR, 2)

    return image

def save_gif(events: list[Event], frames: list[Image.Image], path: str):

    def get_duration(event: Event):
        if event == 'UPDATE':
            return 100
        if event == 'GUESS':
            return 1000
        if event == 'SOLVED':
            return 2000

    frames[0].save(path, save_all=True, append_images=frames[1:], duration=[get_duration(event) for event in events], loop=0)

def render_animation_solve(fixture: fixtures.Fixture, path: str):
    frames:List[Image.Image] = []
    events:List[Event] = []

    def append_frame(event: Event, grid: Tuple[str, ...], highlightRow: Optional[int] = None, highlightCol: Optional[int] = None):

        frame = draw_frame(grid, highlightRow, highlightCol)
        frames.append(frame)
        events.append(event)

    results = list(search(fixture.rows, fixture.cols, None, append_frame))
    if len(results) == 1:
        append_frame('SOLVED', results[0], None, None)
    if len(results) > 1:
        append_frame('SOLVED', merge_results(results), None, None)
    
    save_gif(events, frames, path)

def render_animation_dfs(fixture: fixtures.Fixture, path: str):
    frames:List[Image.Image] = []
    events:List[Event] = []

    def append_frame(event: Event, grid: Tuple[str, ...], highlightRow: Optional[int] = None, highlightCol: Optional[int] = None):
        frame = draw_frame(grid, highlightRow, highlightCol)
        frames.append(frame)
        events.append(event)

    result = dfs_search(fixture.rows, fixture.cols, None, append_frame)
    if result: append_frame('SOLVED', result, None, None)
    
    save_gif(events, frames, path)

if __name__ == '__main__':
    
    render_animation_solve(fixtures.indeterminate, 'indeterminate.gif')
    render_animation_solve(fixtures.multiline, 'multiline.gif')
    render_animation_solve(fixtures.faulty, 'faulty.gif')

    render_animation_solve(fixtures.chessboard, 'chessboard.gif')
    render_animation_solve(fixtures.apple, 'apple.gif')
    render_animation_solve(fixtures.wikipedia, 'wikipedia.gif')
    render_animation_solve(fixtures.rose, 'rose.gif')
    render_animation_solve(fixtures.galaxy, 'galaxy.gif')
    render_animation_solve(fixtures.duck, 'duck.gif')

    render_animation_dfs(fixtures.simple, 'simple_dfs.gif')
    render_animation_dfs(fixtures.apple, 'apple_dfs.gif')
    render_animation_dfs(fixtures.duck, 'duck_dfs.gif')    
