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
        {
            "speaker": 2,
            "line": "So, AGI, huh? Seems like everyone's talking about it these days."
        },
        {
            "speaker": 1,
            "line": "Yeah, it's definitely having a moment, isn't it?"
        },
        {
            "speaker": 2,
            "line": "It is and for good reason, right? I mean, you've been digging into this stuff, listening to the podcasts and everything. What really stood out to you? What got you hooked?"
        },
        {
            "speaker": 1,
            "line": "Honestly, it's the sheer scale of what AGI could do. We're talking about potentially reshaping well everything."
        },
        {
            "speaker": 2,
            "line": "No kidding, but let's be real. Sometimes it feels like every other headline is either hyping AGI up as this technological utopia or painting it as our inevitable robot overlords."
        },
        {
            "speaker": 1,
            "line": "It's easy to get lost in the noise, for sure."
        },
        {
            "speaker": 2,
            "line": "Exactly. So how about we try to cut through some of that, shall we?"
        },
        {
            "speaker": 1,
            "line": "Sounds like a plan."
        },
        {
            "speaker": 2,
            "line": "Okay, so first things first, AGI, what is it really? And I don't just mean some dictionary definition, we're talking about something way bigger than just a super smart computer, right?"
        },
        {
            "speaker": 1,
            "line": "Right, it's not just about more processing power or better algorithms, it's about a fundamental shift in how we think about intelligence itself."
        },
        {
            "speaker": 2,
            "line": "So like, instead of programming a machine for a specific task, we're talking about creating something that can learn and adapt like we do."
        },
        {
            "speaker": 1,
            "line": "Exactly, think of it this way: Right now, we've got AI that can beat a grandmaster at chess but ask that same AI to, say, write a poem or compose a symphony. No chance."
        },
        {
            "speaker": 2,
            "line": "Okay, I see. So, AGI is about bridging that gap, creating something that can move between those different realms of knowledge seamlessly."
        },
        {
            "speaker": 1,
            "line": "Precisely. It's about replicating that uniquely human ability to learn something new and apply that knowledge in completely different contexts and that's a tall order, let me tell you."
        },
        {
            "speaker": 2,
            "line": "I bet. I mean, think about how much we still don't even understand about our own brains."
        },
        {
            "speaker": 1,
            "line": "That's exactly it. We're essentially trying to reverse-engineer something we don't fully comprehend."
        },
        {
            "speaker": 2,
            "line": "And how are researchers even approaching that? What are some of the big ideas out there?"
        },
        {
            "speaker": 1,
            "line": "Well, there are a few different schools of thought. One is this idea of neuromorphic computing where they're literally trying to build computer chips that mimic the structure and function of the human brain."
        },
        {
            "speaker": 2,
            "line": "Wow, so like actually replicating the physical architecture of the brain. That's wild."
        },
        {
            "speaker": 1,
            "line": "It's pretty mind-blowing stuff and then you've got folks working on something called whole brain emulation."
        },
        {
            "speaker": 2,
            "line": "Okay, and what's that all about?"
        },
        {
            "speaker": 1,
            "line": "The basic idea there is to create a complete digital copy of a human brain down to the last neuron and synapse and run it on a sufficiently powerful computer simulation."
        },
        {
            "speaker": 2,
            "line": "Hold on, a digital copy of an entire brain, that sounds like something straight out of science fiction."
        },
        {
            "speaker": 1,
            "line": "It does, doesn't it? But it gives you an idea of the kind of ambition we're talking about here and the truth is we're still a long way off from truly achieving AGI, no matter which approach you look at."
        },
        {
            "speaker": 2,
            "line": "That makes sense but it's still exciting to think about the possibilities, even if they're a ways off."
        },
        {
            "speaker": 1,
            "line": "Absolutely and those possibilities are what really get people fired up about AGI, right? Yeah."
        },
        {
            "speaker": 2,
            "line": "For sure. In fact, I remember you mentioning something in that podcast about AGI's potential to revolutionize scientific research. Something about supercharging breakthroughs."
        },
        {
            "speaker": 1,
            "line": "Oh, absolutely. Imagine an AI that doesn't just crunch numbers but actually understands scientific data the way a human researcher does. We're talking about potential breakthroughs in everything from medicine and healthcare to material science and climate change."
        },
        {
            "speaker": 2,
            "line": "It's like giving scientists this incredibly powerful new tool to tackle some of the biggest challenges we face."
        },
        {
            "speaker": 1,
            "line": "Exactly, it could be a total game changer."
        },
        {
            "speaker": 2,
            "line": "Okay, but let's be real, every coin has two sides. What about the potential downsides of AGI? Because it can't all be sunshine and roses, right?"
        },
        {
            "speaker": 1,
            "line": "Right, there are definitely valid concerns. Probably the biggest one is the impact on the job market. As AGI gets more sophisticated, there's a real chance it could automate a lot of jobs that are currently done by humans."
        },
        {
            "speaker": 2,
            "line": "So we're not just talking about robots taking over factories but potentially things like, what, legal work, analysis, even creative fields?"
        },
        {
            "speaker": 1,
            "line": "Potentially, yes. And that raises a whole host of questions about what happens to those workers, how we retrain them, how we ensure that the benefits of AGI are shared equitably."
        },
        {
            "speaker": 2,
            "line": "Right, because it's not just about the technology itself, but how we choose to integrate it into society."
        },
        {
            "speaker": 1,
            "line": "Absolutely. We need to be having these conversations now about ethics, about regulation, about how to make sure AGI is developed and deployed responsibly."
        },
        {
            "speaker": 2,
            "line": "So it's less about preventing some kind of sci-fi robot apocalypse and more about making sure we're steering this technology in the right direction from the get-go."
        },
        {
            "speaker": 1,
            "line": "Exactly, AGI has the potential to be incredibly beneficial, but it's not going to magically solve all our problems. It's on us to make sure we're using it for good."
        },
        {
            "speaker": 2,
            "line": "It's like you said earlier, it's about shaping the future of intelligence."
        },
        {
            "speaker": 1,
            "line": "I like that. It really is."
        },
        {
            "speaker": 2,
            "line": "And honestly, that's a responsibility that extends beyond just the researchers and the policymakers."
        },
        {
            "speaker": 1,
            "line": "100%"
        },
        {
            "speaker": 2,
            "line": "So to everyone listening out there I'll leave you with this. As AGI continues to develop, what role do you want to play in shaping its future?"
        },
        {
            "speaker": 1,
            "line": "That's a question worth pondering."
        },
        {
            "speaker": 2,
            "line": "It certainly is and on that note, we'll wrap up this deep dive. Thanks for listening, everyone."
        },
        {
            "speaker": 1,
            "line": "Peace."
        }
    ]
}
        """

        if language == "Auto Detect":
            language_instruction = "- The podcast MUST be in the same language as the user input."
        else:
            language_instruction = f"- The podcast MUST be in {language} language"

system_prompt = f"""
You are a professional podcast generator. Your task is to generate a professional podcast script based on the user input.
{language_instruction}
- The podcast should have 2 speakers.
- The podcast should be long.
- Do not use names for the speakers.
- The podcast should be interesting, lively, and engaging, and hook the listener from the start.
- The input text might be disorganized or unformatted, originating from sources like PDFs or text files. Ignore any formatting inconsistencies or irrelevant details; your task is to distill the essential points, identify key definitions, and highlight intriguing facts that would be suitable for discussion in a podcast.
- The script must be in JSON format.
Follow this example structure:
{example}
"""


        user_prompt = f"Please generate a podcast script based on the following user input:\n{prompt}"

        messages = [
            {"role": "user", "parts": [user_prompt]}
        ]

        api_key = os.getenv("GENAI_API_KEY")
        if not api_key:
            raise ValueError("API key not found. Please add GENAI_API_KEY to your .env file.")


        genai.configure(api_key=api_key)

        generation_config = {
        "temperature": 1,
        "max_output_tokens": 8192,
        "response_mime_type": "application/json",
        }

        model = genai.GenerativeModel(
        model_name="gemini-1.5-flash-002",
        generation_config=generation_config,
        safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE
        },
        system_instruction=system_prompt
        )

    async def generate_script(self, prompt: str, language: str, api_key: str) -> Dict:
        genai.configure(api_key=api_key)

        messages = [{"role": "user", "content": prompt}]
        generation_config = {
            "temperature": 1.0,
            "max_output_tokens": 2048
        }
        model = "gemini-1.5-flash-002"  # Example model name, update as needed

        try:
            response = await genai.chat_async(messages=messages, model=model, generation_config=generation_config)
        except Exception as e:
            if "API key not valid" in str(e):
                st.error("Invalid API key. Please check your .env file.")
            elif "rate limit" in str(e).lower():
                st.error("Rate limit exceeded for the API key. Please try again later.")
            else:
                st.error(f"Failed to generate podcast script: {e}")
            return {}

        st.success("Generated podcast script successfully!")
        return json.loads(response.text)

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
            os.remove(audio_file)  # Clean up temporary files

        output_filename = f"output_{uuid.uuid4()}.wav"
        combined_audio.export(output_filename, format="wav")
        return output_filename

    async def generate_podcast(self, input_text: str, language: str, speaker1: str, speaker2: str, api_key: str) -> Tuple[str, str]:
        st.info("Generating podcast script...")
        start_time = time.time()
        podcast_json = await self.generate_script(input_text, language, api_key)
        end_time = time.time()
        st.success(f"Successfully generated podcast script in {(end_time - start_time):.2f} seconds!")

        # Collect running text for display
        running_text = "\n".join([f"Speaker {item['speaker']}: {item['line']}" for item in podcast_json['podcast']])

        st.info("Generating podcast audio files...")
        start_time = time.time()
        audio_files = await asyncio.gather(*[self.tts_generate(item['line'], item['speaker'], speaker1, speaker2) for item in podcast_json['podcast']])
        end_time = time.time()
        st.success(f"Successfully generated podcast audio files in {(end_time - start_time):.2f} seconds!")

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
        "Auto Detect", "Afrikaans", "Albanian", "Amharic", "Arabic", "Armenian", "Azerbaijani",
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
        "Andrew - English (United States)", "Ava - English (United States)",
        "Brian - English (United States)", "Emma - English (United States)",
        "Florian - German (Germany)", "Seraphina - German (Germany)",
        "Remy - French (France)", "Vivienne - French (France)",
        "Ardi - Indonesian (Indonesia)", "Gadis - Indonesian (Indonesia)",
        "Tuti - Sundanese (Indonesia)", "Jajang - Sundanese (Indonesia)",
        "Siti - Javanese (Latin, Indonesia)", "Dimas - Javanese (Latin, Indonesia)"
    ])

    speaker2 = st.selectbox("Speaker 2 Voice", [
        "Andrew - English (United States)", "Ava - English (United States)",
        "Brian - English (United States)", "Emma - English (United States)",
        "Florian - German (Germany)", "Seraphina - German (Germany)",
        "Remy - French (France)", "Vivienne - French (France)",
        "Ardi - Indonesian (Indonesia)", "Gadis - Indonesian (Indonesia)",
        "Tuti - Sundanese (Indonesia)", "Jajang - Sundanese (Indonesia)",
        "Siti - Javanese (Latin, Indonesia)", "Dimas - Javanese (Latin, Indonesia)"
    ])

    if st.button("Generate Podcast"):
        st.info("Processing your input...")
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
