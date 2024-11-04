import os
class ArtworkCategory:
    def __init__(self, sheet_name = "", output_path = "", fandoms_list = [], base_url = "", spoilers_filename = "", nospoilers_filename = ""):
        self.SheetName = sheet_name
        self.Fandoms = fandoms_list
        self.BaseURL = base_url

        self.OutputPath = output_path
        self.SpoilersFileName = spoilers_filename
        self.NoSpoilersFileName = nospoilers_filename

        self.SpoilersFileNamePath = os.path.join(self.OutputPath, spoilers_filename)
        self.NoSpoilersFileNamePath = os.path.join(self.OutputPath, nospoilers_filename)
        