from flask import Flask, Response, request
from pydantic import BaseModel, Field
from langchain_core.messages import AIMessageChunk
from langchain_core.runnables import RunnableGenerator
import json
import time
from typing import Iterable, Literal
from uuid import uuid4
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOllama

system_fingerprint = str(uuid4())
app = Flask(__name__)
model = "mistral"

class Message(BaseModel):
    role: Literal["user", "assistant"]
    content:str

class OpenAIRequest(BaseModel):
    model: str
    temperature: float
    top_p: int = Field(gt=0)
    presence_penalty: float
    frequency_penalty: float
    user: str
    stream: bool
    messages: list[Message]


@RunnableGenerator
def stream_openai_response(chunks: Iterable[AIMessageChunk]) -> Iterable[bytes]:
    for chunk in chunks:
        data = json.dumps({"id": chunk.id, 
                           "object": 
                           "chat.completion.chunk", 
                           "created": int(time.time()), 
                           "model": model, 
                           "system_fingerprint": system_fingerprint,
                           "choices":[
                               {
                                "index": 0,
                                "delta": {"content": chunk.content},
                                "logprobs": None,
                                "finish_reason": None
                                }
                                    ]})
        b = bytes(f"data: {data}\n\n", "utf-8")
        yield b

def build_chain():
    prompt = ChatPromptTemplate.from_template("Question: {input}")
    llm = ChatOllama(model="mistral")
    return prompt | llm

chain = build_chain() | stream_openai_response

@app.route("/chat/completions", methods=["POST"])
def chat():
    chat = OpenAIRequest(**request.get_json())
    question = chat.messages[-1].content
    return Response(chain.stream(question), mimetype="text/event-stream")

if __name__ == "__main__":
    app.run(debug=True, port=8000)
