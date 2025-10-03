import os
from typing import List, Optional

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI


class AIGenerator:
    """Handles interactions with Perplexity for generating responses."""

    SYSTEM_PROMPT = (
        "You are an AI assistant specialized in course materials and educational"
        " content with access to a comprehensive search tool for course information.\n\n"
        "Search Tool Usage:\n"
        "- Use the search tool **only** for questions about specific course content"
        " or detailed educational materials\n"
        "- **One search per query maximum**\n"
        "- Synthesize search results into accurate, fact-based responses\n"
        "- If search yields no results, state this clearly without offering alternatives\n\n"
        "Response Protocol:\n"
        "- **General knowledge questions**: Answer using existing knowledge without searching\n"
        "- **Course-specific questions**: Search first, then answer\n"
        "- **No meta-commentary**:\n"
        "  - Provide direct answers only — no reasoning process, search explanations, or"
        " question-type analysis\n"
        '  - Do not mention "based on the search results"\n\n'
        "All responses must be:\n"
        "1. **Brief, Concise and focused** - Get to the point quickly\n"
        "2. **Educational** - Maintain instructional value\n"
        "3. **Clear** - Use accessible language\n"
        "4. **Example-supported** - Include relevant examples when they aid understanding\n"
        "Provide only the direct answer to what was asked."
    )

    def __init__(self, model: str = "llama-3.1-sonar-hybrid"):
        self.model = model
        api_key = os.getenv("PERPLEXITY_API_KEY") or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "PERPLEXITY_API_KEY or OPENAI_API_KEY environment variable is required"
            )

        self.llm = ChatOpenAI(
            model=self.model,
            temperature=0,
            api_key=api_key,
            base_url="https://api.perplexity.ai",
        )

    def generate_response(
        self,
        query: str,
        conversation_history: Optional[str] = None,
        tools: Optional[List] = None,
        tool_manager=None,
    ) -> str:
        """Generate an AI response with optional tool usage and context."""

        messages = [SystemMessage(content=self.SYSTEM_PROMPT)]
        if conversation_history:
            messages.append(
                HumanMessage(content=f"Previous conversation:\n{conversation_history}")
            )

        messages.append(HumanMessage(content=query))

        response = (
            self.llm.bind_tools(tools).invoke(messages)
            if tools
            else self.llm.invoke(messages)
        )

        if hasattr(response, "tool_calls") and response.tool_calls and tool_manager:
            tool_results = []
            for tool_call in response.tool_calls:
                if isinstance(tool_call, dict):
                    tool_name = tool_call.get("name")
                    tool_args = tool_call.get("args", {})
                    call_id = tool_call.get("id", "")
                else:
                    tool_name = getattr(tool_call, "name", None)
                    tool_args = getattr(tool_call, "args", {}) or {}
                    call_id = getattr(tool_call, "id", "")

                if not tool_name:
                    continue

                tool_result = tool_manager.execute_tool(tool_name, **tool_args)
                tool_results.append(
                    {
                        "tool_call_id": call_id,
                        "name": tool_name,
                        "content": tool_result,
                    }
                )

            messages.append(response)
            for tool_result in tool_results:
                messages.append(
                    AIMessage(
                        content=str(tool_result["content"]),
                        tool_call_id=tool_result["tool_call_id"],
                    )
                )

            final_response = self.llm.invoke(messages)
            return getattr(final_response, "content", final_response)

        return getattr(response, "content", response)
