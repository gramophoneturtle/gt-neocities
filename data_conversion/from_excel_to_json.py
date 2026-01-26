#make sure pandas and openpyxl are installed
# Winwdows
# > py -m pip install pandas
import pandas
import urllib3
import json
import os
import re

from models.RelatedSeries import RelatedSeriesList
from models.ArtworkCategory import ArtworkCategory

# Excel Database Filename
filename_input = "Where Is My Art.xlsx"

# GENERATE - PERSONA 5 JSON Files
filename_output_p5 = "art-persona5.json"
filename_output_p5_nospoilers = "art-persona5-spoiler-free.json"

# GENERATE - Related Series Files
filename_output_related_twewy = "relatedtwewy.json"
filename_output_related_xcx = "relatedxcx.json"

file_path_input = os.path.join(os.getcwd(),"data_conversion\\", filename_input)
file_path_output_path = os.path.join(os.getcwd(),"src\\_data\\")

date_column_name = "Earliest Date"
max_num_images = 8
max_num_videos = 1

# Related Series
twewy_related_series_list = RelatedSeriesList()

# functions

# IMAGE LISTS -------------------------------------
def make_img_list(_row: pandas.Series) -> list:
    '''
    Must have IMG source URL AND Alt Text
    '''
    img_list = [] 

    for i in range(1, max_num_images+1):
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

        test_url = get_img_url(_row, kay_img)
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

def get_img_url(rw, st_nm) -> str:
    return_url = ""

    list_of_urls = rw[st_nm]

    urls = list_of_urls.split(";")
    # split by ;
    # get the first/0th url and return the string

    return_url = urls[0]

    return return_url

def make_vid_list(_row: pandas.Series) -> list:
    vid_list = [] 

    for i in range(1, max_num_videos+1):
        # init
        key_vid = 'VID {0}'.format(i)
        artwork_id = _row['Artwork'].replace("\n","")[0:40]
        
        # guards
        # if there is no more videos, we don't need to continue
        if _row[key_vid] == "" :
            break

        test_url = get_img_url(_row, key_vid)
        # make sure we don't have the src directory - might get included by accident!
        if "src" in test_url:
            # print("    !! VIDEO URL contains src. Fixing for |{0}| #{1}".format(artwork_id, i))
            test_url = test_url.replace("src","")

        # we have an image and alt text - good to add
        vid_list.append({'id': i, 'url': test_url})

    return vid_list

def update_related_dictionary(rw, aw_dict):

    artworkname = rw['Artwork'].replace("\n","")[0:40]

    foundseries = rw['RelatedSeries'].split(";")
    foundindices = str(rw['RelatedSeriesOrder']).split(";")

    for i_index, i_name in enumerate(foundseries):
        i_name = i_name.strip()

        twewy_related_series_list.update(i_index, i_name, aw_dict, foundindices)
    return 

# https://stackoverflow.com/questions/1007481/how-to-replace-whitespaces-with-underscore
def urlify(s):

    # Remove all non-word characters (everything except numbers and letters)
    s = re.sub(r'[^\w\s-]', '', s).strip() 

    # Replace all runs of whitespace with a single dash
    s = re.sub(r"\s+", '-', s)

    s = urllib3.util.parse_url(s).url

    return s

