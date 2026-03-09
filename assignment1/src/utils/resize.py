import cv2
import numpy as np

from cv2.typing import MatLike
from abc import ABC, abstractmethod

class ResizeStrategy(ABC):
        @abstractmethod
        def resize(self, image: MatLike, x: int, y: int)->MatLike:...

class ResizeNearest(ResizeStrategy):
        def __init__(self):
                pass

        def resize(self, image: MatLike, x: int, y: int) -> MatLike:
               modify_image = cv2.resize(image, (x,y), interpolation=cv2.INTER_NEAREST)

               return modify_image
        
class ResizeBilinear(ResizeStrategy):
        def __init__(self):
                pass
        def resize(self, image: MatLike, x: int, y: int) -> MatLike:
                modify_image = cv2.resize(image, (x,y), interpolation=cv2.INTER_LINEAR)

                return modify_image
        
class ResizeBicubic(ResizeStrategy):
        def __init__(self):
                pass
        def resize(self, image: MatLike, x: int, y: int) -> MatLike:
                modify_image = cv2.resize(image, (x,y), interpolation=cv2.INTER_CUBIC)

                return modify_image
