import requests
import json
from typing import Dict, Any, Generator
from flask import Response

DEEPSEEK_API_URL = "http://localhost:11434/api/generate"

class DeepseekService:
    def __init__(self):
        self.context = []
        self.max_context = 5

    def query_deepseek_stream(self, prompt: str) -> Generator[str, None, None]:
        """
        Streams the DeepSeek response with real-time cleaning of thinking process
        """
        try:
            context_prompt = self._build_context_prompt(prompt)
            payload = {
                "model": "deepseek-r1:7b",
                "prompt": context_prompt,
                "stream": True,
                "temperature": 0.7,
                "top_p": 0.9
            }

            with requests.post(DEEPSEEK_API_URL, json=payload, stream=True) as response:
                response.raise_for_status()
                buffer = ""
                thinking = True
                complete_response = ""

                for line in response.iter_lines():
                    if line:
                        data = json.loads(line.decode())
                        chunk = data.get('response', '')
                        
                        if thinking:
                            buffer += chunk
                            
                            # Check for different thinking patterns
                            if "</think>" in buffer:
                                thinking = False
                                clean_chunk = buffer.split("</think>")[-1]
                                clean_chunk = clean_chunk.replace("<think>", "").replace("</think>", "").strip()
                                
                            elif "Final response:" in buffer:
                                thinking = False
                                clean_chunk = buffer.split("Final response:")[-1].strip()
                                
                            elif buffer.strip().startswith("Think:") and "Final response:" in buffer:
                                thinking = False
                                clean_chunk = buffer.split("Final response:")[-1].strip()
                                
                            else:
                                # Still in thinking mode, continue collecting
                                continue
                                
                            # Process the clean chunk
                            if clean_chunk:
                                complete_response += clean_chunk
                                yield clean_chunk
                            buffer = ""
                        else:
                            # Even in non-thinking mode, clean any thinking patterns
                            clean_chunk = chunk
                            clean_chunk = clean_chunk.replace("<think>", "").replace("</think>", "")
                            clean_chunk = clean_chunk.replace("Think:", "").replace("Final response:", "")
                            
                            complete_response += clean_chunk
                            yield clean_chunk

                # Update context with complete response
                if complete_response:
                    self._update_context(prompt, complete_response.strip())

        except requests.Timeout:
            yield "I'm sorry, but I'm taking too long to respond. Please try again."
        except requests.RequestException as e:
            print(f"DeepSeek API error: {e}")
            yield "I apologize, but I'm having trouble connecting to my knowledge base."
        except Exception as e:
            print(f"Unexpected error: {e}")
            yield "I encountered an unexpected error. Please try again."

    def _build_context_prompt(self, new_prompt: str) -> str:
        """
        Builds a prompt with conversation context
        """
        context_str = "\n".join([
            f"User: {msg['user']}\nAssistant: {msg['assistant']}"
            for msg in self.context
        ])
        
        base_prompt = """You are Aurora, an empathetic mental health assistant. Follow these rules strictly:
1. Never provide medical diagnoses or treatment recommendations
2. Encourage professional help when appropriate
3. Use compassionate and supportive language
4. Respect user privacy and maintain confidentiality
5. Focus on emotional support and coping strategies
6. IMPORTANT: Always enclose your thinking process in <think></think> tags
7. After the think tags, provide ONLY your final response without any explanation
8. Keep responses concise and focused

Previous conversation:
{context}

User: {prompt}
Response:"""

        return base_prompt.format(context=context_str, prompt=new_prompt)

    def _update_context(self, user_msg: str, assistant_msg: str) -> None:
        """
        Updates conversation context, maintaining the maximum context length
        """
        self.context.append({
            "user": user_msg,
            "assistant": assistant_msg
        })
        
        if len(self.context) > self.max_context:
            self.context.pop(0)

deepseek_service = DeepseekService()