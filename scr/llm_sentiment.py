import openai
import os

class LLMSentiment:

    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def analyze_sentiment(self, news_titles: list):
        if not news_titles:
            return "Neutral"

        prompt = (
            "You are a financial sentiment analysis model. "
            "Analyze the overall market sentiment (Positive, Negative, Neutral) "
            "based on the following headlines:\n\n"
        )
        prompt += "\n".join(f"- {title}" for title in news_titles)
        prompt += "\n\nAnswer only with one of: Positive, Negative, or Neutral."

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a financial market sentiment classifier."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        sentiment = response.choices[0].message.content.strip()
        return sentiment
