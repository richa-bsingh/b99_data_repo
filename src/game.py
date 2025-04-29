# src/game.py

import random
import streamlit as st
from langchain_openai import ChatOpenAI
from rag_chain import answer

# LLM for fallback clue generation
clue_llm = ChatOpenAI(model_name="gpt-4", temperature=0.8)

# Who could’ve done it?
SUSPECTS = [
    "Detective Diaz",
    "Sergeant Jeffords",
    "Captain Holt",
    "Amy Santiago",
    "Charles Boyle",
    "Gina Linetti"
]

def generate_ai_clue(suspect: str, is_guilty: bool) -> str:
    """
    Returns a guilt clue if is_guilty=True, else an alibi clue.
    """
    if is_guilty:
        prompt = (
            f"You’re Jake Peralta from Brooklyn Nine‑Nine. "
            f"Invent a brief forensic clue that IMPLICATES {suspect} "
            "in the precinct diamond heist. Stay in character."
        )
    else:
        prompt = (
            f"You’re Jake Peralta from Brooklyn Nine‑Nine. "
            f"Invent a brief alibi statement that EXONERATES {suspect}, "
            "showing why they couldn’t have stolen the diamond."
        )
    return clue_llm.predict(prompt).strip()

def run_heist_game():
    """Main diamond‑heist flow."""
    # ─── Initialize state ─────────
    if "game_step" not in st.session_state:
        st.session_state.game_step = 1
        st.session_state.game_clues = []
        st.session_state.game_thief = random.choice(SUSPECTS)

    step = st.session_state.game_step

    # ─── Step 1: Pick Suspect ─────
    if step == 1:
        st.write("### Who do you want to interrogate first?")
        suspect = st.selectbox(
            "Select a suspect", SUSPECTS, key="game_suspect_select"
        )
        if st.button("Interrogate", key="game_btn_interrogate"):
            st.session_state.game_chosen = suspect
            st.session_state.game_clues.append(f"Suspect: {suspect}")
            st.session_state.game_step = 2

    # ─── Step 2: Interrogate ──────
    elif step == 2:
        suspect = st.session_state.game_chosen
        st.write(f"### Interrogating **{suspect}**…")
        question = f"What does {suspect} say about missing evidence?"
        raw_clue = answer(question)

        # If RAG fails, generate LLM‑based clue
        if "transcript" in raw_clue.lower() or "sorry" in raw_clue.lower():
            is_guilty = (suspect == st.session_state.game_thief)
            ai_clue = generate_ai_clue(suspect, is_guilty)
            label = "Guilt" if is_guilty else "Alibi"
            st.info(f"⚠️ No direct quote found.\n**{label} clue:** {ai_clue}")
            st.session_state.game_clues.append(f"{label} clue: {ai_clue}")
        else:
            st.markdown(f"> {raw_clue}")
            st.session_state.game_clues.append(raw_clue)

        if st.button("Next Clue", key="game_btn_next"):
            st.session_state.game_step = 3

    # ─── Step 3: Accusation ───────
    elif step == 3:
        st.write("### Review your clues so far:")
        for i, c in enumerate(st.session_state.game_clues, start=1):
            st.write(f"{i}. {c}")

        accusation = st.selectbox(
            "Who is the real thief?", SUSPECTS, key="game_accuse_select"
        )
        if st.button("Accuse", key="game_btn_accuse"):
            if accusation == st.session_state.game_thief:
                st.success("🎉 Correct! You’ve unmasked the culprit and recovered the diamond.")
            else:
                st.error("🚨 Wrong! The real thief slipped away…")
        if st.button("Restart Heist", key="game_btn_restart"):
            for k in ["game_step","game_clues","game_thief","game_chosen"]:
                st.session_state.pop(k, None)
