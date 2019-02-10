import pandas as pd
import re
import os


def formattingData(df):
    # Check Gender column

    df["Gender"] = df.Gender.str.replace("Female", "F")
    df["Gender"] = df.Gender.str.replace("Male", "M")

    df["Acceptable_country"] = df.Acceptable_country.str.replace(", ", ",")  # remove the white space after ,
    df["Likes"] = df.Likes.str.replace(", ", ",")  # remove white spaces after ,
    df["Dislikes"] = df.Dislikes.str.replace(", ", ",")  # remove white spaces after ,
    df = df.replace('\n', '|', regex=True)  # replace all the \n in Books to ','

    return df


class FUNCTION_1(object):
    def __init__(self, files, profiles):
        # specify the column header
        self.HEADERS = ['Name', 'Gender', 'Country', 'Acceptable_country', 'Age', 'Acceptable_age_range', 'Likes',
                        'Dislikes', 'Books']

        self.DATA = []  # create the empty list to store profiles

        for file in files:  # iterate over each file
            filename = profiles + file  # full path name of the data files

            text_file = open(filename, "r")  # open the file
            lines = text_file.read()  # read the file in memory
            text_file.close()  # close the file

            """
            Regex to filter out all the column header and row data. 
            Odd Number == Header, Even Number == Data
            """
            profiles_data = re.search(
                "(Name):(.*)\n+(Gender):(.*)\n+(Country):(.*)\n+(Acceptable_country):(.*)\n+(Age):(.*)\n+(Acceptable_age_range):(.*)\n+(Likes):(.*)\n+(Dislikes):(.*)\n+(Books):((?<=Books:)\D+)",
                lines)

            # append data into DATA list
            self.DATA.append([profiles_data.group(i).strip() for i in range(len(profiles_data.groups()) + 1) if
                              not i % 2 and i != 0])

    def profilesDF(self, headers, data):
        df = pd.DataFrame(data, columns=headers)  # create the dataframe
        df = formattingData(df)  # format and make data nicer
        df["Rank"] = 0.0  # create a column Rank to rank the matches
        return df

    def writeBooks2File(self, booklist_dir, book_list):
        # store all the books in the a text file
        if not os.path.exists(booklist_dir):
            open(booklist_dir, "w").close()

        BOOKS = []
        condition = map(lambda b: b.split("|"), book_list)
        for i in condition:
            map(lambda a: BOOKS.append(a.rstrip()), i)

        BOOKS = list(set(BOOKS))

        rf = open(booklist_dir, "r").read().splitlines()
        af = open(booklist_dir, "a")

        re_genre = []

        for book in rf:
            if re.findall("::.*", book):
                re_genre.append(re.sub(re.findall("::.*", book)[0], '', book).rstrip())

        for val in BOOKS:
            if val not in rf and val not in re_genre:
                af.write(val + '\n')
        af.close()
