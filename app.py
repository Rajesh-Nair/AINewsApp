import streamlit as st

from modules.frontend.loadui import LoadStreamlitUI
from modules.graph.graph_builder import GraphBuilder
from modules.frontend.display_results import DisplayResultStreamlit
from modules.genai.groqllm import GroqLLM

def load_app():
    print("Hello from ainewsapp!")

    ##Load UI
    ui=LoadStreamlitUI()
    user_input=ui.load_streamlit_ui()

    if not user_input:
        st.error("Error: Failed to load user input from the UI.")
        return
    
    # Text input for user message
    if st.session_state.IsFetchButtonClicked:
        user_message = st.session_state.timeframe 
    else :
        user_message = st.chat_input("Enter your message:")

    if user_message:
        if not st.session_state.IsFetchButtonClicked:
            st.error(f"Chatbot feature is Not Active Now")
            return
        try:
            ## Configure The LLM's
            obj_llm_config=GroqLLM(user_controls_input=user_input)
            model=obj_llm_config.get_llm_model()

            if not model:
                st.error("Error: LLM model could not be initialized")
                return
            
            # Initialize and set up the graph based on use case
            usecase=user_input.get("selected_usecase")

            if not usecase:
                st.error("Error: No use case selected.")
                return

            ## Graph Builder
            graph_builder=GraphBuilder(model)
            try:
                 graph=graph_builder.setup_graph(usecase)
                 print(user_message)
                 DisplayResultStreamlit(usecase,graph,user_message).display_result_on_ui()
            except Exception as e:
                 st.error(f"Error: Graph set up failed- {e}")
                 return

        except Exception as e:
             st.error(f"Error: Graph set up failed- {e}")
             return   



if __name__ == "__main__":
    load_app()