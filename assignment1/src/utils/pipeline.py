import cv2
import ui

from tkinter import filedialog
from cv2.typing import MatLike

from utils.io import photoRW
from utils.roi import RoiSelector
from utils.rotate import RotateStrategy
from utils.resize import ResizeStrategy


class ImagePipeline(ui.ActionsProvider):
        def __init__(self):
                pass

        def apply_roi(self, img: MatLike, ROI: RoiSelector)->MatLike:
                #dependent on abstract
                roi = ROI.run(img)
                return roi


        def apply_rotate(self, img: MatLike, Rotate: RotateStrategy, angle:int)->MatLike:
                rotate = Rotate.rotate(img, angle)
                return rotate

        def apply_resize(self, img: MatLike, Resize: ResizeStrategy, x:int, y:int)->MatLike:
                resize = Resize.resize(img, x, y)
                return resize
        
        def open_file(self) -> str:
                file_path = filedialog.askopenfilename(
                        title="PleaseChooseImage",
                        filetypes=[("Image files", "*.jpg *.png *.jpeg"), ("All files", "*.*")],
                )
                
                return file_path


if __name__ == '__main__':
        UI = ui.MainWindow(ImagePipeline())
        UI.run()