import os
from typing import Any

from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, select_autoescape
from openai import OpenAI
from thefuzz import process


def process_template(template_file: str, data: dict[str, Any]) -> str:
    jinja_env = Environment(
        loader=FileSystemLoader(searchpath="./"), autoescape=select_autoescape()
    )

    template = jinja_env.get_template(template_file)
    return template.render(**data)


load_dotenv()

with open("cpu_names.txt", "r") as f:
    names = [line.strip() for line in f.readlines()]


results = process.extract(
    "amd ryzen 9 7950x3d 16-cores 128m cache , 64mb 3d v-cache", names, limit=5
)

data = {
    "product": "amd ryzen 9 7950x3d 16-cores 128m cache , 64mb 3d v-cache",
    "product_list": [result[0] for result in results],
}

prompt = process_template("product-matcher/prompt_template.jinja", data)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="gpt-4o",
)

print(results[int(chat_completion.choices[0].message.content)])
