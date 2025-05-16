import os
from openai import OpenAI # type: ignore
from google import genai

class OpenAIService:
    def __init__(self, config):
        """
        Initialize the OpenAIService with the API key from environment variables.
        """
        self.config = config
        self.api_key = config["openai_api_key"]
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set.")

    def generate_response(self, prompt, instructions):
        """
        Generate a response using OpenAI's GPT model.

        :param prompt: The input prompt for the model.
        :return: The generated response text.
        """
        # client = OpenAI(api_key=self.api_key)

        # response = client.responses.create(
        #     model="gpt-4o",
        #     instructions=instructions,
        #     input=prompt,
        # )

        # # Log the generated response
        # print(f"Generated response: {response.output_text}")
        # return response.output_text

        client = genai.Client(api_key=self.config["gemini_api_key"])

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"{instructions} CONTENT: {prompt}",
        )

        print(f"Generated response: {response.text}")
        return response.text


    def generate_web_search_response(self, prompt):
        """
        Generate a response using OpenAI's GPT model with web search capabilities.

        :param prompt: The input prompt for the model.
        :return: The generated response text.
        """
        client = OpenAI(api_key=self.api_key)

        response = client.responses.create(
            model="gpt-4.1",
            tools=[{"type": "web_search_preview"}],
            input=prompt
        )

        # Log the generated response
        print(f"Generated response: {response.output_text}")
        return response.output_text