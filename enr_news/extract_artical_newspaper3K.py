import newspaper
import pandas as pd
import os
import nltk

# file_name = 'ENR_Suicide1707251574.5247946.csv'
# file_name = 'ENR_Kashmir1707799530.7017083.csv'
# # nltk.download('punkt')
#
# script_dir = os.path.dirname(os.path.abspath(__file__))
# csv_file_path = os.path.join(script_dir, '../outputs/'+file_name)
# df = pd.read_csv(csv_file_path)


def extract_articles(df):
    for index, row in df.iterrows():
        try:
            try:
                current_article = newspaper.Article(row.get('web_link'))
                current_article.download()
                current_article.parse()
                current_article.nlp()
            except:
                print('')
            try:
                author_list = current_article.authors
                df.at[index, 'Authors'] = ','.join(author_list)
            except:
                print(f"Issue with authors for panda index {index}")
            try:
                df.at[index, 'Keywords'] = ','.join(current_article.keywords)
            except:
                print(f"Issue with Keywords for panda index {index}")
            try:
                df.at[index, 'Summary'] = current_article.summary
            except:
                print(f"Issue with Summary for panda index {index}")

            try:
                df.at[index, 'MetaData'] = current_article.meta_data
            except:
                print(f"Issue with MetaData for panda index {index}")
            try:
                df.at[index, 'Article'] = current_article.text
            except:
                print(f"Issue with Article for panda index {index}")

        except:
            print(f"Had issue with index :{index} in pandas, while extracting articles")
            continue
    return df

# print(df)

# csv_path = 'D:/Applications/Idea-Projects/scrappings/outputs/final/ENR_' + file_name
# df.to_csv(csv_path, index=False)
# Display the DataFrame
# print(df)

