import tkinter as tk
import cv2
import numpy as np

from PIL import Image, ImageTk
from typing import Iterable
from cv2.typing import MatLike
from pipeline import ActionsProvider

class MainWindow:
        window: tk.Tk
        img: MatLike | None = None
        original_img: MatLike | None = None
        def __init__(
                self,
                actions: ActionsProvider,
                roi_strategy_options: Iterable[str],
                resize_strategy_options: Iterable[str],
                window_name: str = "MainWindow",
                window_width: int = 900,
                window_height: int = 600,
        ) -> None:
                ###UI Init
                self.window = tk.Tk()
                self.window.title(window_name)
                self.window.geometry(f"{window_width}x{window_height}")
                self.window.resizable(True, True)
                #self.preview_label = tk.Label(self.window, width = 400, height = 400)

                ###Dependency Injection
                self.actions = actions
                self.roi_strategy_options = roi_strategy_options
                self.resize_strategy_options = resize_strategy_options

                ###Build other parts
                self._build_layout()
                self.filemenu.add_command(label="Open", command=self._on_open)
                self.filemenu.add_command(label="Save", command=self._on_save)

        def _on_open(self)->None:
                img = self.actions.open_file()
                assert img is not None
                self.img = img
                self.original_img = img
                self._show_image_from_mat(img)
                self._set_roi_controls_state(enabled=True)
                self._set_resize_controls_state(True)
                self._set_rotate_controls_state(True)
                self._set_compare_control(True)

        def _on_save(self)->None:
                assert self.img is not None
                self.actions.save_file(self.img)

        ###SET WIDGET STATE
        def _set_roi_controls_state(self, enabled: bool) -> None:
                state = "normal" if enabled else "disabled"
                self._roi_strategy_menu.config(state=state)
                self.roi_button.configure(state=state)

        def _set_resize_controls_state(self, enabled: bool) -> None:
                state = "normal" if enabled else "disabled"
                self._resize_strategy_menu.config(state=state)
                self.resize_button.configure(state=state)

        def _set_rotate_controls_state(self, enabled: bool) -> None:
                state = "normal" if enabled else "disabled"
                self.rotate_button.configure(state=state)

        def _set_compare_control(self, enabled: bool) -> None:
                state = "normal" if enabled else "disabled"
                self.comapre_button.configure(state=state)
        ###SET WIDGET STATE

        ###WIDGET EVENT###
        def _on_roi_start(self) -> None:
                if self.img is None:
                        return
                result = self.actions.apply_roi(self.img, self._roi_strategy_var.get())
                if result.shape == (0,0,3):
                        print("User press C to exit ROI mod, please retry.")
                        return
                self._show_image_from_mat(result)

        def _on_resize_start(self) -> None:
                if self.img is None:
                        return
                
                x,y = int(self._resize_input_x.get()), int(self._resize_input_y.get())
                result = self.actions.apply_resize(self.img, self._resize_strategy_var.get(), x, y)

                self._show_image_from_mat(result)#FIX: need to scale with equal ratio

        def _on_rotate_start(self) -> None:
                if self.img is None:
                        return
                angle = int(self._rotate_input.get())
                result = self.actions.apply_rotate(self.img, "default", angle)

                self._show_image_from_mat(result)

        def _on_compare(self)->MatLike | None:
                if self.img is None or self.original_img is None:
                        return None
                
                return self.actions.compare(self.img, self.original_img)
        ###WIDGET EVENT###

        ###RENDER
        def _show_image_from_mat(self, bgr: MatLike) -> None:
                """
                Args:
                        rgb: the color of each pixel is formated as r,g,b
                """
                rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(rgb)
                self._photo = ImageTk.PhotoImage(img)
                self.preview_label.config(image=self._photo, text="")


        def _build_layout(self) -> None:
                self.window.columnconfigure(0, weight=1)
                self.window.rowconfigure(1, weight=1)


                self.menubar = tk.Menu(self.window, background="#8F8F8F", tearoff=0)
                self.filemenu = tk.Menu(self.menubar, tearoff=0)
                self.savemenu = tk.Menu(self.menubar, tearoff=0)
                self.menubar.add_cascade(label='File', menu=self.filemenu)
                self.window.config(menu=self.menubar)

                main_area = tk.Frame(self.window)
                main_area.grid(row=1, column=0, sticky="nsew")
                main_area.columnconfigure(1, weight=1)
                main_area.rowconfigure(0, weight=1)


                left_panel = tk.Frame(main_area, width=140)
                left_panel.grid(row=0, column=0, sticky="ns", padx=8, pady=8)

                self.roi_button = tk.Button(
                        left_panel,
                        text="ROI",
                        activebackground="#8F8F8F",
                        background="#C2C2C2",
                        width=12,
                        command=self._on_roi_start,
                )
                self.roi_button.pack(side="top", fill="x", pady=6)

                self.resize_button = tk.Button(
                        left_panel,
                        text="Resize",
                        activebackground="#8F8F8F",
                        background="#C2C2C2",
                        width=12,
                        command=self._on_resize_start
                )
                self.resize_button.pack(side="top", fill="x", pady=6)

                self.rotate_button = tk.Button(
                        left_panel,
                        text="Rotate",
                        activebackground="#8F8F8F",
                        background="#C2C2C2",
                        width=12,
                        command=self._on_rotate_start
                )
                self.rotate_button.pack(side="top", fill="x", pady=6)

                right_panel = tk.Frame(main_area)
                right_panel.grid(row=0, column=1, sticky="nsew", padx=8, pady=8)

                self._roi_controls = tk.Frame(right_panel)
                self._roi_controls.pack(side="top", fill="x", pady=(0, 6))

                self._roi_strategy_var = tk.StringVar(value="rect")
                self._roi_strategy_menu = tk.OptionMenu(
                        self._roi_controls,
                        self._roi_strategy_var,
                        *self.roi_strategy_options
                )
                self._roi_strategy_menu.pack(side="left")

                self._set_roi_controls_state(enabled=False)

                self._resize_control = tk.Frame(right_panel)
                self._resize_control.pack(side="top", fill="x", pady=10)
                self._resize_input_x = tk.Entry(self._resize_control, width=10)
                self._resize_input_y = tk.Entry(self._resize_control, width=10)
                self._resize_input_x.pack(side="left",padx=6)
                self._resize_input_y.pack(side="left",padx=6)
                self._resize_strategy_var = tk.StringVar(value="Bilinear")
                self._resize_strategy_menu = tk.OptionMenu(
                        self._resize_control,
                        self._resize_strategy_var,
                        *self.resize_strategy_options
                )
                self._resize_strategy_menu.pack(side="left")
                self._set_resize_controls_state(False)

                self._rotate_control = tk.Frame(right_panel)
                self._rotate_control.pack(side="top", fill="x", pady=10)
                self._rotate_input = tk.Entry(self._rotate_control, width=10)
                self._rotate_input.pack(side="left", padx=6)
                self._set_rotate_controls_state(False)

                self.comapre_button = tk.Button(
                        left_panel,
                        text="Compare",
                        activebackground="#8F8F8F",
                        background="#C2C2C2",
                        width=12,
                        command=self._on_compare
                )
                self.comapre_button.pack(side="left", padx=6)
                self._set_compare_control(False)



                self.preview_label = tk.Label(
                        right_panel,
                        text="Right panel for inputs and preview",
                        anchor="center",
                        fg="gray",
                )
                self.preview_label.pack(expand=True, fill="both")

        def run(self) -> None:
                self.window.mainloop()