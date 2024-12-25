from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from dconfig import config_object
from service import gemini_llm


class ReadTimeOutput(BaseModel):
    result: str = Field(description="Trả về thời gian theo quy tắc ở hướng dẫn")


class PredictTimeAgent:
    def __init__(self):
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", config_object.PROMPT_READING_TAROT_TIME),
                ("human", "{user_input}")
            ]
        )

        structured_output = gemini_llm.with_structured_output(ReadTimeOutput)
        self.answer_time = prompt | structured_output


def read_time_tarot(state):
    print(f'-----START READING----')
    reader_agent = PredictTimeAgent()
    message = state["human_message"]
    result = reader_agent.answer_time.invoke({"user_input": message})
    state["ai_response"] = result
    print(f'-------END READING-------')
    return state