from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model = "grok-4-1-fast-non-reasoning",
    base_url = "https://api.x.ai/v1",
    temperature = 0.2
)

prompt = ChatPromptTemplate.from_template("Explain {topic} simply.")

prompt.invoke("{topic}")