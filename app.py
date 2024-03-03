# Import necessary modules
from langchain.agents import Tool
from langchain_experimental.utilities import PythonREPL
import streamlit as st
from streamlit_ace import st_ace
import openai
from utils import get_default_code

# Initialize Python REPL
python_repl = PythonREPL()

# Set the page title with page config
st.set_page_config(page_title="PythonREPL", page_icon=":snake:")

# Add custom CSS for padding in the Ace editor
st.markdown(
    """
    <style>
    .ace_editor {
        padding: 10px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Set the title of the page with snake icon
st.title(":snake: PythonREPL")

# Create an Ace editor with default code
code = st_ace(
    language="python",
    theme="dracula",
    keybinding="vscode",
    font_size=16,
    tab_size=4,
    show_gutter=True,
    show_print_margin=True,
    wrap=True,
    auto_update=True,
    placeholder="Enter your code here",
    value=get_default_code(),
)

# Run the code in the Ace editor when the "Run" button is clicked
if code:  
    if st.button("Run"):     
        result = python_repl.run(code)
        
        # Check if the result is an error message
        if "Error" in result:
            color = "#f63366"  # Red for errors
        else:
            color = "#00ff00"  # Green for successful output
        
        # Display the result with custom styling
        st.markdown(f"<p style='font-family:monospace; color: {color};'>{result}</p>", unsafe_allow_html=True)