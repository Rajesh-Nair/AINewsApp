from typing import TypedDict, List, Annotated
from langgraph.graph.message import add_messages

class State(TypedDict):
    """
    Represent the structure of the state used in graph
    """
    messages: Annotated[List, add_messages]

if __name__ == "__main__":
    print("--- State Structure Tests ---")
    # 1. Create an empty state
    state: State = {"messages": []}
    print(type(state))
    print("Empty state:", state)

    # 2. Add a message
    state["messages"].append("Hello, world!")
    print("After adding a message:", state)

    # 3. Add multiple messages
    state["messages"].extend(["How are you?", "Goodbye!"])
    print("After adding multiple messages:", state)

    # 4. Modify a message
    state["messages"][1] = "How are you doing?"
    print("After modifying a message:", state)

    # 5. Remove a message
    removed = state["messages"].pop(0)
    print(f"After removing a message ('{removed}'):", state)

    # 6. Assign invalid type to messages (should raise error in type checkers, but not at runtime)
    try:
        state["messages"] = "Not a list"  # This is not type safe, but Python allows it at runtime
        print("After assigning invalid type to messages:", state)
    except Exception as e:
        print("Error when assigning invalid type:", e)

    # 7. Reset to valid list
    state["messages"] = ["Back to valid list"]
    print("After resetting to valid list:", state)