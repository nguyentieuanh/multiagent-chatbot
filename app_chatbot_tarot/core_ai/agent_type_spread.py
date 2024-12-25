from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from service import gemini_llm
from dconfig import config_object


class OutputType(BaseModel):
    type: str = Field(description="Xác định câu hỏi người dùng thuộc loại nào")


class Supervisor:
    def __init__(self):
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", config_object.STYLE_READING_AGENT),
                ("human", "{user_input}")
            ]
        )

        structured_output = gemini_llm.with_structured_output(OutputType)
        self.get_type = prompt | structured_output


def supervisor(state):
    print(f'-------GET TYPE SPREAD------')
    messsage = state["human_message"]
    supervisor_agent = Supervisor()
    response = supervisor_agent.get_type.invoke({"user_input": messsage})
    state["type"] = response.type
    print(f'------END TYPE SPREAD--------')
    return state


def choose_type_spread(state):
    """
    Determines which worker to do the task.

    Args:
        state (dict): The current graph state

    Returns:
        str: worker do the task
    """

    worker = state['type']
    print(f"---DECISION: {worker} DO THE TASK---")

    return worker