def make_url_dict(mydataframe: pandas.DataFrame,base_url) -> list:
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
        
        artwork_dictionary['date'] = row[date_column_name]
        artwork_dictionary['dateYear'] = row[date_column_name][0:4]
        artwork_dictionary["WebsiteDateUTC"] = str(row["WebsIteDateUTC"])

        # Set up the URL ahead of time - will act as a Key for the artwork
        artwork_dictionary['uniqueUrl'] = "{0}-{1}".format(row[date_column_name],row['Artwork'].replace("\n","").strip()[0:10])
        artwork_dictionary['uniqueUrl'] = urlify(artwork_dictionary['uniqueUrl'] )
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
        
        site_name = "Mastodon"
        if row['{0} URL'.format(site_name)]:
           artwork_dictionary[urls_key].append({'sitename': site_name, 'url': row['{0} URL'.format(site_name)]})
        
        site_name = "Sheezy"
        if row['{0} URL'.format(site_name)]:
           artwork_dictionary[urls_key].append({'sitename': site_name, 'url': row['{0} URL'.format(site_name)]})

        site_name = "Cara"
        if row['{0} URL'.format(site_name)]:
           artwork_dictionary[urls_key].append({'sitename': site_name, 'url': row['{0} URL'.format(site_name)]})

        # IMAGES -------------------------------------------------
        artwork_dictionary['imgs'] = make_img_list(row)

        # CHECK IF HAVE MINIMUM -----------------------------------
        # Add if img + alt was found, otherwise, print warning message
        if artwork_dictionary['imgs']:
            # completed, add to final dictionary
            tmp_dict[dict_key].append(artwork_dictionary)

            # Add Image thumbnail and alt text if present
            artwork_dictionary['thumbnailUrl'] = ""
            artwork_dictionary['thumbnailAlt'] = ""
            if row['IMG THMB'] != "" or row['ALT THMB'] != "":
                if row['IMG THMB'] == "":
                    print("    IMG THMB is missing for |{0}|".format(artworkname))
                elif row['ALT THMB'] == "":
                    print("    ALT THMB is missing for |{0}|".format(artworkname))
                else:
                    artwork_dictionary['thumbnailUrl'] = row['IMG THMB'].replace("src","")
                    artwork_dictionary['thumbnailAlt'] = row['ALT THMB']

            # REFS ---------------------------------------------------
            # At the moment for testing, have 1 reference image
            artwork_dictionary['REF1'] = row['REF 1'].replace("src","")
            artwork_dictionary['REFALT1'] = row['REF ALT 1']

            # Wanrings
            artwork_dictionary['Warnings'] = row['warnings']

            # VIDEOS -------------------------------------------------
            artwork_dictionary['vids'] = make_vid_list(row)

            # FANDOM LISTING -----------------------------------------
            artwork_dictionary['fandom'] = [x.strip() for x in row['fandom'].split(",")]

            # List of related artworks
            # Add Image thumbnail and alt text if present
            if row['RelatedSeries'] != "" or row['RelatedSeriesOrder'] != "":
                update_related_dictionary(row, artwork_dictionary)
                
                # Add to artwork so it can link back! Complex List of Lists
                artwork_dictionary['RelatedSeriesAndURL'] = [[u.strip(), urlify(u)] for u in row['RelatedSeries'].split(";")]
        
            # Add Related Writing
            artwork_dictionary['RelatedWritingURL'] = row['RelatedWriting']

        else:
            print("        !! Skipped over adding entry. No Img urls found for |{0}|\n".format(row['Artwork'].replace("\n","")[0:40]))

       
    return_list.append(tmp_dict)
    return return_list

def addCategorySingle(fandomKey = "", sheetName = ""):
    artworksCategories = ArtworkCategory(
        sheet_name = sheetName,
        output_path = file_path_output_path,
        fandoms_list = [
                {
                    "Section": fandomKey,
                    "Filename": "art-{0}".format(fandomKey.lower())
                }
            ],
        base_url = "art/{0}/".format(fandomKey.lower()),
    )

    for category in artworksCategories.Fandoms:
        main(artworksCategories.SheetName, artworksCategories.getFileNamePath(spoilers = True, filename = category["Filename"]), fandoms = [category["Section"]], include_spoilers=True, base_url=artworksCategories.BaseURL)
        main(artworksCategories.SheetName, artworksCategories.getFileNamePath(spoilers = False, filename = category["Filename"]), fandoms = [category["Section"]], include_spoilers=False, base_url=artworksCategories.BaseURL)

def addCategoryFromMultiple(fandomKey = "", sheetName = "", exclude_crossover=True):
    artworksCategories = ArtworkCategory(
        sheet_name = sheetName,
        output_path = file_path_output_path,
        fandoms_list = [
                {
                    "Section": fandomKey,
                    "Filename": "art-{0}".format(fandomKey.lower())
                }
            ],
        base_url = "art/{0}/".format(fandomKey.lower()),
    )

    # OLD
    for category in artworksCategories.Fandoms:
        main(artworksCategories.SheetName, 
             artworksCategories.getFileNamePath(spoilers = True, filename = category["Filename"]), 
             fandoms = [category["Section"]], include_spoilers=True, 
             base_url=artworksCategories.NewBaseURL,
             fandoms_str=category["Section"],
             exclude_crossover = exclude_crossover)
        main(artworksCategories.SheetName, 
             artworksCategories.getFileNamePath(spoilers = False, filename = category["Filename"]), 
             fandoms = [category["Section"]], include_spoilers=False, 
             base_url=artworksCategories.NewBaseURL,
             fandoms_str=category["Section"],
             exclude_crossover = exclude_crossover)
   
    # # NEW
    # for category in artworksCategories.Fandoms:
    #     main(artworksCategories.SheetName, 
    #          artworksCategories.getFileNamePath(spoilers = False, filename = category["Filename"]), 
    #          fandoms = [category["Section"]], include_spoilers=False, 
    #          base_url=artworksCategories.NewBaseURL, 
    #          fandoms_str=category["Section"])
    #     main(artworksCategories.SheetName, 
    #          artworksCategories.getFileNamePath(spoilers = True, filename = category["Filename"]), 
    #          fandoms = [category["Section"]], include_spoilers=True, 
    #          base_url=artworksCategories.NewBaseURL, 
    #          fandoms_str=category["Section"])



