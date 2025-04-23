# Speech Recognition Settings
SPEECH_TIMEOUT = 5  # seconds
AMBIENT_DURATION = 1  # seconds for ambient noise calibration

# Text-to-Speech Settings
RATE = 175  # words per minute
VOLUME = 1.0  # volume level (0.0 to 1.0)

# LLM Settings
TEMPERATURE = 0.7
MAX_TOKENS = 150
SYSTEM_PROMPT = """You are a helpful AI assistant engaging in verbal conversation. 
Keep your responses concise and natural, as they will be spoken aloud. 
Aim to respond within 2-3 sentences unless more detail is specifically requested."""

# RAG Settings
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
SIMILARITY_K = 3  # number of similar documents to retrieve

# GUI Settings
WINDOW_TITLE = "Speech-to-Speech LLM Bot"
WINDOW_SIZE = "800x600"
DISPLAY_FONT = ("Arial", 10)
STATUS_UPDATE_MS = 100  # milliseconds between status updates

# Performance Settings
RESPONSE_TIMEOUT = 3.0  # maximum seconds to wait for response
CACHE_SIZE = 1000  # number of responses to cache
THREADING_MAX_WORKERS = 3  # maximum number of concurrent threads 
