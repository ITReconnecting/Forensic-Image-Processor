import tkinter as tk
from tkinter import ttk, Menu, Entry

from imageDeleteFileAnalysis import deletedFileAnalysis, Folder, File

class DeletedItemsBrowser(ttk.LabelFrame):

    def __init__(self, container, runner, file, imageInfo):
        super().__init__(container)

        self["text"] = f"Deleted File Informations"

        # All Folder and File objects
        self.itemList = deletedFileAnalysis(runner, file, imageInfo).deletedFiles

        # Current directory and navigation history
        self.current_folder = None
        self.history = []

        # Configure layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        # Navigation bar
        navigation = ttk.Frame(self)
        navigation.grid(
            row=0, column=0, sticky="ew", padx=5, pady=5
        )
        navigation.columnconfigure(1, weight=1)

        self.back_button = ttk.Button(
            navigation,
            text="← Back",
            command=self.go_back,
            state="disabled"
        )
        self.back_button.grid(row=0, column=0, padx=(0, 10))

        self.path_label = ttk.Label(
            navigation,
            text="/"
        )
        self.path_label.grid(row=0, column=1, sticky="w")

        # Table
        columns = ("type", "name", "path")

        self.table = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            height=10,
            selectmode="browse"
        )

        self.table.heading("type", text="Type")
        self.table.heading("name", text="Name")
        self.table.heading("path", text="Path")

        self.table.column("type", width=100, stretch=False)
        self.table.column("name", width=180)
        self.table.column("path", width=300)

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.table.yview
        )
        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.grid(
            row=1, column=0, sticky="nsew", padx=(5, 0), pady=5
        )
        scrollbar.grid(
            row=1, column=1, sticky="ns", padx=(0, 5), pady=5
        )

        # File details section
        self.details = ttk.LabelFrame(
            self,
            text="File Information"
        )
        self.details.grid(
            row=2, column=0, columnspan=2,
            sticky="nsew", padx=5, pady=5
        )

        self.details.columnconfigure(0, weight=1)

        self.details_label = ttk.Label(
            self.details,
            text="Select a file to view its information.",
            justify="left",
            anchor="nw"
        )
        self.details_label.grid(
            row=0, column=0, sticky="nsew", padx=5, pady=5
        )

        # Single-click selects a row and displays file information.
        self.table.bind(
            "<<TreeviewSelect>>",
            self.on_select
        )

        # Double-click opens a folder.
        self.table.bind(
            "<Double-1>",
            self.on_double_click
        )

        # Find and display the root folder.
        root_folder = self.find_root_folder(self.itemList)

        if root_folder is not None:
            self.show_folder(root_folder)
        else:
            self.path_label.config(text="No root folder found")

    def find_root_folder(self, items):
        """Find the Folder whose parent is None."""
        for item in items:
            if (item.parent is None) and (item.name is "ROOT"):
                return item

        return None

    def show_folder(self, folder):
        """Display the children of a folder."""
        self.current_folder = folder

        # Update current path
        self.path_label.config(text=folder.path)

        # Clear the existing table
        for row_id in self.table.get_children():
            self.table.delete(row_id)

        # Clear previously displayed file information
        self.clear_details()

        # Insert each child into the table.
        for child in folder.children:
            print(child)
            for item in self.itemList:
                if item.name == child:
                    print(item)
                    self.table.insert(
                        "",
                        "end",
                        values=(
                            item.type,
                            item.name,
                            item.path
                        )
                    )

        # Enable Back only when there is a previous directory.
        self.back_button.config(
            state="normal" if self.history else "disabled"
        )

    def get_selected_item(self):
        """Return the Folder or File object for the selected row."""
        selected = self.table.selection()

        if not selected or self.current_folder is None:
            return None

        values = self.table.item(selected[0], "values")

        if not values:
            return None

        selected_name = values[1]
        selected_path = values[2]

        # Match the table row to its original object.
        for child in self.current_folder.children:
            if (
                child.name == selected_name
                and child.path == selected_path
            ):
                return child

        return None

    def on_select(self, event=None):
        """Display file information when a file is selected."""
        item = self.get_selected_item()

        if isinstance(item, File):
            self.show_file_details(item)
        elif isinstance(item, Folder):
            self.clear_details()

    def on_double_click(self, event=None):
        """Open a folder when it is double-clicked."""
        # Identify the row under the mouse pointer.
        row_id = self.table.identify_row(event.y)

        if not row_id:
            return

        # Select the clicked row.
        self.table.selection_set(row_id)
        self.table.focus(row_id)

        item = self.get_selected_item()

        if isinstance(item, Folder):
            # Save the current directory before navigating.
            self.history.append(self.current_folder)

            # Display the selected folder's children.
            self.show_folder(item)

    def go_back(self):
        """Return to the previously opened directory."""
        if not self.history:
            return

        previous_folder = self.history.pop()
        self.show_folder(previous_folder)

    def show_file_details(self, file):
        """Display information about the selected file."""
        info = (
            f"Name: {file.name}\n"
            f"Type: {file.type}\n"
            f"Path: {file.path}\n"
            f"Inode: {file.inode}"
        )

        self.details_label.config(text=info)

    def clear_details(self):
        """Reset the file information section."""
        self.details_label.config(
            text="Select a file to view its information."
        )