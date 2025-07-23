from PIL import Image, ImageDraw
from typing import Tuple, Optional, List
from nono import FILLED, EMPTY, UNKNOWN, search, Event
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

def render_animation(fixture: fixtures.Fixture, path: str):
    frames:List[Image.Image] = []
    events:List[Event] = []

    def append_frame(event: Event, grid: Tuple[str, ...], highlightRow: Optional[int] = None, highlightCol: Optional[int] = None):

        frame = draw_frame(grid, highlightRow, highlightCol)
        frames.append(frame)
        events.append(event)

    for _ in search(fixture.rows, fixture.cols, None, append_frame):
        pass
    
    save_gif(events, frames, path)

if __name__ == '__main__':

    indeterminate = fixtures.Fixture(((5,),(1,),(1,1,),(1,),(1,1,),),
                    ((5,),(1,),(1,1,),(1,),(1,1,),),'')
    render_animation(indeterminate, 'indeterminate.gif')

    multiline_reasoning = fixtures.Fixture((
            (2,),(1,),(),(2,),(2,)
        ,), (
            (2,),(2,),(),(2,),(1,)
        ,),'')
    render_animation(multiline_reasoning, 'multiline.gif')

    faulty = fixtures.Fixture(((5,),(1,1,),(1,1,),(1,),(5,),),
                    ((5,),(1,1,),(1,1,),(1,1,),(5,),),'')
    render_animation(faulty, 'faulty.gif')

    render_animation(fixtures.chessboard, 'chessboard.gif')
    render_animation(fixtures.apple, 'apple.gif')
    render_animation(fixtures.wikipedia, 'wikipedia.gif')
    render_animation(fixtures.rose, 'rose.gif')
    render_animation(fixtures.galaxy, 'galaxy.gif')
