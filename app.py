from langchain.agents import Tool
from langchain_experimental.utilities import PythonREPL
import streamlit as st
from streamlit_ace import st_ace
import openai
from utils import get_default_code
from langchain_experimental.agents.agent_toolkits.python.base import create_python_agent
from langchain.llms import OpenAI
from langchain_experimental.tools import PythonREPLTool
import os

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
python_repl = PythonREPL()

st.set_page_config(page_title="PythonREPL", page_icon=":snake:", layout="wide")
st.title(":snake: PythonREPL with Langchain")
st.markdown("### Ready to Code? 🚀 Let's Autocomplete!")
st.markdown("1. Write a well-commented Python function `fibonacci(n)` to return the first `n` numbers in the Fibonacci series.")
st.markdown("2. Create a simple Python function `is_prime(num)` that checks if `num` is a prime number and returns `True` or `False`.")
st.markdown("3. Draft a Python function `factorial(x)` that calculates and returns the factorial of a given number `x`.")

col1, col2 = st.columns(2)

with col1:
  st.markdown("### Type your Python code here:")
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
  )

disable_text_generation = st.checkbox('Disable autocomplete', value=False)
response = ""

# Initialize session state if it doesn't exist
if 'response' not in st.session_state:
    st.session_state['response'] = ""

with col2:
    st.markdown("### Autocompletion Suggestions")
    with st.spinner("Please wait a while for autocompletion to load"):
        if not disable_text_generation:
            # Only generate a new response if the code has changed
            if st.session_state['response'] == "" or st.session_state['last_code'] != code:
                llm=OpenAI(temperature=0)
                agent = create_python_agent(llm, tool=PythonREPLTool(), verbose=True)
                st.session_state['response'] = agent.run(f"""Given the following incomplete Python code snippet, 
                               provide the code that logically continues or completes it:\n\n{code}\n\n
                               # Your completion should maintain the logic, structure, and intent of the original code and follow the python syntax and prettier format and 4 spaces indentation.""")
                st.session_state['last_code'] = code
        else:
            st.markdown("<span style='background-color:#f63366; padding:2px 4px; border-radius:5px;'>Autocomplete is disabled</span>", unsafe_allow_html=True)

    if st.session_state['response'] != "":
        response_editor = st_ace(
            language="python",
            theme="dracula",
            keybinding="vscode",
            font_size=16,
            tab_size=4,
            show_gutter=True,
            show_print_margin=True,
            wrap=True,
            auto_update=True,
            placeholder="Response will be displayed here",
            value=str(st.session_state['response']),
            readonly=True,
        )

if code:  
    if st.button("Run Code"):     
        result = python_repl.run(code)
        if result:
            color = "#f63366" if "Error" in result else "#00ff00"
           
            st.markdown(f"<p style='font-family:monospace; color: {color};'>Output:</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-family:monospace; color: {color};'>{result}</p>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='font-family:monospace; color: #f63366;'>Output:</p>", unsafe_allow_html=True)
            st.markdown("<p style='font-family:monospace; color: #f63366;'>No output from the code. Please ensure that you have a print statement in your code.</p>", unsafe_allow_html=True)