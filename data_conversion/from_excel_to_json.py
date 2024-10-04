#make sure pandas and openpyxl are installed
# Winwdows
# > py -m pip install pandas
import pandas
import urllib3
import json
import os
import re

# Excel Database Filename
filename_input = "Where Is My Art.xlsx"

# GENERATE - TWEWY JSON Files
filename_output_twewy_og_all = "twewy-art.json"
filename_output_twewy_og_nospoilers = "twewy-art-spoiler-free.json"
filename_output_twewy_neo_all = "twewy-neo-art.json"
filename_output_twewy_neo_nospoilers = "twewy-neo-art-spoiler-free.json"
filename_output_twewy_series_all = "twewy-series.json"
filename_output_twewy_series_nospoilers = "twewy-series-spoiler-free.json"

# GENERATE - PERSONA 5 JSON Files
filename_output_p5 = "art-persona5.json"
filename_output_p5_nospoilers = "art-persona5-spoiler-free.json"

# GENERATE - Related Series Files
filename_output_related_twewy = "relatedtwewy.json"

file_path_input = os.path.join(os.getcwd(),"data_conversion\\", filename_input)
file_path_output_path = os.path.join(os.getcwd(),"src\\_data\\")

date_column_name = "Earliest Date"
max_num_images = 8
max_num_videos = 1

related_series_list = []

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
            print("Img URL missing: |{0}| for #{1}".format(artwork_id, i))
            continue

        # if there is an image, but no alt text - warn
        if _row['IMG {0}'.format(i)] != "" and _row['ALT {0}'.format(i)] == "":
            print("Alt text missing! |{0}| for #{1}".format(artwork_id, i))
            continue

        test_url = get_img_url(_row, kay_img)
        # make sure we don't have the src directory - might get included by accident!
        if "src" in test_url:
            print("!! Img URL contains src. Fixing for |{0}| #{1}".format(artwork_id, i))
            test_url = test_url.replace("src","")

        # make sure it's at root if not using https
        if "https" not in test_url and '\\' != test_url[0:1]:
            print("!! Img URL missing \\. Fixing for |{0}| #{1}".format(artwork_id, i))
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
            print("!! VIDEO URL contains src. Fixing for |{0}| #{1}".format(artwork_id, i))
            test_url = test_url.replace("src","")

        # we have an image and alt text - good to add
        vid_list.append({'id': i, 'url': test_url})

    return vid_list

