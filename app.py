import json
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import base64

# Streamlit application for Wedding RSVP
st.set_page_config(page_title="Wedding RSVP", page_icon="💛")

hide_streamlit_style = """
                <style>
                div[data-testid="stToolbar"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stDecoration"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stStatusWidget"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                #MainMenu {
                visibility: hidden;
                height: 0%;
                }
                header {
                visibility: hidden;
                height: 0%;
                }
                footer {
                visibility: hidden;
                height: 0%;
                }
                </style>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown("""
<style>
html, body, [class*="css"]  {
    font-size: 20px !important;   /* Increase base font size */
}

label, .stTextInput label {
    font-size: 20px !important;   /* Form label size */
}

div.stButton > button {
    font-size: 20px !important;   /* Bigger submit button text */
}
</style>
""", unsafe_allow_html=True)

def style_submit_button():
    custom_button_css = '''
    <style>
    div.stButton > button:first-child {
        background-color: #000000;
        color: #FFF8E1;  /* cream text */
        padding: 14px 26px;
        font-size: 18px;
        font-weight: 600;
        border-radius: 10px;
        border: none;
        cursor: pointer;
        box-shadow: 0 0 12px rgba(255, 235, 59, 0.5); /* yellow glow */
        transition: 0.3s;
    }
    div.stButton > button:first-child:hover {
        background-color: #45A049;
        transform: scale(1.05);
        box-shadow: 0 0 18px rgba(255, 235, 59, 0.8);
        color: #000000; /* readable on hover yellow glow */
    }
    </style>
    '''
    st.markdown(custom_button_css, unsafe_allow_html=True)

    
# Cache the base64 encoding of the binary file
@st.cache_data()
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        return base64.b64encode(f.read()).decode()


# Set the background of the Streamlit app
def set_background(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)
    

# Page title and introduction
st.markdown("<h1 style='text-align: center;'>Wedding RSVP</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Rohit & Vishrutha</h3>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center;'><i>We are excited to celebrate this special day with you!</i></h6>", unsafe_allow_html=True)

# st.write("*We are excited to celebrate this special day with you!*")

# Google Sheets integration setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
gc = gspread.authorize(credentials)

# Open the Google Sheet
gsheet = gc.open("Wedding RSVP").worksheet("Sheet2")

# Set background image
set_background('background.png')

# Apply button styling
# style_submit_button()

# RSVP form
with st.form("rsvp_form"):
    st.write("Please let us know if you can join us by filling the form")
    name = st.text_input("**Name**", placeholder="Please enter you name", max_chars=100)
    guests = st.number_input("**Number of Guests**", min_value=1, max_value=10, step=1)
    # st.write("**Reception** *14-December | 6:30PM onwards*")
    attend_both = st.checkbox("**Reception and Wedding**")
    attend_reception = st.checkbox("**Reception** *[6-December-2025]*")
    # st.write("**Wedding** *15-December | 12:01PM Muhurthum*")
    attend_wedding = st.checkbox("**Wedding**&nbsp;&nbsp;*[7-December-2025]*")

    st.markdown("<hr style='margin-top:15px; margin-bottom:15;'>", unsafe_allow_html=True)
    
    # Submit button
    submitted = st.form_submit_button("**Submit RSVP**")
    
    if submitted:
        if name.strip():
            # Append the data to Google Sheets
            st.balloons()
            gsheet.append_row([name, guests, attend_both, attend_reception, attend_wedding])
            st.success("Thank you for your RSVP! We'll see you soon!")
        else:
            st.error("Please fill out all required fields.")


st.markdown(
    "<h4 style='text-align: center;'>Venue: Chamara Vajra, Mukta</h3>",
    unsafe_allow_html=True
)
# [theme]
# base="light"
# primaryColor = "#A64DFF"  # Lighter purple for primaryColor
# backgroundColor = "#F8F8F8"  # Off-white background color
# #secondaryBackgroundColor = "#F2E6F9"  # Very light purple background color
# secondaryBackgroundColor = "#ECE9F7"
# textColor = "#800080"  # Purple text color
# font = "sans serif"  # Font can be changed here