from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.prompts import ChatPromptTemplate
from dconfig import config_object
from app_chatbot_tarot.service import gemini_llm


# define structure output
class ResultSpread(BaseModel):
    result: str = Field(description="Đây là câu trả lời cho câu hỏi về Tarot người dùng đã đưa ra")


# define chain
class ReadingSpreadChain:
    def __init__(self):
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", config_object.PROMPT_READING_TAROT),
                ("human", "{user_input}")
            ]
        )

        structured_reading_spread = gemini_llm.with_structured_output(ResultSpread)
        self.gen_result = prompt | structured_reading_spread


def reader(state):
    print(f'-----START READING----')
    reader_agent = ReadingSpreadChain()
    message = state["human_message"]
    result = reader_agent.gen_result.invoke({"user_input": message})
    state["ai_response"] = result
    print(f'-------END READING-------')
    return state
