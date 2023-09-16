from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple

from pynput.mouse import Button


class ClickState(Enum):
    RELEASED = 0
    PRESSED = 1


@dataclass(slots=True)
class MouseEvent:
    position: Tuple[float, float]
    click: Optional[Button] = None
    click_state: Optional[ClickState] = None
    scroll_delta: Optional[Tuple[float, float]] = None
