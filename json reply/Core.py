from dotenv import load_dotenv

load_dotenv()
from langchain_core.prompts import ChatPromptTemplate
from typing import List, Optional
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from langchain_mistralai import ChatMistralAI

model = ChatMistralAI(
    model="mistral-small-2603"
)

class movie(BaseModel):
    title: str
    release_year: Optional[int]
    genre: List[str]
    director: Optional[str]
    cast: List[str]
    rating: Optional[float]
    summary: str


parser = PydanticOutputParser(pydantic_object=movie)


prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
Extract accurate movie information from the user's query.
Do not invent facts; use null for unknown optional fields.
Return only the structured Movie output.
{format_instructions}
""",
    ),
    ("human", "{paragraph}")
])

para = input("Give your paragraph")

final_prompt = prompt.invoke({
    "paragraph": para,
    "format_instructions": parser.get_format_instructions()
})
response= model.invoke(final_prompt)
print(response.content)