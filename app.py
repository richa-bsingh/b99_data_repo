# src/app.py

import streamlit as st
from src.rag_chain import answer
from src.game import run_heist_game
import random

# Set page configuration with B99 theme
st.set_page_config(
    page_title="99th Precinct",
    page_icon="🚔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Brooklyn 99 theming
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    .main {
        background-color: #f0f2f6;
        background-image: url('https://via.placeholder.com/100x100.png?text=99');
        background-repeat: repeat;
        background-opacity: 0.1;
    }
    .css-18e3th9 {
        padding-top: 1rem;
    }
    .stTitle {
        color: #00008B;
        font-family: 'Arial Black', Gadget, sans-serif;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        border-bottom: 3px solid #FF9800;
        padding-bottom: 10px;
    }
    .stButton>button {
        background-color: #00008B;
        color: white;
        font-weight: bold;
        border-radius: 4px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #FF9800;
        transform: scale(1.05);
    }
    .stSidebar {
        background-color: #00008B;
        border-right: 3px solid #FF9800;
    }
    .css-1d391kg {
        background-color: #00008B;
    }
    .sidebar-content {
        color: white;
        font-family: 'Roboto', sans-serif;
    }
    .quote-box {
        padding: 15px;
        border-radius: 5px;
        background-color: #00008B;
        margin: 10px 0px;
        color: white;
        border-left: 5px solid #FF9800;
        font-style: italic;
    }
    .stTextInput>div>div>input {
        border: 2px solid #00008B;
        border-radius: 4px;
    }
    .stSuccess {
        background-color: #424242;
        color: white;
        border-left: 5px solid #FF9800;
    }
    .stWarning {
        background-color: #FF9800;
        color: white;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# B99 quotes for random display
b99_quotes = [
    "'Cool, cool, cool, cool.' - Jake Peralta",
    "'I'm the human form of the 💯 emoji.' - Gina Linetti",
    "'BONE?!?!' - Captain Holt",
    "'Title of your sex tape.' - Jake Peralta",
    "'Hot damn!' - Captain Holt",
    "'Yippie kayak, other buckets!' - Charles Boyle",
    "'I'm playing Kwazy Cupcakes… I've got my own party going on.' - Rosa Diaz",
    "'The English language cannot fully capture the depth…' - Captain Holt",
    "'Terry loves yogurt!' - Terry Jeffords",
    "'NINE‑NINE!' - Everyone"
]

# Sidebar customization
with st.sidebar:
    st.image("b99-1.png", width=300)
    st.markdown('<div class="sidebar-content"><h2>99th Precinct</h2></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center; margin-bottom:20px;">
        <div style="background-color:#FF9800; color:#00008B; padding:5px 15px; border-radius:50%; 
                    display:inline-block; font-weight:bold; font-size:24px; margin:10px;">
            99
        </div>
        <div style="font-size:12px; color:white;">BROOKLYN PRECINCT</div>
    </div>
    """, unsafe_allow_html=True)
    mode = st.radio(
        "Choose Your Mode",
        ["👮 Ask 99 Assistant", "🔍 Heist Game", "🏆 Character Quiz"],
        key="sidebar_mode"
    )
    st.markdown(
        '<div class="quote-box">' + random.choice(b99_quotes) + '</div>',
        unsafe_allow_html=True
    )

# Main content
if mode == "👮 Ask 99 Assistant":
    st.title("🕵🏽‍♀️ 99th Precinct Detective Assistant")
    st.subheader("What case do you need help with, detective?")
    q = st.text_input("Your question:", key="assistant_question")
    if st.button("Investigate", key="assistant_investigate"):
        if q:
            with st.spinner("Captain Holt is analyzing your case..."):
                resp = answer(q)
            st.success(f"**99 Assistant:** {resp}")
            if "cool" in q.lower():
                st.markdown("![Cool](https://via.placeholder.com/400x200.png?text=Cool+Cool+Cool+Cool)")
            elif "99" in q:
                st.balloons()
                st.markdown("NINE‑NINE!")
        else:
            st.warning("Please enter a question, detective.", key="assistant_warn")

elif mode == "🔍 Heist Game":
    st.title("💰 Annual Halloween Heist")
    st.subheader("Can you unmask the culprit of the missing diamond?")
    st.image("2.png", width=700, caption="The Annual Precinct Heist")
    # Directly enter the heist flow; run_heist_game() handles its own buttons
    with st.spinner("Assembling case files..."):
        run_heist_game()

elif mode == "🏆 Character Quiz":
    st.title("📺 Which B99 Character Are You?")
    st.subheader("Answer these questions to find out which detective you most resemble")
    # Quiz code...
    q1 = st.radio(
        "🔎 What's your approach to solving cases?",
        [
            "Wing it with style and jokes",
            "Follow procedure precisely and document everything",
            "Intimidate suspects until they confess",
            "Use obscure knowledge and enthusiastic support",
            "POWER POSE and protect your team!"
        ],
        key="quiz_q1"
    )
    q2 = st.radio(
        "🍩 Pick your stakeout snack:",
        [
            "Gummy bears and orange soda",
            "Nothing, food is fuel",
            "Black coffee, no sugar",
            "Yogurt",
            "Something homemade with exotic ingredients"
        ],
        key="quiz_q2"
    )
    q3 = st.radio(
        "🗣️ What's your catchphrase style?",
        [
            "Witty and pop-culture related",
            "Formal, precise and deadpan",
            "Short, intimidating and mysterious",
            "Enthusiastic and passionate",
            "Quirky, misunderstood and overly detailed"
        ],
        key="quiz_q3"
    )

    if st.button("Analyze Detective Profile", key="quiz_analyze"):
        results = {name: 0 for name in [
            "Jake Peralta", "Captain Holt", "Rosa Diaz",
            "Terry Jeffords", "Charles Boyle", "Amy Santiago"
        ]}
        # Scoring logic...
        if "Wing" in q1: results["Jake Peralta"] += 2
        elif "procedur" in q1: results["Amy Santiago"] += 2
        elif "Intimidate" in q1: results["Rosa Diaz"] += 2
        elif "obscure" in q1: results["Charles Boyle"] += 2
        elif "POWER" in q1: results["Terry Jeffords"] += 2

        if "Gummy" in q2: results["Jake Peralta"] += 2
        elif "Nothing" in q2: results["Captain Holt"] += 2
        elif "Black coffee" in q2: results["Rosa Diaz"] += 2
        elif "Yogurt" in q2: results["Terry Jeffords"] += 2
        elif "homemade" in q2: results["Charles Boyle"] += 2

        if "pop-culture" in q3: results["Jake Peralta"] += 2
        elif "deadpan" in q3: results["Captain Holt"] += 2
        elif "intimidating" in q3: results["Rosa Diaz"] += 2
        elif "passionate" in q3: results["Terry Jeffords"] += 2
        elif "Quirky" in q3: results["Charles Boyle"] += 2

        character = max(results, key=results.get)
        descriptions = {
            "Jake Peralta": "You're Jake! Chaotic, clever, and full of Die Hard references. Cool, cool, cool, cool!",
            "Captain Holt": "You're Holt! Stoic, by-the-book, but with a heart of gold beneath that deadpan exterior.",
            "Rosa Diaz": "You're Rosa! Tough, mysterious, and secretly a softie for certain people you’d never admit.",
            "Terry Jeffords": "You're Terry! Big muscles, big heart, and a yogurt connoisseur extraordinaire.",
            "Charles Boyle": "You're Charles! Loyal, enthusiastic about obscure foods, and the precinct’s biggest cheerleader.",
            "Amy Santiago": "You're Amy! Ultra‐organized, competitive, and in love with binders and spreadsheets."
        }
        st.markdown(f"<h2 style='color:#ADD8E6;'>{character}</h2>", unsafe_allow_html=True)
        st.write(descriptions[character])
        st.markdown("""
        <div style="text-align:center; margin-top:20px;">
            <div style="color:#ADD8E6; font-weight:bold; font-size:20px;">
                NINE‑NINE!
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.balloons()

# Footer
st.markdown("---")
st.markdown("Nine‑Nine! Made with Streamlit")
