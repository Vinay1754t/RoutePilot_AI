# ✈️ RoutePilot_AI: Your Intelligent Travel Agent

**RoutePilot_AI** is a next-generation travel planning assistant powered by **Agentic AI**. Unlike standard chatbots, RoutePilot doesn't just "talk" — it **thinks, plans, and executes**.

It utilizes **LangChain** and **Google Gemini 1.5 Flash** to autonomously use tools for live weather checking, currency conversion, distance calculation, and visual travel mapping.

![RoutePilot Interface](app_preview.png)

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

* **LLM:** Google Gemini 1.5 Flash (via `langchain-google-genai`)
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
    git clone [https://github.com/vinay1754t/RoutePilot_AI.git](https://github.com/vinay1754t/RoutePilot_AI.git)
    cd RoutePilot_AI
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
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

## 🤖 How It Works (The Agentic Loop)

1.  **User Input:** "Plan a trip from Frankfurt to Manali."
2.  **Thought Process:** The Agent breaks this down -> *Get coords -> Calc distance -> Check weather -> Search hotels -> Make map*.
3.  **Tool Execution:** It calls Python functions (`get_coordinates`, `generate_trip_map`, etc.) sequentially.
4.  **Final Response:** Synthesizes data into a structured itinerary with a UI map and PDF download option.

---

## 🙌 Acknowledgments

* **Google GenAI** for the Gemini Model.
* **LangChain** for the Agent framework.
* **Streamlit** for the amazing Python-native UI.
