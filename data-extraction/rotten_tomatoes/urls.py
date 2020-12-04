# movie lens database: https://grouplens.org/datasets/movielens/25m/
# movie url ex.: https://www.rottentomatoes.com/m/indiana_jones

import pandas as pd
import string

def clean(name):
    return name.rsplit(' ', 1)[0]

def toUrl(name):
    # lowercase
    name = name.lower()

    # Remove THE word
    if name.split()[-1] == 'the':
        name = clean(name)
    
    # exclude punctuation marks
    exclude = set(string.punctuation)
    name = ''.join(ch for ch in name if ch not in exclude)

    # replace [', , (, )] --> _
    name = name.replace(" ", "_")
    return name

def generateUrls(input_path, output_path):
    df = pd.read_csv(input_path)
    dropColumns = ['genres']
    column_name = 'title'
    column_url = 'url_name'

    # Clean process
    df = df.drop(columns = dropColumns)
    df[column_name] = df[column_name].apply(clean)
    df[column_url] = df[column_name].apply(toUrl)

    # Save process
    df.to_csv(output_path, index = False)

def nameToUrl(name):
    url_template = "https://www.rottentomatoes.com/m/{}"
    return url_template.format(name)

def get_urls(base_path):
    import pandas as pd
    df = pd.read_csv(base_path)

    # Transform url_name to url
    df['url_name'] = df['url_name'].apply(nameToUrl)

    return df['url_name'].tolist(),df['movieId'].tolist()

if __name__ == '__main__':
    import pandas as pd

    base_path = '../../raw-data/'
    in_filename = 'movies.csv'
    out_filename = 'movies_names.csv'

    generateUrls(base_path + in_filename, base_path + out_filename)
