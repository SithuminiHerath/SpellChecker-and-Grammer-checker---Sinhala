# src/model/grammar_checker.py
import re
import logging
import Levenshtein  # Ensure you have installed python-Levenshtein

# Configure logging
logging.basicConfig(
    filename='sinhala_scribe.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class GrammarChecker:
    def __init__(self, dictionary_path, bert_model=None):
        self.dictionary = self.load_dictionary(dictionary_path)
        self.bert_model = bert_model

    def load_dictionary(self, path):
        """Load Sinhala dictionary from file into a set for O(1) lookups."""
        try:
            with open(path, 'r', encoding='utf-8') as file:
                dictionary = set(word.strip() for word in file.readlines())
            logging.info(f"Dictionary loaded successfully from {path}. Total words: {len(dictionary)}")
            return dictionary
        except Exception as e:
            logging.error(f"Error loading dictionary from {path}: {e}")
            return set()

    def check_grammar(self, text):
        """Check grammar rules and spelling in the text."""
        sentences = [s.strip() for s in re.split(r'[।.!?]', text) if s.strip()]
        grammar_errors = []
        correct_sentences = []
        spelling_errors = []

        for sentence in sentences:
            words = sentence.split()
            if not words:
                continue

            # Spell Checking
            misspelled = self.get_misspelled_words(words)
            if misspelled:
                spelling_errors.append({
                    'sentence': sentence,
                    'misspelled': misspelled,
                    'suggestions': self.get_spelling_suggestions(misspelled)
                })
                logging.info(f"Spelling errors found in sentence: '{sentence}' - Misspelled words: {misspelled}")
                # Skip grammar checking if spelling errors exist
                continue

            # Grammar Checking
            grammar_issues = self.check_grammar_rules(words)
            if grammar_issues:
                grammar_errors.extend(grammar_issues)
                logging.info(f"Grammar errors found in sentence: '{sentence}' - Issues: {grammar_issues}")
            else:
                correct_sentences.append(sentence)
                logging.info(f"Sentence is correct: '{sentence}'")

        return {
            'grammar_errors': grammar_errors,
            'correct_sentences': correct_sentences,
            'spelling_errors': spelling_errors
        }

    def get_misspelled_words(self, words):
        """Identify misspelled words."""
        return [word for word in words if word not in self.dictionary]

    def get_spelling_suggestions(self, misspelled_words):
        """Enhanced spelling suggestions using multiple techniques."""
        suggestions = {}
        for word in misspelled_words:
            # Combine multiple suggestion methods
            closest_matches = set()
            
            # 1. Levenshtein distance for basic similarity
            levenshtein_matches = self.find_closest_words(word, max_distance=2, max_suggestions=5)
            closest_matches.update(levenshtein_matches)
            
            # 2. Character n-gram similarity
            ngram_matches = self.find_ngram_matches(word, n=3, max_suggestions=3)
            closest_matches.update(ngram_matches)
            
            # 3. Common Sinhala typing error patterns
            pattern_matches = self.check_common_patterns(word)
            closest_matches.update(pattern_matches)
            
            # Combine and rank suggestions
            ranked_suggestions = self.rank_suggestions(word, list(closest_matches))
            suggestions[word] = ranked_suggestions[:5]  # Keep top 5 suggestions
            
        return suggestions

    def find_closest_words(self, word, max_distance=2, max_suggestions=5):
        """Find closest words in the dictionary based on Levenshtein distance."""
        closest = []
        for dict_word in self.dictionary:
            distance = Levenshtein.distance(word, dict_word)
            if distance <= max_distance:
                closest.append((dict_word, distance))
        # Sort by distance and return the closest matches
        closest_sorted = sorted(closest, key=lambda x: x[1])
        return [word for word, dist in closest_sorted[:max_suggestions]]

    def find_ngram_matches(self, word, n=3, max_suggestions=3):
        """Find matches based on character n-grams."""
        def get_ngrams(text, n):
            return set(text[i:i+n] for i in range(len(text)-n+1))
        
        word_ngrams = get_ngrams(word, n)
        matches = []
        
        for dict_word in self.dictionary:
            if abs(len(dict_word) - len(word)) <= 3:  # Length similarity threshold
                dict_ngrams = get_ngrams(dict_word, n)
                if not word_ngrams or not dict_ngrams:
                    continue
                similarity = len(word_ngrams & dict_ngrams) / len(word_ngrams | dict_ngrams)
                if similarity > 0.5:  # Similarity threshold
                    matches.append((dict_word, similarity))
        
        return [word for word, _ in sorted(matches, key=lambda x: x[1], reverse=True)[:max_suggestions]]

    def check_common_patterns(self, word):
        """Check for common Sinhala typing patterns and variants."""
        patterns = {
            'ං': 'ණ',  # Common confusion pairs
            'න': 'ණ',
            'ල': 'ළ',
            'ශ': 'ෂ',
            'ස': 'ශ',
            'බ': 'භ',
            'ද': 'ධ'
        }
        
        suggestions = set()
        for char in word:
            if char in patterns:
                variant = word.replace(char, patterns[char])
                if variant in self.dictionary:
                    suggestions.add(variant)
        
        return suggestions

    def rank_suggestions(self, original_word, suggestions):
        """Rank suggestions based on multiple factors."""
        ranked = []
        for suggestion in suggestions:
            score = 0
            # Length similarity
            length_diff = abs(len(suggestion) - len(original_word))
            score -= length_diff * 0.5
            
            # First character similarity
            if suggestion[0] == original_word[0]:
                score += 2
            
            # Common prefix length
            prefix_len = 0
            for c1, c2 in zip(original_word, suggestion):
                if c1 == c2:
                    prefix_len += 1
                else:
                    break
            score += prefix_len
            
            ranked.append((suggestion, score))
        
        return [word for word, _ in sorted(ranked, key=lambda x: x[1], reverse=True)]

    def check_grammar_rules(self, words):
        """Check grammar rules based on sentence structure."""
        errors = []
        first_word = words[0]
        last_word = words[-1]

        # Define grammar rules based on pronouns
        pronoun_rules = {
            "මම": {"ending": "මි", "description": "Should end with 'මි'"},
            "අපි": {"ending": "මු", "description": "Should end with 'මු'"},

            # Add more pronouns and their rules as needed
        }

        if first_word in pronoun_rules:
            expected_ending = pronoun_rules[first_word]["ending"]
            description = pronoun_rules[first_word]["description"]
            if not last_word.endswith(expected_ending):
                suggestion = self.generate_suggestion(words, expected_ending)
                errors.append({
                    'sentence': ' '.join(words),
                    'type': f"{first_word}_rule",
                    'description': description,
                    'suggestion': suggestion
                })
        else:
            # Handle sentences with other pronouns or structures if needed
            pass

        return errors

    def generate_suggestion(self, words, expected_ending):
        """Generate a suggestion by replacing the ending of the last word."""
        last_word = words[-1]
        # Remove common verb endings and append the expected ending
        verb_endings = ["නවා", "නේ", "නෝ"]
        for ending in verb_endings:
            if last_word.endswith(ending):
                base = last_word[:-len(ending)]
                return ' '.join(words[:-1] + [base + expected_ending])
        # If no common ending found, append the expected ending directly
        return ' '.join(words[:-1] + [last_word + expected_ending])

    def get_word_suggestions(self, current_input, is_space_pressed=False):
        """Get word suggestions based on input."""
        if is_space_pressed and self.bert_model:
            try:
                # Use BERT model for next word prediction
                text_with_mask = current_input + " " + self.bert_model.tokenizer.mask_token
                predictions = self.bert_model(text_with_mask)
                suggestions = [pred['token_str'].strip() for pred in predictions[:5]]
                # Clean suggestions by removing special tokens or incomplete words
                clean_suggestions = [s for s in suggestions if s and not s.startswith("[")]
                logging.info(f"BERT suggestions for input '{current_input}': {clean_suggestions}")
                return clean_suggestions
            except Exception as e:
                logging.error(f"Error in BERT prediction: {e}")
                return []
        else:
            # Use dictionary for word completion
            if not current_input:
                return []
            # Return up to 5 words that start with the current input
            suggestions = [word for word in self.dictionary if word.startswith(current_input)][:5]
            logging.info(f"Dictionary suggestions for input '{current_input}': {suggestions}")
            return suggestions