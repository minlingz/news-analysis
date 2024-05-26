# Global news analysis using LLMs

## Security
### Secure the API key
- The API key is stored in the `.env` file. This file is not included in the repository. This can be done by adding the file to the `.gitignore` file.

```python
# Environments
.env
```
- Example of the `.env` file:
```python
EVENT_REGISTRY_API_KEY=******************
OPENAI_API_KEY=********************
```
- The API key is loaded using the `os` and `load_dotenv` library in Python.
```python
import os
from dotenv import load_dotenv

load_dotenv()  # This loads the environment variables from .env file
api_key = os.getenv("EVENT_REGISTRY_API_KEY")

load_dotenv(override=True)  # This loads the environment variables from .env file and overrides the existing ones
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```

- The API key is used in the following way:
```python
from eventregistry import EventRegistry
er = EventRegistry(apiKey=api_key, allowUseOfArchive=False)
```

```python
from openai import OpenAI
def get_summary(
    art,
    client,
    model="gpt-3.5-turbo",
    language="English",
):

    prompt_complete = f"Summarize the following text in {language}: " + art["body"]
    model = model
    messages = [{"role": "user", "content": prompt_complete}]
    try:
        response = client.chat.completions.create(
            model=model, messages=messages, temperature=0
        )

        content = response.choices[0].message.content
        return content
    except Exception as e:  # if the model fails to return a response
        print(f"Error: {e}")
        return "Sorry, error from GPT."
```