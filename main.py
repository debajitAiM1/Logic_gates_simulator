import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# Page config
st.set_page_config(page_title="Logic Gate Simulator", page_icon="🔌")
st.title("🔌 Interactive Logic Gate Simulator")

# Gate selection
gate = st.selectbox("Select Logic Gate:", ["AND", "OR", "NOT", "NAND", "NOR", "XOR", "XNOR"])

st.markdown("---")

# Input columns
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Input A")
    input_a = st.radio("A", [0, 1], horizontal=True, key="a", label_visibility="collapsed")

input_b = 0
if gate != "NOT":
    with col2:
        st.markdown("### Input B")
        input_b = st.radio("B", [0, 1], horizontal=True, key="b", label_visibility="collapsed")


# Logic Function
def calculate_logic(g, a, b):
    if g == "AND":
        return int(a and b)
    elif g == "OR":
        return int(a or b)
    elif g == "NOT":
        return int(not a)
    elif g == "NAND":
        return int(not (a and b))
    elif g == "NOR":
        return int(not (a or b))
    elif g == "XOR":
        return int(a != b)
    elif g == "XNOR":
        return int(a == b)


result = calculate_logic(gate, input_a, input_b)

# Display Result
with col3:
    st.markdown("### Output")
    if result == 1:
        st.success("💡 ON (1)")
    else:
        st.error("⚫ OFF (0)")

st.markdown("---")

# ----------------- TRUTH TABLE -----------------
st.markdown(f"### 📊 {gate} Gate Truth Table")

if gate == "NOT":
    data = {"A": [0, 1], "Output": [1, 0]}
    df = pd.DataFrame(data)


    def highlight_row(row):
        if row['A'] == input_a:
            return ['background-color: #4CAF50; color: white'] * len(row)
        return [''] * len(row)
else:
    data = {
        "A": [0, 0, 1, 1],
        "B": [0, 1, 0, 1],
        "Output": [calculate_logic(gate, 0, 0),
                   calculate_logic(gate, 0, 1),
                   calculate_logic(gate, 1, 0),
                   calculate_logic(gate, 1, 1)]
    }
    df = pd.DataFrame(data)


    def highlight_row(row):
        if row['A'] == input_a and row['B'] == input_b:
            return ['background-color: #2e7b32; color: white; font-weight: bold'] * len(row)
        return [''] * len(row)

styled_df = df.style.apply(highlight_row, axis=1)
st.dataframe(styled_df, use_container_width=True)

st.markdown("---")


# ----------------- ANIMATIONS -----------------

# 1. LOGIC GATE BLOCK ANIMATION
def get_logic_block_svg(g, a, b, out):
    color_a = "#00ff00" if a else "#555555"
    color_b = "#00ff00" if b else "#555555"
    color_out = "#00ff00" if out else "#555555"
    bulb_color = "#ffdd00" if out else "#222222"
    glow = 'filter="url(#glow1)"' if out else ''

    svg = f"""
    <div style="display: flex; justify-content: center; align-items: center; padding: 10px; background-color: #1e1e1e; border-radius: 10px; height: 100%;">
    <svg width="350" height="180" viewBox="0 0 400 200" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <filter id="glow1" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="8" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
        </defs>
        <text x="200" y="20" fill="#aaaaaa" font-size="16" font-family="Arial" text-anchor="middle">Logic Symbol View</text>
        <line x1="40" y1="70" x2="160" y2="70" stroke="{color_a}" stroke-width="8" stroke-linecap="round"/>
        <text x="15" y="76" fill="white" font-size="20" font-family="Arial" font-weight="bold">A</text>
    """
    if g != "NOT":
        svg += f"""
        <line x1="40" y1="130" x2="160" y2="130" stroke="{color_b}" stroke-width="8" stroke-linecap="round"/>
        <text x="15" y="136" fill="white" font-size="20" font-family="Arial" font-weight="bold">B</text>
        """
    svg += f"""
        <rect x="160" y="30" width="100" height="140" fill="#333333" stroke="#ffffff" stroke-width="3" rx="10"/>
        <text x="210" y="108" fill="white" font-size="28" font-family="Arial" font-weight="bold" text-anchor="middle">{g}</text>
        <line x1="260" y1="100" x2="330" y2="100" stroke="{color_out}" stroke-width="8" stroke-linecap="round"/>
        <circle cx="350" cy="100" r="24" fill="{bulb_color}" {glow} stroke="#ffffff" stroke-width="2"/>
        <path d="M338,122 L362,122 L356,138 L344,138 Z" fill="#777777" />
    </svg>
    </div>
    """
    return svg


