from typing import Literal, Callable, Tuple, Optional

FILLED = '#'
EMPTY = ' '
UNKNOWN = '?'

Event = Literal['SOLVED', 'UPDATE', 'GUESS']

OnUpdateFunc = Callable[[Event, Tuple[str, ...], Optional[int], Optional[int]], None]
