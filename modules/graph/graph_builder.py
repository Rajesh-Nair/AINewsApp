from langgraph.graph import StateGraph, START, END
from modules.state.state import State
from modules.nodes import AINewsNode


class GraphBuilder:
    def __init__(self, model):
        self.llm = model
        self.graph_builder = StateGraph(State)


    def ai_news_graph(self):

        # Node initialization
        ai_news_node = AINewsNode()
        
        # Add nodes to the graph
        self.graph_builder.add_node("fetch_news", AINewsNode.fetch_news)
        self.graph_builder.add_node("generate_summary", AINewsNode.generate_summary)
        self.graph_builder.add_node("save_news  ", AINewsNode.save_news)

        # Add edges to the graph
        self.graph_builder.add_edge(START, "fetch_news")
        self.graph_builder.add_edge("fetch_news", "generate_summary")
        self.graph_builder.add_edge("generate_summary", "save_news")
        self.graph_builder.add_edge("save_news", END)

