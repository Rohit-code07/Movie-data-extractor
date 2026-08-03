from dotenv import load_dotenv

load_dotenv()

from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage,SystemMessage,HumanMessage
message=[
SystemMessage(content="you are teaching assistant")
]
print("-----------------Welcome wirte 0 to exit---------------------")

while True:
    model = init_chat_model("google_genai:gemini-2.5-flash")
    
    prompt = input("you: " )
    if prompt == "0":
        print(message)
        break
    message.append(HumanMessage(prompt))
    reponse = model.invoke(message)
    message.append(AIMessage(reponse.content))
    print("Bot: ",reponse.content)
    