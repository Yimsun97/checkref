class ReferenceChecker:
    def __init__(self, api_info, model, system_content_path):
        from api.llm_client import LLMClient
        base_url = api_info['base_url']
        api_key = api_info['api_key']
        self.client = LLMClient(base_url, api_key, model)
        self.client.set_system_content(system_content_path)

    def check_references(self, references, stream=True):
        # Check references using the language model
        modified_references = self.client.get_response(references, stream=stream)
        return modified_references
