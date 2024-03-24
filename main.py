from shortGPT.config.api_db import ApiKeyManager, ApiProvider
from shortGPT.config.asset_db import AssetDatabase, AssetType
from shortGPT.engine.facts_short_engine import FactsShortEngine
from shortGPT.audio.eleven_voice_module import ElevenLabsVoiceModule
from shortGPT.config.languages import Language
from shortGPT.audio.edge_voice_module import EdgeTTSVoiceModule, EDGE_TTS_VOICENAME_MAPPING
import os

# Set API Keys
ApiKeyManager.set_api_key(ApiProvider.OPENAI, os.getenv("openApiKey"))
ApiKeyManager.set_api_key(ApiProvider.ELEVEN_LABS, os.getenv("elevenLabsApiKey"))

# Add Assets
AssetDatabase.add_remote_asset("minecraft background cube", AssetType.BACKGROUND_VIDEO, "https://www.youtube.com/watch?v=Pt5_GSKIWQM")
AssetDatabase.add_remote_asset('chill music', AssetType.BACKGROUND_MUSIC, "https://www.youtube.com/watch?v=uUu1NcSHg2E")
AssetDatabase.add_local_asset('my_music', AssetType.AUDIO, "./my_music.wav")

USE_ELEVEN_LABS = False
# Configure the ElevenLabs Voice Module
if USE_ELEVEN_LABS:
    eleven_labs_key = ApiKeyManager.get_api_key(ApiProvider.ELEVEN_LABS)
    voice_module = ElevenLabsVoiceModule(api_key = eleven_labs_key, voiceName="Antoni")
else:
    ## You can also use the EdgeTTS for Free voice synthesis
    voice_name = EDGE_TTS_VOICENAME_MAPPING[Language.GERMAN]['male']
    voice_module = EdgeTTSVoiceModule(voice_name)

# Configure Content Engine
facts_video_topic = "Interesting scientific facts from the 19th century"
content_engine = FactsShortEngine(voiceModule=voice_module,
    facts_type=facts_video_topic,
    background_video_name="minecraft background cube", # <--- use the same name you saved in  the AssetDatabase
    background_music_name='chill music', # <--- use the same name you saved in  the AssetDatabase
    num_images=5, # If you don't want images in your video, put 0 or None
    language=Language.GERMAN)

# Generate Content
for step_num, step_logs in content_engine.makeContent():
    print(f" {step_logs}")

# Get Video Output Path
print(content_engine.get_video_output_path())