import nltk
import matplotlib.pyplot as plt
from nltk import FreqDist
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download necessary NLTK resources
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("averaged_perceptron_tagger")
nltk.download("wordnet")
nltk.download("gutenberg")  # Download the Gutenberg corpus

# Read Moby Dick text from Gutenberg corpus
moby_dick_text = nltk.corpus.gutenberg.raw("melville-moby_dick.txt")

# Tokenization
tokens = word_tokenize(moby_dick_text)

# Lowercase and remove stopwords during tokenization
stop_words = set(stopwords.words("english"))
filtered_tokens = [word.lower() for word in tokens if word.isalnum() and word.lower() not in stop_words]

# Parts-of-Speech (POS) tagging
pos_tags = nltk.pos_tag(filtered_tokens)

# Calculate POS frequency
pos_freq = FreqDist(tag for _, tag in pos_tags)
common_pos = pos_freq.most_common(5)

print("Top 5 Most Common Parts of Speech:")
for pos, count in common_pos:
    print(f"{pos}: {count}")

# Lemmatization
lemmatizer = WordNetLemmatizer()
top_20_tokens = [word for word, _ in pos_freq.most_common(20)]
lemmatized_tokens = [lemmatizer.lemmatize(word, pos=get_wordnet_pos(tag)) for word, tag in pos_tags if word in top_20_tokens]

# Extract parts of speech and their frequencies
pos_counts = pos_freq.items()

# Separate parts of speech and frequencies
pos, counts = zip(*pos_counts)

# Create a bar chart for POS frequency distribution
plt.figure(figsize=(12, 6))
plt.bar(pos, counts)
plt.xlabel("Parts of Speech")
plt.ylabel("Frequency")
plt.title("POS Frequency Distribution")
plt.xticks(rotation=45)  # Rotate x-axis labels to avoid overlap
plt.tight_layout()
plt.show()
