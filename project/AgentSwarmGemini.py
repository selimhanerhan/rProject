from Configurations import configs
import autogen
from autogen.code_utils import content_str

assistant = autogen.AssistantAgent("assistant", llm_config={"config_list": configs.specific_llm("gemini-pro"), "seed": 42}, max_consecutive_auto_reply=3)

user_proxy = autogen.UserProxyAgent("user_proxy", code_execution_config={"work_dir": "coding", "use_docker": False}, human_input_mode="NEVER", is_termination_msg = lambda x: content_str(x.get("content")).find("TERMINATE") >= 0)

user_proxy.initiate_chat(assistant, message="Sort the array with Bubble Sort: [4, 1, 3, 2]")
