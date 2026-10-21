import tkinter as tk
from tkinter import ttk, Menu, Entry
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

class mmlsGUI(ttk.LabelFrame):

    def __init__(self, container, imageInfo):
        super().__init__(container)

        self['text'] = 'mmls Information'

        options = {'padx': 5, 'pady': 5}

        # --- mmls table --- 
        for i in range(len(imageInfo.mmls)):
            for j in range(0, 6):
                if i == 0:
                    self.table = Entry(self, width=25, fg='black', font=('Arial',12,'bold'))
                else:
                    self.table = Entry(self, width=25, fg='black', font=('Arial',12))
                self.table.grid(row=i, column=j)
                if (i != 0) and (j == 0):
                    self.table.insert(tk.END, imageInfo.mmls[i][j][:-1])
                elif j != 5:
                    self.table.insert(tk.END, imageInfo.mmls[i][j])
                else:
                    self.table.insert(tk.END, " ".join(imageInfo.mmls[i][j:]))

        self.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

class importantMmlsGUI(ttk.LabelFrame):

    def __init__(self, container, fsstatInfo, number):
        super().__init__(container)

        self['text'] = f'mmls {number[:-1]} Information'

        options = {'padx': 5, 'pady': 5}

        # --- Headers ---

        self.fileSystemHeaderTextLabel = ttk.Label(self, text="File System:")
        self.fileSystemHeaderTextLabel.grid(column=0, row=0, sticky='w', **options)

        self.volumeNameHeaderTextLabel = ttk.Label(self, text="Volume Name:")
        self.volumeNameHeaderTextLabel.grid(column=0, row=1, sticky='w', **options)

        self.versionNameHeaderTextLabel = ttk.Label(self, text="Version:")
        self.versionNameHeaderTextLabel.grid(column=0, row=2, sticky='w', **options)

        self.clusterSizeHeaderTextLabel = ttk.Label(self, text="Cluster Size:")
        self.clusterSizeHeaderTextLabel.grid(column=0, row=3, sticky='w', **options)

        self.clusterRangeHeaderTextLabel = ttk.Label(self, text="Cluster Range:")
        self.clusterRangeHeaderTextLabel.grid(column=0, row=4, sticky='w', **options)

        self.sectorRangeHeaderTextLabel = ttk.Label(self, text="Sector Range:")
        self.sectorRangeHeaderTextLabel.grid(column=0, row=5, sticky='w', **options)

        # --- Data For Headers ---

        self.fileSystemTextLabel = ttk.Label(self, text=fsstatInfo[0])
        self.fileSystemTextLabel.grid(column=1, row=0, sticky='w', **options)

        self.volumeHeaderTextLabel = ttk.Label(self, text=fsstatInfo[1])
        self.volumeHeaderTextLabel.grid(column=1, row=1, sticky='w', **options)

        self.versionNameTextLabel = ttk.Label(self, text=fsstatInfo[2])
        self.versionNameTextLabel.grid(column=1, row=2, sticky='w', **options)

        self.clusterSizeTextLabel = ttk.Label(self, text=fsstatInfo[3])
        self.clusterSizeTextLabel.grid(column=1, row=3, sticky='w', **options)

        self.clusterRangeTextLabel = ttk.Label(self, text=fsstatInfo[4])
        self.clusterRangeTextLabel.grid(column=1, row=4, sticky='w', **options)

        self.sectorRangeTextLabel = ttk.Label(self, text=fsstatInfo[5])
        self.sectorRangeTextLabel.grid(column=1, row=5, sticky='w', **options)

        self.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")