# 2. PHYSICAL SWITCH ANIMATION
def get_physical_switch_svg(g, a, b, out):
    bulb_color = "#ffdd00" if out else "#222222"
    glow = 'filter="url(#glow2)"' if out else ''

    state_a = "ON" if a else "OFF"
    state_b = "ON" if b else "OFF"

    svg_base = f"""
    <div style="display: flex; justify-content: center; align-items: center; padding: 10px; background-color: #1a252c; border-radius: 10px; height: 100%;">
    <svg width="350" height="220" viewBox="0 0 400 200" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <filter id="glow2" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="8" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
        </defs>
        <text x="200" y="20" fill="#aaaaaa" font-size="16" font-family="Arial" text-anchor="middle">Physical Circuit View</text>

        <rect x="20" y="80" width="20" height="40" fill="#ff4444" rx="3"/>
        <rect x="15" y="90" width="5" height="20" fill="#cccccc"/>
        <text x="30" y="70" fill="white" font-size="14" font-family="Arial" text-anchor="middle">Power</text>
    """

    inner_svg = ""

    if g == "AND" or g == "NOR":
        # SERIES CIRCUIT
        is_nc = (g == "NOR")
        closed_a = (a == 0) if is_nc else (a == 1)
        closed_b = (b == 0) if is_nc else (b == 1)
        tilt_a = 100 if closed_a else 80
        tilt_b = 100 if closed_b else 80

        inner_svg = f"""
        <line x1="40" y1="100" x2="100" y2="100" stroke="#888888" stroke-width="4"/>
        <circle cx="100" cy="100" r="5" fill="white"/>
        <line x1="100" y1="100" x2="160" y2="{tilt_a}" stroke="#00ccff" stroke-width="6" stroke-linecap="round"/>
        <circle cx="160" cy="100" r="5" fill="white"/>
        <text x="130" y="65" fill="white" font-size="14" font-family="Arial" text-anchor="middle" font-weight="bold">A ({state_a}, {a})</text>

        <line x1="160" y1="100" x2="200" y2="100" stroke="#888888" stroke-width="4"/>
        <circle cx="200" cy="100" r="5" fill="white"/>
        <line x1="200" y1="100" x2="260" y2="{tilt_b}" stroke="#00ccff" stroke-width="6" stroke-linecap="round"/>
        <circle cx="260" cy="100" r="5" fill="white"/>
        <text x="230" y="65" fill="white" font-size="14" font-family="Arial" text-anchor="middle" font-weight="bold">B ({state_b}, {b})</text>

        <line x1="260" y1="100" x2="330" y2="100" stroke="#888888" stroke-width="4"/>
        """

    elif g == "OR" or g == "NAND":
        # PARALLEL CIRCUIT
        is_nc = (g == "NAND")
        closed_a = (a == 0) if is_nc else (a == 1)
        closed_b = (b == 0) if is_nc else (b == 1)
        tilt_a = 60 if closed_a else 40
        tilt_b = 140 if closed_b else 120

        inner_svg = f"""
        <line x1="40" y1="100" x2="80" y2="100" stroke="#888888" stroke-width="4"/>
        <line x1="80" y1="60" x2="80" y2="140" stroke="#888888" stroke-width="4"/>

        <line x1="80" y1="60" x2="120" y2="60" stroke="#888888" stroke-width="4"/>
        <circle cx="120" cy="60" r="5" fill="white"/>
        <line x1="120" y1="60" x2="180" y2="{tilt_a}" stroke="#00ccff" stroke-width="6" stroke-linecap="round"/>
        <circle cx="180" cy="60" r="5" fill="white"/>
        <line x1="180" y1="60" x2="220" y2="60" stroke="#888888" stroke-width="4"/>
        <text x="150" y="35" fill="white" font-size="14" font-family="Arial" text-anchor="middle" font-weight="bold">A ({state_a}, {a})</text>

        <line x1="80" y1="140" x2="120" y2="140" stroke="#888888" stroke-width="4"/>
        <circle cx="120" cy="140" r="5" fill="white"/>
        <line x1="120" y1="140" x2="180" y2="{tilt_b}" stroke="#00ccff" stroke-width="6" stroke-linecap="round"/>
        <circle cx="180" cy="140" r="5" fill="white"/>
        <line x1="180" y1="140" x2="220" y2="140" stroke="#888888" stroke-width="4"/>
        <text x="150" y="175" fill="white" font-size="14" font-family="Arial" text-anchor="middle" font-weight="bold">B ({state_b}, {b})</text>

        <line x1="220" y1="60" x2="220" y2="140" stroke="#888888" stroke-width="4"/>
        <line x1="220" y1="100" x2="330" y2="100" stroke="#888888" stroke-width="4"/>
        """

    elif g == "NOT":
        # SINGLE SWITCH
        closed_a = (a == 0)
        tilt_a = 100 if closed_a else 80
        inner_svg = f"""
        <line x1="40" y1="100" x2="140" y2="100" stroke="#888888" stroke-width="4"/>
        <circle cx="140" cy="100" r="5" fill="white"/>
        <line x1="140" y1="100" x2="200" y2="{tilt_a}" stroke="#00ccff" stroke-width="6" stroke-linecap="round"/>
        <circle cx="200" cy="100" r="5" fill="white"/>
        <text x="170" y="70" fill="white" font-size="14" font-family="Arial" text-anchor="middle" font-weight="bold">A ({state_a}, {a})</text>
        <line x1="200" y1="100" x2="330" y2="100" stroke="#888888" stroke-width="4"/>
        """
    elif g == "XOR" or g == "XNOR":
        # SPDT (Two-Way Switch) Staircase Wiring Circuit
        y_a = 70 if a else 130
        y_b = 70 if b else 130

        # XNOR ke liye wires seedhi hoti hain, XOR ke liye cross
        cross_top = 70 if g == "XNOR" else 130
        cross_bot = 130 if g == "XNOR" else 70

        inner_svg = f"""
        <line x1="40" y1="100" x2="80" y2="100" stroke="#888888" stroke-width="4"/>

        <circle cx="80" cy="100" r="5" fill="white"/>
        <circle cx="140" cy="70" r="4" fill="#aaaaaa"/>
        <circle cx="140" cy="130" r="4" fill="#aaaaaa"/>
        <line x1="80" y1="100" x2="140" y2="{y_a}" stroke="#00ccff" stroke-width="6" stroke-linecap="round"/>
        <text x="110" y="55" fill="white" font-size="14" font-family="Arial" text-anchor="middle" font-weight="bold">A ({state_a}, {a})</text>

        <line x1="140" y1="70" x2="200" y2="{cross_top}" stroke="#888888" stroke-width="4"/>
        <line x1="140" y1="130" x2="200" y2="{cross_bot}" stroke="#888888" stroke-width="4"/>

        <circle cx="200" cy="70" r="4" fill="#aaaaaa"/>
        <circle cx="200" cy="130" r="4" fill="#aaaaaa"/>
        <circle cx="260" cy="100" r="5" fill="white"/>
        <line x1="260" y1="100" x2="200" y2="{y_b}" stroke="#00ccff" stroke-width="6" stroke-linecap="round"/>
        <text x="230" y="165" fill="white" font-size="14" font-family="Arial" text-anchor="middle" font-weight="bold">B ({state_b}, {b})</text>

        <line x1="260" y1="100" x2="330" y2="100" stroke="#888888" stroke-width="4"/>
        """

    svg_end = f"""
        <circle cx="350" cy="100" r="24" fill="{bulb_color}" {glow} stroke="#ffffff" stroke-width="2"/>
        <path d="M338,122 L362,122 L356,138 L344,138 Z" fill="#777777" />
        <text x="350" y="155" fill="white" font-size="14" font-family="Arial" text-anchor="middle" font-weight="bold">{"ON" if out else "OFF"}</text>
    </svg>
    </div>
    """
    return svg_base + inner_svg + svg_end


# Render Components
st.markdown("### 🔌 Logic Symbol")
components.html(get_logic_block_svg(gate, input_a, input_b, result), height=260)

st.markdown("### ⚡ Physical Circuit")
components.html(get_physical_switch_svg(gate, input_a, input_b, result), height=260)

# Add some spacing
st.markdown("<br><br>", unsafe_allow_html=True)

# Professional Footer
st.markdown(
    """
    <div style='text-align: center; color: #888888; padding: 20px; font-family: Arial, sans-serif;'>
        <hr style='border: 1px solid #444444; width: 50%; margin: 0 auto 15px auto;'>
        <p style='font-size: 16px; margin: 0;'>
            ✨ Designed & Developed By <strong>Debajit Mallik</strong> ✨
        </p>
    </div>
    """,
    unsafe_allow_html=True
)