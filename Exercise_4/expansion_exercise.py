import nltk
from nltk.corpus import gutenberg
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import string
from gensim import corpora
from gensim.models import LdaModel
import pyLDAvis.gensim_models as gensimvis
import pyLDAvis
import joblib
import os

# Set the backend for joblib to 'threading'
joblib.parallel.DEFAULT_BACKEND = 'threading'

# Set the temporary folder path for joblib to an ASCII character path
os.environ['JOBLIB_TEMP_FOLDER'] = 'Exercise_4'

# Download necessary NLTK data
nltk.download('gutenberg')
nltk.download('punkt')
nltk.download('stopwords')

# Load the text of "Alice's Adventures in Wonderland"
alice_text = gutenberg.raw('carroll-alice.txt')

# Tokenize the text into sentences and words
sentences = sent_tokenize(alice_text)
words = [word_tokenize(sentence) for sentence in sentences]

# Define stop words and punctuation
stop_words = set(stopwords.words('english'))
punctuation = set(string.punctuation)

# Preprocess the text
processed_words = [
    [word.lower() for word in sentence if word.lower() not in stop_words and word not in punctuation]
    for sentence in words
]

# Create a dictionary and a corpus
dictionary = corpora.Dictionary(processed_words)
corpus = [dictionary.doc2bow(text) for text in processed_words]

# Set the number of topics
num_topics = 5

# Build the LDA model
lda_model = LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=15)

# Create the topic visualization
vis_data = gensimvis.prepare(lda_model, corpus, dictionary)
pyLDAvis.display(vis_data)

# Save the HTML visualization in the Exercise_4 folder
html_file_path = 'Exercise_4/lda_visualization.html'
pyLDAvis.save_html(vis_data, html_file_path)
