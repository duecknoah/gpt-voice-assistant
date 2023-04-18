# gpt-voice-assistant
Very easily use your Microphone to talk to OpenAI's GPT3 Turbo. Transcribes your microphone audio to text and have OpenAI's response streamed and read back to you.
ElvenLabs provides a very realistic sounding voice.

### Requirements:
- OpenAI API key: https://openai.com/blog/openai-api
- ElvenLabs API key (optional but recommended): https://beta.elevenlabs.io/speech-synthesis

### Setup:
1. Rename `.env.sample` -> `.env`
2. Put your OpenAI and optional Elvenlabs API key in there (Resorts to default TTS if no ElvenLabs API key provided)
3. Install requirements: `pip install -r requirements.txt`
4. Make sure to have a microphone plugged in
4. Run via `python main.py`
