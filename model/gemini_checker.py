# gemini_checker.py
class GeminiChecker:
    def __init__(self, model):
        self.model = model

    def check_grammar(self, text: str) -> str:
        """Check grammar using Gemini AI"""
        prompt = f"""
        Please analyze the following Sinhala text for grammar and spelling errors:
        Text: {text}
        
        Please provide:
        1. Any grammar errors found
        2. Any spelling errors found
        3. Suggestions for improvement
        4. Corrected version

        Here are some sinhala grammer rules to help you:
        start->end
        මම -> මි
        අපි -> මු

        Please respond in Sinhala. As follow only,,
        1. ව්‍යාකරණ වැරදි:
        2. අක්ෂර වැරදි:
        3. නිවැරදි යෝජනා:
        4. නිවැරදි වාක්‍යය:
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error getting AI suggestions: {str(e)}"