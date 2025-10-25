import streamlit as st
from PIL import Image
import time

st.set_page_config(page_title="Ancient Tale", layout="wide")

# --- Initialize session state ---
if "page" not in st.session_state:
    st.session_state.page = "menu"
if "character" not in st.session_state:
    st.session_state.character = None
if "hearts" not in st.session_state:
    st.session_state.hearts = 4
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "kids_question_index" not in st.session_state:
    st.session_state.kids_question_index = 0
if "ship_question_index" not in st.session_state:
    st.session_state.ship_question_index = 0
if "pearls_answered" not in st.session_state:
    st.session_state.pearls_answered = 0

# --- Helper functions ---
def next_page(page):
    st.session_state.page = page

def show_scene_background(image_path):
    try:
        img = Image.open(image_path)
        st.image(img, use_container_width=True)
    except FileNotFoundError:
        st.warning(f"⚠️ Missing image: {image_path}")

# --- MENU PAGE ---
if st.session_state.page == "menu":
    show_scene_background("menu.png")
    st.markdown("<h1 style='text-align:center; font-size:60px; color:white;'>Ancient Tales</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sign In", use_container_width=True):
            next_page("signin")
    with col2:
        if st.button("Enter as Guest", use_container_width=True):
            next_page("choose_character")

# --- SIGN IN PAGE ---
elif st.session_state.page == "signin":
    show_scene_background("menu.png")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Submit"):
        if email and password:
            next_page("choose_character")
        else:
            st.warning("Please enter both email and password")

# --- CHARACTER SELECTION ---
elif st.session_state.page == "choose_character":
    show_scene_background("character.png")
    col1, col2 = st.columns(2)
    with col1:
        st.image("dhabia.png", width=300)
        if st.button("Choose Dhabia"):
            st.session_state.character = "girl"
            next_page("scene_dubai1")
    with col2:
        st.image("nahyan.png", width=300)
        if st.button("Choose Nahyan"):
            st.session_state.character = "boy"
            next_page("scene_dubai1")

c = st.session_state.character

# --- SIMPLE SCENE HELPER ---
def show_scene(scene_name, next_scene):
    show_scene_background(f"{scene_name}{c}.png")
    if st.button("Next ➜", use_container_width=True):
        next_page(next_scene)

# --- DUBAI SCENES ---
if st.session_state.page == "scene_dubai1":
    show_scene("dubainew1", "scene_dubai2")
elif st.session_state.page == "scene_dubai2":
    show_scene("dubainew2", "scene_welcome1")

# --- WELCOME SCENES ---
if st.session_state.page == "scene_welcome1":
    show_scene("welcome1", "scene_welcome2")
elif st.session_state.page == "scene_welcome2":
    show_scene("welcome2", "scene_kids1")

# --- KIDS SCENES WITH QUESTIONS ---
kids_questions = [
    ("Which game are they playing?", ["Tila", "Qubba", "Salam bil Aqaal", "Khosah Biboosah"], "Tila"),
    ("Second game?", ["Khosah Biboosah", "Tila", "Mawiyah", "Alghimayah"], "Khosah Biboosah"),
    ("Who is leading the game?", ["Kid1", "Kid2", "Both"], "Both"),
    ("Where are they playing?", ["Beach", "Park", "Ship"], "Beach")
]

for i in range(1, 5):
    if st.session_state.page == f"scene_kids{i}":
        show_scene_background(f"kids{i}{c}.png")
        idx = st.session_state.kids_question_index
        q, opts, ans = kids_questions[idx]
        choice = st.radio(q, opts, key=f"kids_q{idx}")
        if st.button("Submit Answer"):
            if choice == ans:
                st.success("Correct! +1 point")
            else:
                st.error(f"Wrong! Correct: {ans}")
            st.session_state.kids_question_index += 1
            next_scene = f"scene_kids{i+1}" if i < 4 else "scene_crew1"
            next_page(next_scene)

# --- CREW SCENES ---
for i in range(1, 10):
    if st.session_state.page == f"scene_crew{i}":
        next_scene = "pearl_game" if i == 9 else f"scene_crew{i+1}"
        show_scene(f"crew{i}", next_scene)

# --- PEARL GAME ---
if st.session_state.page == "pearl_game":
    show_scene_background(f"pearlgame{c}.png")
    if st.session_state.start_time is None:
        st.session_state.start_time = time.time()
    elapsed = time.time() - st.session_state.start_time
    hearts_left = 4 - int(elapsed // 30)
    st.session_state.hearts = max(hearts_left, 0)
    hearts_display = "❤️ " * st.session_state.hearts
    st.markdown(f"<h3 style='color:red; text-align:center;'>{hearts_display}</h3>", unsafe_allow_html=True)

    pearls = [
        ("pearl1.png", "What is the knife used to open oysters?", "Sakaria"),
        ("pearl2.png", "Large white/pinkish pearl?", "Danah"),
        ("pearl3.png", "Smaller white shiny pearl?", "Yaqooti"),
        ("pearl4.png", "Yellowish/blueish pearl?", "Qimashi")
    ]

    cols = st.columns(4)
    for i, (img, q, a) in enumerate(pearls):
        with cols[i]:
            try:
                st.image(img, width=100)
                if st.button(f"Pearl {i+1}", key=f"pearl{i}"):
                    ans = st.text_input(q, key=f"q{i}")
                    if ans:
                        st.success(f"Correct: {a}")
                        st.session_state.pearls_answered += 1
            except:
                st.warning(f"⚠️ Missing image: {img}")

    if st.session_state.pearls_answered >= 4 or st.session_state.hearts == 0:
        next_page("ship")

# --- SHIP SCENE WITH QUESTIONS ---
ship_questions = [
    ("What is the Naukhada's role?", ["Captain / Chief", "Main diver", "Assistant diver"], "Captain / Chief"),
    ("Who is Naham?", ["Motivator and singer", "Main diver", "Pearl inspector"], "Motivator and singer"),
    ("Who steers the ship?", ["Skuni", "Seeb", "Naham"], "Skuni"),
    ("The song 'Oh Ya Mal' is sung during?", ["Pearl diving", "Fishing", "Exploration"], "Pearl diving"),
    ("Why is 'Oh Ya Mal' sung?", ["Beauty", "Communication / morale", "No reason"], "Communication / morale")
]

if st.session_state.page == "ship":
    show_scene_background(f"ship{c}1.png")
    idx = st.session_state.ship_question_index
    q, opts, ans = ship_questions[idx]
    choice = st.radio(q, opts, key=f"ship_q{idx}")
    if st.button("Submit Answer"):
        if choice == ans:
            st.success("Correct! +1 point")
        else:
            st.error(f"Wrong! Correct: {ans}")
        st.session_state.ship_question_index += 1
        if st.session_state.ship_question_index >= len(ship_questions):
            next_page("congrats1")

# --- CONGRATS SCENES ---
if st.session_state.page == "congrats1":
    show_scene_background(f"congrats1{c}.png")
    st.markdown("<h1 style='color:gold; text-align:center;'>Congratulations!</h1>", unsafe_allow_html=True)
    time.sleep(5)
    next_page("congrats2")

elif st.session_state.page == "congrats2":
    show_scene_background(f"congrats2{c}.png")
    st.markdown("<h2 style='color:white; text-align:center;'>You completed the Ancient Tale!</h2>", unsafe_allow_html=True)
