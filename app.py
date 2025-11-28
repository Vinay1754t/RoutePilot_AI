import streamlit as st
import os
import tempfile
import base64
import streamlit.components.v1 as components
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage

# --- IMPORT AGENT LOGIC ---
from src.agents.main_agent import get_agent

# --- PAGE CONFIG ---
st.set_page_config(page_title="RoutePilot_AI", page_icon="✈️", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stChatFloatingInputContainer {bottom: 20px;}
    .sidebar .sidebar-content {background-image: linear-gradient(#2e7bcf,#2e7bcf);}
    h1 {color: #2e7bcf;}
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3125/3125848.png", width=80)
    st.title("RoutePilot_AI 🌍")
    
    st.markdown("### 🔑 API Keys")
    gemini_key = st.text_input("Gemini API Key", type="password")
    tavily_key = st.text_input("Tavily API Key", type="password")
    openai_weather_key = st.text_input("OpenWeatherMap Key", type="password")
    exchangerate_key = st.text_input("ExchangeRate API Key", type="password")
    
    st.divider()
    
    st.markdown("### 📸 Visual Intelligence")
    uploaded_file = st.file_uploader("Upload location photo", type=["jpg", "png", "jpeg"])

    st.divider()
    
    st.markdown("### ⚙️ Preferences")
    travel_style = st.selectbox("Style", ["Budget Backpacker", "Luxury/Comfort", "Adventure/Nature"])
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# --- MAIN APP ---
st.title("✈️ RoutePilot_AI: Agentic Travel Planner")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- AGENT EXECUTION ---
if gemini_key and tavily_key:
    # SET ENV VARS GLOBALLY (Fixes Validation Errors)
    os.environ["GOOGLE_API_KEY"] = gemini_key
    os.environ["TAVILY_API_KEY"] = tavily_key
    if openai_weather_key: os.environ["OPENWEATHER_API_KEY"] = openai_weather_key
    if exchangerate_key: os.environ["EXCHANGERATE_API_KEY"] = exchangerate_key

    # Initialize Agent (No keys passed, it uses os.environ)
    agent_executor = get_agent()
    
    user_input = st.chat_input("Where to next?")

    if user_input:
        # 1. CLEANUP
        map_path = os.path.join(tempfile.gettempdir(), "map_route.html")
        pdf_path = os.path.join(tempfile.gettempdir(), "itinerary.pdf")
        if os.path.exists(map_path): os.remove(map_path)
        if os.path.exists(pdf_path): os.remove(pdf_path)

        # 2. Add User Message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # 3. MEMORY
        chat_history = []
        for msg in st.session_state.messages[:-1]:
            if msg["role"] == "user":
                chat_history.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                chat_history.append(AIMessage(content=msg["content"]))

        # 4. VISION LOGIC
        image_description = ""
        if uploaded_file:
            vision_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=gemini_key)
            with st.spinner("Analyzing image..."):
                bytes_data = uploaded_file.getvalue()
                image_data = base64.b64encode(bytes_data).decode('utf-8')
                mime_type = uploaded_file.type
                image_url_str = f"data:{mime_type};base64,{image_data}"

                vision_msg = HumanMessage(content=[
                    {"type": "text", "text": "Describe this image in detail. If it is a landmark, name it. If it is food, identify it and guess its origin country."},
                    {"type": "image_url", "image_url": image_url_str} 
                ])
                try:
                    vision_response = vision_llm.invoke([vision_msg])
                    image_description = vision_response.content
                    with st.expander("📸 Image Analysis"):
                        st.write(image_description)
                except Exception as e:
                    st.error(f"Vision Error: {e}")

        # 5. AGENT LOGIC
        with st.chat_message("assistant"):
            with st.status("🤖 RoutePilot is working...", expanded=True) as status:
                st.write("🌎 Accessing Tools (Search, Geo, Budget)...")
                
                if image_description:
                    final_prompt = (
                        f"SYSTEM NOTE: The user has uploaded an image. Vision Analysis: '{image_description}'.\n"
                        f"USER REQUEST: {user_input}\n"
                        "INSTRUCTION: Use the image analysis to answer. Do NOT complain that you cannot see the image."
                    )
                else:
                    final_prompt = f"User Request: {user_input}. Travel Style: {travel_style}."
                
                try:
                    response = agent_executor.invoke({
                        "input": final_prompt,
                        "chat_history": chat_history 
                    })
                    result = response["output"]
                    status.update(label="✅ Plan Ready!", state="complete", expanded=False)
                    
                    st.markdown(result)
                    st.session_state.messages.append({"role": "assistant", "content": result})
                    
                    if os.path.exists(map_path):
                        with open(map_path, 'r', encoding='utf-8') as f:
                            st.markdown("### 🗺️ Your Route Map")
                            components.html(f.read(), height=400)
                    
                    if os.path.exists(pdf_path):
                        with open(pdf_path, "rb") as pdf_file:
                            st.download_button("📥 Download Itinerary PDF", pdf_file, "RoutePilot_Itinerary.pdf", "application/pdf")
                            
                except Exception as e:
                    st.error(f"Agent Error: {e}")

else:
    st.warning("⚠️ Enter API Keys to start.")
