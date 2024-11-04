import os
class ArtworkCategory:
    spoiler_free_filename = "-spoiler-free"
    filename_ext = ".json"

    def __init__(self, sheet_name = "", output_path = "", fandoms_list = [], base_url = "", spoilers_filename = "", nospoilers_filename = ""):
        self.SheetName = sheet_name
        self.Fandoms = fandoms_list
        self.BaseURL = base_url

        self.OutputPath = output_path

    def getFileNamePath(self, spoilers = False, filename = ""):
        if spoilers:
            return os.path.join(self.OutputPath, filename + self.filename_ext)
        else:
            return os.path.join(self.OutputPath, filename + self.spoiler_free_filename + self.filename_ext)

        