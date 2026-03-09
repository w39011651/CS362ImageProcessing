import cv2
import ui

from tkinter import filedialog

class ImagePipeline(ui.ActionsProvider):
        def __init__(self):
                pass

        def apply_roi(self):
                ...

        def apply_rotate(self):
                ...

        def apply_resize(self):
                ...
        
        def open_file(self) -> str:
                file_path = filedialog.askopenfilename(
                        title="PleaseChooseImage",
                        filetypes=[("Image files", "*.jpg *.png *.jpeg"), ("All files", "*.*")],
                )
                return file_path


if __name__ == '__main__':
        UI = ui.MainWindow(ImagePipeline())
        UI.run()