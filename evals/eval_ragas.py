from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from ragas.evaluation import evaluate
from langchain_openai import OpenAIEmbeddings
from datasets import Dataset
import pandas as pd
from app.llm.agent import create
from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage
from app.database import get_adm_db
import app.config as config

data = [
    {
        "user_input": "What is the goal of a low histamine diet ?",
        "ground_truth": "the goal is to pay attention to what foods are making you symptomatic and try to eat foods that contain smaller levels of histamine whenever possible"
    },
    {
        "user_input": "What are some common symptoms of histamine intolerance ?",
        "ground_truth": "Common symptoms of histamine intolerance include headaches, hives, digestive issues, nasal congestion, fatigue, and flushing."
    },
    {
        "user_input": "Which foods should be avoided on a low histamine diet ?",
        "ground_truth": "Foods to avoid on a low histamine diet include aged cheeses, fermented foods, processed meats, alcohol, and certain fish like tuna and mackerel."
    },
]

agent = create(db=get_adm_db())

for i, item in enumerate(data):
    result = agent.invoke(
        { "messages": [{"role": "user", "content": item["user_input"]}]},
        {"configurable": {"thread_id": f"eval-{i}"}}
    )

    contexts = [
        m.content
        for m in result["messages"]
        if isinstance(m, ToolMessage)
    ]
    
    item["contexts"] = contexts
    item["response"] = result["messages"][-1].content

df = pd.DataFrame(data, columns=["user_input", "response", "contexts", "ground_truth"])

dataset = Dataset.from_pandas(df)

llm = ChatOpenAI(
    openai_api_key=config.vars['openai_api_key'],
    model="gpt-3.5-turbo",
    temperature=0.0,
)

results = evaluate(
    llm = llm,
    dataset=dataset,
    metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
    embeddings=OpenAIEmbeddings(model="text-embedding-3-large", openai_api_key=config.vars["openai_api_key"])
)

print(results)