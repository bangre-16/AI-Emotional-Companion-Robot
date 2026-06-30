\# Ollama Bridge



\## Overview



This module acts as a communication bridge between the Raspberry Pi 4B and the locally hosted Ollama Large Language Model (Phi-3).



A Flask server exposes a REST API that receives prompts from the Raspberry Pi, forwards them to Ollama, and returns AI-generated responses.



\---



\## Requirements



\- Python 3.10+

\- Ollama

\- Phi-3 Model



Install dependencies:



```bash

pip install -r requirements.txt

```



\---



\## Run the Server



```bash

python ollama\_server.py

```



The server starts at:



```

http://0.0.0.0:5000

```



\---



\## API Endpoint



\### POST `/generate`



Example Request



```json

{

&#x20;   "prompt": "I am feeling sad today."

}

```



Example Response



```json

{

&#x20;   "text": "I'm sorry you're feeling sad. Would you like to talk about it?"

}

```



\---



\## Model Used



\- Ollama

\- Phi-3

