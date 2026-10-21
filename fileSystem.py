class Folder():

    def __init__(self, name, parent, children, path):
        self.name = name
        self.parent = parent
        self.children = children
        self.path = path
        self.type = "FOLDER"

    def addChild(self, child):
        self.children.append(child)

class File():

    def __init__(self, name, parent, path, inode=None):
        self.name = name
        self.parent = parent
        self.path = path
        self.inode = inode
        self.type = "FILE"

class fileSystem():

    def __init__(self):
        self.system = Folder("ROOT", None, [], "ROOT")

    def checkFolder(self, name, path):
        result = getChildren(name, path)
        
        if result == None:
            return False
        else:
            return True

    def addFolder(self, name, parent, path):
        folder = Folder(name, parent, [], path)

        if parent == None:
            self.system.addChild(Folder(name, "ROOT", [], path))
        else:
            for child in self.system.children:
                if (child.type == "FOLDER") and (child.name == parent):
                    child.addChild()
                    return True
            
    def iterativeFolderAdd(self, folder, target, targetPath, toAdd):
        for child in folder.children:
            if (child.name == target) and (child.path == targetPath):
                child.children.append(toAdd)
                return True
        
        for child in folder.children:
            if child.type == "FOLDER":
                self.iterativeFolderAdd(child, target, targetPath, toAdd)

    def addFile(self, name, parent, folderPath, path, inode=None):
        if parent == None:
            self.system.addChild(File(name, "ROOT", path, inode))
        else:
            for child in self.system.children:
                if (child.type == "FOLDER") and (child.name == parent):
                    child.addChild(File(name, child.name, path, inode))

    def getFile(self, name, folderPath):
        return self.iterativeFileSearch(self.system, name, folderPath)

    def iterativeFileSearch(self, folder, target, targetPath):
        for child in folder.children:
            if (child.name == target) and (child.path == targetPath):
                return child
        
        for child in folder.children:
            if child.type == "FOLDER":
                self.iterativeChildSearch(child, target, targetPath)
        

"""
look in folder
    is this folder needed
        if yes
            return children
        if not
            for each child
                look in folder
"""