# ✈️ RoutePilot_AI: Agentic Travel Planner

**RoutePilot_AI** is a next-generation travel planning assistant powered by **Agentic AI**. Unlike standard chatbots, RoutePilot doesn't just "talk" — it **thinks, plans, and executes**.

It utilizes **LangChain** and **Google Gemini 2.5 Flash** to autonomously use tools for live weather checking, currency conversion, distance calculation, and visual travel mapping.

![RoutePilot Interface](app_preview.png)

### 📄 Sample Output
[Click here to view a generated Trip PDF](file:///C:/Users/Vinay%20Wankhade/OneDrive/Desktop/RoutePilot_Ai/RoutePilot_Itinerary.pdf)

---

## 🌟 Key Features

* **🧠 Visual Intelligence:** Upload a photo of any location (landmark, food, scenery), and the Agent identifies it and plans a trip there.
* **🗺️ Interactive Mapping:** Automatically generates and renders route maps between cities.
* **🌤️ Real-Time Data:** Fetches live weather updates and real-time currency exchange rates.
* **📄 PDF Itineraries:** Generates downloadable, formatted PDF travel plans.
* **🎒 Persona-Based Planning:** Adjusts itineraries based on travel style (Budget, Luxury, Adventure).
* **💾 Context Awareness:** Remembers your conversation history for seamless adjustments.

---

## 🛠️ Tech Stack & Architecture

* **LLM:** Google Gemini 2.5 Flash (via `langchain-google-genai`)
* **Orchestration:** LangChain (Agents & Tool Calling)
* **Frontend:** Streamlit
* **Tools:** * `Tavily Search API` (Web Browsing)
    * `OpenWeatherMap API` (Live Weather)
    * `ExchangeRate API` (Currency)
    * `Geopy` & `Folium` (Geospatial logic & Mapping)
    * `FPDF` (Report Generation)

---

## 🚀 Setup Instructions

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/Vinay1754t/RoutePilot_AI.git](https://github.com/Vinay1754t/RoutePilot_AI.git)
    cd RoutePilot_AI
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  
    On Windows use: venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Application**
    ```bash
    streamlit run app.py
    ```

5.  **Enter API Keys**
    * Launch the app and look at the Sidebar.
    * Enter your **Gemini**, **Tavily**, **OpenWeather**, and **ExchangeRate** API keys to activate the Agent's tools.

---

## 📂 Project Structure

```bash
RoutePilot_AI/
├── src/
│   ├── agents/
│   │   └── main_agent.py    # The Brain: Agent definition and prompt logic
│   └── tools/
│       ├── geo_tools.py     # Distance & Coordinate logic
│       ├── map_tools.py     # Folium Map generation
│       ├── weather_tools.py # OpenWeather API wrapper
│       ├── budget_tools.py  # Mathematical estimation logic
│       └── currency_tools.py # Real-time exchange rates
│       └── report_tools.py  #PDF Generation
├── app.py                   # Main Streamlit Interface
├── requirements.txt         # Project dependencies
└── README.md                # Documentation