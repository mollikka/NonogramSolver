from PIL import Image, ImageDraw, ImageFont
from typing import Tuple, Optional, List
from definitions import EMPTY, FILLED, UNKNOWN, Event
from solve import search, merge_results
from dfs import search as dfs_search
import fixtures

FONT = ImageFont.load_default()

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
    image = Image.new('RGB', (max(1,width * CELL_SIZE+1), max(1,height * CELL_SIZE+1)), ERROR_COLOR)
    draw = ImageDraw.Draw(image)

    for j, row in enumerate(grid):
        for i, cell in enumerate(row):
            top_left = (i * CELL_SIZE, j * CELL_SIZE)
            bottom_right = ((i+1) * CELL_SIZE - 1, (j+1) * CELL_SIZE - 1)
            if (highlightRow == j or highlightCol == i):
                draw.rectangle([top_left, bottom_right], fill=COLORS_HIGHLIGHT[cell])
            else:
                draw.rectangle([top_left, bottom_right], fill=COLORS_NORMAL[cell])


    for j in range(0, height+1, 1):
        draw.line(((0, j * CELL_SIZE ),(width*CELL_SIZE, j * CELL_SIZE)), GRID_COLOR, 1)

    for i in range(0, width+1, 1):
        draw.line(((i * CELL_SIZE, 0),(i * CELL_SIZE,height*CELL_SIZE)), GRID_COLOR, 1)

    return image


def draw_frame_with_hints(
    grid: Tuple[str, ...],
    row_hints: Tuple[Tuple[int]],
    col_hints: Tuple[Tuple[int]],
    highlightRow: Optional[int] = None,
    highlightCol: Optional[int] = None
) -> Image.Image:
    height = len(grid)
    width = len(grid[0]) if height else 0

    max_row_hints_length = max(len(h) for h in row_hints) if row_hints else 0
    max_col_hints_length = max(len(h) for h in col_hints) if col_hints else 0

    left_margin = max_row_hints_length * CELL_SIZE
    top_margin = max_col_hints_length * CELL_SIZE

    grid_img = draw_frame(grid, highlightRow, highlightCol)

    img_width = left_margin + grid_img.width
    img_height = top_margin + grid_img.height
    image = Image.new("RGB", (img_width+1, img_height+1), COLORS_NORMAL[EMPTY])
    image.paste(grid_img, (left_margin, top_margin))

    draw = ImageDraw.Draw(image)

    for i, hints in enumerate(row_hints):
        for j, hint in enumerate(reversed(hints)):
            x = left_margin - (j + 0.5) * CELL_SIZE
            y = top_margin + (i + 1) * CELL_SIZE - 5
            draw.text((x, y), str(hint), font=FONT, fill=(0, 0, 0), anchor='ms')

    for i, hints in enumerate(col_hints):
        for j, hint in enumerate(reversed(hints)):
            x = left_margin + (i + 0.5) * CELL_SIZE
            y = top_margin - j * CELL_SIZE - 5
            draw.text((x, y), str(hint), font=FONT, fill=(0, 0, 0), anchor='ms')

    for j in range(0, height+1, 5):
        draw.line(((0, top_margin + j * CELL_SIZE ),(img_width, top_margin + j * CELL_SIZE)), GRID_COLOR, 3)

    for i in range(0, width+1, 5):
        draw.line(((left_margin+i * CELL_SIZE, 0),(left_margin+i * CELL_SIZE,img_height)), GRID_COLOR, 3)

    return image

def save_gif(events: list[Event], frames: list[Image.Image], path: str):

    def get_duration(event: Event):
        if event == 'UPDATE':
            return 100
        if event == 'GUESS':
            return 1000
        if event == 'SOLVED':
            return 10000
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=[get_duration(event) for event in events], loop=0)

def render_animation_solve(fixture: fixtures.Fixture, path: str):
    frames:List[Image.Image] = []
    events:List[Event] = []

    def append_frame(event: Event, grid: Tuple[str, ...], highlightRow: Optional[int] = None, highlightCol: Optional[int] = None):

        frame = draw_frame_with_hints(grid, fixture.rows, fixture.cols, highlightRow, highlightCol)
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

        frame = draw_frame_with_hints(grid, fixture.rows, fixture.cols, highlightRow, highlightCol)
        frames.append(frame)
        events.append(event)

    result = dfs_search(fixture.rows, fixture.cols, None, append_frame)
    if result: append_frame('SOLVED', result, None, None)
    
    save_gif(events, frames, path)

if __name__ == '__main__':
    
    render_animation_solve(fixtures.indeterminate, 'renders/indeterminate.gif')
    render_animation_solve(fixtures.multiline2, 'renders/multiline.gif')
    render_animation_solve(fixtures.faulty, 'renders/faulty.gif')

    render_animation_solve(fixtures.chessboard, 'renders/chessboard.gif')
    render_animation_solve(fixtures.apple, 'renders/apple.gif')
    render_animation_solve(fixtures.wikipedia, 'renders/wikipedia.gif')
    render_animation_solve(fixtures.rose, 'renders/rose.gif')
    render_animation_solve(fixtures.galaxy, 'renders/galaxy.gif')
    render_animation_solve(fixtures.duck, 'renders/duck.gif')

    render_animation_dfs(fixtures.simple, 'renders/simple_dfs.gif')
    render_animation_dfs(fixtures.apple, 'renders/apple_dfs.gif')
    render_animation_dfs(fixtures.duck, 'renders/duck_dfs.gif')    
