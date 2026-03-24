"""Utility functions for PromptLab.

Helper functions for sorting, filtering, searching, validating, and
extracting template variables from prompts.
"""

import re
from typing import List
from app.models import Prompt


def sort_prompts_by_date(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:
    """Sort prompts by their creation date.

    Args:
        prompts: The list of prompts to sort.
        descending: If True (default), newest prompts come first.
            If False, oldest prompts come first.

    Returns:
        A new list of prompts in the requested order.

    Example:
        >>> sorted_prompts = sort_prompts_by_date(prompts, descending=True)
        >>> sorted_prompts[0].created_at >= sorted_prompts[-1].created_at
        True
    """
    return sorted(prompts, key=lambda p: p.created_at, reverse=descending)


def filter_prompts_by_collection(prompts: List[Prompt], collection_id: str) -> List[Prompt]:
    """Filter prompts to only those belonging to a specific collection.

    Args:
        prompts: The list of prompts to filter.
        collection_id: The collection ID to match against.

    Returns:
        A list containing only prompts whose ``collection_id`` matches.

    Example:
        >>> filtered = filter_prompts_by_collection(prompts, "col-123")
    """
    return [p for p in prompts if p.collection_id == collection_id]


def search_prompts(prompts: List[Prompt], query: str) -> List[Prompt]:
    """Search prompts by title or description (case-insensitive).

    Args:
        prompts: The list of prompts to search through.
        query: The search substring to look for.

    Returns:
        A list of prompts whose title or description contains the query.

    Example:
        >>> results = search_prompts(prompts, "python")
    """
    query_lower = query.lower()
    return [
        p for p in prompts
        if query_lower in p.title.lower()
        or (p.description and query_lower in p.description.lower())
    ]


def validate_prompt_content(content: str) -> bool:
    """Check if prompt content meets minimum validity requirements.

    A valid prompt must not be empty, not be only whitespace, and must
    contain at least 10 non-whitespace-padded characters.

    Args:
        content: The prompt content string to validate.

    Returns:
        True if the content is valid, False otherwise.

    Example:
        >>> validate_prompt_content("Short")
        False
        >>> validate_prompt_content("This is a valid prompt content")
        True
    """
    if not content or not content.strip():
        return False
    return len(content.strip()) >= 10


def extract_variables(content: str) -> List[str]:
    """Extract template variable names from prompt content.

    Variables use the ``{{variable_name}}`` syntax. Only word characters
    (letters, digits, underscores) are captured.

    Args:
        content: The prompt content string to scan.

    Returns:
        A list of variable names found in the content.

    Example:
        >>> extract_variables("Hello {{name}}, welcome to {{place}}")
        ['name', 'place']
    """
    pattern = r'\{\{(\w+)\}\}'
    return re.findall(pattern, content)



def normalise_tags(tags: List[str]) -> List[str]:
    """Normalise a list of tags: lowercase, strip whitespace, deduplicate.

    Preserves the order of first occurrence.

    Args:
        tags: Raw tag strings from user input.

    Returns:
        A deduplicated list of cleaned tag strings.

    Example:
        >>> normalise_tags(["Python", " AI ", "python"])
        ['python', 'ai']
    """
    seen: set = set()
    result: List[str] = []
    for tag in tags:
        cleaned = tag.strip().lower()
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            result.append(cleaned)
    return result


def filter_prompts_by_tags(prompts: List[Prompt], tags: List[str]) -> List[Prompt]:
    """Filter prompts that contain all specified tags (AND logic).

    Args:
        prompts: The list of prompts to filter.
        tags: Tag strings to require. An empty list matches everything.

    Returns:
        Prompts that have every tag in ``tags``.

    Example:
        >>> filter_prompts_by_tags(prompts, ["python", "ai"])
    """
    if not tags:
        return prompts
    tag_set = set(t.lower() for t in tags)
    return [p for p in prompts if tag_set.issubset(set(p.tags))]
