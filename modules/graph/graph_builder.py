from langgraph.graph import StateGraph, START, END
from modules.state.state import State
from modules.nodes.ai_news import AINewsNode


class GraphBuilder:
    def __init__(self, model):
        self.llm = model
        self.graph_builder = StateGraph(State)


    def ai_news_graph(self):

        # Node initialization
        ai_news_node = AINewsNode(self.llm)
        
        # Add nodes to the graph
        self.graph_builder.add_node("fetch_news", ai_news_node.fetch_news)
        self.graph_builder.add_node("generate_summary", ai_news_node.generate_summary)
        self.graph_builder.add_node("save_news  ", ai_news_node.save_news)

        # Add edges to the graph
        self.graph_builder.add_edge(START, "fetch_news")
        self.graph_builder.add_edge("fetch_news", "generate_summary")
        self.graph_builder.add_edge("generate_summary", "save_news")
        self.graph_builder.add_edge("save_news", END)

    def setup_graph(self, usecase: str):
        """
        Set up the graph for the selected usecase
        """
        if usecase == "AI News":
            self.ai_news_graph()

        return self.graph_builder.compile()

