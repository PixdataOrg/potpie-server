import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from .repo_schema import RepoAnalysisOutput

def build_llm():
    return ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "anthropic/claude-3.5-sonnet"),
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1"),
        temperature=0,
    )

async def run_structured_repo_analysis(final_prompt: str) -> RepoAnalysisOutput:
    llm = build_llm()
    structured = llm.with_structured_output(RepoAnalysisOutput, method="json_schema")

    result: RepoAnalysisOutput = await structured.ainvoke(
        [
            SystemMessage(content="You are a strict JSON-producing repository analysis engine."),
            HumanMessage(content=final_prompt),
        ]
    )

    # Fix snippets_count in modo deterministic
    if result.snippets_count != len(result.snippets):
        result.snippets_count = len(result.snippets)

    return result
