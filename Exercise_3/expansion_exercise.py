import nltk
from nltk import sentiment
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download necessary NLTK resources
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("vader_lexicon")  # Download VADER lexicon

# Read Moby Dick text from Gutenberg corpus
moby_dick_text = nltk.corpus.gutenberg.raw("melville-moby_dick.txt")

# Tokenization
tokens = word_tokenize(moby_dick_text)

# Lowercase and remove stopwords during tokenization
stop_words = set(stopwords.words("english"))
filtered_tokens = [word.lower() for word in tokens if word.isalnum() and word.lower() not in stop_words]

# Sentiment analysis using VADER
sia = SentimentIntensityAnalyzer()
sentiments = [sia.polarity_scores(word)["compound"] for word in filtered_tokens]

# Calculate the average sentiment score
average_sentiment = sum(sentiments) / len(sentiments)

# Determine the overall sentiment
overall_sentiment = "positive" if average_sentiment > 0.05 else "negative"

print(f"Average Sentiment Score: {average_sentiment}")
print(f"Overall Text Sentiment: {overall_sentiment}")
