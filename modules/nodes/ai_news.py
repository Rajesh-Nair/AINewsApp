from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate

class AINewsNode:
    def __init__(self, llm):
        """
        Initialize the AINewsNode with a language model and websearch using Tavily API
        Args:
            llm: Language model to use
        """
        self.llm = llm
        self.tavily = TavilyClient()
        self.state = {}

    def fetch_news(self, state: dict) -> dict:
        """
        Fetch the latest news from the web
        Args:
            state (dict): State dictionary containing frequency
        Returns:
            dict: AI News data with key 'news_data'
        """
        try :
            print(state)
            frequency = state['messages'][0].content.lower()
            self.state['frequency'] = frequency
            time_range_map = {'daily': 'd', 'weekly': 'w', 'monthly': 'm', 'year': 'y'}
            days_map = {'daily': 1, 'weekly': 7, 'monthly': 30, 'year': 366}
        
        
            # Search for news using tavily web search API
            response = self.tavily.search(
                query = "Top Artificial Intelligence (AI) news Globally and UK",
                topic = "News",
                time_range = time_range_map[frequency],
                include_answer="advanced",
                max_results=20,
                days = days_map[frequency]
                )
        except Exception as e :
            print("Exception ",e)
            raise Exception(e)
        
        state['news_data'] = response.get("results", [])
        self.state['news_data'] = state['news_data']
        return state

    def generate_summary(self, state : dict) -> dict:
        """
        Generate a summary of the news
        Args:
            state (dict): State dictionary containing news with key 'news_data'
        Returns:
            dict : Updated state with 'summary' key containing the summarized news based on the frequency
        """
        news_items = self.state['news_data']

        prompt_template = ChatPromptTemplate.from_messages([
            ("system","""Summarize AI news articles into markdown format. For each item include:
            - Date in **YYYY-MM-DD** format in BST timezone
            - Concise sentences summary from latest news
            - Sort news by date wise (latest first)
            - Source URL as link
            Use format:
            ### [Date]
            - [Summary](URL)"""),
            ("user", "Articles:\n{articles}")
        ])

        articles_str = "\n\n".join([
            f"Content: {item.get('content', '')}\nURL: {item.get('url', '')}\nDate: {item.get('published_date', '')}"
            for item in news_items
        ])
        print(prompt_template.format(articles=articles_str))
        response = self.llm.invoke(prompt_template.format(articles=articles_str))
        print(response)
        state['summary'] = response.content
        self.state['summary'] = state['summary']
        return self.state

    def save_result(self, state : dict):
        frequency = self.state['frequency']
        summary = self.state['summary']
        filename = f"AINews/{frequency}_summary.md"
        with open(filename, 'w') as f :
            f.write(f"# {frequency.capitalize()} AI News Summary\n\n")
            f.write(summary)
        self.state['filename'] = filename
        return self.state