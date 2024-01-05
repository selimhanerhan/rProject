from autogen import OpenAIWrapper
import autogen

class configs:
    def __init__(self,config_list, chosenLLM):
        self.config_list = config_list
        self.chosenLLM = chosenLLM
    
        
    config_list = OpenAIWrapper(
        config_list=[
            {
                "model": "gpt-3.5-turbo",
                "api_key": "",
                "base_url": "https://api.openai.com/v1",
            },
            {
                "model": "llama2-chat-7B",
                "base_url": "http://127.0.0.1:8080",
            },
            {
                "model": "gemini-pro",
                "api_key": "",
                "api_type": "google"
            }
        ],
    )
    
    def specific_llm(self, llm_model_name):
        specified_list = autogen.config_list_from_json(
            "config_list",
            filter_dict={
                "model": [llm_model_name],
            }
        )
        return specified_list
