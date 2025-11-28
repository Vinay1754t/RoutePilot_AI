from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools.tavily_search import TavilySearchResults

# --- IMPORT TOOLS ---
from src.tools.geo_tools import get_coordinates, calculate_distance
from src.tools.budget_tools import estimate_local_costs
from src.tools.report_tools import generate_itinerary_pdf
from src.tools.weather_tools import get_current_weather
from src.tools.currency_tools import convert_currency
from src.tools.map_tools import generate_trip_map

def get_agent():
    """
    Constructs the Agent. 
    Note: We do NOT pass API keys here anymore. 
    They are read directly from os.environ for safety and Pydantic compatibility.
    """
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        temperature=0.6
    )


    search_tool = TavilySearchResults(max_results=3) 
    
    tools = [
        search_tool, 
        get_coordinates, 
        calculate_distance, 
        estimate_local_costs,
        generate_itinerary_pdf,
        get_current_weather,
        convert_currency,
        generate_trip_map 
    ]


    prompt = ChatPromptTemplate.from_messages([
        ("system", 
         """You are RoutePilot_AI, an elite travel planner.
         
         CORE INSTRUCTION:
         Your goal is to provide a COMPLETE TRAVEL PLAN. A plan is not complete without a Day-by-Day Itinerary.
         
         EXECUTION FLOW:
         1. **Visuals:** Call 'generate_trip_map' if cities are known.
         2. **Data:** Check 'get_current_weather' and 'calculate_distance'.
         3. **Planning:** Generate a detailed Day-by-Day Itinerary.
         4. **Budget:** Estimate costs.
         
         FORMATTING RULES:
         - Start with "🌍 **Trip Overview**".
         - Then "📅 **Daily Itinerary**".
         - End with "💰 **Estimated Budget**".
         """),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

    return agent_executor
