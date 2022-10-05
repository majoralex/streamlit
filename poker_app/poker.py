import regex
import streamlit as st
import re
from PIL import Image
import os

from treys import Card
from treys import Evaluator
from treys import Deck

@st.experimental_singleton
def draw_deck():
    return list(zip(Deck().GetFullDeck(), str(Deck()).replace('[','').replace(']','').strip().split(",")))

def get_board_values(board):
    cards = draw_deck()
    return [c[0] for c in cards if c[1] in board]

def main():
    
    st.set_page_config(
     page_title="Pokerhand Evaluator",
     page_icon="🃏",
    #  layout="wide",
     initial_sidebar_state="expanded",
    #  menu_items={
    #      'Get Help': 'https://www.extremelycoolapp.com/help',
    #      'Report a bug': "https://www.extremelycoolapp.com/bug",
    #      'About': "# This is a header. This is an *extremely* cool app!"
    #  }
    )
    st.title("🃏 Pokerhand Evaluator")

  
    cards = draw_deck()
    card_labels = [str("Select"), *[c[1] for c in cards]]
    card_values = [str("Select"), *[c[0] for c in cards]]
    


    
    col1, col2, col3 = st.columns((4,1,1))

    col1.subheader("Flop")
    col2.subheader("Turn")
    col3.subheader("River")


    col1, col2, col3, col4, col5 = st.columns(5)

    flop1= col1.selectbox("Card #1", options=card_labels, key="card_1")

    # col1.write(os.getcwd() + f"\\cards\\2_of_clubs.png")
    card1 = Image.open(os.getcwd() + f"\\poker_app\\cards\\2_of_clubs.png")
    col1.image(card1, caption='Sunrise by the mountains')



    flop2 = col2.selectbox("Card #2", options=card_labels, key="card_2")

    card2 = Image.open(os.getcwd() + f"\\poker_app\\cards\\2_of_clubs.png")
    col2.image(card2)

    flop3 = col3.selectbox("Card #3", options=card_labels, key="card_3")
    card3 = Image.open(os.getcwd() + f"\\poker_app\\cards\\2_of_clubs.png")
    col3.image(card3)

    st.write(flop1, flop2, flop3)
    st.write(flop1.replace({
        
    }))

    if flop1 != "Select" and flop2  != "Select" and flop3 != "Select":
        turn= col4.selectbox("Card #4", options=card_labels, key="card_4")

        card4 = Image.open(os.getcwd() + f"\\poker_app\\cards\\2_of_clubs.png")
        col4.image(card4)




        if turn != "Select":
        
            
            river = col5.selectbox("Card #5", options=card_labels, key="card_5")

            card5 = Image.open(os.getcwd() + f"\\poker_app\\cards\\2_of_clubs.png")
            col5.image(card5)



            board = [flop1, flop2, flop3, turn, river]
            if len(board) < 5:
                st.error("Looks you've picked a duplicate card!")
            st.markdown("***")

            board_values = get_board_values(board)


    col1, col2, col3, col4 = st.columns(4)
    playercard1 = col1.selectbox("Card #1", options=card_labels, key="player_card_1")
    playercard2 = col2.selectbox("Card #2", options=card_labels, key="player_card_2")

    evaluator = Evaluator()
    try:
        p1_score = evaluator.evaluate(board_values, get_board_values([playercard1, playercard2]))
        st.write('p1 score', p1_score)
    except KeyError:
        st.error("There is a card that is duplicated")
    except UnboundLocalError:
         st.success("Input the rest of the cards to evaluate your hand...")
    
    
    

if __name__ == "__main__":
    main()



   