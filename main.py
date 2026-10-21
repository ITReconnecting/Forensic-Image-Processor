import tkinter as tk
from tkinter import filedialog, messagebox, ttk, Menu
import csv
from pathlib import Path

from runner import Runner
from report import Report

from imageStructureGUI import imageStructureGUI, imageHashGUI, mmlsGUI, importantMmlsGUI
from imageStructure import imageStructure

class App(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Forensic Image Viewer")
        self.geometry("")

        self.report = Report()
        self.runner = Runner(self.report)
        self.diskInfo = None

        self.allowed_extensions = {
            ".001",
            ".dd",
            ".img",
            ".raw"
        }

        self.file_path = None

        menubar = Menu(self)
        self.config(menu=menubar)

        options_menu = Menu(menubar)

        options_menu.add_command(label='Disk Image Info', command=self.diskImageInfo)
        options_menu.add_separator()
        options_menu.add_command(label='Exit', command=self.destroy)

        menubar.add_cascade(label="Options", menu=options_menu)

        self.after(100, self.selectImage)

    def selectImage(self):
        """Ask the user for a file and parse it."""

        self.file_path = filedialog.askopenfilename(
            parent=self,
            title="Select a file to use",
            filetypes=[
                ("RAW Image files", "*.001 *.dd *.img *.raw"),
                ("All files", "*.*")
            ]
        )

        if not self.file_path:
            # Let the user retry rather than closing the app
            if self.image_path is None:
                messagebox.showinfo(
                    "Image required",
                    "Please select a disk image to continue.",
                    parent=self
                )
                self.after(100, self.select_image)
            return

        extension = Path(self.file_path).suffix.lower()

        if extension not in self.allowed_extensions:
            messagebox.showerror(
                "Unsupported format",
                "The selected file extension is not supported.",
                parent=self,
            )
            self.destroy()
            return False
        
        self.startUp()

    def startUp(self):
        self.diskInfo = imageStructure(self.runner, self.file_path)
        self.diskImageInfo()

    def diskImageInfo(self):
        frame_1 = imageHashGUI(self, self.diskInfo)
        frame_1.grid(row=0, column=0)

        frame_2 = imageStructureGUI(self, self.diskInfo)
        frame_2.grid(row=1, column=0)

        frame_3 = mmlsGUI(self, self.diskInfo)
        frame_3.grid(row=2, column=0)

        for x in range(len(self.diskInfo.importantMmls)):
            mmlsFrame = importantMmlsGUI(self, self.diskInfo.importantMmls[x][3], self.diskInfo.importantMmls[x][0])
            x += 2
            mmlsFrame.grid(row=x, column=1)

        self.geometry('1700x450')

if __name__ == "__main__":
    app = App()
    app.mainloop()