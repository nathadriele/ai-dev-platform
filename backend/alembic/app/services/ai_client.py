"""
AI Client Service - Real Integration with OpenAI and Anthropic

This service provides actual AI model invocations for agents and features.
"""
import os
from typing import Dict, List, Optional, Any
import httpx
from app.core.config import settings


class AIClient:
    """Client for AI model APIs (OpenAI, Anthropic)."""

    def __init__(self):
        self.openai_key = settings.openai_api_key
        self.anthropic_key = settings.anthropic_api_key

    async def call_openai(
        self,
        messages: List[Dict],
        model: str = "gpt-4",
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> Dict[str, Any]:
        """Call OpenAI API."""
        if not self.openai_key:
            raise ValueError("OpenAI API key not configured")

        headers = {
            "Authorization": f"Bearer {self.openai_key}",
            "Content-Type": "application/json",
        }

        data = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            **kwargs
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data
            )
            response.raise_for_status()
            result = response.json()

            return {
                "content": result["choices"][0]["message"]["content"],
                "model": result["model"],
                "usage": result.get("usage", {}),
                "provider": "openai",
            }

    async def call_anthropic(
        self,
        message: str,
        model: str = "claude-3-sonnet-20240229",
        max_tokens: int = 2000,
        temperature: float = 0.7,
        **kwargs
    ) -> Dict[str, Any]:
        """Call Anthropic Claude API."""
        if not self.anthropic_key:
            raise ValueError("Anthropic API key not configured")

        headers = {
            "x-api-key": self.anthropic_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01",
        }

        data = {
            "model": model,
            "max_tokens": max_tokens,
            "messages": [
                {"role": "user", "content": message}
            ],
            "temperature": temperature,
            **kwargs
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=data
            )
            response.raise_for_status()
            result = response.json()

            return {
                "content": result["content"][0]["text"],
                "model": result["model"],
                "usage": result.get("usage", {}),
                "provider": "anthropic",
            }

    async def call_model(
        self,
        prompt: str,
        provider: str = "anthropic",
        **kwargs
    ) -> str:
        """Convenient method to call any AI model."""
        if provider == "openai":
            messages = [{"role": "user", "content": prompt}]
            result = await self.call_openai(messages, **kwargs)
        else:
            result = await self.call_anthropic(prompt, **kwargs)

        return result["content"]

    async def estimate_cost(
        self,
        provider: str,
        model: str,
        input_tokens: int,
        output_tokens: int
    ) -> float:
        """Estimate API cost in USD."""
        # Pricing as of 2024 (approximate)
        pricing = {
            "openai": {
                "gpt-4": {"input": 0.00003, "output": 0.00006},
                "gpt-3.5-turbo": {"input": 0.0000015, "output": 0.000002},
            },
            "anthropic": {
                "claude-3-opus-20240229": {"input": 0.000015, "output": 0.000075},
                "claude-3-sonnet-20240229": {"input": 0.000003, "output": 0.000015},
            }
        }

        if provider not in pricing or model not in pricing[provider]:
            return 0.0

        rates = pricing[provider][model]
        input_cost = input_tokens * rates["input"] / 1000
        output_cost = output_tokens * rates["output"] / 1000

        return input_cost + output_cost
