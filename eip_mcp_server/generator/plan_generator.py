import os
import logging
from google import genai
from google.genai import types

logger = logging.getLogger("eip_mcp_server.generator")

class PlanGenerator:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required.")
        self.client = genai.Client(api_key=self.api_key)

    def generate_markdown_plan(self, system_prompt: str, context: str, model_name: str = "gemini-3.1-pro-preview") -> str:
        """
        Generates a comprehensive Markdown plan using the Gemini API.
        """
        try:
            logger.info(f"Generating plan using {model_name}...")
            response = self.client.models.generate_content(
                model=model_name,
                contents=context,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.2,
                    max_output_tokens=8192,
                ),
            )
            return response.text
        except Exception as e:
            logger.error(f"Failed to generate plan via API: {str(e)}. Falling back to STUB.")
            return f"# STUB Plan\n\nGeneration failed with error: {str(e)}\n\nThis is a fallback stub to ensure the pipeline continues."
