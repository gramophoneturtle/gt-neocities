import utility

class RelatedSeriesList:
    Series = []

    def __init__(self):
        self.Series = []

    def loadSeriesOnlyFromJson(self, json):
        self.Series = []
        
        # for each series
        for item_series in json:
            # see if RelatedSeries alreayd exists
            index_dict = self.find_rel_dict_ser_name_index(item_series["SeriesName"])

            if index_dict == -1:
                rel_dictionary = RelatedSeries(item_series["SeriesName"], 
                                               thumbnailURL = item_series["ThumbnailURL"],
                                               thumbnailAlt = item_series["ThumbnailAlt"])
                
                #reset here so it's not [ [] ] - will make it better later
                rel_dictionary.SeriesEntries = []
                
                # Add with defaults
                self.Series.append(rel_dictionary)

    def find_rel_dict_ser_name_index(self, value):
        for i, dic in enumerate(self.Series):
            if dic.SeriesName == value:
                return i
        return -1

    def update(self, i_index, i_name, aw_dict, foundindices):

        index_dict = self.find_rel_dict_ser_name_index(i_name)

         # Get the index of the entry in the series
        int_i_index = -1
        if i_index < len(foundindices):
            try:
                int_i_index = foundindices[i_index]
                int_i_index = int(int_i_index)
            except ValueError:
                int_i_index = -1
                print("    Related -AU/Series- {1}".format(i_name))
                print("      !! TODO: Current index [{0}] for foundindices is not an int! Default to [-1].".format(i_index,foundindices[i_index]))
        else:
            print("    Related for -AU/Series- {1}".format(i_name))
            print("      '! Current index [{0}] is less than indices found: {1}. Default to [-1].".format(i_index,foundindices))

        new_entry = RelatedEntry(int_i_index, aw_dict)
        
        if index_dict == -1:
            rel_dictionary = RelatedSeries(i_name, new_entry)
            # Add with defaults
            self.Series.append(rel_dictionary)
        # Add new entry to existing series
        else:
            self.Series[index_dict].SeriesEntries.append(new_entry)

    def sortSeriesEntries(self):
        for rel_list_item in self.Series:
            rel_list_item.SeriesEntries.sort(key=lambda x: x.Index)

class RelatedSeries:
    SeriesName = ""
    SeriesURL = ""
    SeriesEntries = []
    ThumbnailURL = ""
    ThumbnailAlt = ""

    def __init__(self, name, new_entry = [], thumbnailURL = "", thumbnailAlt = ""):
        self.SeriesName = name
        self.SeriesURL = utility.urlify(name)
        self.ThumbnailURL = thumbnailURL
        self.ThumbnailAlt = thumbnailAlt
        self.SeriesEntries = [ new_entry ]

class RelatedEntry:
    Name = ""
    URL = ""
    Index = -1
    ThumbnailURL = ""
    ThumbnailAlt = ""

    def __init__(self, int_i_index, aw_dict):
        self.Index = int_i_index
        self.Name = aw_dict['title']
        self.URL = aw_dict['UniqueURLKey']
        self.ThumbnailURL = aw_dict['thumbnailUrl']
        self.ThumbnailAlt = aw_dict['thumbnailAlt']



