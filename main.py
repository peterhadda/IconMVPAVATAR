import os
import json
import openai
from dotenv import load_dotenv
from google.cloud import texttospeech
from playsound import playsound

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google-tts.json"

# Initialize OpenAI client
client = openai.OpenAI(api_key=openai_api_key)

# Load conversation flows
with open("flow.json", "r") as f:
    flows = json.load(f)

# Choose flow
flow_id = "tip"  # Change to 'intro', 'faq', etc.
user_prompt = flows[flow_id]["prompt"]

# Ask OpenAI
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a supportive AI leadership mentor."},
        {"role": "user", "content": user_prompt}
    ]
)

ai_reply = response.choices[0].message.content.strip()
print(f"\n🧠 Flow: {flow_id}")
print(f"👤 User: {user_prompt}")
print(f"🤖 AI: {ai_reply}")

# Initialize Google TTS
tts_client = texttospeech.TextToSpeechClient()

synthesis_input = texttospeech.SynthesisInput(text=ai_reply)
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US",
    ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
)
audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

# Synthesize and save
tts_response = tts_client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
)

with open("avatar_response.mp3", "wb") as out:
    out.write(tts_response.audio_content)
    print("\n🔊 Saved response to 'avatar_response.mp3'")

# Play the audio
playsound("avatar_response.mp3")




