import streamlit as st
from dotenv import load_dotenv
from pydub import AudioSegment
import google.generativeai as genai
import json
import uuid
import io
import edge_tts
import asyncio
import aiofiles
import pypdf
import os
import time
from typing import List, Dict, Tuple

# Load environment variables from .env file
load_dotenv()

class PodcastGenerator:
    def __init__(self):
        pass

    async def generate_script(self, prompt: str, language: str, api_key: str) -> Dict:
        example = """
        {
        "topic": "AGI",
        "podcast": [
            {"speaker": 2, "line": "So, AGI, huh? Seems like everyone's talking about it these days."},
            {"speaker": 1, "line": "Yeah, it's definitely having a moment, isn't it?"},
            ...
        ]
        }
        """

        if language == "Auto Detect":
            language_instruction = "- The podcast MUST be in the same language as the user input."
        else:
            language_instruction = f"- The podcast MUST be in {language} language."

        system_prompt = f"""
        You are a professional podcast generator. Your task is to generate a professional podcast script based on the user input.
        {language_instruction}
        - The podcast should have 2 speakers.
        - The podcast should be long.
        - Do not use names for the speakers.
        - The podcast should be interesting, lively, and engaging, and hook the listener from the start.
        - Ignore formatting inconsistencies or irrelevant details in the input text.
        - The script must be in JSON format.
        Follow this example structure:
        {example}
        """

        user_prompt = f"Please generate a podcast script based on the following user input:\n{prompt}"

        messages = [{"role": "user", "content": user_prompt}]

        api_key = os.getenv("GENAI_API_KEY")
        if not api_key:
            raise ValueError("API key not found. Please add GENAI_API_KEY to your .env file.")

        genai.configure(api_key=api_key)

        generation_config = {
            "temperature": 1,
            "max_output_tokens": 8192,
        }

        try:
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash-002",
                generation_config=generation_config,
                safety_settings={
                    "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
                    "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
                    "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
                    "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
                },
                system_instruction=system_prompt
            )
            response = await model.chat_async(messages)
            return json.loads(response.text)
        except Exception as e:
            raise e

    async def tts_generate(self, text: str, speaker: int, speaker1: str, speaker2: str) -> str:
        voice = speaker1 if speaker == 1 else speaker2
        speech = edge_tts.Communicate(text, voice)

        temp_filename = f"temp_{uuid.uuid4()}.wav"
        try:
            await speech.save(temp_filename)
            return temp_filename
        except Exception as e:
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
            raise e

    async def combine_audio_files(self, audio_files: List[str]) -> str:
        combined_audio = AudioSegment.empty()
        for audio_file in audio_files:
            combined_audio += AudioSegment.from_file(audio_file)
            os.remove(audio_file)

        output_filename = f"output_{uuid.uuid4()}.wav"
        combined_audio.export(output_filename, format="wav")
        return output_filename

    async def generate_podcast(self, input_text: str, language: str, speaker1: str, speaker2: str, api_key: str) -> Tuple[str, str]:
        podcast_json = await self.generate_script(input_text, language, api_key)
        running_text = "\n".join([f"Speaker {item['speaker']}: {item['line']}" for item in podcast_json['podcast']])

        audio_files = await asyncio.gather(*[
            self.tts_generate(item['line'], item['speaker'], speaker1, speaker2) for item in podcast_json['podcast']
        ])
        combined_audio = await self.combine_audio_files(audio_files)
        return combined_audio, running_text

class TextExtractor:
    @staticmethod
    async def extract_from_pdf(file_path: str) -> str:
        async with aiofiles.open(file_path, mode='rb') as f:
            pdf_reader = pypdf.PdfReader(io.BytesIO(await f.read()))
            return "\n".join(page.extract_text() for page in pdf_reader.pages if page.extract_text())

    @staticmethod
    async def extract_from_txt(file_path: str) -> str:
        async with aiofiles.open(file_path, mode='r', encoding='utf-8') as f:
            return await f.read()

    @classmethod
    async def extract_text(cls, file_path: str) -> str:
        _, file_extension = os.path.splitext(file_path)
        if file_extension.lower() == '.pdf':
            return await cls.extract_from_pdf(file_path)
        elif file_extension.lower() == '.txt':
            return await cls.extract_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

