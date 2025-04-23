import os
import threading
import queue
import tkinter as tk
from tkinter import ttk, scrolledtext
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv
from openai import OpenAI
import time
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

class SpeechLLMBot:
    def __init__(self):
        # Initialize OpenAI client
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize text-to-speech
        self.engine = pyttsx3.init()
        
        # Initialize GUI
        self.root = tk.Tk()
        self.root.title("Speech-to-Speech LLM Bot")
        self.setup_gui()
        
        # Initialize state variables
        self.is_listening = False
        self.is_speaking = False
        self.should_stop = False
        
        # Initialize queues for async processing
        self.speech_queue = queue.Queue()
        self.response_queue = queue.Queue()
        
        # Initialize RAG components
        self.setup_rag()
        
        # Calibrate microphone
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
    
    def setup_rag(self):
        """Initialize RAG components with a knowledge base"""
        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings()
        
        # Create a simple knowledge base (you can expand this)
        texts = [
            "The bot can process speech input and generate responses.",
            "You can interrupt the bot at any time during conversation.",
            "The bot uses advanced AI to understand and respond to queries.",
        ]
        
        # Split texts and create vector store
        text_splitter = RecursiveCharacterTextSplitter()
        split_texts = text_splitter.split_text("\n".join(texts))
        
        # Create vector store
        self.vectorstore = FAISS.from_texts(
            split_texts,
            self.embeddings
        )
        
        # Initialize retrieval chain
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            ChatOpenAI(temperature=0),
            self.vectorstore.as_retriever(),
            return_source_documents=True
        )
    
    def setup_gui(self):
        """Set up the graphical user interface"""
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create conversation display
        self.conversation_display = scrolledtext.ScrolledText(
            main_frame, width=50, height=20)
        self.conversation_display.grid(row=0, column=0, columnspan=2, pady=5)
        
        # Create buttons
        self.listen_button = ttk.Button(
            main_frame, text="Start Listening", command=self.toggle_listening)
        self.listen_button.grid(row=1, column=0, pady=5)
        
        self.interrupt_button = ttk.Button(
            main_frame, text="Interrupt", command=self.interrupt_conversation)
        self.interrupt_button.grid(row=1, column=1, pady=5)
        
        # Create status label
        self.status_label = ttk.Label(main_frame, text="Ready")
        self.status_label.grid(row=2, column=0, columnspan=2, pady=5)
    
    def toggle_listening(self):
        """Toggle the listening state"""
        if not self.is_listening:
            self.is_listening = True
            self.listen_button.config(text="Stop Listening")
            self.status_label.config(text="Listening...")
            threading.Thread(target=self.listen_loop, daemon=True).start()
        else:
            self.is_listening = False
            self.listen_button.config(text="Start Listening")
            self.status_label.config(text="Ready")
    
    def listen_loop(self):
        """Continuous listening loop"""
        while self.is_listening:
            try:
                with self.microphone as source:
                    audio = self.recognizer.listen(source, timeout=5)
                    text = self.recognizer.recognize_google(audio)
                    self.speech_queue.put(text)
                    self.process_speech()
            except sr.WaitTimeoutError:
                continue
            except Exception as e:
                self.update_conversation(f"Error: {str(e)}")
    
    def process_speech(self):
        """Process speech input and generate response"""
        if not self.speech_queue.empty():
            text = self.speech_queue.get()
            self.update_conversation(f"You: {text}")
            
            # Generate response using RAG
            chat_history = []
            result = self.qa_chain({"question": text, "chat_history": chat_history})
            response = result["answer"]
            
            self.response_queue.put(response)
            self.update_conversation(f"Bot: {response}")
            
            if not self.should_stop:
                threading.Thread(target=self.speak_response, args=(response,), daemon=True).start()
    
    def speak_response(self, text):
        """Convert text to speech and play it"""
        self.is_speaking = True
        self.engine.say(text)
        self.engine.runAndWait()
        self.is_speaking = False
    
    def interrupt_conversation(self):
        """Handle user interruption"""
        self.should_stop = True
        if self.is_speaking:
            self.engine.stop()
        self.should_stop = False
        self.update_conversation("*Conversation interrupted*")
    
    def update_conversation(self, text):
        """Update the conversation display"""
        self.conversation_display.insert(tk.END, f"{text}\n")
        self.conversation_display.see(tk.END)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    bot = SpeechLLMBot()
    bot.run() 
