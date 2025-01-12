import pandas
import urllib3
import os
import json



import utility

# Excel Database Filename
FILENAME_INPUT = "Where Is My Art.xlsx"

FILE_PATH_INPUT = os.path.join(os.getcwd(),"data_conversion\\", FILENAME_INPUT)
FILE_PATH_OUTPUT_PATH = os.path.join(os.getcwd(),"src\\_data\\")


DATE_COLUMN_NAME = "Earliest Date"


MAX_NUM_IMAGES = 2

class Crochet:


    Title = ""		
    
    Date = ""	
    
    TumblrURL = ""	
    TumblrDate = ""	
    PillowfortURL = ""
    PillowfortDate = ""
    BlueskyURL = ""
    BlueskyDate = ""
    
    Introduction = ""	
    MiddleText = ""
    
    PatternTitle = ""	
    PatternAuthor = ""	
    
    PatternType = ""
    PatternLinks = ""
    Modifcations = ""
    
    Yarn = ""
    Notions = ""
    Size = ""
    
    RelatedStoryURL = ""	
    
    # BEFOREIMG1	
    # BEFOREIMG2	
    # MIDDLEIMG1	
    # MIDDLEIMG2	
    # AFTERIMG1	
    # AFTERIMG2	
    # BEFOREIMG1ALT
    # BEFOREIMG2ALT	
    # MIDDLE IMG 1 ALT	
    # MIDDLE IMG 2 ALT	
    # AFTER IMG 1 ALT	AFTER IMG 2 ALT	
    # characters	
    # fandom	
    # Spoilers	
    # Tags		

    def __init__(self, int_i_index, aw_dict):
        self.Index = int_i_index
        self.Name = aw_dict['title']
        self.URL = aw_dict['UniqueURLKey']
        self.ThumbnailURL = aw_dict['thumbnailUrl']
        self.ThumbnailAlt = aw_dict['thumbnailAlt']

def process_crochet(sheet_name = "Crochet", file_path_output = "", fandoms = ["OC"], include_spoilers = True, base_url="/"):
    print('Processing. Sheet: {0}. Include Spoilers: {1}'.format(sheet_name, include_spoilers), end="")
    print(' Fandom: {0}.'.format(fandoms))

    # Read Excel file
    excel_data_df = pandas.read_excel(
        FILE_PATH_INPUT,
        sheet_name=sheet_name,
        usecols=['Artwork', 'NS?', "Earliest Date",
                 'Spoilers',
                'characters','fandom','PF tags',
                'Title','Introduction', 'MiddleText',
                'PatternTitle', 'PatternAuthor', 'PatternType', 'PatternLinks', 'Modifcations',
                'Yarn', 'Notions', 'Size',
                'RelatedStoryURL',
                'BEFORE IMG 1','BEFORE IMG 2','MIDDLE IMG 1','MIDDLE IMG 2','AFTER IMG 1','AFTER IMG 2',
                'BEFORE IMG 1 ALT','BEFORE IMG 2 ALT','MIDDLE IMG 1 ALT','MIDDLE IMG 2 ALT','AFTER IMG 1 ALT','AFTER IMG 2 ALT',
                'Tumblr URL',
                'Pillowfort URL',
                'Bluesky URL',
                'Cohost URL' 
                ]
        )
                # 'IMG THMB', 'ALT THMB',
    
    # only get nightshaded artworks and...
    options = ['Yes','yes']
    nightshadeOnlyTMP = excel_data_df[excel_data_df["NS?"].isin(options)]
    
    # CLEAN UP - Set Defaults
    # fill in NaN as with default values for each column as an empty string = ""
    nightshadeOnlyTMP = nightshadeOnlyTMP.infer_objects().fillna("")

    # Filter by spoilers
    if include_spoilers == False:
        options = ['No','no']
        nightshadeOnly = nightshadeOnlyTMP[nightshadeOnlyTMP["Spoilers"].isin(options)]
    else:
        options = ['Yes','yes','']
        nightshadeOnly = nightshadeOnlyTMP[nightshadeOnlyTMP["Spoilers"].isin(options)]

    # Choose to filter by fandoms
    if len(fandoms) == 1:
        nightshadeOnly = nightshadeOnly[nightshadeOnly["fandom"].isin(fandoms)]

    # "The Sheets API doesn't know what to do with a Python datetime/timestamp. You'll need to convert it - most likely to a str." 
    #https://stackoverflow.com/questions/49243736/how-do-i-handle-object-of-type-timestamp-is-not-json-serializable-in-python
    # '%Y-%m-%d' -> yyyy-MM-dd
    # ex: Timestamp('2024-03-23 00:00:00') -> '2024-03-23' for Fathers using Windows 11 Paint  
    nightshadeOnly[DATE_COLUMN_NAME] = nightshadeOnly[DATE_COLUMN_NAME].dt.strftime('%Y-%m-%d')

    # sort
    nightshadeOnly.sort_values(by=[DATE_COLUMN_NAME], inplace=True, ascending=False)

    print(" 1. Processing DataFrame", end="...\n")
    # Convert DataFrame to JSON
    json_str = _generate_json(nightshadeOnly, base_url)

    print("testing - printing: {0}".format(json_str))

    # print(" 2. Updating JSON Data", end="...")
    # # Output - can ge to the json file in the src area
    # with open(file_path_output, 'w', encoding='utf-8') as f:
    #     f.write(json_str)

    print(" Completed!\n")


