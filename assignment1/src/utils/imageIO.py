import cv2
import logging
import numpy as np

from typing import Protocol
from pathlib import Path
from os import PathLike

logger = logging.getLogger(__name__)

class ReadWriteInterface(Protocol):
        @classmethod
        def read(cls, path: str | PathLike[str] | None)->cv2.typing.MatLike | None:...
        @classmethod
        def write(cls, image: cv2.typing.MatLike, filename: PathLike[str] | str = "newPicture.jpg")->None:...
        @classmethod
        def show(cls, image: cv2.typing.MatLike ,windowsName: str = "pic", waittime: int = 0):
                cv2.imshow(windowsName, image)
                cv2.waitKey(waittime)
                cv2.destroyAllWindows()


class photoRW(Protocol):
        path: Path | None
        def __init__(self, path: str | PathLike[str]):
                if path is not None:
                        self.path = Path(path)
        @classmethod
        def read(cls, path: str | PathLike[str] | None)->cv2.typing.MatLike | None:
                try:
                        assert path is not None
                except AssertionError as e:
                        logger.error("The path of image is None, please retry.")
                        return None
                
                img_data = np.fromfile(path, dtype=np.uint8)
                img = cv2.imdecode(img_data, cv2.IMREAD_COLOR)
                
                if img is None:
                        logger.error("The image is None, please retry.")
                        return None
                
                return img
        @classmethod
        def write(cls, image: cv2.typing.MatLike, filename: PathLike[str] | str = "newPicture.jpg")->None:
                try:
                        cv2.imwrite(filename, image)
                except Exception as e:
                        logger.error(e)
                        logger.info("Write failed.")

                logger.info("Write Success.")

        @classmethod
        def show(cls, image: cv2.typing.MatLike ,windowsName: str = "pic", waittime: int = 0):
                cv2.imshow(windowsName, image)
                cv2.waitKey(waittime)
                cv2.destroyAllWindows()
