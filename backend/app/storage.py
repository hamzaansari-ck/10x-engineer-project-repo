"""In-memory storage layer for PromptLab.

This module provides a simple dictionary-backed storage implementation for
prompts and collections. Data lives only for the lifetime of the process.
In production this would be replaced with a persistent database (e.g. SQLite,
PostgreSQL).
"""

from typing import Dict, List, Optional
from app.models import Prompt, Collection


class Storage:
    """In-memory store for prompts and collections.

    Uses two internal dictionaries keyed by resource ID. A single global
    instance (``storage``) is created at module level and shared across
    the application.

    Attributes:
        _prompts: Internal dict mapping prompt IDs to Prompt objects.
        _collections: Internal dict mapping collection IDs to Collection objects.
    """

    def __init__(self) -> None:
        """Initialise empty prompt and collection stores."""
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}

    # ============== Prompt Operations ==============

    def create_prompt(self, prompt: Prompt) -> Prompt:
        """Persist a new prompt.

        Args:
            prompt: The Prompt object to store.

        Returns:
            The same Prompt object after it has been saved.
        """
        self._prompts[prompt.id] = prompt
        return prompt

    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """Retrieve a prompt by ID.

        Args:
            prompt_id: The unique identifier of the prompt.

        Returns:
            The Prompt if found, otherwise None.
        """
        return self._prompts.get(prompt_id)

    def get_all_prompts(self) -> List[Prompt]:
        """Return every stored prompt.

        Returns:
            A list of all Prompt objects currently in storage.
        """
        return list(self._prompts.values())

    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        """Replace an existing prompt with new data.

        Args:
            prompt_id: The ID of the prompt to update.
            prompt: The new Prompt object to store.

        Returns:
            The updated Prompt, or None if the ID was not found.
        """
        if prompt_id not in self._prompts:
            return None
        self._prompts[prompt_id] = prompt
        return prompt

    def delete_prompt(self, prompt_id: str) -> bool:
        """Remove a prompt from storage.

        Args:
            prompt_id: The ID of the prompt to delete.

        Returns:
            True if the prompt was deleted, False if it did not exist.
        """
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            return True
        return False

    # ============== Collection Operations ==============

    def create_collection(self, collection: Collection) -> Collection:
        """Persist a new collection.

        Args:
            collection: The Collection object to store.

        Returns:
            The same Collection object after it has been saved.
        """
        self._collections[collection.id] = collection
        return collection

    def get_collection(self, collection_id: str) -> Optional[Collection]:
        """Retrieve a collection by ID.

        Args:
            collection_id: The unique identifier of the collection.

        Returns:
            The Collection if found, otherwise None.
        """
        return self._collections.get(collection_id)

    def get_all_collections(self) -> List[Collection]:
        """Return every stored collection.

        Returns:
            A list of all Collection objects currently in storage.
        """
        return list(self._collections.values())

    def delete_collection(self, collection_id: str) -> bool:
        """Remove a collection from storage.

        Args:
            collection_id: The ID of the collection to delete.

        Returns:
            True if the collection was deleted, False if it did not exist.
        """
        if collection_id in self._collections:
            del self._collections[collection_id]
            return True
        return False

    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        """Return all prompts belonging to a specific collection.

        Args:
            collection_id: The collection ID to filter by.

        Returns:
            A list of Prompt objects whose ``collection_id`` matches.
        """
        return [p for p in self._prompts.values() if p.collection_id == collection_id]

    # ============== Utility ==============

    def clear(self) -> None:
        """Remove all prompts and collections from storage.

        Primarily used in test fixtures to reset state between tests.
        """
        self._prompts.clear()
        self._collections.clear()


# Global storage instance
storage = Storage()
