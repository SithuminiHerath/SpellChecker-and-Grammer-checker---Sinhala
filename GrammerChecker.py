def correct_sentence_with_rules(sentence):
    """
    Corrects Sinhala grammar errors in a given sentence based on subject-specific rules.
    """
    # Split the sentence into words
    words = sentence.split()

    if not words:
        return sentence  # Return as is if the sentence is empty

    # Identify the subject (first word)
    subject = words[0]

    # Define corrections based on the subject
    if subject == "මම":
        corrections = {
            "ගියෙමු": "ගියෙමි",
            "කලෙමු": "කලෙමි",
            "යමු": "යමි",
        }
    elif subject == "අපි":
        corrections = {
            "ගියෙමි": "ගියෙමු",
            "සෙල්ලම් කලෝය": "සෙල්ලම් කලෙමු",
        }
    elif subject in ["අක්කා", "අම්මා"]:
        corrections = {
            "ගියෙමි": "ගියාය",
            "ගියහ": "ගියාය",
            "කීවේය": "කීවාය",
        }
    elif subject in ["අයියා", "මල්ලී"]:
        corrections = {
            "ගියාය": "ගියේය",
            "ගියෙමි": "ගියේය",
            "ගියෙමු": "ගියේය",
            "කලාය": "කලේය",
            "කලෙමි": "කලේය",
            "කීවාය": "කීවේය",
        }
    else:
        corrections = {}  # Default, no corrections

    # Check for the correction in the sentence
    corrected_sentence = sentence
    for incorrect, correct in corrections.items():
        if incorrect in sentence:
            corrected_sentence = sentence.replace(incorrect, correct)
            break

    return corrected_sentence


# Example Sentences
sentences = [
    "මම කඩේ ගියෙමි ",       # Correct
    "අපි සෙල්ලම් කලෝය",     # Incorrect
    "අක්කා සිංදු කීවේය",    # Incorrect
    "අයියා පාසල් ගියෙමි",   # Incorrect
    "අම්මා උදෑසනම රැකියාවට ගියහ",  # Incorrect
]

# Applying corrections
for sentence in sentences:
    corrected = correct_sentence_with_rules(sentence)
    print(f"Given Sentence: {sentence}")
    print(f"Correct: {corrected}\n")