def _generate_json(nsOnly: pandas.DataFrame,base_url) -> str:
    artwork_dictionary_list = _make_url_dict(nsOnly,base_url)
    
    # remove the outer dictionary/list
    nested_json = json.dumps(artwork_dictionary_list[0]["ARTWORK"], indent=2)

    return nested_json

def _make_url_dict(mydataframe: pandas.DataFrame,base_url) -> list:
    return_list = []
    dict_key = "ARTWORK"
    urls_key = "urls"
    tmp_dict = {dict_key: []}
    for _, row in mydataframe.iterrows():

        # MAIN INFO
        artwork_dictionary =  {
            'title': row['title'], 
            'summary': row['summary'], 
            'details': row['detail'],
            'characters': row['characters']
        }
        artworkname = row['Artwork'].replace("\n","")[0:40]
        
        artwork_dictionary['date'] = row[DATE_COLUMN_NAME]
        artwork_dictionary['dateYear'] = row[DATE_COLUMN_NAME][0:4]

        # Set up the URL ahead of time - will act as a Key for the artwork
        artwork_dictionary['uniqueUrl'] = "{0}-{1}".format(row[DATE_COLUMN_NAME],row['Artwork'].replace("\n","").strip()[0:10])
        artwork_dictionary['uniqueUrl'] = utility.urlify(artwork_dictionary['uniqueUrl'] )
        artwork_dictionary['uniqueUrl'] = urllib3.util.parse_url(artwork_dictionary['uniqueUrl']).url

        #full relative URL in order to link to other pieces
        artwork_dictionary['UniqueURLKey'] = os.path.join(base_url, artwork_dictionary['uniqueUrl'])

        artwork_dictionary['spoilers'] = row['Spoilers']

        if row['title'] == "":
            print("        Title is missing for |{0}|".format(artworkname))

        if row['characters'] == "":
            print("        characters is missing for |{0}|".format(artworkname))

        # URLS -------------------------------------------------
        artwork_dictionary['urls'] = []

        # Gather URL posts on other websites
        site_name = "Tumblr"
        if row['{0} URL'.format(site_name)] != "":
            artwork_dictionary[urls_key].append({'sitename': site_name, 'url': row['{0} URL'.format(site_name)]})
        site_name = "Pillowfort"
        if row['{0} URL'.format(site_name)] != "":
            artwork_dictionary[urls_key].append({'sitename': site_name, 'url': row['{0} URL'.format(site_name)]})
        site_name = "Bluesky"
        if row['{0} URL'.format(site_name)]:
           artwork_dictionary[urls_key].append({'sitename': site_name, 'url': row['{0} URL'.format(site_name)]})
        site_name = "Cohost"
        if row['{0} URL'.format(site_name)] != "" and row['{0} URL'.format(site_name)].upper() != "Drafted".upper():
            artwork_dictionary[urls_key].append({'sitename': site_name.lower(), 'url': row['{0} URL'.format(site_name)]})

        # IMAGES -------------------------------------------------
        # artwork_dictionary['imgs'] = _make_img_list(row)

        # # CHECK IF HAVE MINIMUM -----------------------------------
        # # Add if img + alt was found, otherwise, print warning message
        # if artwork_dictionary['imgs']:
        #     # completed, add to final dictionary
        #     tmp_dict[dict_key].append(artwork_dictionary)

        #     # Add Image thumbnail and alt text if present
        #     artwork_dictionary['thumbnailUrl'] = ""
        #     artwork_dictionary['thumbnailAlt'] = ""
        #     if row['IMG THMB'] != "" or row['ALT THMB'] != "":
        #         if row['IMG THMB'] == "":
        #             print("    IMG THMB is missing for |{0}|".format(artworkname))
        #         elif row['ALT THMB'] == "":
        #             print("    ALT THMB is missing for |{0}|".format(artworkname))
        #         else:
        #             artwork_dictionary['thumbnailUrl'] = row['IMG THMB'].replace("src","")
        #             artwork_dictionary['thumbnailAlt'] = row['ALT THMB']


        #     # FANDOM LISTING -----------------------------------------
        #     artwork_dictionary['fandom'] = row['fandom'].split(",")

        #     # Add Related Writing
        #     artwork_dictionary['RelatedWritingURL'] = row['RelatedWritingURL']

        # else:
        #     print("        !! Skipped over adding entry. No Img urls found for |{0}|\n".format(row['Artwork'].replace("\n","")[0:40]))
       
    return_list.append(tmp_dict)
    return return_list

