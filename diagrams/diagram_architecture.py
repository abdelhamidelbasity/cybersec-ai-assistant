"""
CyberGuard AI - System Architecture Diagram
Libraries: matplotlib
Generates: diagrams/01_system_architecture.png
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(1, 1, figsize=(16, 9))
fig.patch.set_facecolor('#0B0F19')
ax.set_facecolor('#0B0F19')
ax.set_xlim(0, 16)
ax.set_ylim(0, 9)
ax.axis('off')

# Title
ax.text(8, 8.5, 'CyberGuard AI — System Architecture', fontsize=22, fontweight='bold',
        color='white', ha='center', va='center', fontfamily='sans-serif')
ax.text(8, 8.05, 'Local Privacy-Preserving Cybersecurity RAG Assistant', fontsize=11,
        color='#94A3B8', ha='center', va='center')

# Helper function to draw boxes
def draw_box(ax, x, y, w, h, label, sublabel, color, icon_text=''):
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15",
                          facecolor=color, edgecolor='white', linewidth=1.2, alpha=0.85)
    ax.add_patch(box)
    if icon_text:
        ax.text(x + w/2, y + h*0.65, icon_text, fontsize=14, ha='center', va='center', color='white')
    ax.text(x + w/2, y + h*0.38, label, fontsize=10, fontweight='bold',
            ha='center', va='center', color='white', fontfamily='sans-serif')
    if sublabel:
        ax.text(x + w/2, y + h*0.12, sublabel, fontsize=7.5,
                ha='center', va='center', color='#CBD5E1', fontfamily='sans-serif')

def draw_arrow(ax, x1, y1, x2, y2, label='', color='#3B82F6'):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=2))
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx, my + 0.2, label, fontsize=7, ha='center', va='center',
                color='#94A3B8', fontfamily='sans-serif',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#0B0F19', edgecolor='none'))

# --- Secure Environment Box ---
env_box = FancyBboxPatch((3.5, 0.8), 12, 6.5, boxstyle="round,pad=0.3",
                          facecolor='none', edgecolor='#10B981', linewidth=2, linestyle='--', alpha=0.6)
ax.add_patch(env_box)
ax.text(9.5, 7.1, '🔒 Secure Local Environment (100% Offline)', fontsize=10,
        color='#10B981', ha='center', va='center', fontweight='bold')

# --- User ---
draw_box(ax, 0.3, 3.5, 2.5, 1.8, 'User', 'Security Analyst', '#3B82F6', '👤')

# --- Web UI ---
draw_box(ax, 4.2, 5, 3, 1.5, 'Flask Web Server', 'app.py / REST API', '#1E293B', '🌐')
draw_box(ax, 4.2, 2.5, 3, 1.5, 'Frontend UI', 'HTML / CSS / JavaScript', '#1E293B', '🖥️')

# --- LangChain ---
draw_box(ax, 8.5, 3.8, 2.5, 1.5, 'LangChain', 'Orchestration Layer', '#6366F1', '🦜')

# --- ChromaDB ---
draw_box(ax, 12, 5, 3, 1.5, 'ChromaDB', 'Vector Database', '#10B981', '📚')

# --- Ollama ---
draw_box(ax, 12, 2.5, 3, 1.5, 'Ollama Engine', 'Local Inference', '#8B5CF6', '⚙️')

# --- Models (sub-boxes under Ollama) ---
draw_box(ax, 12.1, 0.9, 1.3, 1.0, 'nomic', 'Embeddings', '#7C3AED', '🔢')
draw_box(ax, 13.6, 0.9, 1.3, 1.0, 'LLM', 'CyberSec-Llama2', '#7C3AED', '🧠')

# --- Arrows ---
draw_arrow(ax, 2.8, 4.4, 4.2, 4.0, 'HTTP Request')
draw_arrow(ax, 4.2, 3.8, 2.8, 3.8, 'JSON Response')
draw_arrow(ax, 5.7, 5.0, 5.7, 4.0, '', '#475569')
draw_arrow(ax, 7.2, 5.5, 8.5, 4.8, '')
draw_arrow(ax, 7.2, 3.3, 8.5, 4.0, '')
draw_arrow(ax, 11, 4.8, 12, 5.5, 'Semantic Search')
draw_arrow(ax, 11, 4.2, 12, 3.5, 'LLM Inference')
draw_arrow(ax, 12.7, 2.5, 12.7, 1.9, '', '#7C3AED')
draw_arrow(ax, 14.2, 2.5, 14.2, 1.9, '', '#7C3AED')

plt.tight_layout()
plt.savefig('diagrams/01_system_architecture.png', dpi=200, bbox_inches='tight',
            facecolor='#0B0F19', edgecolor='none')
plt.close()
print("Created: diagrams/01_system_architecture.png")
