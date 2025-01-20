#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from textblob import TextBlob
import nltk
import syllapy

# Initialize necessary NLP tools
nltk.download('punkt')

# Define the analysis function
def analyze_text(text):
    # Initialize analysis results
    analysis_results = {}

    # 1. Positive Score & 2. Negative Score
    blob = TextBlob(text)
    analysis_results['POSITIVE SCORE'] = sum(1 for word in blob.sentiment if word > 0)  # Adjust to count positive words
    analysis_results['NEGATIVE SCORE'] = sum(1 for word in blob.sentiment if word < 0)  # Adjust for negative words
    
    # 3. Polarity Score & 4. Subjectivity Score
    analysis_results['POLARITY SCORE'] = blob.sentiment.polarity
    analysis_results['SUBJECTIVITY SCORE'] = blob.sentiment.subjectivity

    # 5. Avg Sentence Length
    sentences = nltk.sent_tokenize(text)
    analysis_results['AVG SENTENCE LENGTH'] = sum(len(nltk.word_tokenize(s)) for s in sentences) / len(sentences)

    # 6. Percentage of Complex Words (words with 3 or more syllables)
    words = nltk.word_tokenize(text)
    complex_words = [word for word in words if syllapy.count(word) >= 3]
    analysis_results['PERCENTAGE OF COMPLEX WORDS'] = len(complex_words) / len(words) * 100

    # 7. FOG Index
    analysis_results['FOG INDEX'] = analysis_results['AVG SENTENCE LENGTH'] * (100 * analysis_results['PERCENTAGE OF COMPLEX WORDS'] / len(words))

    # 8. Avg Number of Words per Sentence (already calculated as Avg Sentence Length)
    analysis_results['AVG NUMBER OF WORDS PER SENTENCE'] = analysis_results['AVG SENTENCE LENGTH']

    # 9. Complex Word Count
    analysis_results['COMPLEX WORD COUNT'] = len(complex_words)

    # 10. Word Count
    analysis_results['WORD COUNT'] = len(words)

    # 11. Syllables per Word
    syllables_per_word = sum(syllapy.count(word) for word in words) / len(words)
    analysis_results['SYLLABLE PER WORD'] = syllables_per_word

    # 12. Personal Pronouns (heuristic: 'I', 'you', 'he', 'she', etc.)
    personal_pronouns = ['I', 'you', 'he', 'she', 'it', 'we', 'they']
    analysis_results['PERSONAL PRONOUNS'] = sum(1 for word in words if word.lower() in personal_pronouns)

    # 13. Avg Word Length
    analysis_results['AVG WORD LENGTH'] = sum(len(word) for word in words) / len(words)

    return analysis_results

# Load your dataset (replace 'your_data.csv' with the actual file name)
df = pd.read_csv('final_output.csv')

# Apply the analysis function to the 'Content' column
results = df['Content'].apply(analyze_text)

# Convert results to DataFrame
results_df = pd.DataFrame(results.tolist())

# Reorder the columns as specified in your request
ordered_columns = [
    'URL_ID', 'URL', 'Title', 'Content',  # Original input columns
    'POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE', 'SUBJECTIVITY SCORE',
    'AVG SENTENCE LENGTH', 'PERCENTAGE OF COMPLEX WORDS', 'FOG INDEX',
    'AVG NUMBER OF WORDS PER SENTENCE', 'COMPLEX WORD COUNT', 'WORD COUNT',
    'SYLLABLE PER WORD', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH'
]

# Concatenate the original data with the computed results
final_output_df = pd.concat([df[['URL_ID', 'URL', 'Title', 'Content']], results_df], axis=1)

# Reorder columns to match the output structure
final_output_df = final_output_df[ordered_columns]

# Save to Excel format
final_output_df.to_excel("Output Data Structure.xlsx", index=False)

# Save to CSV format
final_output_df.to_csv("Output Data Structure.csv", index=False)

print("Analysis completed and saved to Output Data Structure.xlsx and Output Data Structure.csv")


# In[ ]:




