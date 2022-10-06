from typing import List, Union
from numpy import str0
import regex
import streamlit as st
import re
from PIL import Image
import os
from treys import Card, Evaluator, Deck
import collections


@st.experimental_singleton
def draw_deck() -> List[Union[int, str]]:
    """
    :returns: a list of cards and their respective values in a list of lists (based on the treys library)
    """
    return [[c, Card.int_to_pretty_str(c).replace("[", "").replace("]", "")] for c in Deck().cards]

def get_board_values(board):
    return [c[0] for c in draw_deck() if c[1] in board]

def clean_deck(cards) -> str:
    """
    the purpose of this function is to clean the names of the cards from int/symbol to the .png file names in ./cards/ folder
    """
    card =  f"{cards[0].replace('T', '10').replace('A', 'ace').replace('Q', 'queen').replace('K', 'king').replace('J', 'jack')}_of_{cards[1].replace('♥','hearts').replace('♦', 'diamonds').replace('♠','spades').replace('♣', 'clubs')}"
    try:
        return card
    except FileNotFoundError:
        return card + '2'

def open_image(card_string) -> str: 
    """Depending on what the select option says, serve a different image"""
    if card_string != "Select":
        return f"https://github.com/majoralex/streamlit/blob/main/poker_app/cards/{clean_deck(card_string)}.png?raw=true"
    else:
        return f"https://github.com/majoralex/streamlit/blob/main/poker_app/cards/default.jpg?raw=true"


def main():
    "Run the App"
    st.set_page_config(
        page_title="Pokerhand Evaluator",
        page_icon="🃏",
        initial_sidebar_state="expanded",
    )
    st.title("🃏 Pokerhand Evaluator")

    cards = draw_deck()
    card_labels = [str("Select"), *[c[1] for c in cards]]

    col1, col2, col3, col4 = st.columns(4)
    playercard1 = col1.selectbox("Card #1", options=card_labels, key="player_card_1")
    playercard2 = col2.selectbox("Card #2", options=card_labels, key="player_card_2")
    hand = [playercard1, playercard2] # create a list for each card in your hand

    col3.image(open_image(card_string=playercard1))
    col4.image(open_image(card_string=playercard2))

    st.markdown("***")
    col1, col2, col3 = st.columns((4, 1, 1))

    col1.subheader("Flop")
    
    if playercard1 != "Select" and playercard2 != "Select":
        col2.subheader("Turn")
        col3.subheader("River")


    col1, col2, col3, col4, col5 = st.columns(5)

    flop1 = col1.selectbox("Card #1", options=card_labels, key="card_1")
    if flop1:
        col1.image(open_image(card_string=flop1))

    flop2 = col2.selectbox("Card #2", options=card_labels, key="card_2")

    if flop2:
        col2.image(open_image(card_string=flop2))

    flop3 = col3.selectbox("Card #3", options=card_labels, key="card_3") 
    if flop3:
        col3.image(open_image(card_string=flop3))

    turn = col4.selectbox("Card #4", options=card_labels, key="card_4")

    if turn:
        col4.image(open_image(card_string=turn))

    river = col5.selectbox("Card #5", options=card_labels, key="card_5")
    if river:
        col5.image(open_image(card_string=river))

    board = [flop1, flop2, flop3, turn, river]
    if len(board) < 5:
        st.error("Looks you've picked a duplicate card!")
    st.markdown("***")
    
    board_values = get_board_values(board)

    duplicates = [item for item, count in collections.Counter([*board, *hand]).items() if count > 1 and item != "Select"]
    if duplicates:
        st.warning("⚠️ There are duplicates in the cards you selected")
        st.write(duplicates)
    
    try:
        evaluator = Evaluator()

        p1_score = evaluator.evaluate(
            board_values, get_board_values(hand)
        )
        p1_class = evaluator.get_rank_class(p1_score)

        st.title(f"{evaluator.class_to_string(p1_class)} |  {p1_score:,} points out of 7,462")
        st.subheader('Royal Flush is equal to 1')

        
    except KeyError:
        st.success("♠ ♣ Select your Cards ♥ ♦")
    
    with st.expander("Resources"):
        st.write("**Poker Evalulation Library from**")
        st.write("[treys 0.1.8](https://pypi.org/project/treys/)")
        st.markdown("***")
        st.write("**The GitHub Repo**")
        st.write("[majoralex/streamlit/poker_app/](https://github.com/majoralex/streamlit/blob/main/poker_app/poker.py)")


if __name__ == "__main__":
    main()
