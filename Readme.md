This project performs a text analysis on a collection of articles to extract various linguistic metrics. The analysis involves fetching article content from specified URLs, cleaning the text, and then applying several natural language processing techniques to calculate metrics such as sentiment scores, readability indices, and word counts. The results are compiled into a structured format and saved to an Excel file.

**Key Steps and Components:**

1.  **Google Drive Integration:** The notebook starts by mounting Google Drive to access necessary input files and save the output.
2.  **File Unzipping and Loading:** It unzips compressed files containing stop words and master dictionaries (positive/negative words) and loads these word lists into Python for later use.
3.  **Input Data Loading:** An Excel file (`Input.xlsx`) is read into a pandas DataFrame. This file is expected to contain a list of article URLs and potentially URL IDs.
4.  **Article Fetching and Cleaning:**
    *   The code iterates through the URLs provided in the input DataFrame.
    *   For each URL, it uses the `requests` library to fetch the web page content.
    *   `BeautifulSoup` is used to parse the HTML and extract the article title and the main article text content.
    *   The extracted text undergoes basic cleaning to remove leading/trailing spaces and handle line breaks.
    *   The titles and cleaned article texts are stored.
5.  **Text Preprocessing (Tokenization and Stop Word Removal):**
    *   A `tokenizer` function is defined to break down the text into individual words (tokens) using a regular expression to remove punctuation.
    *   This tokenizer also filters out common words (stop words) based on the loaded stop word list.
6.  **Metric Calculation Functions:** Several Python functions are defined to calculate various linguistic metrics:
    *   `positive_score`: Counts the number of positive words in the text based on the positive words dictionary.
    *   `negative_score`: Counts the number of negative words.
    *   `polarity_score`: Calculates the sentiment polarity based on positive and negative scores.
    *   `total_word_count`: Counts the total number of words after tokenization and stop word removal.
    *   `subjectivity_score`: Measures the subjectivity of the text based on positive, negative, and total word counts.
    *   `AverageSentenceLength`: Calculates the average number of words per sentence.
    *   `complex_word_count`: Estimates the number of complex words (words with more than 2 vowels, excluding those ending in 'es' or 'ed').
    *   `percentage_complex_word`: Calculates the percentage of complex words in the text.
    *   `fog_index`: Computes the Fog Index, a readability score, based on average sentence length and percentage of complex words.
    *   `average_words_per_sentence`: Calculates the average number of words per sentence (redefined, potentially redundant with `AverageSentenceLength`).
    *   `syllable_count`: Estimates the total number of syllables in the text based on vowel counts.
    *   `count_personal_pronouns`: Counts the occurrences of specific personal pronouns (I, we, my, ours, us), with a check to exclude 'US' as a country code.
    *   `average_word_length`: Calculates the average number of characters per word.
7.  **Applying Metrics to Articles:**
    *   The fetched article content is organized into a pandas DataFrame along with their titles and URLs.
    *   Each of the defined metric calculation functions is applied to the article text column of the DataFrame to compute the respective scores for each article. These scores are added as new columns to the DataFrame.
8.  **DataFrame Restructuring:** The DataFrame is adjusted to include the 'URL\_ID' from the input file if it exists, and the original 'title' and 'corps' (article text) columns are removed to keep only the calculated metrics.
9.  **Output Saving:** The final DataFrame containing the calculated metrics is saved as an Excel file named `output_analysis.xlsx` in the designated Google Drive folder.






How to run task.py ---

1.Upload all files to your Google Drive at the specified locations.

2.Open Colab, copy-paste the code above into a cell.

3.Run the cell.

The output Excel file will be saved at /content/drive/MyDrive/Assignment/output_analysis.xlsx.


