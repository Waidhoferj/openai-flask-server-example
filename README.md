# OpenAI Flask Server

Example of a Langchain Flask Server that adheres to the OpenAI completions API.

## Setup

Prerequisites: Install Python

1. Install Dependencies

```bash
pip install -r requirements.txt
```

2. Start the server

```bash
python app.py
```

## Using with Librechat

### Natively

1. Start the server.

```bash
python app.py
```

2. Update your [librechat.yaml](https://www.librechat.ai/docs/configuration/librechat_yaml) to include your server as a custom endpoint.

```yaml filename="librechat.yaml"
endpoints:
  custom:
    - name: "LangChain" # Could be anything
      apiKey: "super-secret" # Could be anything
      baseURL: "http://host.docker.internal:8000/"
      models:
        default: ["MyModel"] # Could be anything
      titleConvo: true
      titleModel: "current_model"
      summarize: false
      summaryModel: "current_model"
      forcePrompt: false
      modelDisplayLabel: "LangChain" # Could be anything
```

3. Create and start Librechat containers.

```bash
cd Librechat
docker compose up -d
```

4. Open UI and choose your endpoint from the dropdown menu at the top left.
5. Start conversing with the model!

### Using Docker

1. Build an image using the provided dockerfile.
2. Reference the Docker image in the [docker-compose.override.yml](https://www.librechat.ai/docs/configuration/docker_override).
3. Create and start Librechat containers.

```bash
cd Librechat
docker compose up -d
```

## Resources

- [OpenAI API Chat Docs](https://platform.openai.com/docs/api-reference/chat/create)
