#make sure pandas and openpyxl are installed
# Winwdows
# > py -m pip install pandas
import pandas
import logging, sys
import json
import os

filename_input = "Where Is My Art.xlsx"
filename_output_twewy = "twewy-art.json"
filename_output_p5 = "art-persona5.json"
file_path_input = os.path.join(os.getcwd(),"data_conversion\\", filename_input)
file_path_output_path = os.path.join(os.getcwd(),"src\_data\\")

date_column_name = "Earliest Date"
max_num_images = 6

# functions
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

def make_url_dict(mydataframe: pandas.DataFrame) -> list:
    return_list = []
    dict_key = "ARTWORK"
    urls_key = "urls"
    tmp_dict = {dict_key: []}
    for _, row in mydataframe.iterrows():

        artwork_dictionary =  {
            'title': row['title'], 
            'summary': row['summary'], 
            'details': row['detail'],
            'characters': row['characters']
        }
        artwork_dictionary['date'] = row[date_column_name]
        artwork_dictionary['dateYear'] = row[date_column_name][0:4]
        artwork_dictionary['uniqueUrl'] = "{0}-{1}".format(row[date_column_name],row['Artwork'].replace("\n","")[0:10])
        artwork_dictionary['spoilers'] = row['Spoilers']

        if row['title'] == "":
            print("Title is missing for |{0}|".format(row['Artwork'].replace("\n","")[0:40]))

        if row['characters'] == "":
            print("characters is missing for |{0}|".format(row['Artwork'].replace("\n","")[0:40]))

        artwork_dictionary['urls'] = []

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

        artwork_dictionary['imgs'] = make_img_list(row)

        artwork_dictionary['fandom'] = row['fandom'].split(",")

        if artwork_dictionary['imgs']:
            # completed, add to final dictionary
            tmp_dict[dict_key].append(artwork_dictionary)
        else:
            print("    Skipped over adding entry. No Img urls found for |{0}|\n".format(row['Artwork'].replace("\n","")[0:40]))

    return_list.append(tmp_dict)
    return return_list

def method1(nsOnly: pandas.DataFrame) -> str:
    artwork_dictionary_list = make_url_dict(nsOnly)
    
    # remove the outer dictionary/list
    nested_json = json.dumps(artwork_dictionary_list[0]["ARTWORK"], indent=2)

    #TO DO?
    # Another variant of the dumps() function, called dump(), simply serializes the object to a text file. So if f is a text file object opened for writing, we can do this:
    # json.dump(x, f)

    return nested_json

def main(sheet_name, file_path_output, fandom = [""], include_spoilers = True):
    print('\n1. Reading Excel File for {0}\n'.format(sheet_name))

    # Read Excel file
    excel_data_df = pandas.read_excel(
        file_path_input,
        sheet_name=sheet_name,
        usecols=['Artwork', 'NS?', "Earliest Date",
                 'Spoilers',
                'Tumblr URL',
                'Pillowfort URL',
                'Bluesky URL',
                'Cohost URL', 
                'ALT 1','ALT 2','ALT 3','ALT 4','ALT 5','ALT 6',
                'characters','fandom','PF tags',
                'title','summary','detail',
                'IMG 1','IMG 2','IMG 3','IMG 4','IMG 5','IMG 6']
        )

    # only get nightshaded artworks
    options = ['Yes','yes']
    nightshadeOnly = excel_data_df[excel_data_df["NS?"].isin(options)]

    # CLEAN UP - Set Defaults
    # fill in NaN as ""
    # nightshadeOnly.fillna("", inplace=True)


    values = {"Spoilers": "Unknown", "fandom": "Unknown", "NS?": ""}

    nightshadeOnly.fillna(value=values, inplace=True)
    

    # "The Sheets API doesn't know what to do with a Python datetime/timestamp. You'll need to convert it - most likely to a str." 
    #https://stackoverflow.com/questions/49243736/how-do-i-handle-object-of-type-timestamp-is-not-json-serializable-in-python
    # '%Y-%m-%d' -> yyyy-MM-dd
    # ex: Timestamp('2024-03-23 00:00:00') -> '2024-03-23' for Fathers using Windows 11 Paint  
    nightshadeOnly[date_column_name] = nightshadeOnly[date_column_name].dt.strftime('%Y-%m-%d')

    nightshadeOnly.sort_values(by=[date_column_name], inplace=True, ascending=False)

    print("\n2. Processing DataFrame.\n")
    # Convert DataFrame to JSON
    json_str = method1(nightshadeOnly)

    print("\n3. Updating JSON Data.\n")
    # Output - can ge to the json file in the src area
    with open(file_path_output, 'w', encoding='utf-8') as f:
        f.write(json_str)

    print("\n4. Completed.\n")

if __name__ == '__main__':
    # TWEWY
    file_path_output = os.path.join(file_path_output_path, filename_output_twewy)
    main('TWEWY Series', file_path_output)

    # Persona 5 Sheet
    # file_path_output = os.path.join(file_path_output_path, filename_output_p5)
    # main('Other', file_path_output)