# IMAGE LISTS -------------------------------------
def _make_img_list(_row: pandas.Series) -> list:
    '''
    Must have IMG source URL AND Alt Text
    '''
    img_list = [] 

    for i in range(1, MAX_NUM_IMAGES+1):
        # init
        kay_img = 'IMG {0}'.format(i)
        key_alt = 'ALT {0}'.format(i)
        artwork_id = _row['Artwork'].replace("\n","")[0:40]
        
        # guards
        # if there is no more images, we don't need to continue
        if _row[kay_img] == "" and _row[key_alt] == "" :
            break

        # if there is no image - warn
        if _row['IMG {0}'.format(i)] == "":
            print("    Img URL missing: |{0}| for #{1}".format(artwork_id, i))
            continue

        # if there is an image, but no alt text - warn
        if _row['IMG {0}'.format(i)] != "" and _row['ALT {0}'.format(i)] == "":
            print("    Alt text missing! |{0}| for #{1}".format(artwork_id, i))
            continue

        test_url = _get_img_url(_row, kay_img)
        # make sure we don't have the src directory - might get included by accident!
        if "src" in test_url:
            # print("    !! Img URL contains src. Fixing for |{0}| #{1}".format(artwork_id, i))
            test_url = test_url.replace("src","")

        # make sure it's at root if not using https
        if "https" not in test_url and '\\' != test_url[0:1]:
            print("    !! Img URL missing \\. Fixing for |{0}| #{1}".format(artwork_id, i))
            test_url = "\\" + test_url

        # we have an image and alt text - good to add
        img_list.append({'id': i, 'url': test_url,'alt': _row[key_alt]})

    return img_list


def _get_img_url(rw, st_nm) -> str:
    return_url = ""

    list_of_urls = rw[st_nm]

    urls = list_of_urls.split(";")
    # split by ;
    # get the first/0th url and return the string

    return_url = urls[0]

    return return_url