"""
CyberGuard AI - RAG Ingestion Pipeline Diagram
Libraries: matplotlib
Generates: diagrams/03_rag_ingestion.png
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(1, 1, figsize=(16, 7))
fig.patch.set_facecolor('#0B0F19')
ax.set_facecolor('#0B0F19')
ax.set_xlim(0, 16)
ax.set_ylim(0, 7)
ax.axis('off')

ax.text(8, 6.5, 'Phase 2 — RAG Document Ingestion Pipeline', fontsize=22, fontweight='bold',
        color='white', ha='center', va='center')
ax.text(8, 6.05, 'Converting Security Documents into Searchable Vector Embeddings',
        fontsize=11, color='#94A3B8', ha='center', va='center')

def draw_box(ax, x, y, w, h, title, desc, color):
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.12",
                          facecolor=color, edgecolor='white', linewidth=1.2, alpha=0.85)
    ax.add_patch(box)
    ax.text(x + w/2, y + h*0.62, title, fontsize=11, fontweight='bold',
            ha='center', va='center', color='white')
    ax.text(x + w/2, y + h*0.25, desc, fontsize=8,
            ha='center', va='center', color='#CBD5E1')

def arrow(ax, x1, y1, x2, y2, label=''):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color='#10B981', lw=2.5))
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx, my + 0.3, label, fontsize=8, ha='center', color='#10B981', fontweight='bold')

# Step 1: Documents
draw_box(ax, 0.5, 2.5, 2.8, 2.2, '📄 Documents', 'PDF & TXT files\nin data/ folder', '#B45309')
# Visual: small doc icons
for i, (label, yoff) in enumerate([('report.pdf', 0.2), ('policy.txt', -0.1), ('threats.pdf', -0.4)]):
    ax.text(1.9, 3.6 + yoff, f'  📋 {label}', fontsize=6.5, color='#FCD34D', fontfamily='monospace')

arrow(ax, 3.3, 3.6, 4.2, 3.6, 'Load')

# Step 2: Document Loader
draw_box(ax, 4.2, 2.5, 2.5, 2.2, '📥 Doc Loader', 'LangChain\nPyPDFLoader\nTextLoader', '#0E7490')

arrow(ax, 6.7, 3.6, 7.5, 3.6, 'Split')

# Step 3: Text Splitter
draw_box(ax, 7.5, 2.5, 2.5, 2.2, '✂️ Text Splitter', 'Chunk Size: 800\nOverlap: 100\nRecursive', '#3B82F6')

# Visual: chunks
for i, yoff in enumerate([0.8, 0.4, 0, -0.4]):
    chunk_box = FancyBboxPatch((7.7, 2.8 + yoff*0.5 + 1.3), 0.4, 0.3,
                                boxstyle="round,pad=0.05", facecolor='#60A5FA', alpha=0.3,
                                edgecolor='#93C5FD', linewidth=0.8)
    ax.add_patch(chunk_box)

arrow(ax, 10, 3.6, 10.8, 3.6, 'Embed')

# Step 4: Embedding Model
draw_box(ax, 10.8, 2.5, 2.5, 2.2, '🔢 Embeddings', 'nomic-embed-text\nvia Ollama\n768-dim vectors', '#6366F1')

arrow(ax, 13.3, 3.6, 14.1, 3.6, 'Store')

# Step 5: Vector Database
draw_box(ax, 14.1, 2.5, 1.5, 2.2, '💾 ChromaDB', 'Local\nVector\nStore', '#10B981')

# Bottom explanation boxes
info_data = [
    (1.2, 0.5, 'Input', 'Raw security\ndocuments', '#B45309'),
    (4.7, 0.5, 'Parse', 'Extract text\nfrom files', '#0E7490'),
    (8.0, 0.5, 'Chunk', '800-character\ntext segments', '#3B82F6'),
    (11.3, 0.5, 'Vectorize', 'Numerical\nrepresentations', '#6366F1'),
    (14.3, 0.5, 'Persist', 'Ready for\nsearch', '#10B981'),
]
for x, y, title, desc, color in info_data:
    ax.text(x, y + 0.55, title, fontsize=9, fontweight='bold', ha='center', color=color)
    ax.text(x, y + 0.1, desc, fontsize=7, ha='center', color='#94A3B8')

plt.tight_layout()
plt.savefig('diagrams/03_rag_ingestion.png', dpi=200, bbox_inches='tight',
            facecolor='#0B0F19', edgecolor='none')
plt.close()
print("Created: diagrams/03_rag_ingestion.png")
