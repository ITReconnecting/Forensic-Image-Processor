import os
from pathlib import Path
import sys

class imageStructure():

    def __init__(self, runner, file):
        self.file = file
        self.runner = runner
        self._importantMmmlsLabels = ("Basic data partition", "PlaceHolder")

        self.sectorSize = ""
        self.guid = ""
        self.partitions = []
        self.mmls = []
        self.importantMmls = []
        self.hash = ""

        self.gpt = self._fdisk()
        self._getHash()

        if self.gpt:
            self._gdisk()

        self._mmls()

        for line in self.mmls:
            for label in self._importantMmmlsLabels:
                if " ".join(line[-3:]) in label:
                    self.importantMmls.append((line[0], line[2], line[3]))

    def _getHash(self):
        self.hash = self.runner.runCommand(f"sha256sum {self.file}")[0].split(" ")[0]

    def _fdisk(self): # Runs and processes fdisk
        fdiskResponse = self.runner.runCommand(f"fdisk -l {self.file}")
        fdiskList = fdiskResponse[0].split("\n") # Gets the fdisk output

        if fdiskList[4].split(" ")[-1] == "gpt":
            return True

        self.sectorSize = fdiskList[2]
        self.guid = fdiskList[5]

        for x in range(8, len(fdiskList)):
            self.partitions.append(fdiskList[x])
        
        return False

    def _gdisk(self): # Runs and processes gdisk
        gdiskResponse = self.runner.runCommand(f"gdisk -l {self.file}")
        gdiskList = gdiskResponse[0].split("\n")

        self.guid = gdiskList[11]
        self.sectorSize = gdiskList[10]

        for x in range(18, len(gdiskList)):
            self.partitions.append(gdiskList[x])


    def _mmls(self): # Runs and processes mmls

        mmlsResponse = self.runner.runCommand(f"mmls {self.file}")
        mmlsTemp = mmlsResponse[0].split("\n")
        
        for x in range(5, len(mmlsTemp)):
            splitLine = mmlsTemp[x].split(" ")
            splitLine = list(filter(('').__ne__, splitLine))
            if splitLine != []:
                self.mmls.append(splitLine)