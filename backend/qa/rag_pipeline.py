from groq import Groq


class VideoQA:

    def __init__(self, api_key):

        if not api_key:
            raise ValueError("GROQ_API_KEY is missing. Set it in backend/.env")

        self.client = Groq(
            api_key=api_key
        )

    def answer_question(
        self,
        question,
        retrieved_context
    ):

        audio_context = "\n".join(
            [
                f"[{item['start']:.0f}s - {item['end']:.0f}s] {item['text']}"
                for item in retrieved_context["audio"]
            ]
        )

        visual_context = "\n".join(
            [
                f"{item.get('timestamp', 'N/A')} : {item['caption']}"
                for item in retrieved_context["visual"]
            ]
        )

        prompt = f"""
You are a multimodal video QA assistant.

The context contains timestamps.
When answering:
- Mention relevant timestamps.
- Quote timestamps when possible.
- If asked for important moments, return timestamps.

Transcript Context:
{audio_context}

Visual Context:
{visual_context}

Question:
{question}

Answer using BOTH transcript and visual evidence.
"""

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        return response.choices[0].message.content
