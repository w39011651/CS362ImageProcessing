import cv2
import ui

import matplotlib.pyplot as plt

from tkinter import filedialog
from cv2.typing import MatLike
from pathlib import Path
from abc import ABC
from typing import Any, Protocol, Iterable


from imageIO import photoRW
from roi import RoiSelector, RoiEllipseSelector, RoiRectSelector
from rotate import RotateStrategy, RotateAngle
from resize import ResizeStrategy, ResizeBicubic, ResizeBilinear, ResizeNearest

class ActionsProvider(Protocol):
        def open_file(self)-> MatLike:...
        def apply_roi(self, img: MatLike, pattern: str)->MatLike:...
        def apply_rotate(self, img: MatLike, pattern: str, angle:int)->MatLike:...
        def apply_resize(self, img: MatLike, pattern: str, x:int, y:int)->MatLike:...
        def save_file(self, img: MatLike):...
        def compare(self, img1: MatLike, img2: MatLike)->None:...

class ImagePipeline(ActionsProvider):
        def __init__(self):
                pass

        def open_file(self)->MatLike:
                file_path = filedialog.askopenfilename(
                        title="PleaseChooseImage",
                        filetypes=[("Image files", "*.jpg *.png *.jpeg"), ("All files", "*.*")],
                )
                file_path.replace('\\', '/')
                print(file_path)
                assert file_path is not None
                bgr = photoRW.read(file_path)
                assert bgr is not None
                return bgr
        
        def apply_roi(self, img: MatLike, pattern: str)->MatLike:
                #dependent on abstract
                ROI = ROIFactory.get_object_by_pattern(pattern)
                roi = ROI.run(img)
                return roi

        def apply_rotate(self, img: MatLike, pattern: str, angle:int)->MatLike:
                Rotate = RotateFactory.get_object_by_pattern(pattern)
                rotate = Rotate.rotate(img, angle)
                return rotate

        def apply_resize(self, img: MatLike, pattern: str, x:int, y:int)->MatLike:
                Resize = ResizeFactory.get_object_by_pattern(pattern)
                resize = Resize.resize(img, x, y)
                return resize
        
        def save_file(self, img: MatLike):
                path = filedialog.asksaveasfilename(
                        title="PleaseChooseImage",
                        filetypes=[("Image files", "*.jpg *.png *.jpeg"), ("All files", "*.*")],
                        defaultextension=".jpg",
                )
                if not path:
                        return

                output_path = Path(path)
                ext = output_path.suffix.lower()
                if ext not in {".jpg", ".jpeg", ".png"}:
                        output_path = output_path.with_suffix(".png")
                        ext = ".png"

                ok, buf = cv2.imencode(ext, img)
                if not ok:
                        return

                buf.tofile(output_path)

        def compare(self, img1: MatLike, img2: MatLike)->None:
                """
                Compare two images in the same window (with matplotlib)
                Args:
                        img1: images (before modify),
                        img2: images (after  modify)
                """
                if img1 is None or img2 is None:
                        return
                img1_rgb = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
                img2_rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
                plt.figure()
                plt.subplot(1, 2, 1)
                plt.imshow(img1_rgb)
                plt.title("before modify")
                plt.axis("off")
                plt.subplot(1,2,2)
                plt.imshow(img2_rgb)
                plt.title("after modify")
                plt.axis("off")

                plt.tight_layout()
                plt.show()


class Factory(ABC):
        options: Iterable[str]
        @classmethod
        def get_object_by_pattern(cls, pattern: str) -> Any:...


class ROIFactory(Factory):
        options = ["rect", "ellipse"]
        @classmethod
        def get_object_by_pattern(cls, pattern: str)->RoiSelector:
                if pattern == "ellipse":
                        return RoiEllipseSelector()
                return RoiRectSelector()
        
class ResizeFactory(Factory):
        options = ["Nearest", "Bicubic", "Bilinear"]
        @classmethod
        def get_object_by_pattern(cls, pattern: str)->ResizeStrategy:
                if pattern == "Nearest":
                        return ResizeNearest()
                elif pattern == "Bicubic":
                        return ResizeBicubic()
                return ResizeBilinear()#default
        
class RotateFactory(Factory):
        @classmethod
        def get_object_by_pattern(cls, pattern: str)->RotateStrategy:
                return RotateAngle()


if __name__ == '__main__':
         UI = ui.MainWindow(ImagePipeline(), ROIFactory.options, ResizeFactory.options)
         UI.run()