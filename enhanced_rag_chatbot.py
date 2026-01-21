from huggingface_hub import login
from dotenv import load_dotenv
from transformers import AutoModelForCausalLM
from llama_index.llms.huggingface import HuggingFaceLLM

import os
import config

load_dotenv()

def hf_login():
    token = os.getenv("HUGGINGFACE_HUB_TOKEN")
    if not token:
        raise RuntimeError("HUGGINGFACE_HUB_TOKEN not set")
    login(token=token)

def create_hf_LLM(
    temperature: float = config.TEMPERATURE,
    max_new_tokens: int = config.MAX_NEW_TOKENS,
    decoding_method: str = "sample",
):
    model = AutoModelForCausalLM.from_pretrained(
        config.LLM_MODEL_ID,
        device_map='auto',
        dtype='auto'
    )
    try:
        llm = HuggingFaceLLM(
            model_name=config.LLM_MODEL_ID,
            tokenizer_name=config.LLM_MODEL_ID,
            max_new_tokens=max_new_tokens,
            model=model,
            messages_to_prompt=None,
            completion_to_prompt=None,
            generate_kwargs={
                "temperature": temperature,
                "top_k": config.TOP_K,
                "top_p": config.TOP_P,
                "do_sample": decoding_method == "sample",
            }
        )

        print(f"Created HuggingFace LLM model: {config.LLM_MODEL_ID}")
        return llm
    except Exception as e:
        print(f"Failed to create HuggingFace LLM: {e}")
        return None