# RELATED DICTIONARY -------------------------------------
def find_rel_dict_ser_name_index(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1

def update_related_dictionary(rw, rw_unique_url):

    artworkname = rw['Artwork'].replace("\n","")[0:40]

    foundseries = rw['RelatedSeries'].split(";")
    foundindices = rw['RelatedSeriesOrder'].split(";")

    for i_index, i_name in enumerate(foundseries):
        i_name = i_name.strip()

        index_dict = find_rel_dict_ser_name_index(related_series_list, "SeriesName", i_name)

        # Get the index of the entry in the series
        int_i_index = -1
        if i_index < len(foundindices):
            try:
                int_i_index = foundindices[i_index]
                int_i_index = int(int_i_index)
            except ValueError:
                int_i_index = -1
                print("    Related for {0} -AU/Series- {1}".format(artworkname,i_name))
                print("      !! TODO: Current index [{0}] for foundindices is not an int! Default to [-1].".format(i_index,foundindices[i_index]))
        else:
            print("    Related for {0} -AU/Series- {1}".format(artworkname,i_name))
            print("      '! Current index [{0}] is less than indices found: {1}. Default to [-1].".format(i_index,foundindices))
        
        # Add new seriesand first entry
        if index_dict == -1:
            rel_dictionary = {
                'SeriesName': i_name,
                "SeriesURL": urlify(i_name),
                'SeriesEntries': [ {
                        'Index': int_i_index,
                        'Name': rw['title'],
                        'URL': rw_unique_url
                    }
                ]
            }
            # Add with defaults
            related_series_list.append(rel_dictionary)
        # Add new entry to existing series
        else:
            new_entry = {
                    'Index': int_i_index,
                    'Name': rw['title'],
                    'URL': rw_unique_url
                }
            
            related_series_list[index_dict]["SeriesEntries"].append(new_entry)
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

        # Set up the URL ahead of time - will act as a Key for the artwork
        artwork_dictionary['uniqueUrl'] = "{0}-{1}".format(row[date_column_name],row['Artwork'].replace("\n","").strip()[0:10])
        artwork_dictionary['uniqueUrl'] = urlify(artwork_dictionary['uniqueUrl'] )
        artwork_dictionary['uniqueUrl'] = urllib3.util.parse_url(artwork_dictionary['uniqueUrl']).url

        #full relative URL in order to link to other pieces
        artwork_dictionary['UniqueURLKey'] = os.path.join(base_url, artwork_dictionary['uniqueUrl'])

        artwork_dictionary['spoilers'] = row['Spoilers']

        if row['title'] == "":
            print("    Title is missing for |{0}|".format(artworkname))

        if row['characters'] == "":
            print("    characters is missing for |{0}|".format(artworkname))

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
        artwork_dictionary['imgs'] = make_img_list(row)

        # Add Image thumbnail and alt text if present
        if row['IMG THMB'] != "" or row['ALT THMB'] != "":
            if row['IMG THMB'] == "":
                print("    IMG THMB is missing for |{0}|".format(artworkname))
            elif row['ALT THMB'] == "":
                print("    ALT THMB is missing for |{0}|".format(artworkname))
            else:
                artwork_dictionary['thumbnailUrl'] = row['IMG THMB']
                artwork_dictionary['thumbnailAlt'] = row['ALT THMB']

        # CHECK IF HAVE MINIMUM -----------------------------------
        # Add if img + alt was found, otherwise, print warning message
        if artwork_dictionary['imgs']:
            # completed, add to final dictionary
            tmp_dict[dict_key].append(artwork_dictionary)
        else:
            print("    Skipped over adding entry. No Img urls found for |{0}|\n".format(row['Artwork'].replace("\n","")[0:40]))

        # VIDEOS -------------------------------------------------
        artwork_dictionary['vids'] = make_vid_list(row)

         # FANDOM LISTING -----------------------------------------
        artwork_dictionary['fandom'] = row['fandom'].split(",")

        # List of related artworks
        # Add Image thumbnail and alt text if present
        if row['RelatedSeries'] != "" or row['RelatedSeriesOrder'] != "":
            update_related_dictionary(row, artwork_dictionary['UniqueURLKey'])
            
            # Add to artwork so it can link back! Complex List of Lists
            artwork_dictionary['RelatedSeriesAndURL'] = [[u.strip(), urlify(u)] for u in row['RelatedSeries'].split(";")]

    return_list.append(tmp_dict)
    return return_list

def method1(nsOnly: pandas.DataFrame,base_url) -> str:
    artwork_dictionary_list = make_url_dict(nsOnly,base_url)
    
    # remove the outer dictionary/list
    nested_json = json.dumps(artwork_dictionary_list[0]["ARTWORK"], indent=2)

    return nested_json

def main(sheet_name, file_path_output, fandoms = [""], include_spoilers = True, base_url="/"):
    print('Processing: {0}. Include Spoilers: {1}'.format(sheet_name,  include_spoilers))
    print(' 1. Reading Excel File for {0}'.format(sheet_name), end="...\n")

    # Read Excel file
    excel_data_df = pandas.read_excel(
        file_path_input,
        sheet_name=sheet_name,
        usecols=['Artwork', 'NS?', "Earliest Date",
                 'Spoilers',
                'characters','fandom','PF tags',
                'title','summary','detail',
                'RelatedSeries','RelatedSeriesOrder',
                'IMG THMB', 'ALT THMB',
                'IMG 1','IMG 2','IMG 3','IMG 4','IMG 5','IMG 6','IMG 7','IMG 8',
                'ALT 1','ALT 2','ALT 3','ALT 4','ALT 5','ALT 6','ALT 7','ALT 8',
                'VID 1',
                'Tumblr URL',
                'Pillowfort URL',
                'Bluesky URL',
                'Cohost URL' 
                ]
        )

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
    nightshadeOnly[date_column_name] = nightshadeOnly[date_column_name].dt.strftime('%Y-%m-%d')

    # sort
    nightshadeOnly.sort_values(by=[date_column_name], inplace=True, ascending=False)

    print(" 2. Processing DataFrame", end="...\n")
    # Convert DataFrame to JSON
    json_str = method1(nightshadeOnly, base_url)

    print(" 3. Updating JSON Data", end="...\n")
    # Output - can ge to the json file in the src area
    with open(file_path_output, 'w', encoding='utf-8') as f:
        f.write(json_str)

    print(" 4. Completed!\n")

if __name__ == '__main__':
    # # TWEWY OG
    # file_path_output = os.path.join(file_path_output_path, filename_output_twewy_og_all)
    # main('TWEWY Series', file_path_output, fandoms = ["TWEWY"], include_spoilers=True, base_url="art/twewy/")

    # file_path_output = os.path.join(file_path_output_path, filename_output_twewy_og_nospoilers)
    # main('TWEWY Series', file_path_output, fandoms = ["TWEWY"], include_spoilers=False, base_url="art/twewy/")

    # # NEO TWEWY
    # file_path_output = os.path.join(file_path_output_path, filename_output_twewy_neo_nospoilers)
    # main('TWEWY Series', file_path_output, fandoms = ["NTWEWY"], include_spoilers=False, base_url="art/twewy/")

    # file_path_output = os.path.join(file_path_output_path, filename_output_twewy_neo_all)
    # main('TWEWY Series', file_path_output, fandoms = ["NTWEWY"], include_spoilers=True, base_url="art/twewy/")

    # # TWEWY Series
    # file_path_output = os.path.join(file_path_output_path, filename_output_twewy_series_nospoilers)
    # main('TWEWY Series', file_path_output, fandoms = ["TWEWY, NTWEWY"], include_spoilers=False, base_url="art/twewy/")

    # file_path_output = os.path.join(file_path_output_path, filename_output_twewy_series_all)
    # main('TWEWY Series', file_path_output, fandoms = ["TWEWY, NTWEWY"], include_spoilers=True, base_url="art/twewy/")

    # # Write Related Series JSON
    # # Output - can ge to the json file in the src area

    # for rel_list_item in related_series_list:
    #     rel_list_item["SeriesEntries"].sort(key=lambda x: x["Index"])

    # nested_json = json.dumps(related_series_list, indent=2)
    # file_path_output = os.path.join(file_path_output_path, filename_output_related_twewy)
    # with open(file_path_output, 'w', encoding='utf-8') as f:
    #     f.write(nested_json)

    # OTHER - Persona 5 Sheet
    fandomkey="persona5"
    file_path_output = os.path.join(file_path_output_path, filename_output_p5)
    main('Other', file_path_output, fandoms = [fandomkey], include_spoilers=True, base_url="art/{0}/".format(fandomkey))

    
    file_path_output = os.path.join(file_path_output_path, filename_output_p5_nospoilers)
    main('Other', file_path_output, fandoms = [fandomkey], include_spoilers=False, base_url="art/{0}/".format(fandomkey))


    print("\nMAIN: C O M P L E T E!\n")


