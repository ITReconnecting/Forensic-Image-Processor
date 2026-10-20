import tkinter as tk
from tkinter import ttk, Menu
from imageStructure import imageStructure

class imageStructureGUI(ttk.LabelFrame):

    def __init__(self, container, imageInfo):
        super().__init__(container)
        gpt = ""

        if imageInfo.gpt:
            gpt = "True"

        else:
            gpt = "False"

        self['text'] = 'Image Structure'

        options = {'padx': 5, 'pady': 5}

        # --- Headers ---

        self.gptHeaderTextLabel = ttk.Label(self, text="GPT:")
        self.gptHeaderTextLabel.grid(column=0, row=0, sticky='w', **options)

        self.guidHeaderTextLabel = ttk.Label(self, text="GUID:")
        self.guidHeaderTextLabel.grid(column=0, row=1, sticky='w', **options)

        self.sectorHeaderTextLabel = ttk.Label(self, text="Sector Size:")
        self.sectorHeaderTextLabel.grid(column=0, row=2, sticky='w', **options)

        # --- Data For Headers ---

        self.gptTextLabel = ttk.Label(self, text=gpt)
        self.gptTextLabel.grid(column=1, row=0, sticky='w', **options)

        self.guidTextLabel = ttk.Label(self, text=imageInfo.guid.split(":")[1])
        self.guidTextLabel.grid(column=1, row=1, sticky='w', **options)

        self.sectorTextLabel = ttk.Label(self, text=imageInfo.sectorSize.split(":")[1])
        self.sectorTextLabel.grid(column=1, row=2, sticky='w', **options)

        self.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

class imageHashGUI(ttk.LabelFrame):

    def __init__(self, container, imageInfo):
        super().__init__(container)

        self['text'] = 'Image Information'

        options = {'padx': 5, 'pady': 5}

        # --- Headers ---

        self.hashHeaderTextLabel = ttk.Label(self, text="Sha256 hash:")
        self.hashHeaderTextLabel.grid(column=0, row=0, sticky='w', **options)

        # --- Data For Headers ---

        self.hashTextLabel = ttk.Label(self, text=imageInfo.hash)
        self.hashTextLabel.grid(column=1, row=0, sticky='w', **options)

        self.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")