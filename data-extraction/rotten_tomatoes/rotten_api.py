import requests

def clean(name):
    return name.rsplit(' ', 1)[0]

def generateUrls(input_path, output_path):
    df = pd.read_csv(input_path)
    column_name = 'title'
    column_url = 'url_name'

    # Clean process
    df = df.drop(columns = dropColumns)
    df[column_name] = df[column_name].apply(clean)
    df[column_url] = df[column_name].apply(toUrl)

    # Save process
    df.to_csv(output_path, index = False)

if __name__ == '__main__':
    import pandas as pd

    base_path = '../movielens/'
    in_filename = 'movies_names.csv'
    out_filename = 'movies_urls.csv'

    generateUrls(base_path + in_filename, base_path + out_filename)
