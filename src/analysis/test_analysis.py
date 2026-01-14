import os
import sys
import re
from pathlib import Path
import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
nltk.download('punkt_tab')


try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("Downloading NLTK punkt tokenizer...")
    nltk.download('punkt', quiet=True)


class TextAnalyzer:
    """Text analyzer class for calculating sentiment and readability metrics."""
    
    def __init__(self, stopwords_folder='resources/StopWords', 
                 master_dict_folder='resources/MasterDictionary'):
        """
        Initialize the text analyzer.
        
        Args:
            stopwords_folder: Path to StopWords folder
            master_dict_folder: Path to MasterDictionary folder
        """
        self.stopwords = self.load_stopwords(stopwords_folder)
        self.positive_words, self.negative_words = self.load_sentiment_words(master_dict_folder)
    
    def load_stopwords(self, folder_path):
        """
        Load all stopwords from multiple files in the StopWords folder.
        
        Returns: set of stopwords in lowercase
        """
        stopwords = set()
        
        if not os.path.exists(folder_path):
            print(f"Warning: {folder_path} not found. Using empty stopwords.")
            return stopwords
        
        # Read all text files in the folder
        for filename in os.listdir(folder_path):
            if filename.endswith('.txt'):
                filepath = os.path.join(folder_path, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        words = f.read().splitlines()
                        stopwords.update([word.strip().lower() for word in words if word.strip()])
                except Exception as e:
                    print(f"Error reading {filename}: {e}")
        
        print(f"Loaded {len(stopwords)} stopwords")
        return stopwords
    
    def load_sentiment_words(self, folder_path):
        """
        Load positive and negative words from MasterDictionary.
        
        Returns: tuple of (positive_words set, negative_words set)
        """
        positive_words = set()
        negative_words = set()
        
        if not os.path.exists(folder_path):
            print(f"Warning: {folder_path} not found. Using empty sentiment dictionaries.")
            return positive_words, negative_words
        
        # Load positive words
        pos_file = os.path.join(folder_path, 'positive-words.txt')
        if os.path.exists(pos_file):
            try:
                with open(pos_file, 'r', encoding='utf-8', errors='ignore') as f:
                    words = f.read().splitlines()
                    # Only add words NOT in stopwords
                    positive_words = set([word.strip().lower() for word in words 
                                        if word.strip() and word.strip().lower() not in self.stopwords])
                print(f"Loaded {len(positive_words)} positive words")
            except Exception as e:
                print(f"Error reading positive words: {e}")
        
        # Load negative words
        neg_file = os.path.join(folder_path, 'negative-words.txt')
        if os.path.exists(neg_file):
            try:
                with open(neg_file, 'r', encoding='utf-8', errors='ignore') as f:
                    words = f.read().splitlines()
                    # Only add words NOT in stopwords
                    negative_words = set([word.strip().lower() for word in words 
                                        if word.strip() and word.strip().lower() not in self.stopwords])
                print(f"Loaded {len(negative_words)} negative words")
            except Exception as e:
                print(f"Error reading negative words: {e}")
        
        return positive_words, negative_words
    
    def count_syllables(self, word):
        """
        Count syllables in a word.
        
        Rules:
        - Count vowel groups
        - Don't count 'es' or 'ed' at the end
        - Minimum 1 syllable per word
        """
        word = word.lower()
        vowels = "aeiouy"
        syllable_count = 0
        previous_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                syllable_count += 1
            previous_was_vowel = is_vowel
        
        # Handle exceptions
        if word.endswith(('es', 'ed')):
            syllable_count -= 1
        
        return max(syllable_count, 1)
    
    def count_personal_pronouns(self, text):
        """
        Count personal pronouns: I, we, my, ours, us (but not "US" as country).
        """
        # Pattern for personal pronouns
        pronoun_pattern = r'\b(I|we|my|ours|us)\b'
        pronouns = re.findall(pronoun_pattern, text, re.IGNORECASE)
        
        # Exclude "US" (country)
        us_country_pattern = r'\bUS\b'
        us_country_count = len(re.findall(us_country_pattern, text))
        
        total_count = len(pronouns) - us_country_count
        return max(0, total_count)
    
    def analyze_text(self, text):
        """
        Perform complete text analysis and calculate all 13 metrics.
        
        Args:
            text: The article text to analyze
        
        Returns:
            Dictionary containing all calculated metrics
        """
        # Tokenize
        sentences = sent_tokenize(text)
        words = word_tokenize(text)
        words = [word for word in words if word.isalpha()]
        words_lower = [word.lower() for word in words]
        
        # Clean words (remove stopwords)
        cleaned_words = [word for word in words_lower if word not in self.stopwords]
        
        # Safety checks for division
        num_sentences = max(len(sentences), 1)
        num_words = max(len(words), 1)
        num_cleaned_words = max(len(cleaned_words), 1)
        epsilon = 0.000001
        
        # Calculate sentiment scores
        positive_score = sum(1 for word in cleaned_words if word in self.positive_words)
        negative_score = sum(1 for word in cleaned_words if word in self.negative_words)
        
        polarity_score = (positive_score - negative_score) / (
            (positive_score + negative_score) + epsilon
        )
        
        subjectivity_score = (positive_score + negative_score) / (
            num_cleaned_words + epsilon
        )
        
        # Calculate readability metrics
        avg_sentence_length = num_words / num_sentences
        
        complex_words = [word for word in words if self.count_syllables(word) > 2]
        complex_word_count = len(complex_words)
        
        percentage_complex_words = complex_word_count / num_words
        
        fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)
        
        # Word statistics
        word_count = num_cleaned_words
        
        total_syllables = sum(self.count_syllables(word) for word in words)
        syllable_per_word = total_syllables / num_words
        
        personal_pronouns = self.count_personal_pronouns(text)
        
        total_characters = sum(len(word) for word in words)
        avg_word_length = total_characters / num_words
        
        return {
            'POSITIVE SCORE': positive_score,
            'NEGATIVE SCORE': negative_score,
            'POLARITY SCORE': polarity_score,
            'SUBJECTIVITY SCORE': subjectivity_score,
            'AVG SENTENCE LENGTH': avg_sentence_length,
            'PERCENTAGE OF COMPLEX WORDS': percentage_complex_words,
            'FOG INDEX': fog_index,
            'AVG NUMBER OF WORDS PER SENTENCE': avg_sentence_length,
            'COMPLEX WORD COUNT': complex_word_count,
            'WORD COUNT': word_count,
            'SYLLABLE PER WORD': syllable_per_word,
            'PERSONAL PRONOUNS': personal_pronouns,
            'AVG WORD LENGTH': avg_word_length
        }
    
    def analyze_file(self, filepath):
        """
        Analyze a text file.
        
        Args:
            filepath: Path to the text file
        
        Returns:
            Dictionary of calculated metrics
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
            
            return self.analyze_text(text)
            
        except Exception as e:
            print(f"Error analyzing file {filepath}: {e}")
            return self._get_zero_metrics()
    
    def _get_zero_metrics(self):
        """Return a dictionary with all metrics set to zero."""
        return {
            'POSITIVE SCORE': 0,
            'NEGATIVE SCORE': 0,
            'POLARITY SCORE': 0,
            'SUBJECTIVITY SCORE': 0,
            'AVG SENTENCE LENGTH': 0,
            'PERCENTAGE OF COMPLEX WORDS': 0,
            'FOG INDEX': 0,
            'AVG NUMBER OF WORDS PER SENTENCE': 0,
            'COMPLEX WORD COUNT': 0,
            'WORD COUNT': 0,
            'SYLLABLE PER WORD': 0,
            'PERSONAL PRONOUNS': 0,
            'AVG WORD LENGTH': 0
        }


def main():
    """Main function to analyze all articles."""
    
    print("=" * 70)
    print("BLACKCOFFER TEXT ANALYSIS")
    print("=" * 70)
    print()
    
    # Initialize analyzer
    print("Loading stopwords and sentiment dictionaries...\n")
    analyzer = TextAnalyzer(
        stopwords_folder='resources/StopWords',
        master_dict_folder='resources/MasterDictionary'
    )
    
    # Load input data
    input_file = 'data/input/Input.xlsx'
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found!")
        print("Make sure Input.xlsx is in the data/input/ folder.")
        return
    
    print(f"Loading input from {input_file}...\n")
    input_df = pd.read_excel(input_file)
    
    print(f"Analyzing {len(input_df)} articles...\n")
    
    # Process each article
    results = []
    success_count = 0
    extracted_articles_dir = 'extracted_articles'
    
    for index, row in input_df.iterrows():
        url_id = row['URL_ID']
        url = row['URL']
        
        print(f"[{index + 1}/{len(input_df)}] Analyzing {url_id}...", end=' ')
        
        # Path to article file
        article_file = os.path.join(extracted_articles_dir, f"{url_id}.txt")
        
        if not os.path.exists(article_file):
            print("✗ (file not found)")
            metrics = analyzer._get_zero_metrics()
        else:
            try:
                metrics = analyzer.analyze_file(article_file)
                print("✓")
                success_count += 1
            except Exception as e:
                print(f"✗ (error: {e})")
                metrics = analyzer._get_zero_metrics()
        
        # Combine input data with metrics
        result = {
            'URL_ID': url_id,
            'URL': url,
            **metrics
        }
        results.append(result)
    
    # Create output DataFrame
    output_df = pd.DataFrame(results)
    
    # Save to Excel
    output_file = 'data/output/Output_Data_Structure.xlsx'
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    try:
        output_df.to_excel(output_file, index=False)
        
        print("\n" + "=" * 70)
        print("ANALYSIS COMPLETE")
        print("=" * 70)
        print(f"Total articles:    {len(input_df)}")
        print(f"✓ Analyzed:        {success_count}")
        print(f"✗ Not found:       {len(input_df) - success_count}")
        print(f"\n Results saved to: {output_file}")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n Error saving output file: {e}")


if __name__ == "__main__":
    main()
    #