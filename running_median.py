import streamlit as st
import heapq
import matplotlib.pyplot as plt
import numpy as np

# ---------- Initialization ----------
if 'min_heap' not in st.session_state:
    st.session_state.min_heap = []
if 'max_heap' not in st.session_state:
    st.session_state.max_heap = []
if 'numbers' not in st.session_state:
    st.session_state.numbers = []

# ---------- Page Config ----------
st.set_page_config(page_title="💎 Realtime Median Tracker", layout="centered")

custom_css = """
<style>
body {
    background-color: #0f1117;
    color: #ffffff;
}
section.main > div {
    background-color: #1e1f26;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
}
.stButton > button {
    background: linear-gradient(135deg, #6e8efb, #a777e3);
    border: none;
    color: white;
    padding: 10px 20px;
    border-radius: 10px;
    font-weight: bold;
    transition: 0.3s;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #ff758c, #ff7eb3);
    transform: scale(1.05);
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ---------- Title Section ----------
st.title("💎 Realtime Median Tracker")
st.markdown("""
This app uses two heaps to maintain a real-time running median:
- 🔺 **Max Heap**: for the smaller half
- 🔻 **Min Heap**: for the larger half
""")

# ---------- Input Section ----------
number = st.number_input("Enter a number:", step=1, format="%d")
col1, col2 = st.columns(2)
with col1:
    if st.button("➕ Insert Number"):
        st.session_state.numbers.append(number)

        if not st.session_state.max_heap or number <= -st.session_state.max_heap[0]:
            heapq.heappush(st.session_state.max_heap, -number)
        else:
            heapq.heappush(st.session_state.min_heap, number)

        if len(st.session_state.max_heap) > len(st.session_state.min_heap) + 1:
            heapq.heappush(st.session_state.min_heap, -heapq.heappop(st.session_state.max_heap))
        elif len(st.session_state.min_heap) > len(st.session_state.max_heap):
            heapq.heappush(st.session_state.max_heap, -heapq.heappop(st.session_state.min_heap))

with col2:
    if st.button("🔄 Reset"):
        st.session_state.numbers.clear()
        st.session_state.max_heap.clear()
        st.session_state.min_heap.clear()
        st.success("App reset!")

# ---------- Display Numbers ----------
st.subheader("🔢 Numbers Entered")
if st.session_state.numbers:
    st.code(", ".join(map(str, st.session_state.numbers)))
else:
    st.info("No numbers entered yet.")

# ---------- Median Result ----------
if st.session_state.numbers:
    if len(st.session_state.max_heap) == len(st.session_state.min_heap):
        median = (-st.session_state.max_heap[0] + st.session_state.min_heap[0]) / 2
    else:
        median = -st.session_state.max_heap[0]

    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #43e97b, #38f9d7); padding: 25px; border-radius: 15px; text-align: center; color: black;'>
        <h2 style='margin:0;'>🎯 <u>Current Median</u></h2>
        <h1 style='font-size: 50px; margin-top: 10px;'>{median:.2f}</h1>
    </div>
    """, unsafe_allow_html=True)

# ---------- Bar Chart ----------
    st.subheader("📊 Heap Visualization")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_facecolor("#1e1f26")
    fig.patch.set_facecolor("#1e1f26")
    
    max_vals = sorted([-x for x in st.session_state.max_heap], reverse=True)
    min_vals = sorted(st.session_state.min_heap)
    max_x = np.arange(len(max_vals))
    min_x = np.arange(len(min_vals)) + len(max_vals) + 1

    ax.bar(max_x, max_vals, color='#00bfff', label='Max Heap')
    ax.bar(min_x, min_vals, color='#ff69b4', label='Min Heap')
    ax.axhline(y=median, color='lime', linestyle='--', linewidth=2, label=f'Median: {median:.2f}')
    
    for i, val in enumerate(max_vals):
        ax.text(max_x[i], val + 0.3, str(val), ha='center', fontsize=9, color='white')
    for i, val in enumerate(min_vals):
        ax.text(min_x[i], val + 0.3, str(val), ha='center', fontsize=9, color='white')

    ax.set_ylabel("Values", color='white')
    ax.set_xticks([])
    ax.tick_params(colors='white')
    ax.legend()
    st.pyplot(fig)
