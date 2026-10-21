import os
from pathlib import Path
import sys

from fileSystem import fileSystem

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

class deletedFileAnalysis():

    def __init__(self, runner, file, imageInfo):
        self.file = file
        self.runner = runner

        self.deletedFiles = []

        for row in imageInfo.importantMmls:
            self._getDeletedFiles(row[1])

    def _getDeletedFiles(self, start):
        flsResult = self._fls(start)

        self.deletedFiles.append(Folder("ROOT", None, [], "/"))

        for row in flsResult:
            if row != []:
                inode = row[0]
                fileName = row[2]
                folders = row[1].split("/")

                # Add Folders
                for x in range(0, len(folders)):
                    if (folders[x][:2] == '\\t') and (not self.checkFolders(folders[x][:2])):
                        self.deletedFiles.append(Folder(folders[x][2:], "ROOT", [], "/".join(folders[:x])))
                        self.deletedFiles[0].addChild(folders[x][2:])

                    elif (folders[x][:2] != '\\t') and (not self.checkFolders(folders[x])):
                        self.deletedFiles.append(Folder(folders[x], folders[x - 1], [], "/".join(folders[:x])))

                        for item in self.deletedFiles:
                            if (item.name == folders[x]) and (item.type == "FOLDER"):
                                item.addChild(folders[x])
                
                self.deletedFiles.append(File(fileName, folders[-1], row[1], inode))
                for item in self.deletedFiles:
                    if (item.name == folders[-1]):
                        item.addChild(fileName)
        
    def checkFolders(self, folderName):
        for item in self.deletedFiles:
            if (item.name == folderName):
                return True
        return False

    def _fls(self, start):
        flsResult = self.runner.runCommand(f"fls -o {start} -Frd {self.file}")
        flsResultSplit = flsResult[0].split("\n")

        files = []

        for row in flsResultSplit:

            fileInodePath = []

            splitRow = row.split(" ")
            splitRow = list(filter(('').__ne__, splitRow))

            if splitRow != []:
                splitInodePath = splitRow[2].split(":")
                inode = splitInodePath[0]
                if inode != "0":
                    fileInodePath.append(inode)

                    pathSplit = splitInodePath[1].split("/")
                    path = "/".join(pathSplit[:-1])
                    fileName = pathSplit[-1]

                    fileInodePath.append(path)
                    fileInodePath.append(fileName)

            files.append(fileInodePath)

        return files

    def istat(self, start, inode):
        return self.runner.runCommand(f"istat -o {start} {self.file} {inode}")[0]
        