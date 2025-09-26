from langchain_community.chat_models.ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from typing import List, Optional

class AIGenerator:
    """Handles interactions with Ollama for generating responses"""
    
    SYSTEM_PROMPT = """ You are an AI assistant specialized in course materials and educational content with access to a comprehensive search tool for course information.

Search Tool Usage:
- Use the search tool **only** for questions about specific course content or detailed educational materials
- **One search per query maximum**
- Synthesize search results into accurate, fact-based responses
- If search yields no results, state this clearly without offering alternatives

Response Protocol:
- **General knowledge questions**: Answer using existing knowledge without searching
- **Course-specific questions**: Search first, then answer
- **No meta-commentary**:
 - Provide direct answers only — no reasoning process, search explanations, or question-type analysis
 - Do not mention "based on the search results"


All responses must be:
1. **Brief, Concise and focused** - Get to the point quickly
2. **Educational** - Maintain instructional value
3. **Clear** - Use accessible language
4. **Example-supported** - Include relevant examples when they aid understanding
Provide only the direct answer to what was asked.
"""
    
    def __init__(self, model: str):
        self.model = model
        self.llm = ChatOllama(model=self.model, temperature=0)
        
    def generate_response(self, query: str,
                         conversation_history: Optional[str] = None,
                         tools: Optional[List] = None,
                         tool_manager=None) -> str:
        """
        Generate AI response with optional tool usage and conversation context. 
        
        Args:
            query: The user's question or request
            conversation_history: Previous messages for context
            tools: Available tools the AI can use
            tool_manager: Manager to execute tools
            
        Returns:
            Generated response as string
        """
        
        messages = [SystemMessage(content=self.SYSTEM_PROMPT)]
        if conversation_history:
            messages.append(HumanMessage(content=f"Previous conversation:\n{conversation_history}"))

        messages.append(HumanMessage(content=query))

        if tools:
            self.llm_with_tools = self.llm.bind_tools(tools)
            response = self.llm_with_tools.invoke(messages)
        else:
            response = self.llm.invoke(messages)

        if response.tool_calls and tool_manager:
            tool_results = []
            for tool_call in response.tool_calls:
                tool_result = tool_manager.execute_tool(
                    tool_call["name"], 
                    **tool_call["args"]
                )
                tool_results.append(
                    {
                        "tool_call_id": tool_call["id"],
                        "name": tool_call["name"],
                        "content": tool_result,
                    }
                )
            
            messages.append(response)
            for tool_result in tool_results:
                messages.append(AIMessage(content=str(tool_result), tool_call_id=tool_result["tool_call_id"]))

            final_response = self.llm.invoke(messages)
            return final_response.content
        
        return response.content
