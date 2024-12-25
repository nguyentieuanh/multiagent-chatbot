from typing_extensions import TypedDict
from typing import List, Optional
from langgraph.graph import END, StateGraph, START
from agent_read_spread import reader
from agent_spread_time import read_time_tarot
from agent_type_spread import choose_type_spread, supervisor


class AgentState(TypedDict):
    human_message: Optional[str]
    ai_response: Optional[str]
    type: Optional[str]


class GraphBotTarot:
    def __init__(self):
        self.chain = self.build_graph()

    @staticmethod
    def build_graph():
        workflow = StateGraph(AgentState)

        workflow.add_node("Reader", reader)
        workflow.add_node("Time", read_time_tarot)
        workflow.add_node("Supervisor", supervisor)

        workflow.add_edge(START,
                          "Supervisor")

        workflow.add_conditional_edges(
            "Supervisor",
            choose_type_spread,
            {
                "TIME": "Time",
                "SPREAD": "Reader"
            },

            END
        )

        # workflow.add_edge(
        #     "Reader",
        #     END
        # )
        #
        # workflow.add_edge(
        #     "Time",
        #     END
        # )

        return workflow.compile()

    def process(self, message):
        input_message = {"human_message": message}
        response = self.chain.invoke(input=input_message)
        return response


if __name__ == "__main__":
    bot_tarot = GraphBotTarot()
    while True:
        message = input(f"Nhập câu hỏi:")
        if message == "exit":
            break
        response = bot_tarot.process(message)
        result_format = response["ai_response"].result.replace("\\n", "\n")
        print(result_format)