def method1(nsOnly: pandas.DataFrame,base_url) -> str:
    artwork_dictionary_list = make_url_dict(nsOnly,base_url)
    
    # remove the outer dictionary/list
    nested_json = json.dumps(artwork_dictionary_list[0]["ARTWORK"], indent=2)

    return nested_json

def main(sheet_name, file_path_output, fandoms = [""], include_spoilers = True, base_url="/", fandoms_str="", exclude_crossover=True):
    print('Processing. Sheet: {0}. Include Spoilers: {1}'.format(sheet_name, include_spoilers), end="")
    print(' Fandom: {0}.'.format(fandoms))

    # Read Excel file
    excel_data_df = pandas.read_excel(
        file_path_input,
        sheet_name=sheet_name,
        usecols=['Artwork', 'NS?', "Earliest Date", "WebsIteDateUTC",
                 'Spoilers',
                'characters','fandom','PF Tags',
                'title','summary','detail', 'warnings',
                'RelatedSeries','RelatedSeriesOrder', 'RelatedWriting',
                'IMG THMB', 'ALT THMB',
                'IMG 1','IMG 2','IMG 3','IMG 4','IMG 5','IMG 6','IMG 7','IMG 8',
                'ALT 1','ALT 2','ALT 3','ALT 4','ALT 5','ALT 6','ALT 7','ALT 8',
                'REF 1', 'REF ALT 1',
                'VID 1',
                'Tumblr URL',
                'Pillowfort URL',
                'Bluesky URL',
                'Cohost URL', 'Mastodon URL', 'Sheezy URL', 'Cara URL'
                ]
        )

    # only get nightshaded artworks and...
    options = ['Yes','yes', 'skipped', 'Skipped']
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

    # Filter by Crossover
    if exclude_crossover:
        nightshadeOnly = nightshadeOnly[~nightshadeOnly["fandom"].str.contains("Crossover", regex=False)]


    # Choose to filter by fandoms
    # 25.03: use fandom_str to filter by a fandom when multiple are listed - good for crossovers...kinda
    
    # Second thought. If it's a cross over, just... put them in a general/crossover section?
    # Then in the 11ty JS file, filter based on the fandom list? Kinda like how spoilers/nospoilers are?
    
    #    Ex: fandom: ["TWEWY, LobotomyCorporation, Crossover"]
    #    if fandom_str is "LobotomyCorporation", is will be returned 
    # using fandoms (a list/array) is the old way of doing is and will only work for EXACT matches
    # plan for TWEWY and NTWEWY is to get them seperate here and then combine them in the 11ty js file
    # like how no-spoilers and spoilers are combined.
    if fandoms_str != "":
        nightshadeOnly = nightshadeOnly[nightshadeOnly["fandom"].str.contains(fandoms_str, regex=False)]
    elif len(fandoms) == 1:
        nightshadeOnly = nightshadeOnly[nightshadeOnly["fandom"].isin(fandoms)]

    # "The Sheets API doesn't know what to do with a Python datetime/timestamp. You'll need to convert it - most likely to a str." 
    #https://stackoverflow.com/questions/49243736/how-do-i-handle-object-of-type-timestamp-is-not-json-serializable-in-python
    # '%Y-%m-%d' -> yyyy-MM-dd
    # ex: Timestamp('2024-03-23 00:00:00') -> '2024-03-23' for Fathers using Windows 11 Paint  
    nightshadeOnly[date_column_name] = nightshadeOnly[date_column_name].dt.strftime('%Y-%m-%d')

    # sort
    nightshadeOnly.sort_values(by=[date_column_name], inplace=True, ascending=False)

    print(" 1. Processing DataFrame", end="...\n")
    # Convert DataFrame to JSON
    json_str = method1(nightshadeOnly, base_url)

    print(" 2. Updating JSON Data", end="...")
    # Output - can ge to the json file in the src area
    with open(file_path_output, 'w', encoding='utf-8') as f:
        f.write(json_str)

    print(" Completed!\n")

