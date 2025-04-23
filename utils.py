import time
from functools import lru_cache
import threading
from queue import Queue
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ResponseCache:
    """Cache for storing and retrieving responses"""
    def __init__(self, max_size=1000):
        self.cache = {}
        self.max_size = max_size
        self.lock = threading.Lock()
    
    def get(self, key):
        """Get a cached response"""
        with self.lock:
            return self.cache.get(key)
    
    def put(self, key, value):
        """Store a response in the cache"""
        with self.lock:
            if len(self.cache) >= self.max_size:
                # Remove oldest item
                oldest_key = next(iter(self.cache))
                del self.cache[oldest_key]
            self.cache[key] = value

class RateLimiter:
    """Rate limiter for API calls"""
    def __init__(self, max_calls_per_minute):
        self.max_calls = max_calls_per_minute
        self.calls = []
        self.lock = threading.Lock()
    
    def wait_if_needed(self):
        """Wait if rate limit is exceeded"""
        now = time.time()
        with self.lock:
            # Remove calls older than 1 minute
            self.calls = [t for t in self.calls if now - t < 60]
            
            if len(self.calls) >= self.max_calls:
                sleep_time = 60 - (now - self.calls[0])
                if sleep_time > 0:
                    time.sleep(sleep_time)
            
            self.calls.append(now)

class AsyncProcessor:
    """Asynchronous processor for handling tasks"""
    def __init__(self, max_workers=3):
        self.queue = Queue()
        self.workers = []
        self.max_workers = max_workers
        self.running = True
    
    def start(self):
        """Start worker threads"""
        for _ in range(self.max_workers):
            worker = threading.Thread(target=self._worker_loop, daemon=True)
            worker.start()
            self.workers.append(worker)
    
    def stop(self):
        """Stop worker threads"""
        self.running = False
        for worker in self.workers:
            worker.join()
    
    def _worker_loop(self):
        """Worker thread loop"""
        while self.running:
            try:
                task, args, kwargs = self.queue.get(timeout=1)
                task(*args, **kwargs)
                self.queue.task_done()
            except Queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Error in worker thread: {e}")
    
    def submit(self, task, *args, **kwargs):
        """Submit a task for processing"""
        self.queue.put((task, args, kwargs))

@lru_cache(maxsize=1000)
def preprocess_text(text):
    """Preprocess text for better speech synthesis"""
    # Remove special characters that might affect speech
    text = text.replace('_', ' ')
    text = text.replace('-', ' ')
    
    # Add pauses for better speech rhythm
    text = text.replace('.', '. ')
    text = text.replace('!', '! ')
    text = text.replace('?', '? ')
    
    # Clean up extra whitespace
    text = ' '.join(text.split())
    
    return text

def measure_response_time(func):
    """Decorator to measure response time of functions"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        logger.info(f"{func.__name__} took {duration:.2f} seconds")
        return result
    return wrapper

def safe_thread_execution(func):
    """Decorator for safe thread execution"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in thread {threading.current_thread().name}: {e}")
            raise
    return wrapper 
