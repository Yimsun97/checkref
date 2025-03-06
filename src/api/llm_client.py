from openai import OpenAI
from utils.file_handler import read_text_file


class LLMClient:
    def __init__(self, base_url, api_key, model):
        if not api_key or not isinstance(api_key, str) or api_key.strip() == "":
            raise ValueError("API key cannot be empty")
        if not base_url or not isinstance(base_url, str) or base_url.strip() == "":
            raise ValueError("Base URL cannot be empty")
            
        self.client = OpenAI(
            base_url=base_url.strip(),
            api_key=api_key.strip()
        )
        self.model = model
        self.system_content = ""

    def set_system_content(self, system_content_path):
        self.system_content = read_text_file(system_content_path)

    def get_response(self, user_content, stream=True):
        """Get response from LLM with optional streaming support.
        
        Args:
            user_content (str): The user's input content
            stream (bool, optional): Whether to stream the response. Defaults to True.
        
        Returns:
            str: The complete response text
        """
        assert self.system_content, "System content is not set"
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_content},
                    {"role": "user", "content": user_content}
                ],
                stream=stream
            )
            
            if stream:
                # Handle streaming response
                response_text = ""
                for chunk in completion:
                    response_text_chunk = chunk.choices[0].delta.content
                    if response_text_chunk is not None:
                        response_text += response_text_chunk
                        print(response_text_chunk, end='', flush=True)    # Print response in real-time
                return response_text
            else:
                # Handle non-streaming response
                return completion.choices[0].message.content
        except Exception as e:
            raise Exception(f"API Error: {str(e)}")