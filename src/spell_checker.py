import re
from typing import List, Tuple
from nltk.metrics import edit_distance

class SinhalaSpellChecker:
    def __init__(self, dictionary_path: str):
        """
        Initialize the spell checker with a Sinhala dictionary
        
        :param dictionary_path: Path to the dictionary text file
        """
        self.dictionary = self._load_dictionary(dictionary_path)
    
    def _load_dictionary(self, path: str) -> set:
        """
        Load dictionary words from file
        
        :param path: Path to dictionary file
        :return: Set of dictionary words
        """
        with open(path, 'r', encoding='utf-8') as f:
            return set(word.strip() for word in f)
    
    def suggest_corrections(self, word: str, max_suggestions: int = 5) -> List[Tuple[str, float]]:
        """
        Generate spell correction suggestions
        
        :param word: Misspelled word
        :param max_suggestions: Maximum number of suggestions
        :return: List of (suggested word, similarity score) tuples
        """
        # If word is in dictionary, return it
        if word in self.dictionary:
            return [(word, 1.0)]
        
        # Calculate edit distances to find closest matches
        suggestions = []
        for dict_word in self.dictionary:
            # Calculate normalized edit distance
            dist = edit_distance(word, dict_word)
            similarity = 1 - (dist / max(len(word), len(dict_word)))
            
            # Only keep suggestions above a similarity threshold
            if similarity > 0.6:
                suggestions.append((dict_word, similarity))
        
        # Sort suggestions by similarity and return top max_suggestions
        return sorted(suggestions, key=lambda x: x[1], reverse=True)[:max_suggestions]
    
    def correct_text(self, text: str) -> str:
        """
        Correct spelling in the entire text
        
        :param text: Input text
        :return: Text with spelling corrections
        """
        # Split text into words
        words = re.findall(r'\S+', text)
        
        # Correct each word
        corrected_words = []   
        for word in words:
            # Check if word needs correction
            if word not in self.dictionary:
                suggestions = self.suggest_corrections(word)
                if suggestions:
                    # Replace with the best suggestion
                    corrected_words.append(suggestions[0][0])
                else:
                    corrected_words.append(word)
            else:
                corrected_words.append(word)
        
        # Reconstruct text
        return ' '.join(corrected_words)

# Path to your Sinhala dictionary file
dictionary_path = r"sinhala_dictionary.txt"

# Create an instance of the spell checker
spell_checker = SinhalaSpellChecker(dictionary_path)

# Test 1: Check if dictionary is loaded correctly
print("Loaded dictionary words: ", list(spell_checker.dictionary)[:10])  # Print first 10 words

# Test 2: Test spell correction for a single misspelled word
misspelled_word = "පසල"  # Example misspelled word
suggestions = spell_checker.suggest_corrections(misspelled_word)
print(f"Suggestions for '{misspelled_word}':", suggestions)

misspelled_word = "අක්ක"  # Example misspelled word
suggestions = spell_checker.suggest_corrections(misspelled_word)
print(f"Suggestions for '{misspelled_word}':", suggestions)

misspelled_word = "සෙලලම්"  # Example misspelled word
suggestions = spell_checker.suggest_corrections(misspelled_word)
print(f"Suggestions for '{misspelled_word}':", suggestions)

misspelled_word = "කීවය"  # Example misspelled word
suggestions = spell_checker.suggest_corrections(misspelled_word)
print(f"Suggestions for '{misspelled_word}':", suggestions)

misspelled_word = "අමමා"  # Example misspelled word
suggestions = spell_checker.suggest_corrections(misspelled_word)
print(f"Suggestions for '{misspelled_word}':", suggestions)

misspelled_word = "ගියෙම"  # Example misspelled word
suggestions = spell_checker.suggest_corrections(misspelled_word)
print(f"Suggestions for '{misspelled_word}':", suggestions)

# Test 3: Correct an entire sentence
sentence = "අක්ක පාසල් ගියේය."
corrected_sentence = spell_checker.correct_text(sentence)
print("Original sentence",sentence)
print("Corrected sentence:", corrected_sentence)

# Test 4: Correct an entire sentence
sentence = "අපි සෙලලම් කලෙමු."
corrected_sentence = spell_checker.correct_text(sentence)
print("Original sentence",sentence)
print("Corrected sentence:", corrected_sentence)

# Test 5: Correct an entire sentence
sentence = "අයයා සිංදු කීවාය."
corrected_sentence = spell_checker.correct_text(sentence)
print("Original sentence",sentence)
print("Corrected sentence:", corrected_sentence)

# Test 6: Correct an entire sentence
sentence = "අමමා උදෑසනම රැකියාවට ගියාය."
corrected_sentence = spell_checker.correct_text(sentence)
print("Original sentence",sentence)
print("Corrected sentence:", corrected_sentence)

# Test 7: Correct an entire sentence
sentence = "මම කඩේ ගියෙම."
corrected_sentence = spell_checker.correct_text(sentence)
print("Original sentence",sentence)
print("Corrected sentence:", corrected_sentence)
# Test 5: Test edge case: Empty string
empty_text = ""
corrected_empty_text = spell_checker.correct_text(empty_text)
print("Corrected empty text:", corrected_empty_text)
