import random
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from langchain.prompts import ChatPromptTemplate
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser


# TODO:
# need to debug the get_clarified_topic 
#       need to find a way to generate a response in line 61
#       need to find a way to connect the input with the current topic
# need to work on other parts as well
#

class VideoSearchAgent():
        
    def __init__(self, api_key):
        """
        Initializes the VideoSearchAgent with the YouTube API key.

        Args:
            api_key (str): The YouTube API key.
        """
        
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        
        
    def get_clarified_topic(self):
        """
        Runs the interactive help tool to clarify the user's topic.
        Returns:
            str: The clarified and refined topic chosen by the user.
        """
        
        initial_prompt = ChatPromptTemplate.from_messages(
            [("ai","Hi there! I can help you find videos on youtube based on the topic you want."),
             ("human","Hi, I have questions for you"),
             ("ai","Great! Go Ahead")
            ]
            
        )
        clarifying_prompt = {
            "health": ["What aspect of health are you interested in? (e.g., fitness, nutrition, specific diseases)",
                      "Are you looking for educational content, personal experiences, or entertainment?",],
            "technology": ["What kind of technology are you curious about?", 
                           "Do you prefer anything specific?"],
            "sport": ["Do you prefer olympic sports or non-olympic sports?",
                      "Do you prefer the indoor or outdoor sports?"],
            "science": ["Which area of the science are you interested in?",
                        "Do you want something profitable?"]
        }
        #output_parser = OpenAIFunctionsAgentOutputParser.get_format_instructions(
        #    {
        #        "text": lambda text: text.lower()
        #    }
        #)
        current_topic = None
        while True:
            if current_topic is None:
                response = initial_prompt.invoke()
                print(response)
            else:
                prompts = clarifying_prompt.get(current_topic, [])
                if prompts:
                    next_prompt = ChatPromptTemplate(random.choice(prompts))
                    print(next_prompt.generate())
                else:
                    prompts = clarifying_prompt.get(current_topic, [])
                    if prompts:
                        next_prompt = ChatPromptTemplate(random.choice(prompts))
                        print(next_prompt.generate())
                    else:
                        break
            
                user_input = input()
                current_topic = (user_input)["text"]
        return current_topic
        
    
    def search_videos(self, topic, max_results = 10, **kwargs):
        """
        Searches for videos on YouTube based on a topic and returns a list of metadata.

        Args:
            topic: The keyword or phrase to search for.
            max_results: Maximum number of videos to return (default: 10).
            **kwargs: Additional search parameters (e.g., channel_id, published_after).

        Returns:
            A list of dictionaries containing video metadata, each including:
                - title: Video title.
                - video_id: YouTube video ID.
                - channel_name: Channel name.
                - upload_date: Upload date as YYYY-MM-DD.
                - link: URL to the video.
                - (optional) additional extracted information.
        """
        try:
            search_response = self.youtube.search().list(
                part='snippet',
                q=topic,
                type='video',
                maxResults=max_results,
                **kwargs
            ).execute()
            videos = []
            for item in search_response['items']:
                video = {
                    'title': item['snippet']['title'],
                    'video_id': item['id']['videoId'],
                    'channel_name': item['snippet']['channelTitle'],
                    'upload_date': item['snippet']['publishedAt'][:10],
                    'link': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                }
                videos.append(video)
            return videos
        except HttpError as error:
            print(f"Youtube API Error: {error}")
            return []
       
# youtube data api key
api_key = ""
agent = VideoSearchAgent(api_key)

user_input = input("What would you like to learn about today? ")
clarified_topic = agent.get_clarified_topic()
print(f"Searching for videos on '{clarified_topic}'...")

videos = agent.search_videos(clarified_topic, max_results = 5)
print(f"Found {len(videos)} videos: ")
for video in videos:
    print(f"- {video['title']} ({video['link']})")
    


    
