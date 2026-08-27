"""
Discover available Gemini models for the configured API key
"""

import os
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

# Load environment variables
try:
    from dotenv import load_dotenv
    env_path = PROJECT_ROOT / '.env'
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    pass

print("=" * 70)
print("Discovering Available Gemini Models")
print("=" * 70)

# Check API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("\nError: GEMINI_API_KEY not found in environment")
    sys.exit(1)

print("\nAPI key configured: Yes (not shown)")

# Import Gemini SDK
try:
    from google import genai
    print("Gemini SDK imported successfully")
except ImportError as e:
    print(f"Error: Failed to import google-genai: {e}")
    sys.exit(1)

# Initialize client
try:
    client = genai.Client(api_key=api_key)
    print("Gemini client initialized")
except Exception as e:
    print(f"Error: Failed to initialize client: {e}")
    sys.exit(1)

# List available models
print("\n" + "=" * 70)
print("Querying available models...")
print("=" * 70)

try:
    models = client.models.list()
    
    # Filter for models that support generateContent
    text_generation_models = []
    
    for model in models:
        # Check if model supports generateContent
        if hasattr(model, 'supported_generation_methods'):
            if 'generateContent' in model.supported_generation_methods:
                text_generation_models.append(model.name)
        elif hasattr(model, 'name'):
            # If no supported_generation_methods, include it and we'll test
            text_generation_models.append(model.name)
    
    if not text_generation_models:
        print("\nNo models found that support text generation")
        print("\nAll available models:")
        for model in models:
            print(f"  - {model.name}")
        sys.exit(1)
    
    print(f"\nFound {len(text_generation_models)} models supporting text generation:\n")
    
    for model_name in text_generation_models:
        print(f"  {model_name}")
    
    # Select the first available model
    selected_model = text_generation_models[0]
    
    print("\n" + "=" * 70)
    print(f"RECOMMENDED MODEL: {selected_model}")
    print("=" * 70)
    
    print(f"\nUpdate .env with:")
    print(f"GEMINI_MODEL={selected_model}")
    
except Exception as e:
    print(f"\nError listing models: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