def main():
    st.title("Lestari Bahasa Podcast Multi Bahasa")
    st.write("Talkshow Lestari Bahasa AI")

    input_text = st.text_area("Input Text")
    input_file = st.file_uploader("Or Upload a PDF or TXT file", type=["pdf", "txt"])

    language = st.selectbox("Language", [
        "Auto Detect",
        "Afrikaans", "Albanian", "Amharic", "Arabic", "Armenian", "Azerbaijani",
        "Bahasa Indonesian", "Bangla", "Basque", "Bengali", "Bosnian", "Bulgarian",
        "Burmese", "Catalan", "Chinese Cantonese", "Chinese Mandarin",
        "Chinese Taiwanese", "Croatian", "Czech", "Danish", "Dutch", "English",
        "Estonian", "Filipino", "Finnish", "French", "Galician", "Georgian",
        "German", "Greek", "Hebrew", "Hindi", "Hungarian", "Icelandic", "Irish",
        "Italian", "Japanese", "Javanese", "Kannada", "Kazakh", "Khmer", "Korean",
        "Lao", "Latvian", "Lithuanian", "Macedonian", "Malay", "Malayalam",
        "Maltese", "Mongolian", "Nepali", "Norwegian Bokmål", "Pashto", "Persian",
        "Polish", "Portuguese", "Romanian", "Russian", "Serbian", "Sinhala",
        "Slovak", "Slovene", "Somali", "Spanish", "Sundanese", "Swahili",
        "Swedish", "Tamil", "Telugu", "Thai", "Turkish", "Ukrainian", "Urdu",
        "Uzbek", "Vietnamese", "Welsh", "Zulu"
    ], index=0)


        speaker1 = st.selectbox("Speaker 1 Voice", [
        "Andrew - English (United States)",
        "Ava - English (United States)",
        "Brian - English (United States)",
        "Emma - English (United States)",
        "Florian - German (Germany)",
        "Seraphina - German (Germany)",
        "Remy - French (France)",
        "Vivienne - French (France)",
        "Ardi - Indonesian (Indonesia)",
        "Gadis - Indonesian (Indonesia)",
        "Tuti - Sundanese (Indonesia)",
        "Jajang - Sundanese (Indonesia)",
        "Siti - Javanese (Latin, Indonesia)",
        "Dimas - Javanese (Latin, Indonesia)"
    ])

    speaker2 = st.selectbox("Speaker 2 Voice", [
        "Andrew - English (United States)",
        "Ava - English (United States)",
        "Brian - English (United States)",
        "Emma - English (United States)",
        "Florian - German (Germany)",
        "Seraphina - German (Germany)",
        "Remy - French (France)",
        "Vivienne - French (France)",
        "Ardi - Indonesian (Indonesia)",
        "Gadis - Indonesian (Indonesia)",
        "Tuti - Sundanese (Indonesia)",
        "Jajang - Sundanese (Indonesia)",
        "Siti - Javanese (Latin, Indonesia)",
        "Dimas - Javanese (Latin, Indonesia)"
    ])
    
    async def process_input(input_text: str, input_file, language: str, speaker1: str, speaker2: str, api_key: str = "") -> Tuple[str, str]:
    st.info("Starting podcast generation...")
    start_time = time.time()

    # Voice mapping
    voice_names = {
        "Andrew - English (United States)": "en-US-AndrewMultilingualNeural",
        "Ava - English (United States)": "en-US-AvaMultilingualNeural",
        "Brian - English (United States)": "en-US-BrianMultilingualNeural",
        "Emma - English (United States)": "en-US-EmmaMultilingualNeural",
        "Florian - German (Germany)": "de-DE-FlorianMultilingualNeural",
        "Seraphina - German (Germany)": "de-DE-SeraphinaMultilingualNeural",
        "Remy - French (France)": "fr-FR-RemyMultilingualNeural",
        "Vivienne - French (France)": "fr-FR-VivienneMultilingualNeural",
        "Ardi - Indonesian (Indonesia)": "id-ID-ArdiNeural",
        "Gadis - Indonesian (Indonesia)": "id-ID-GadisNeural",
        "Tuti - Sundanese (Indonesia)": "su-ID-TutiNeural",
        "Jajang - Sundanese (Indonesia)": "su-ID-JajangNeural",
        "Siti - Javanese (Latin, Indonesia)": "jv-ID-SitiNeural",
        "Dimas - Javanese (Latin, Indonesia)": "jv-ID-DimasNeural"
    }

    speaker1 = voice_names.get(speaker1, "en-US-AndrewMultilingualNeural")
    speaker2 = voice_names.get(speaker2, "en-US-AvaMultilingualNeural")

    # Extract text from uploaded file if provided
    if input_file:
        input_text = await TextExtractor.extract_text(input_file.name)

    # Check API key
    if not api_key:
        api_key = os.getenv("GENAI_API_KEY")
        if not api_key:
            st.error("API key not found. Please set GENAI_API_KEY in your environment.")
            return None, None

    # Generate podcast
    podcast_generator = PodcastGenerator()
    try:
        combined_audio, running_text = await podcast_generator.generate_podcast(input_text, language, speaker1, speaker2, api_key)
    except Exception as e:
        st.error(f"Error during podcast generation: {e}")
        return None, None

    end_time = time.time()
    st.success(f"Successfully generated podcast in {(end_time - start_time):.2f} seconds!")

    return combined_audio, running_text




    
    if st.button("Generate Podcast"):
        if input_file:
            file_path = input_file.name
            with open(file_path, "wb") as f:
                f.write(input_file.read())
            input_text = asyncio.run(TextExtractor.extract_text(file_path))

        if not input_text:
            st.error("Please provide input text or upload a file.")
            return

        api_key = os.getenv("GENAI_API_KEY")
        podcast_generator = PodcastGenerator()

        combined_audio, running_text = asyncio.run(
            podcast_generator.generate_podcast(input_text, language, speaker1, speaker2, api_key)
        )

        st.audio(combined_audio, format="audio/wav")
        st.text_area("Running Text", running_text, height=300)

if __name__ == "__main__":
    main()