if __name__ == '__main__':

    # Read currently existing TWEWY related series information
    # ex: banner stuff + alt text
    file_path_output = os.path.join(file_path_output_path, filename_output_related_twewy)
    with open(file_path_output, 'r') as file:
        test_rel_series = json.load(file)

    twewy_related_series_list = RelatedSeriesList()
    twewy_related_series_list.loadSeriesOnlyFromJson(test_rel_series)
    
    # READ EXCEL FILE
    # TWEWY ----------------------------------------------------------- #
    twewy_art = ArtworkCategory(
        sheet_name = 'TWEWY Series',
        output_path = file_path_output_path,
        fandoms_list = [
                {
                    "Section": "TWEWY",
                    "Filename": "twewy-art"
                },
                {
                    "Section": "NTWEWY",
                    "Filename": "twewy-neo-art"
                },
                {
                    "Section": "TWEWY, NTWEWY",
                    "Filename": "twewy-series"
                } 
            ],
        base_url = "art/twewy/"
    )

    for category in twewy_art.Fandoms:
        main(twewy_art.SheetName, twewy_art.getFileNamePath(spoilers = True, filename = category["Filename"]), fandoms = [category["Section"]], include_spoilers=True, base_url=twewy_art.BaseURL)
        main(twewy_art.SheetName, twewy_art.getFileNamePath(spoilers = False, filename = category["Filename"]), fandoms = [category["Section"]], include_spoilers=False, base_url=twewy_art.BaseURL)

    # Write Related Series JSON
    # Sort Series Enrties by index
    twewy_related_series_list.sortSeriesEntries()

    # Output - can ge to the json file in the src area
    nested_json = json.dumps(twewy_related_series_list.Series, default=lambda x: x.__dict__, indent=2) 
    file_path_output = os.path.join(file_path_output_path, filename_output_related_twewy)
    with open(file_path_output, 'w', encoding='utf-8') as f:
        f.write(nested_json)

    # Reset it???
    twewy_related_series_list = RelatedSeriesList()
    
    # PERSONA 5 ----------------------------------------------------------- #
    persona5_art = ArtworkCategory(
        sheet_name = 'Other',
        output_path = file_path_output_path,
        fandoms_list = [
                {
                    "Section": "persona5",
                    "Filename": "art-persona5"
                }
            ],
        base_url = "art/persona5/"
    )

    for category in persona5_art.Fandoms:
        main(persona5_art.SheetName, persona5_art.getFileNamePath(spoilers = True, filename = category["Filename"]), fandoms = [category["Section"]], include_spoilers=True, base_url=persona5_art.BaseURL)
        main(persona5_art.SheetName, persona5_art.getFileNamePath(spoilers = False, filename = category["Filename"]), fandoms = [category["Section"]], include_spoilers=False, base_url=persona5_art.BaseURL)

    # XCX----------------------------------------------------------- #
    fandomkey = "XCX"
    artworksCategories = ArtworkCategory(
        sheet_name = 'Other',
        output_path = file_path_output_path,
        fandoms_list = [
                {
                    "Section": fandomkey,
                    "Filename": "art-{0}".format(fandomkey.lower())
                }
            ],
        base_url = "art/{0}/".format(fandomkey.lower())
    )

    for category in artworksCategories.Fandoms:
        main(artworksCategories.SheetName, artworksCategories.getFileNamePath(spoilers = True, filename = category["Filename"]), fandoms = [category["Section"]], include_spoilers=True, base_url=artworksCategories.BaseURL)
        main(artworksCategories.SheetName, artworksCategories.getFileNamePath(spoilers = False, filename = category["Filename"]), fandoms = [category["Section"]], include_spoilers=False, base_url=artworksCategories.BaseURL)

    # Write Related Series JSON
    # Sort Series Enrties by index
    twewy_related_series_list.sortSeriesEntries()

    # Output - can ge to the json file in the src area
    nested_json = json.dumps(twewy_related_series_list.Series, default=lambda x: x.__dict__, indent=2) 
    file_path_output = os.path.join(file_path_output_path, filename_output_related_xcx)
    with open(file_path_output, 'w', encoding='utf-8') as f:
        f.write(nested_json)

    # Reset it???
    twewy_related_series_list = RelatedSeriesList()

    # Asura's wrath----------------------------------------------------------- #
    fandomkey = "asuras-wrath"
    artworksCategories = ArtworkCategory(
        sheet_name = 'Other',
        output_path = file_path_output_path,
        fandoms_list = [
                {
                    "Section": fandomkey,
                    "Filename": "art-{0}".format(fandomkey.lower())
                }
            ],
        base_url = "art/{0}/".format(fandomkey.lower()),
    )

    for category in artworksCategories.Fandoms:
        main(artworksCategories.SheetName, artworksCategories.getFileNamePath(spoilers = True, filename = category["Filename"]), fandoms = [category["Section"]], include_spoilers=True, base_url=artworksCategories.BaseURL)
        main(artworksCategories.SheetName, artworksCategories.getFileNamePath(spoilers = False, filename = category["Filename"]), fandoms = [category["Section"]], include_spoilers=False, base_url=artworksCategories.BaseURL)

    ## ArtFight
    # addCategorySingle("ArtFight","Other")


    ## Fandoms
    # addCategorySingle("Splatoon","Other")
    addCategoryFromMultiple("ProjectMoon","Other", exclude_crossover=True)

    # addCategoryFromMultiple("Pikmin","Other")
    addCategoryFromMultiple("void-stranger","Other")
    addCategoryFromMultiple("Pokemon","Other")
    addCategoryFromMultiple("Kirby","Other")
    addCategoryFromMultiple("Deltarune","Other")
    addCategoryFromMultiple("LaMulana","Other")
    # addCategoryFromMultiple("super-puzzled-cat","Other")


    # HOW TO HANDLE THE CROSS OVER STUFF
    # xover ----------------------------------------------------------- #
    # use new base URL which won't have the fandom specific - good for cross overs
    # will use art/gen for the base path
    # As lon as one of the fandoms say "Crossover", it will be included
    fandomkey = "Crossover"
    artworksCategories = ArtworkCategory(
        sheet_name = 'Other',
        output_path = file_path_output_path,
        fandoms_list = [
                {
                    "Section": fandomkey,
                    "Filename": "art-{0}".format(fandomkey.lower())
                }
            ],
        base_url = "art/gen",
    )

    for category in artworksCategories.Fandoms:
        main(artworksCategories.SheetName, 
             artworksCategories.getFileNamePath(spoilers = False, filename = category["Filename"]), 
             fandoms = [category["Section"]], include_spoilers=False, 
             base_url=artworksCategories.NewBaseURL, 
             fandoms_str=category["Section"],
             exclude_crossover=False)
        main(artworksCategories.SheetName, 
             artworksCategories.getFileNamePath(spoilers = True, filename = category["Filename"]), 
             fandoms = [category["Section"]], include_spoilers=True, 
             base_url=artworksCategories.NewBaseURL, 
             fandoms_str=category["Section"]
             ,exclude_crossover=False)

   
        
    # # Void Stranger ----------------------------------------------------------- #
    # # use new base URL which won't have the fandom specific - good for cross overs
    # fandomkey = "void-stranger"
    # artworksCategories = ArtworkCategory(
    #     sheet_name = 'Other',
    #     output_path = file_path_output_path,
    #     fandoms_list = [
    #             {
    #                 "Section": fandomkey,
    #                 "Filename": "art-{0}".format(fandomkey.lower())
    #             }
    #         ],
    #     base_url = "art/".format(fandomkey.lower()),
    #     new_base_url = "art/".format(fandomkey.lower())
    # )

    # for category in artworksCategories.Fandoms:
    #     # main(artworksCategories.SheetName, artworksCategories.getFileNamePath(spoilers = True, filename = category["Filename"]), fandoms = [category["Section"]], include_spoilers=True, base_url=artworksCategories.BaseURL)
    #     main(artworksCategories.SheetName, 
    #          artworksCategories.getFileNamePath(spoilers = False, filename = category["Filename"]), 
    #          fandoms = [category["Section"]], include_spoilers=False, 
    #          base_url=artworksCategories.NewBaseURL, 
    #          fandoms_str=category["Section"])



    print("\nMAIN: C O M P L E T E!\n")


