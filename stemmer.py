import pandas as pd
import nltk
nltk.download('wordnet')
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
from nltk.stem import WordNetLemmatizer
# Use English stemmer.
stemmer = WordNetLemmatizer()

# Sentences to be stemmed.
data = ["programers program with programing languages", "my code is working so there must be a bug in the optimizer"] 
    
# Create the Pandas dataFrame.
df = pd.DataFrame(data, columns = ['unstemmed']) 


# Split the sentences to lists of words.
df['unstemmed'] = df['unstemmed'].str.split()
df['stemmed'] = df['unstemmed'].apply(lambda x: [stemmer.lemmatize(y) for y in x]) # Stem every word.

# Make sure we see the full column.
pd.set_option('display.max_colwidth', None)

# Print dataframe.
print(df) 
