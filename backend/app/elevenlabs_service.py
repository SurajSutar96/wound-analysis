import os
from elevenlabs.client import ElevenLabs
from elevenlabs import save

class ElevenLabsService:
    def __init__(self, api_key="79d813caccb9f7d22be06c94ebc595e1515ae747c320bc6b5c28d64b17a6bc58"):
        self.client = ElevenLabs(api_key=api_key)
        # Choosing a professional medical-sounding voice (Adam)
        self.voice_id = "pNInz6obpgDQGcFmaJgB" 

    def generate_speech(self, text, output_path="static/audio/response.mp3"):
        """
        Generates speech from text and saves it as an MP3 file.
        """
        try:
            audio = self.client.text_to_speech.convert(
                text=text,
                voice_id=self.voice_id,
                model_id="eleven_multilingual_v2"
            )
            # convert returns a generator in v1.x, we need to join it or use a helper
            with open(output_path, "wb") as f:
                for chunk in audio:
                    f.write(chunk)
            return output_path
        except Exception as e:
            print(f"ElevenLabs Error: {e}")
            return None

# Singleton instance
eleven_service = ElevenLabsService()
