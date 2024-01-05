import autogen
from Configurations import configs
# have two different agents
# 1 - Finder = finds the videos on youtube that are related to a specific topic
# 2 - Builder = builds a dynamically updating website that summarizes all videos that is retrieved by {Finder}




def getTopic(message):
    user_proxy.initiate_chat(finder, message = message)
    return user_proxy.last_message()["context"]

user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message="human admin",
    code_execution_config={"last_n_messages": 2, "work_dir": "groupchat"},
    human_input_mode="TERMINATE",
    function_map={"getTopic": getTopic}
)


finder = autogen.AssistantAgent(
    system_message="You find the videos on youtube that are related to a specific topic that is given by the user.",
    name="finder",
    llm_config=configs.specific_llm("gpt-3.5-turbo")
)

builder = autogen.AssistantAgent(
    system_message="You build a dynamically updating website that summarizes all videos that is retrieved by finder agent",
    name="builder",
    llm_config=configs.specific_llm("gpt-3.5-turbo")
)


groupchat = autogen.GroupChat(agents=[user_proxy, finder, builder], messages=[], max_round=12)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=configs.specific_llm("gpt-3.5-turbo"))


user_proxy.initiate_chat(manager, message="")
