from duckduckgo_search import DDGS

def gather_web_context(claims: list) -> str:
    """Searches the live web for the extracted claims to find real-world evidence."""
    if not claims:
        return "No verifiable claims found"
    compiled_research = ""

    with DDGS() as ddgs:
        for claim in claims[:2]:
            compiled_research += f"\n--- Investigating: {claim} ---\n"
            try:
                results = ddgs.text(claim,max_results=3)
                for result in results:
                    compiled_research += f"Title: {result.get('title')}\nSnippet: {result.get('body')}\n\n"
            except Exception as e:
                compiled_resarch += f"Search failed for this claim: {str(e)}\n"
    
    return compiled_research