import streamlit as st
import heapq
import matplotlib.pyplot as plt
import numpy as np

# Initialize session state
if 'min_heap' not in st.session_state:
    st.session_state.min_heap = []
if 'max_heap' not in st.session_state:
    st.session_state.max_heap = []
if 'numbers' not in st.session_state:
    st.session_state.numbers = []

# Page setup
st.set_page_config(page_title="Running Median with Heaps", layout="centered")
st.title("📊 Running Median Finder Using Heaps")
st.markdown("""
This app demonstrates how to maintain a **running median** using two heaps:
- A **max heap** for the smaller half of the data
- A **min heap** for the larger half of the data
""")

# Number input
number = st.number_input("Enter a number to insert:", step=1, format="%d")
if st.button("Insert Number"):
    st.session_state.numbers.append(number)

    # Insert into appropriate heap
    if not st.session_state.max_heap or number <= -st.session_state.max_heap[0]:
        heapq.heappush(st.session_state.max_heap, -number)
    else:
        heapq.heappush(st.session_state.min_heap, number)

    # Balance the heaps
    if len(st.session_state.max_heap) > len(st.session_state.min_heap) + 1:
        moved = -heapq.heappop(st.session_state.max_heap)
        heapq.heappush(st.session_state.min_heap, moved)
    elif len(st.session_state.min_heap) > len(st.session_state.max_heap):
        moved = heapq.heappop(st.session_state.min_heap)
        heapq.heappush(st.session_state.max_heap, -moved)

    st.success(f"Inserted {number}!")

# Display entered numbers
st.subheader("🔢 Numbers Entered")
st.write(", ".join(map(str, st.session_state.numbers)) if st.session_state.numbers else "None")

# Show median and bar chart
if st.session_state.numbers:
    if len(st.session_state.max_heap) == len(st.session_state.min_heap):
        median = (-st.session_state.max_heap[0] + st.session_state.min_heap[0]) / 2
    else:
        median = -st.session_state.max_heap[0]

    st.markdown(f"""
    <div style='background-color:#ffd700; padding:20px; border-radius:10px; text-align:center;'>
        <h2 style='color:#000;'>📍 <u>Current Median</u></h2>
        <h1 style='color:#d63384;'>💡 {median:.2f}</h1>
    </div>
    """, unsafe_allow_html=True)

    # Bar Chart Visualization
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_title("Heap Visualization (Bar Chart)", fontsize=14, weight='bold')

    max_vals = sorted([-x for x in st.session_state.max_heap], reverse=True)
    min_vals = sorted(st.session_state.min_heap)

    max_x = np.arange(len(max_vals))
    min_x = np.arange(len(min_vals)) + len(max_vals) + 1  # space between heaps

    # Plot Max Heap
    ax.bar(max_x, max_vals, color='#1f77b4', label='Max Heap')
    for i, val in enumerate(max_vals):
        ax.text(max_x[i], val + 0.3, str(val), ha='center', fontsize=9)

    # Plot Min Heap
    ax.bar(min_x, min_vals, color='#ff7f0e', label='Min Heap')
    for i, val in enumerate(min_vals):
        ax.text(min_x[i], val + 0.3, str(val), ha='center', fontsize=9)

    # Median line
    ax.axhline(y=median, color='green', linestyle='--', linewidth=2, label=f'Median: {median:.2f}')
    ax.text((len(max_vals) + len(min_vals)) / 2, median + 0.5, f'Median: {median:.2f}', ha='center', color='green')

    ax.set_ylabel("Values")
    ax.set_xticks([])
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    st.pyplot(fig)

# Reset button
if st.button("Reset"):
    st.session_state.numbers.clear()
    st.session_state.max_heap.clear()
    st.session_state.min_heap.clear()
    st.info("All data has been reset.")
