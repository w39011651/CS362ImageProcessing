import cv2
import logging

from pathlib import Path
from os import PathLike

logger = logging.getLogger(__name__)

class photoRW:
        path: Path | None
        def __init__(self, path: str | PathLike[str]):
                self.path = Path(path)

        def read(self, path: str | PathLike[str] | None)->cv2.typing.MatLike | None:
                if path is not None:
                        self.path = Path(path)
                try:
                        assert self.path is not None
                except AssertionError as e:
                        logger.error("The path of image is None, please retry.")
                        return None
                
                img = cv2.imread(self.path)
                
                if img is None:
                        logger.error("The image is None, please retry.")
                        return None
                
                return img

        def write(self, image: cv2.typing.MatLike, filename: PathLike[str] | str = "newPicture.jpg")->None:
                try:
                        cv2.imwrite(filename, image)
                except Exception as e:
                        logger.error(e)
                        logger.info("Write failed.")

                logger.info("Write Success.")

        def show(self, image: cv2.typing.MatLike ,windowsName: str = "pic", waittime: int = 0):
                cv2.imshow(windowsName, image)
                cv2.waitKey(waittime)
                cv2.destroyAllWindows()