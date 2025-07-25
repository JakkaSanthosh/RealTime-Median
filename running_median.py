import numpy as np

# Updated visualization: Heap values as bar plots
fig, ax = plt.subplots(figsize=(10, 4))
ax.set_title("Heap Visualization (Bar Chart)", fontsize=14, weight='bold')

# Get sorted heap values
max_vals = sorted([-x for x in st.session_state.max_heap], reverse=True)
min_vals = sorted(st.session_state.min_heap)

# Bar positions
max_x = np.arange(len(max_vals))
min_x = np.arange(len(min_vals)) + len(max_vals) + 1  # add gap between heaps

# Plot bars for Max Heap
ax.bar(max_x, max_vals, color='#1f77b4', label='Max Heap')
for i, val in enumerate(max_vals):
    ax.text(max_x[i], val + 0.3, str(val), ha='center', fontsize=9)

# Plot bars for Min Heap
ax.bar(min_x, min_vals, color='#ff7f0e', label='Min Heap')
for i, val in enumerate(min_vals):
    ax.text(min_x[i], val + 0.3, str(val), ha='center', fontsize=9)

# Median line
ax.axhline(y=median, color='green', linestyle='--', linewidth=2, label=f'Median: {median:.2f}')
ax.text(len(max_vals) + len(min_vals) / 2, median + 0.3, f'Median: {median:.2f}', color='green', ha='center')

# Labels and formatting
ax.set_ylabel("Values")
ax.set_xticks([])
ax.legend()
ax.grid(axis='y', linestyle='--', alpha=0.5)

st.pyplot(fig)
