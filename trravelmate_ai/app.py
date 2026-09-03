"""
TravelMate AI
An AI-powered, domain-specific tourism chatbot built with Streamlit + LangChain + OpenAI.
"""

import streamlit as st
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# ---------------------------------------------------------------------------
# Environment setup
# ---------------------------------------------------------------------------

load_dotenv(find_dotenv(), override=True)

st.set_page_config(
    page_title="TravelMate AI",
    page_icon="🌊",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Theme (Coastal Adventure — Fresh & Organic)
# ---------------------------------------------------------------------------

PRIMARY_WHITE = "#FFFFFF"
DEEP_NAVY = "#17324D"
OCEAN_TEAL = "#167D8D"
WARM_SAND = "#E8B45B"

CUSTOM_CSS = f"""
<style>
    .stApp {{
        background-color: #EFF7F5;
    }}

    h1, h2, h3 {{
        color: {DEEP_NAVY} !important;
    }}

    section[data-testid="stSidebar"] {{
        background-color: #EAF3F2;
        border-right: 1px solid #D4E5E3;
    }}

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {{
        color: {DEEP_NAVY} !important;
    }}

    .stButton > button {{
        background-color: {OCEAN_TEAL};
        color: {PRIMARY_WHITE};
        border: 1px solid {OCEAN_TEAL};
        border-radius: 8px;
        font-weight: 600;
    }}

    .stButton > button:hover {{
        background-color: {DEEP_NAVY};
        border-color: {DEEP_NAVY};
        color: {PRIMARY_WHITE};
    }}

    div[data-testid="stChatInput"] {{
        border-top: 2px solid {OCEAN_TEAL};
    }}

    .stCaption, [data-testid="stCaptionContainer"] {{
        color: {OCEAN_TEAL};
    }}

    .travel-card {{
        background: {PRIMARY_WHITE};
        border: 1px solid #D4E5E3;
        border-top: 5px solid {WARM_SAND};
        border-radius: 8px;
        padding: 1rem 1rem 0.85rem;
        min-height: 132px;
        box-shadow: 0 5px 16px rgba(23, 50, 77, 0.08);
    }}

    .travel-card-icon {{
        color: {OCEAN_TEAL};
        font-size: 1.45rem;
        line-height: 1;
    }}

    .travel-card-title {{
        color: {DEEP_NAVY};
        font-weight: 700;
        margin: 0.4rem 0 0.2rem;
    }}

    .travel-card-copy {{
        color: {DEEP_NAVY};
        font-size: 0.88rem;
        line-height: 1.35;
    }}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# System prompt — enforces the tourism-only domain restriction
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """
You are TravelMate AI, a specialized AI assistant for tourism and travel planning.

Your ONLY purpose is to help users with travel and tourism-related questions.

You can help with:
- Travel planning
- Destinations
- Personalized itineraries
- Travel budgets
- Trip duration
- Tourist attractions
- Activities
- Hotels and accommodation
- Transportation
- Travel routes
- Packing suggestions
- Travel tips
- Tourist seasons
- Cultural experiences
- Eco-tourism
- Adventure tourism
- Family trips
- Solo trips
- Couple trips
- Food recommendations when related to travel

You should create personalized itineraries when users provide information such as:
destination, budget, duration, interests, number of travelers, and travel style.

IMPORTANT DOMAIN RULE:

If a user's question is unrelated to travel or tourism, DO NOT answer it.

Respond exactly with:

"This question is out of scope. TravelMate AI is designed specifically to help with travel and tourism-related questions."

Do not provide an answer to an unrelated question.

If a question is ambiguous but could reasonably be related to travel, interpret it in a travel context when possible.

When creating itineraries, organize them by day and include:
- Places to visit
- Suggested activities
- Approximate timing
- Transportation suggestions
- Food suggestions where relevant
- Budget considerations

Do not claim that information is real-time unless it has actually been retrieved from a real-time source.

Be transparent when information may have changed.

Always provide practical and useful travel guidance.
"""

MODEL_NAME = "gpt-4o-mini"


# ---------------------------------------------------------------------------
# Core helper functions
# ---------------------------------------------------------------------------

def validate_api_key(api_key: str) -> bool:
    """Validate the OpenAI API key by making a small test request."""

    if not api_key:
        return False

    try:
        test_chat = ChatOpenAI(
            model=MODEL_NAME,
            temperature=0,
            api_key=api_key,
        )

        test_chat.invoke("Reply with OK.")

        return True

    except Exception:
        return False


def initialize_chat(api_key: str) -> ChatOpenAI:
    """Create the ChatOpenAI model instance using the user's API key."""

    return ChatOpenAI(
        model=MODEL_NAME,
        temperature=0.5,
        api_key=api_key,
    )


def initialize_session_state():
    """Initialize all Streamlit session state variables used by the app."""

    if "api_key" not in st.session_state:
        st.session_state.api_key = None

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if "messages" not in st.session_state:
        st.session_state.messages = []


# ---------------------------------------------------------------------------
# Stage 1 — API key screen
# ---------------------------------------------------------------------------

def show_api_key_screen():
    """Display the initial API key setup screen."""

    st.markdown(
        f"<h1 style='text-align:center;'>🌊 TravelMate AI</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<p style='text-align:center; color:{OCEAN_TEAL}; "
        f"font-size:1.1rem;'>Your AI-powered travel and tourism assistant</p>",
        unsafe_allow_html=True,
    )

    st.write("")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.write("Enter your OpenAI API key to continue to TravelMate AI.")

        api_key = st.text_input(
            "Enter your OpenAI API Key",
            type="password",
            placeholder="sk-...",
        )

        if st.button("Continue", type="primary", use_container_width=True):

            if not api_key:
                st.error("Please enter your OpenAI API key.")
                return

            with st.spinner("Checking API key..."):

                if validate_api_key(api_key):
                    st.session_state.api_key = api_key
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error(
                        "Invalid API key. Please check your API key and try again."
                    )


# ---------------------------------------------------------------------------
# Stage 2 — Chatbot interface
# ---------------------------------------------------------------------------

def display_chat_history():
    """Render previous user and assistant messages (system messages hidden)."""

    for message in st.session_state.messages:

        if isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.write(message.content)

        elif isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.write(message.content)


def build_preferences_context() -> str:
    """Turn any sidebar travel-preference inputs into extra context for the model."""

    prefs = st.session_state.get("trip_prefs", {})
    parts = []

    if prefs.get("destination"):
        parts.append(f"Destination: {prefs['destination']}")
    if prefs.get("budget"):
        parts.append(f"Budget: PKR {prefs['budget']}")
    if prefs.get("duration"):
        parts.append(f"Trip duration: {prefs['duration']} day(s)")
    if prefs.get("interests"):
        parts.append(f"Interests: {prefs['interests']}")

    if not parts:
        return ""

    return "Known traveler preferences (use if relevant): " + "; ".join(parts)


def show_chatbot():
    """Render the main ChatGPT-style chatbot interface."""

    st.title("🌊 TravelMate AI")
    st.caption("Your personalized AI travel and tourism assistant")

    card_rows = [
        st.columns(3),
        st.columns(3),
    ]
    cards = [
        ("🗺️", "Build an itinerary", "Plan a day-by-day trip around your interests."),
        ("💰", "Plan your budget", "Find experiences that fit your travel budget."),
        ("🎒", "Get travel tips", "Discover packing ideas, routes, and local advice."),
        ("🏨", "Find accommodation", "Compare stay ideas for your destination and style."),
        ("🚆", "Explore transport", "Choose practical ways to get around with ease."),
        ("☀️", "Pick the best season", "Find the ideal time to visit your destination."),
    ]

    for row_index, card_columns in enumerate(card_rows):
        for column, (icon, title, copy) in zip(
            card_columns, cards[row_index * 3:(row_index + 1) * 3]
        ):
            with column:
                st.markdown(
                    f"<div class='travel-card'>"
                    f"<div class='travel-card-icon'>{icon}</div>"
                    f"<div class='travel-card-title'>{title}</div>"
                    f"<div class='travel-card-copy'>{copy}</div>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

        st.write("")

    st.write("")

    chat = initialize_chat(st.session_state.api_key)

    display_chat_history()

    user_prompt = st.chat_input("Ask TravelMate AI about your next trip...")

    if user_prompt:

        st.session_state.messages.append(HumanMessage(content=user_prompt))

        with st.chat_message("user"):
            st.write(user_prompt)

        messages_for_model = [SystemMessage(content=SYSTEM_PROMPT)]

        preferences_context = build_preferences_context()
        if preferences_context:
            messages_for_model.append(SystemMessage(content=preferences_context))

        messages_for_model.extend(st.session_state.messages)

        with st.chat_message("assistant"):

            with st.spinner("Planning your trip..."):

                try:
                    response = chat.invoke(messages_for_model)
                    response_text = response.content

                    st.write(response_text)

                    st.session_state.messages.append(
                        AIMessage(content=response_text)
                    )

                except Exception:
                    st.error(
                        "Something went wrong while generating your travel "
                        "recommendation. Please try again."
                    )


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

def show_sidebar():
    """Render the sidebar with travel preferences and session controls."""

    with st.sidebar:
        st.header("🌊 TravelMate AI")
        st.subheader("Travel Preferences")

        if "trip_prefs" not in st.session_state:
            st.session_state.trip_prefs = {
                "destination": "",
                "budget": 0,
                "duration": 1,
                "interests": "",
            }

        st.session_state.trip_prefs["destination"] = st.text_input(
            "Destination",
            value=st.session_state.trip_prefs["destination"],
            placeholder="e.g. Hunza",
        )

        st.session_state.trip_prefs["budget"] = st.number_input(
            "Budget (PKR)",
            min_value=0,
            value=st.session_state.trip_prefs["budget"],
        )

        st.session_state.trip_prefs["duration"] = st.number_input(
            "Trip Duration (days)",
            min_value=1,
            value=st.session_state.trip_prefs["duration"],
        )

        st.session_state.trip_prefs["interests"] = st.text_input(
            "Interests",
            value=st.session_state.trip_prefs["interests"],
            placeholder="e.g. hiking, nature",
        )

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            if st.button("New Chat", use_container_width=True):
                st.session_state.messages = []
                st.rerun()

        with col2:
            if st.button("Clear Conversation", use_container_width=True):
                st.session_state.messages = []
                st.rerun()

        st.divider()
        st.caption("✅ API key validated for this session.")


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def main():

    initialize_session_state()

    if not st.session_state.authenticated:
        show_api_key_screen()
    else:
        show_sidebar()
        show_chatbot()


if __name__ == "__main__":
    main()
