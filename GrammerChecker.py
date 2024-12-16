import json

def load_corrections(corrections_file):
    """
    Load correction rules from a JSON file.
    """
    with open(corrections_file, 'r', encoding='utf-8') as file:
        corrections_data = json.load(file)
    return corrections_data


def correct_sentence_with_rules(sentence, corrections_data):
    """
    Corrects Sinhala grammar errors in a given sentence based on subject-specific rules.
    """
    # Split the sentence into words
    words = sentence.split()

    if not words:
        return sentence  # Return as is if the sentence is empty

    # Identify the subject (first word)
    subject = words[0]

    # Find the relevant correction rules for the subject
    corrections = {}
    for key, rules in corrections_data.items():
        if subject in key.split(","):  # Check if the subject matches any key
            corrections = rules
            break

    # Apply corrections if applicable
    corrected_sentence = sentence
    for incorrect, correct in corrections.items():
        if incorrect in sentence:
            corrected_sentence = sentence.replace(incorrect, correct)
            break

    return corrected_sentence


# Example Sentences
sentences = [
    "මම කඩේ ගියෙමු",
    "අපි සෙල්ලම් කලෝය",
    "අක්කා සිංදු කීවේය",
    "අයියා පාසල් ගියෙමි",
    "අක්කා පාසල් ගියෝය",
    "අම්මා උදෑසනම රැකියාවට ගියහ"
]

# Load correction rules from a JSON file
corrections_file = "corrections.json"  # Path to the JSON file with rules
corrections_data = load_corrections(corrections_file)

# Process sentences
for sentence in sentences:
    corrected = correct_sentence_with_rules(sentence, corrections_data)
    print(f"Original: {sentence}")
    print(f"Corrected: {corrected}\n")
