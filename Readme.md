# Blackcoffer Text Analysis

## Project Overview

Extract textual data from 147 URLs and perform sentiment analysis and readability metrics calculation.

---

### **Part 1: Data Extraction**
- Extract article title and content from each URL
- Save each article as `URL_ID.txt`

### **Part 2: Text Analysis**
Calculate 13 variables for each article:
1. POSITIVE SCORE
2. NEGATIVE SCORE
3. POLARITY SCORE
4. SUBJECTIVITY SCORE
5. AVG SENTENCE LENGTH
6. PERCENTAGE OF COMPLEX WORDS
7. FOG INDEX
8. AVG NUMBER OF WORDS PER SENTENCE
9. COMPLEX WORD COUNT
10. WORD COUNT
11. SYLLABLE PER WORD
12. PERSONAL PRONOUNS
13. AVG WORD LENGTH

---

## Required Files/Folders

1. **StopWords/** - Folder containing stopword text files
2. **MasterDictionary/** - Folder containing:
   - `positive-words.txt`
   - `negative-words.txt`
3. **Input.xlsx** - List of URLs to scrape
4. **Output Data Structure.xlsx** - Template for output format

---

## Step-by-Step Instructions

### **Step 0: Setup Environment**

```bash
# Install required libraries
pip install pandas requests beautifulsoup4 openpyxl nltk

# Or create a requirements.txt file:
pip install -r requirements.txt
```

**requirements.txt:**
```
pandas
requests
beautifulsoup4
openpyxl
nltk
```

---

### **Step 1: Extract Articles (Web Scraping)**

Run the web scraper script:

```bash
python step1_web_scraper.py
```

**What it does:**
- Reads URLs from `Input.xlsx`
- Visits each URL
- Extracts article title and content
- Saves to `extracted_articles/URL_ID.txt`

**Expected output:**
- Folder `extracted_articles/` with 147 text files

**Time:** ~10-15 minutes (with delays to avoid overwhelming server)

---

### **Step 2: Perform Text Analysis**

Run the text analysis script:

```bash
python step2_text_analysis.py
```

**What it does:**
- Loads stopwords from `StopWords/` folder
- Loads positive/negative dictionaries from `MasterDictionary/`
- Reads each extracted text file
- Calculates all 13 metrics
- Saves results to `Output Data Structure.xlsx`

**Expected output:**
- Excel file with all URLs and calculated metrics

**Time:** ~2-5 minutes

---

## 📊 Understanding the Calculations

### **1. Sentiment Scores**

**POSITIVE SCORE:**
- Count how many words from the article appear in `positive-words.txt`
- Example: If "good", "excellent", "happy" appear → Score = 3

**NEGATIVE SCORE:**
- Count how many words appear in `negative-words.txt`
- Multiply by -1 and take absolute value
- Example: If "bad", "terrible" appear → Score = 2

**POLARITY SCORE:**
```
Formula: (Positive - Negative) / (Positive + Negative + 0.000001)
Range: -1 to +1
Interpretation:
  +1 = Very positive text
   0 = Neutral text
  -1 = Very negative text
```

**SUBJECTIVITY SCORE:**
```
Formula: (Positive + Negative) / (Total Cleaned Words + 0.000001)
Range: 0 to +1
Interpretation:
  0 = Objective (factual)
  1 = Subjective (opinionated)
```

---

### **2. Readability Metrics**

**AVG SENTENCE LENGTH:**
```
Formula: Total Words / Total Sentences
Example: 100 words in 5 sentences = 20 words/sentence
```

**COMPLEX WORD COUNT:**
- Words with more than 2 syllables
- Example: "beautiful" (3 syllables) = complex
- Example: "happy" (2 syllables) = not complex

**PERCENTAGE OF COMPLEX WORDS:**
```
Formula: Complex Words / Total Words
Example: 20 complex words out of 100 = 0.20 (20%)
```

**FOG INDEX (Gunning Fog Index):**
```
Formula: 0.4 * (Avg Sentence Length + Percentage of Complex Words)
Interpretation:
  8-10 = Easy to read
  11-15 = Moderate
  16+ = Difficult
```

---

### **3. Word Analysis**

**WORD COUNT:**
- Total words after removing stopwords and punctuation
- Example: "The quick brown fox" → Remove "the" → Count = 3

**SYLLABLE PER WORD:**
```
Formula: Total Syllables / Total Words
Example: "beautiful" (3) + "day" (1) = 4 syllables / 2 words = 2
```

**PERSONAL PRONOUNS:**
- Count: I, we, my, ours, us
- Exclude "US" when referring to country
- Example: "I think we should..." = 2 pronouns

**AVG WORD LENGTH:**
```
Formula: Total Characters / Total Words
Example: "cat" (3) + "dog" (3) = 6 chars / 2 words = 3
```

### **Web Scraper (step1_web_scraper.py)**
```

**Key concepts:**
- **Tokenization**: Splitting text into sentences/words
- **sent_tokenize()**: Splits text into sentences
- **word_tokenize()**: Splits text into words
- **List comprehension**: `[w for w in words if ...]` filters words

---

##  Troubleshooting

### **Problem: "No objects to concatenate"**
- **Cause**: All articles failed to extract
- **Solution**: Check your internet connection, verify URLs are accessible

### **Problem: "File not found: StopWords"**
- **Cause**: Missing StopWords folder
- **Solution**: Create folder and add stopword files (or use empty set)

### **Problem: Low scores for all articles**
- **Cause**: Sentiment dictionaries not loaded properly
- **Solution**: Verify `MasterDictionary/` folder exists with word files

### **Problem: Scraper gets blocked**
- **Cause**: Too many requests too fast
- **Solution**: Increase `time.sleep()` delay between requests

---

## Final Checklist

Before submission:

- [ ] All 147 articles extracted successfully
- [ ] `Output Data Structure.xlsx` created with all columns
- [ ] All 13 metrics calculated for each article
- [ ] No missing values (or reasonable defaults for failed extractions)
- [ ] File format matches the provided template exactly
- [ ] Code is well-commented and readable

---

##  Sample Output

Your `Output Data Structure.xlsx` should look like:

| URL_ID | URL | POSITIVE SCORE | NEGATIVE SCORE | POLARITY SCORE | ... |
|--------|-----|----------------|----------------|----------------|-----|
| Netclan20241017 | https://... | 45 | 12 | 0.58 | ... |
| Netclan20241018 | https://... | 38 | 15 | 0.43 | ... |

---

## Learning Outcomes

1. **Web Scraping**: How to extract data from websites
2. **Natural Language Processing**: Text analysis and sentiment analysis
3. **Data Processing**: Cleaning and transforming text data
4. **Metrics Calculation**: Statistical analysis of text
5. **Python Libraries**: pandas, BeautifulSoup, NLTK

---

## Additional Resources

- **BeautifulSoup Documentation**: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- **NLTK Documentation**: https://www.nltk.org/
- **Pandas Documentation**: https://pandas.pydata.org/docs/
- **Sentiment Analysis Guide**: https://monkeylearn.com/sentiment-analysis/
