"""
CyberGuard AI - RAG Query Workflow (Sequence-style Diagram)
Libraries: matplotlib
Generates: diagrams/04_query_workflow.png
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(1, 1, figsize=(14, 10))
fig.patch.set_facecolor('#0B0F19')
ax.set_facecolor('#0B0F19')
ax.set_xlim(0, 14)
ax.set_ylim(0, 10)
ax.axis('off')

ax.text(7, 9.5, 'Phase 3 — RAG Query Workflow', fontsize=22, fontweight='bold',
        color='white', ha='center', va='center')
ax.text(7, 9.05, 'Step-by-Step: From User Question to AI-Generated Answer',
        fontsize=11, color='#94A3B8', ha='center', va='center')

# --- Actors (vertical lines) ---
actors = [
    (2, '👤 User', '#3B82F6'),
    (5.5, '🌐 Flask API', '#1E293B'),
    (9, '📚 ChromaDB', '#10B981'),
    (12, '🧠 LLM', '#8B5CF6'),
]
for x, label, color in actors:
    box = FancyBboxPatch((x - 0.8, 8.2), 1.6, 0.6, boxstyle="round,pad=0.1",
                          facecolor=color, edgecolor='white', linewidth=1.2, alpha=0.9)
    ax.add_patch(box)
    ax.text(x, 8.5, label, fontsize=10, fontweight='bold', ha='center', va='center', color='white')
    # Lifeline
    ax.plot([x, x], [0.5, 8.2], color='#334155', linewidth=1.5, linestyle='--', alpha=0.5)

# --- Messages (horizontal arrows with labels) ---
def msg(ax, x1, x2, y, label, color='#60A5FA', direction='right'):
    if direction == 'right':
        ax.annotate('', xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle='->', color=color, lw=2))
    else:
        ax.annotate('', xy=(x1, y), xytext=(x2, y),
                    arrowprops=dict(arrowstyle='->', color=color, lw=2, linestyle='dashed'))
    mx = (x1 + x2) / 2
    ax.text(mx, y + 0.18, label, fontsize=8, ha='center', va='center', color='white',
            fontweight='bold', bbox=dict(boxstyle='round,pad=0.15', facecolor='#1E293B',
            edgecolor=color, linewidth=0.8))

def step_label(ax, y, num):
    ax.text(0.5, y, num, fontsize=9, fontweight='bold', ha='center', va='center',
            color='#F59E0B', bbox=dict(boxstyle='circle,pad=0.15', facecolor='#1E293B',
            edgecolor='#F59E0B', linewidth=1))

# Step 1
y = 7.5
step_label(ax, y, '1')
msg(ax, 2, 5.5, y, 'User asks a question', '#3B82F6')

# Step 2
y = 6.7
step_label(ax, y, '2')
msg(ax, 5.5, 9, y, 'Semantic search (embed query)', '#10B981')

# Step 3
y = 5.9
step_label(ax, y, '3')
msg(ax, 9, 5.5, y, 'Return top-k similar chunks', '#10B981', 'left')

# Step 4 - Processing box
y = 5.1
step_label(ax, y, '4')
proc_box = FancyBboxPatch((4, 4.7), 3, 0.7, boxstyle="round,pad=0.1",
                           facecolor='#1E293B', edgecolor='#F59E0B', linewidth=1.2, alpha=0.8)
ax.add_patch(proc_box)
ax.text(5.5, 5.05, 'Build Prompt = Rules + Context + Question', fontsize=8,
        ha='center', va='center', color='#FCD34D', fontweight='bold')

# Step 5
y = 4.0
step_label(ax, y, '5')
msg(ax, 5.5, 12, y, 'Send structured prompt for inference', '#8B5CF6')

# Step 6 - LLM processing box
y = 3.2
step_label(ax, y, '6')
llm_box = FancyBboxPatch((10.5, 2.9), 3, 0.7, boxstyle="round,pad=0.1",
                           facecolor='#1E293B', edgecolor='#A78BFA', linewidth=1.2, alpha=0.8)
ax.add_patch(llm_box)
ax.text(12, 3.25, 'Generate contextual answer', fontsize=8,
        ha='center', va='center', color='#C4B5FD', fontweight='bold')

# Step 7
y = 2.2
step_label(ax, y, '7')
msg(ax, 12, 5.5, y, 'Return structured analysis', '#8B5CF6', 'left')

# Step 8
y = 1.4
step_label(ax, y, '8')
msg(ax, 5.5, 2, y, 'Display answer + sources', '#3B82F6', 'left')

# Response note
ax.text(2, 0.7, '✅ User receives a sourced, context-aware answer', fontsize=9,
        ha='left', va='center', color='#10B981', fontweight='bold')

plt.tight_layout()
plt.savefig('diagrams/04_query_workflow.png', dpi=200, bbox_inches='tight',
            facecolor='#0B0F19', edgecolor='none')
plt.close()
print("Created: diagrams/04_query_workflow.png")
