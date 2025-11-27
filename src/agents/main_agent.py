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

def get_agent(gemini_api_key, tavily_api_key):
    
    # 1. Initialize LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        temperature=0.6, # Slightly higher creativity for itineraries
        google_api_key=gemini_api_key
    )

    # 2. Define Tools
    search_tool = TavilySearchResults(max_results=3, tavily_api_key=tavily_api_key)
    
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

    # 3. Define the System Prompt (STRICTER INSTRUCTIONS)
    prompt = ChatPromptTemplate.from_messages([
        ("system", 
         """You are RoutePilot_AI, an elite travel planner.
         
         CORE INSTRUCTION:
         Your goal is to provide a COMPLETE TRAVEL PLAN. A plan is not complete without a Day-by-Day Itinerary.
         
         EXECUTION FLOW (Follow this order):
         1. **Visuals:** Call 'generate_trip_map' if cities are known.
         2. **Data:** Check 'get_current_weather' and 'calculate_distance'.
         3. **Planning (CRITICAL):** Generate a detailed Day-by-Day Itinerary (Morning/Afternoon/Evening) based on the user's Travel Style.
         4. **Budget:** Estimate costs using 'estimate_local_costs' or your own knowledge for flights.
         
         FORMATTING RULES:
         - Start with "🌍 **Trip Overview**" (Map link, Weather, Distance).
         - Then "📅 **Daily Itinerary**" (This is the most important part).
         - End with "💰 **Estimated Budget**".
         
         If a tool fails (like weather), IGNORE the error and proceed with the Itinerary anyway.
         """),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    # 4. Create Agent & Executor
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

    return agent_executor