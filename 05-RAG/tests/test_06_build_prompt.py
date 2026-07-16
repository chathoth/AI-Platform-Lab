import importlib.util
from pathlib import Path
from langchain_core.documents import Document

module_path = Path(__file__).resolve().parents[1] / "src" / "06_build_prompt.py"
spec = importlib.util.spec_from_file_location("prompt_module", module_path)
prompt_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prompt_module)

def test_prompt_contains_question_context_and_source():
    docs = [
        Document(
            page_content="Requests to carry over vacation must be submitted no later than November 1.",
            metadata={"source":"Vacation Time Policy.pdf","page":2},
        )
    ]
    prompt = prompt_module.build_prompt(
        "When must a carry-over request be submitted?",
        docs,
    )
    assert "When must a carry-over request be submitted?" in prompt
    assert "November 1" in prompt
    assert "Vacation Time Policy.pdf, page 2" in prompt
    assert "Use only the supplied context" in prompt
