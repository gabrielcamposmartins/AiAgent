from pprint import pprint
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage
from langchain.schema.output_parser import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import json
from TTS.api import TTS
from playsound import playsound
import logging
import asyncio

async def synthesize_speech(text, file_path="output.wav"):
        tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DCA", progress_bar=False)
        await tts.tts_to_file(text=text, file_path=file_path)

async def main():
    # Suppress progress bar and set logging level
    logging.getLogger("TTS").setLevel(logging.WARNING)

    local_llm = 'llama3'
    llama3 = ChatOllama(model=local_llm, temperature=0)
    question = ""

    while question != 'exit':
        question = input(">>> ")
        prompt = ChatPromptTemplate.from_messages(
            [
                ("user", question)
            ]
        )

        generate_chain = prompt | llama3 | StrOutputParser()
        generation = ""
        # generation = generate_chain.invoke({"question":question})

        async for chunk in generate_chain.astream({"question":question}):
            print(f"{chunk}", end="", flush=True)
            generation += chunk
        print("\n")
        # tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DCA", progress_bar=False)
        # tts.tts_to_file(text=generation, file_path="output.wav")
        await synthesize_speech(generation)

        # playsound('output.wav')

asyncio.run(main())