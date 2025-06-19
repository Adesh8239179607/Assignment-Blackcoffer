# 1. Install required packages
!pip install fake_useragent
import numpy as np
import re
import os
import pandas as pd
from nltk.tokenize import RegexpTokenizer, sent_tokenize
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests

# 2. Unzip dictionary and stopwords files (run only once)
!unzip -o /content/drive/MyDrive/Assignment/MasterDictionary-20250618T042156Z-1-001.zip -d /content/drive/MyDrive/Assignment
!unzip -o /content/drive/MyDrive/Assignment/StopWords-20250618T042155Z-1-001.zip -d /content/drive/MyDrive/Assignment

# 3. File paths
stopWordsFile = '/content/drive/MyDrive/Assignment/StopWords/StopWords_Generic.txt'
positiveWordsFile = '/content/drive/MyDrive/Assignment/MasterDictionary/positive-words.txt'
nagitiveWordsFile = '/content/drive/MyDrive/Assignment/MasterDictionary/negative-words.txt'

# 4. Load input URLs
input_df = pd.read_excel("/content/drive/MyDrive/Assignment/Input.xlsx")

def get_article_names(urls):
    titles = []
    for url in urls:
        try:
            title_clean = url[url.index("m/") + 2 : -1].replace('-', ' ')
            titles.append(title_clean)
        except Exception:
            titles.append(url)
    return titles

urls = input_df["URL"]
urlsTitleDF = get_article_names(urls)

# 5. Load word lists
with open(positiveWordsFile, 'r') as posfile:
    positiveWordList = posfile.read().lower().split('\n')

with open(nagitiveWordsFile, 'r', encoding="ISO-8859-1") as negfile:
    negativeWordList = negfile.read().lower().split('\n')

with open(stopWordsFile, 'r') as stop_words:
    stopWordList = stop_words.read().lower().split('\n')
stopWordList = [w for w in stopWordList if w]

# 6. Tokenizer
def tokenizer(text):
    text = text.lower()
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    filtered_words = [token for token in tokens if token not in stopWordList]
    return filtered_words

# 7. Scoring functions
def positive_score(text):
    return sum(1 for word in tokenizer(text) if word in positiveWordList)

def negative_score(text):
    return sum(1 for word in tokenizer(text) if word in negativeWordList)

def polarity_score(positive, negative):
    return (positive - negative) / ((positive + negative) + 1e-6)

def total_word_count(text):
    return len(tokenizer(text))

def subjectivity_score(positive, negative, total_words):
    return (positive + negative) / (total_words + 1e-6)

def AverageSentenceLength(text):
    Wordcount = len(tokenizer(text))
    SentenceCount = len(sent_tokenize(text))
    return Wordcount / SentenceCount if SentenceCount > 0 else 0

def complex_word_count(text):
    tokens = tokenizer(text)
    complexWord = 0
    for word in tokens:
        vowels = 0
        if word.endswith(('es','ed')):
            pass
        else:
            for w in word:
                if w in 'aeiou':
                    vowels += 1
            if vowels > 2:
                complexWord += 1
    return complexWord

def percentage_complex_word(text):
    tokens = tokenizer(text)
    complexWord = 0
    for word in tokens:
        vowels = 0
        if word.endswith(('es','ed')):
            pass
        else:
            for w in word:
                if w in 'aeiou':
                    vowels += 1
            if vowels > 2:
                complexWord += 1
    return complexWord / len(tokens) if tokens else 0

def fog_index(averageSentenceLength, percentageComplexWord):
    return 0.4 * (averageSentenceLength + percentageComplexWord)

def average_words_per_sentence(text):
    words = tokenizer(text)
    sentences = sent_tokenize(text)
    return len(words) / len(sentences) if len(sentences) > 0 else 0

def syllable_count(text):
    tokens = tokenizer(text)
    total_syllables = 0
    vowels = "aeiou"
    for word in tokens:
        word_lower = word.lower()
        syllables = sum(1 for char in word_lower if char in vowels)
        if word_lower.endswith('es') or word_lower.endswith('ed'):
            if syllables > 1:
                syllables -= 1
        if syllables == 0:
            syllables = 1
        total_syllables += syllables
    return total_syllables

def count_personal_pronouns(text):
    pattern = r'\b(I|we|my|ours|us)\b'
    matches = re.findall(pattern, text, flags=re.IGNORECASE)
    return sum(1 for m in matches if m.lower() != 'us')

def average_word_length(text):
    words = tokenizer(text)
    return sum(len(word) for word in words) / len(words) if words else 0

# 8. Scrape articles
corpus = []
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
for url in urls:
    try:
        page = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(page.text, 'html.parser')
        content_tag = soup.find(attrs={'class': 'td-post-content'})
        text = content_tag.get_text() if content_tag else ""
        # Clean text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        corpus.append(text)
    except Exception as e:
        corpus.append("")
        print(f"Error scraping {url}: {e}")

# 9. Build DataFrame
df = pd.DataFrame({'title': urlsTitleDF, 'corpus': corpus})
df['URL'] = urls

# 10. Apply metrics
df["positive_score"] = df["corpus"].apply(positive_score)
df["negative_score"] = df["corpus"].apply(negative_score)
df["polarity_score"] = np.vectorize(polarity_score)(df['positive_score'], df['negative_score'])
df["total_word_count"] = df["corpus"].apply(total_word_count)
df["subjectivity_score"] = np.vectorize(subjectivity_score)(df['positive_score'], df['negative_score'], df['total_word_count'])
df["AverageSentenceLength"] = df["corpus"].apply(AverageSentenceLength)
df["percentage_complex_word"] = df["corpus"].apply(percentage_complex_word)
df["fog_index"] = np.vectorize(fog_index)(df["AverageSentenceLength"], df["percentage_complex_word"])
df["average_words_per_sentence"] = df["corpus"].apply(average_words_per_sentence)
df["complex_word_count"] = df["corpus"].apply(complex_word_count)
df["syllable_count"] = df["corpus"].apply(syllable_count)
df["personal_pronouns"] = df["corpus"].apply(count_personal_pronouns)
df["average_word_length"] = df["corpus"].apply(average_word_length)

# Insert total_word_count after complex_word_count
complex_word_count_index = df.columns.get_loc('complex_word_count')
total_word_counts = df["corpus"].apply(total_word_count)
df.insert(complex_word_count_index + 1, 'total_word_count', total_word_counts)

# Insert URL_ID if present
if 'URL_ID' in input_df.columns:
    df.insert(0, 'URL_ID', input_df['URL_ID'])

# Drop the 'title' and 'corpus' columns
df = df.drop(columns=['title', 'corpus'])

# 11. Save to Excel
output_file_path = "/content/drive/MyDrive/Assignment/output_analysis.xlsx"
df.to_excel(output_file_path, index=False)
print(f"Analysis saved to {output_file_path}")
