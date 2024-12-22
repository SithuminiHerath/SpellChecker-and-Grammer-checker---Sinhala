import re
from typing import List, Dict, Tuple

class SinhalaGrammarChecker:
    def __init__(self):
        """
        Initialize grammar checking rules for Sinhala
        """
        self.rules = {
            'personal_pronoun_ending': {
                'මම': 'මි',
                'අපි': 'මු'
            }
        }
    
    def check_personal_pronoun_rules(self, sentences: List[str]) -> List[Dict]:
        """
        Check grammar rules for personal pronouns
        
        :param sentences: List of sentences to check
        :return: List of grammar error suggestions
        """
        grammar_errors = []
        
        for idx, sentence in enumerate(sentences):
            # Trim and split sentence
            sentence = sentence.strip()
            words = sentence.split()
            
            # Check for starting pronouns
            if not words:
                continue
            
            first_word = words[0]
            last_word = words[-1]
            
            # Check rules for 'මම'
            if first_word == 'මම' and not last_word.endswith('මි'):
                grammar_errors.append({
                    'sentence_idx': idx,
                    'error_type': 'Personal Pronoun Ending',
                    'current': sentence,
                    'suggestion': f'Sentences starting with "මම" should end with a word containing "මි"',
                    'severity': 'high'
                })
            
            # Check rules for 'අපි'
            if first_word == 'අපි' and not last_word.endswith('මු'):
                grammar_errors.append({
                    'sentence_idx': idx,
                    'error_type': 'Personal Pronoun Ending',
                    'current': sentence,
                    'suggestion': f'Sentences starting with "අපි" should end with a word containing "මු"',
                    'severity': 'high'
                })
        
        return grammar_errors
    
    def apply_suggestions(self, sentences: List[str]) -> Tuple[List[str], List[Dict]]:
        """
        Apply grammar suggestions to sentences
        
        :param sentences: List of input sentences
        :return: Tuple of (corrected sentences, error log)
        """
        # First, check for errors
        grammar_errors = self.check_personal_pronoun_rules(sentences)
        
        # Create a copy of sentences to modify
        corrected_sentences = sentences.copy()
        
        # Attempt to correct sentences
        for error in grammar_errors:
            sentence_idx = error['sentence_idx']
            original_sentence = corrected_sentences[sentence_idx]
            words = original_sentence.split()
            
            # Modify last word based on first word
            if words[0] == 'මම':
                # Ensure last word ends with 'මි'
                words[-1] = words[-1] + 'මි' if not words[-1].endswith('මි') else words[-1]
            
            if words[0] == 'අපි':
                # Ensure last word ends with 'මු'
                words[-1] = words[-1] + 'මු' if not words[-1].endswith('මු') else words[-1]
            
            corrected_sentences[sentence_idx] = ' '.join(words)
        
        return corrected_sentences, grammar_errors