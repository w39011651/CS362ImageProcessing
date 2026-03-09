import tkinter as tk
import cv2
import numpy as np

from PIL import Image, ImageTk
from pathlib import Path
from tkinter import filedialog
from typing import Protocol
from os import PathLike

class ActionsProvider(Protocol):
        def open_file(self)-> str:...


class EventActionProvider(ActionsProvider):
        def open_file(self)->str:
                file_path = filedialog.askopenfilename(
                        title="PleaseChooseImage",
                        filetypes=[("Image files", "*.jpg *.png *.jpeg"), ("All files", "*.*")],
                )
                file_path.replace('\\', '/')
                print(file_path)
                return file_path
                


class MainWindow:
        window: tk.Tk
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

        def _build_layout(self) -> None:
                self.window.columnconfigure(0, weight=1)
                self.window.rowconfigure(1, weight=1)


                self.menubar = tk.Menu(self.window, background="#8F8F8F", tearoff=0)
                self.filemenu = tk.Menu(self.menubar, tearoff=0)
                self.menubar.add_cascade(label='File', menu=self.filemenu)
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
                        width=12
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