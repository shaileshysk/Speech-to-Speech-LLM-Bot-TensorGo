# Speech-to-Speech-LLM-Bot-TensorGo
# Speech-to-Speech LLM Bot

An interactive conversational bot that enables natural speech-based interactions with an AI language model, featuring real-time speech recognition, LLM-powered responses, and text-to-speech output.

## Features

- 🎤 **Speech Recognition**: Real-time voice input processing
- 🤖 **LLM Integration**: Intelligent response generation using OpenAI's GPT models
- 🔊 **Text-to-Speech**: Natural-sounding voice responses
- ⚡ **Quick Response Time**: Under 3-second response latency
- 🔄 **Interruption Handling**: Seamless conversation flow with interrupt capability
- 📚 **RAG Support**: Enhanced responses through Retrieval-Augmented Generation
- 🎯 **User-Friendly Interface**: Simple controls for voice interaction

## Requirements

- Python 3.8+
- OpenAI API key
- Microphone for voice input
- Speakers for audio output

## Installation

1. Clone the repository:
```bash
git clone https://github.com/shaileshysk/Speech-to-Speech-LLM-Bot-TensorGo
cd speech-llm-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

1. Run the main application:
```bash
python main.py
```

2. Click the "Start Listening" button to begin a conversation
3. Speak naturally into your microphone
4. The bot will process your speech and respond verbally
5. You can interrupt the bot at any time by clicking the "Interrupt" button

## Architecture

### Components

1. **Speech Recognition Module**
   - Uses `speech_recognition` library for real-time voice input
   - Supports multiple languages and accents
   - Implements noise reduction and error handling

2. **LLM Integration**
   - Leverages OpenAI's GPT models for response generation
   - Implements context management for coherent conversations
   - Features RAG capabilities for enhanced knowledge retrieval

3. **Text-to-Speech Engine**
   - Uses `pyttsx3` for natural voice synthesis
   - Supports voice customization and speed control
   - Implements async processing for smooth playback

4. **Interrupt Handler**
   - Manages real-time conversation flow
   - Implements graceful interruption of ongoing responses
   - Maintains conversation context during interruptions

5. **User Interface**
   - Simple and intuitive controls
   - Real-time status indicators
   - Visual feedback for voice activity

## Performance Optimization

- Async processing for parallel execution
- Response caching for frequently asked questions
- Stream processing for real-time speech recognition
- Efficient context management for faster responses

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
