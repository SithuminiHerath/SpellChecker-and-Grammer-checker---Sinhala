# src/model/rule_based_checker.py
import re
from typing import Dict, List, Any

class RuleBasedChecker:
    def __init__(self, dictionary_path: str):
        """
        Initialize the rule-based grammar checker with dictionary and rules.
        
        Args:
            dictionary_path (str): Path to the Sinhala dictionary file
        """
        self.dictionary = self._load_dictionary(dictionary_path)
        self.grammar_rules = [
            {
                'pattern': r'([අආඇඈඉඊඋඌඍඎඏඐඑඒඓඔඕඖ])\1+',
                'description': 'Repeated vowels detected',
                'suggestion': 'Remove repeated vowels'
            },
            {
                'pattern': r'\s+([.!?])',
                'description': 'Extra space before punctuation',
                'suggestion': 'Remove space before punctuation mark'
            },
            {
                'pattern': r'([.!?])([^"\s])',
                'description': 'Missing space after sentence end',
                'suggestion': 'Add space after sentence-ending punctuation'
            }
        ]

        # Add new grammar rules for start-to-end mappings
        self.start_end_rules = {
            'මම': ['මි'],
            'අපි': ['මු'],
            'ඔහු': ['ෙය', 'හ'],
            'ඇය': ['ාය', 'ීය']
        }
        
        self.word_endings = {
            'යි': 'ය',
            'න්': 'නය',
            'ට': 'ටය'
        }

    def _load_dictionary(self, path: str) -> set:
        """Load Sinhala dictionary from file."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return set(word.strip() for word in f.readlines())
        except FileNotFoundError:
            print(f"Warning: Dictionary file not found at {path}")
            return set()

    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences using Sinhala-aware sentence boundaries."""
        sentences = re.split(r'([.!?])\s+', text)
        return [''.join(i) for i in zip(sentences[::2], sentences[1::2] + [''])]

    def _check_spelling(self, sentence: str) -> List[Dict[str, Any]]:
        """Check spelling of words in a sentence."""
        words = re.findall(r'\b\w+\b', sentence)
        errors = []

        for word in words:
            if word not in self.dictionary:
                found_match = False
                suggestions = []

                for ending, replacement in self.word_endings.items():
                    if word.endswith(ending):
                        base_word = word[:-len(ending)] + replacement
                        if base_word in self.dictionary:
                            suggestions.append(base_word)
                            found_match = True

                if not found_match:
                    suggestions = [w for w in self.dictionary 
                                 if self._levenshtein_distance(word, w) == 1][:3]

                if not found_match or suggestions:
                    errors.append({
                        'word': word,
                        'suggestions': suggestions
                    })

        return errors

    def _check_grammar(self, sentence: str) -> List[Dict[str, Any]]:
        """Check grammar rules in a sentence."""
        errors = []

        for rule in self.grammar_rules:
            matches = re.finditer(rule['pattern'], sentence)
            for match in matches:
                errors.append({
                    'match': match.group(),
                    'position': match.span(),
                    'description': rule['description'],
                    'suggestion': rule['suggestion']
                })

        # Apply start-to-end rules
        words = sentence.split()
        if words:
            start_word = words[0]
            end_word = words[-1]

            if start_word in self.start_end_rules:
                valid_endings = self.start_end_rules[start_word]
                if not any(end_word.endswith(ending) for ending in valid_endings):
                    errors.append({
                        'description': f"Sentence start '{start_word}' should end with one of {valid_endings}",
                        'suggestion': f"Ensure the sentence ends with one of {valid_endings}",
                        'sentence_start': start_word,
                        'sentence_end': end_word
                    })

        return errors

    def _levenshtein_distance(self, s1: str, s2: str) -> int:
        """Calculate the Levenshtein distance between two strings."""
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    def check_grammar(self, text: str) -> Dict[str, Any]:
        """
        Main method to check grammar and spelling in Sinhala text.
        
        Args:
            text (str): Input Sinhala text to check
            
        Returns:
            Dict containing grammar errors, spelling errors, and correct sentences
        """
        sentences = self._split_sentences(text)
        results = {
            'grammar_errors': [],
            'spelling_errors': [],
            'correct_sentences': []
        }

        for sentence in sentences:
            grammar_errors = self._check_grammar(sentence)
            spelling_errors = self._check_spelling(sentence)

            if grammar_errors:
                results['grammar_errors'].append({
                    'sentence': sentence,
                    'errors': grammar_errors
                })

            if spelling_errors:
                results['spelling_errors'].append({
                    'sentence': sentence,
                    'errors': spelling_errors
                })

            if not grammar_errors and not spelling_errors:
                results['correct_sentences'].append(sentence)

        return results
