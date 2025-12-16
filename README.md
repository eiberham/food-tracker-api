## Food Tracker

This is a FastAPI backend that combines LangChain Agents, Supabase, and pgvector to deliver an AI-powered food tracking system. The API supports natural-language queries, vector search, and tool calling agents to retrieve meals, symptoms, and user-specific data.

It uses an Agentic RAG pipeline to ground responses on user-uploaded documents stored in Supabase.

Features:

- FastAPI backend with clean modular architecture
- LangChain agent with custom tools
- Supabase pgvecytor for document embeddings and semantic search
- Agentic RAG ( tool invocation + retrieval )
- Authentication and per-user data isolation
- SQLAlchemy models + Pydantic schemas
- Chat endpoint with streaming to improve the perceived responsivenes by creating a faster, more fluid, and human-like interaction.
- Guardrails for monitoring agent work

### Deployment

You can deploy it to railway by conteinerizing the application, pushing it to dockerhub and then pulling it from there.

```shell
docker buildx build --platform linux/amd64,linux/arm64 -t username/food-tracker:v1.0 --push .
```

### How to run it locally ?

Clone the repository

```shell
git clone food-tracker-api
```

Create a virtual environment

```shell
python3 -m venv food-tracker-env
```

Activate it

```shell
source food-tracker-env/bin/activate
```

Install your exact dependencies

```shell
pip install -r requirements.txt
```

Run it

```shell
fastapi dev main.py
```
