import os
import base64
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

class GroqService:
    @staticmethod
    def get_mixtral_recommendation(prompt: str):
        # Using Llama 3.3 as requested by user
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are Clinivanta AI, an institutional-grade AI Clinical Intelligence Engine specializing in wound assessment. Analyze inputs like a senior surgeon. Provide definitive diagnosis, tissue breakdown (granulation/slough/necrosis), exudate levels, and clinical staging (Wagner/NPUAP). Always use ### SECTION: header format in structured reports."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content

    @staticmethod
    def get_whisper_transcription(audio_file_path: str):
        with open(audio_file_path, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(audio_file_path, file.read()),
                model="whisper-large-v3-turbo",
                response_format="verbose_json",
            )
        return transcription.text

    @staticmethod
    def get_llama_vision_analysis(image_path: str):
        """
        Performs high-fidelity vision analysis using Llama's latest vision models.
        Acts as a surgical MD to provide tissue analysis even if YOLO fails.
        """
        def encode_image(img_path):
            with open(img_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')

        base64_image = encode_image(image_path)

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": """
                            As a Senior Surgeon/MD, perform a high-fidelity analysis of this wound image. 
                            Provide a detailed clinical assessment including:
                            - Primary Tissue Types: Identify Granulation, Slough, and Necrotic tissue with estimated percentages.
                            - Exudate Level: Analyze for None/Low/Moderate/Heavy discharge.
                            - Peripheral Condition: Check for periwound maceration, erythema, or edema.
                            - Clinical Staging: Categorize based on Wagner Grade (for diabetic ulcers) or NPUAP Stage.
                            
                            Your analysis will be used to generate a structured clinical report. Provide output in clear, medical English.
                            """},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
            # Using the requested Llama 4 Scout or latest vision equivalent
            model="meta-llama/llama-4-scout-17b-16e-instruct", # Fallback to 90b if scout is not in local groq registry yet
        )
        return chat_completion.choices[0].message.content
