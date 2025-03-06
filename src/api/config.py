import os
import json
from dotenv import load_dotenv

def get_api_providers():
    """
    Load API providers from JSON file
    
    Returns:
        dict: API providers configuration
    """
    # Try multiple possible locations for the config file
    possible_locations = []
    
    # Get the current script directory and project paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    
    # Add possible file locations in priority order
    possible_locations = [
        os.path.join(parent_dir, 'api_config.json'),           # src/api_config.json
        os.path.join(os.path.dirname(parent_dir), 'src', 'api_config.json'),  # project_root/src/api_config.json
        os.path.join(os.getcwd(), 'api_config.json'),          # Current working directory
        os.path.join(os.getcwd(), 'src', 'api_config.json')    # Current working directory + src
    ]
    
    # Try each location until we find the file
    for filepath in possible_locations:
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    print(f"Loading API config from: {filepath}")
                    return json.load(f)
            except Exception as e:
                print(f"Error reading {filepath}: {str(e)}")
                continue
    
    # If we reach here, we couldn't find the config file
    print(f"Warning: API config file not found. Tried locations: {possible_locations}")
    
    # Return a default configuration as fallback
    default_config = {
        'deepseek': {
            'base_url': "https://api.deepseek.com",
            'api_name': 'DEEPSEEK_API_KEY',
            'models': ["deepseek-chat", "deepseek-reasoning"]
        },
        'aliyun': {
            'base_url': "https://dashscope.aliyuncs.com/compatible-mode/v1",
            'api_name': 'DASHSCOPE_API_KEY',
            'models': ["deepseek-r1", "deepseek-v3", "qwen-max", "qwen-turbo"]
        },
        # Add other providers as needed
    }
    
    print("Using default configuration")
    return default_config


def load_api_info(api_provider):
    """
    Load the API configuration and key for the specified provider.
    
    Args:
        api_provider (str): The name of the API provider to use
        
    Returns:
        dict: API information including base_url, api_key and available models
        
    Raises:
        AssertionError: If an invalid API provider is specified
        ValueError: If the API key is not found in environment variables
    """

    load_dotenv()  # Load environment variables from .env file
    api_providers = get_api_providers()

    # Ensure the API provider is valid
    assert api_provider in api_providers, \
        f"Invalid API provider. Must be one of: {', '.join(api_providers.keys())}"
    
    # Get provider configuration from dictionary
    provider_config = api_providers[api_provider]
    base_url = provider_config['base_url']
    models = provider_config['models']
    api_name = provider_config['api_name']  # Get the environment variable name from the config
    
    # Get API key using the specified environment variable name
    api_key = os.getenv(api_name)
    
    # Ensure the API key is available
    if not api_key:
        raise ValueError(f"Missing API key. Please set the {api_name} environment variable.")

    # Return the API information
    api_info = {
        'base_url': base_url,
        'api_key': api_key,
        'models': models
    }

    return api_info
