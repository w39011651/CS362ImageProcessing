import tkinter as tk
import cv2
import numpy as np

from PIL import Image, ImageTk
from pathlib import Path
from tkinter import filedialog
from typing import Protocol
from os import PathLike
from cv2.typing import MatLike

from roi import RoiSelector, RoiRectSelector, RoiEllipseSelector
from resize import ResizeStrategy
from rotate import RotateStrategy

class ActionsProvider(Protocol):
        def open_file(self)-> str:...
        def apply_roi(self, img: MatLike, ROI: RoiSelector)->MatLike:...
        def apply_rotate(self, img: MatLike, Rotate: RotateStrategy, angle:int)->MatLike:...
        def apply_resize(self, img: MatLike, Resize: ResizeStrategy, x:int, y:int)->MatLike:...

class EventActionProvider(ActionsProvider):
        def open_file(self)->str:
                file_path = filedialog.askopenfilename(
                        title="PleaseChooseImage",
                        filetypes=[("Image files", "*.jpg *.png *.jpeg"), ("All files", "*.*")],
                )
                file_path.replace('\\', '/')
                print(file_path)
                return file_path

        
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


class MainWindow:
        window: tk.Tk
        img: MatLike | None = None
        def __init__(
                self,
                actions: ActionsProvider,
                window_name: str = "MainWindow",
                window_width: int = 900,
                window_height: int = 600,
        ) -> None:
                ###UI Init
                self.window = tk.Tk()
                self.window.title(window_name)
                self.window.geometry(f"{window_width}x{window_height}")
                self.window.resizable(False, False)
                #self.preview_label = tk.Label(self.window, width = 400, height = 400)

                ###Dependency Injection
                self.actions = actions

                ###Build other parts
                self._build_layout()
                self.filemenu.add_command(label="Open", command=self._on_open)
        
        def _show_image(self, path:PathLike[str] | str):
                img_data = np.fromfile(path, dtype=np.uint8)
                bgr = cv2.imdecode(img_data, cv2.IMREAD_COLOR)
                assert bgr is not None

                self.img = bgr

                rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(rgb)
                img = img.resize((400, 400))

                self._photo = ImageTk.PhotoImage(img)
                self.preview_label.config(image = self._photo, text="")


        def _on_open(self)->None:
                path = self.actions.open_file()
                if not path:
                        return
                
                self._show_image(Path(path))
                self._set_roi_controls_state(enabled=True)


        def _on_roi_click(self) -> None:
                if self.img is None:
                        return
                self._set_roi_controls_state(enabled=True)


        def _on_roi_start(self) -> None:
                if self.img is None:
                        return

                selector = self._create_roi_selector(self._roi_strategy_var.get())
                result = self.actions.apply_roi(self.img, selector)
                self._show_image_from_mat(result)


        def _create_roi_selector(self, strategy: str) -> RoiSelector:
                if strategy == "ellipse":
                        return RoiEllipseSelector()
                return RoiRectSelector()


        def _set_roi_controls_state(self, enabled: bool) -> None:
                state = "normal" if enabled else "disabled"
                self._roi_strategy_menu.config(state=state)
                self._roi_start_button.config(state=state)


        def _show_image_from_mat(self, bgr: MatLike) -> None:
                self.img = bgr

                rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(rgb)
                img = img.resize((400, 400))

                self._photo = ImageTk.PhotoImage(img)
                self.preview_label.config(image=self._photo, text="")


        def _build_layout(self) -> None:
                self.window.columnconfigure(0, weight=1)
                self.window.rowconfigure(1, weight=1)


                self.menubar = tk.Menu(self.window, background="#8F8F8F", tearoff=0)
                self.filemenu = tk.Menu(self.menubar, tearoff=0)
                self.savemenu = tk.Menu(self.menubar, tearoff=0)
                self.menubar.add_cascade(label='File', menu=self.filemenu)
                self.menubar.add_cascade(label="Save", menu=self.savemenu)
                self.window.config(menu=self.menubar)

                main_area = tk.Frame(self.window)
                main_area.grid(row=1, column=0, sticky="nsew")
                main_area.columnconfigure(1, weight=1)
                main_area.rowconfigure(0, weight=1)


                left_panel = tk.Frame(main_area, width=140)
                left_panel.grid(row=0, column=0, sticky="ns", padx=8, pady=8)

                roi_button = tk.Button(
                        left_panel,
                        text="ROI",
                        activebackground="#8F8F8F",
                        background="#C2C2C2",
                        width=12,
                        command=self._on_roi_click,
                )
                roi_button.pack(side="top", fill="x", pady=6)

                resize_button = tk.Button(
                        left_panel,
                        text="Resize",
                        activebackground="#8F8F8F",
                        background="#C2C2C2",
                        width=12,
                )
                resize_button.pack(side="top", fill="x", pady=6)

                rotate_button = tk.Button(
                        left_panel,
                        text="Rotate",
                        activebackground="#8F8F8F",
                        background="#C2C2C2",
                        width=12,
                )
                rotate_button.pack(side="top", fill="x", pady=6)

                right_panel = tk.Frame(main_area)
                right_panel.grid(row=0, column=1, sticky="nsew", padx=8, pady=8)

                self._roi_controls = tk.Frame(right_panel)
                self._roi_controls.pack(side="top", fill="x", pady=(0, 8))

                self._roi_strategy_var = tk.StringVar(value="rect")
                self._roi_strategy_menu = tk.OptionMenu(
                        self._roi_controls,
                        self._roi_strategy_var,
                        "rect",
                        "ellipse",
                )
                self._roi_strategy_menu.pack(side="left")

                self._roi_start_button = tk.Button(
                        self._roi_controls,
                        text="Start",
                        command=self._on_roi_start,
                )
                self._roi_start_button.pack(side="left", padx=8)

                self._set_roi_controls_state(enabled=False)

                self.preview_label = tk.Label(
                        right_panel,
                        text="Right panel for inputs and preview",
                        anchor="center",
                        fg="gray",
                )
                self.preview_label.pack(expand=True, fill="both")

        def run(self) -> None:
                self.window.mainloop()


if __name__ == "__main__":
        w = MainWindow(EventActionProvider())
        w.run()