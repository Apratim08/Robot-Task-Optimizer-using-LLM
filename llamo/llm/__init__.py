"""
LLM interface components for OpenAI and LangChain integration.
"""

# Note: llm.py contains global functions, not classes
# Import the module for access to llm_init, llm_query functions
from . import llm

__all__ = ['llm']