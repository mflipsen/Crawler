import pandas as pd
from setup import base, case
from general import dir_case


def read_information():
    # go to case folder and create path to csv file
    dir_case(base, case)
    f = case + "_text.csv"

    # create dataframe from csv file
    df = pd.read_csv(f, sep=',',
                     encoding='utf-8',
                     error_bad_lines=False,
                     header=None,
                     index_col=0)

    # find all the keywords that didn't yield information
    empty = []
    col = df[1]

    for i, j in col.iteritems():
        if j == '[]':
            empty.append(i)

    # drop all keywords that don't have information
    df2 = df[df.index.map(lambda x: str(x) not in empty)]

    # join all columns into one
    cols = len(df.columns)
    ser = df2.iloc[:, 0:cols].apply(lambda x: '\n'.join(x.map(str)), axis=1)

    # for each keyword, create separate text file
    for i, j in ser.iteritems():
        path = str(i) + '.txt'
        with open(path, 'w', encoding="utf-8") as f:
            f.write(j)
