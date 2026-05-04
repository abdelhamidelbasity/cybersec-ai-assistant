"""
CyberGuard AI - Fine-Tuning Pipeline Diagram
Libraries: matplotlib
Generates: diagrams/02_finetuning_pipeline.png
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(1, 1, figsize=(16, 8))
fig.patch.set_facecolor('#0B0F19')
ax.set_facecolor('#0B0F19')
ax.set_xlim(0, 16)
ax.set_ylim(0, 8)
ax.axis('off')

ax.text(8, 7.5, 'Phase 1 — Fine-Tuning Pipeline (QLoRA)', fontsize=22, fontweight='bold',
        color='white', ha='center', va='center')
ax.text(8, 7.05, 'Training Llama-2 7B as a Cybersecurity Expert using Parameter-Efficient Methods',
        fontsize=11, color='#94A3B8', ha='center', va='center')

def draw_step(ax, x, y, w, h, title, desc, color, step_num=''):
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.12",
                          facecolor=color, edgecolor='white', linewidth=1.2, alpha=0.85)
    ax.add_patch(box)
    if step_num:
        circle = plt.Circle((x + 0.3, y + h - 0.25), 0.18, color='white', alpha=0.2)
        ax.add_patch(circle)
        ax.text(x + 0.3, y + h - 0.25, step_num, fontsize=8, fontweight='bold',
                ha='center', va='center', color='white')
    ax.text(x + w/2, y + h*0.6, title, fontsize=10, fontweight='bold',
            ha='center', va='center', color='white')
    ax.text(x + w/2, y + h*0.22, desc, fontsize=7.5,
            ha='center', va='center', color='#CBD5E1', wrap=True)

def arrow_right(ax, x1, y1, x2, y2, label=''):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color='#F59E0B', lw=2.5))
    if label:
        ax.text((x1+x2)/2, y1 + 0.25, label, fontsize=7, ha='center', color='#F59E0B')

# Row 1: Data Preparation
draw_step(ax, 0.5, 4.5, 3, 1.8, '📁 Cybersecurity Dataset', '5000+ Q&A pairs\nCausal Reasoning Format', '#B45309', '1')
arrow_right(ax, 3.5, 5.4, 4.3, 5.4)
draw_step(ax, 4.3, 4.5, 3, 1.8, '🔧 Data Preparation', 'Format to Instruction\nTuning Template (Alpaca)', '#92400E', '2')
arrow_right(ax, 7.3, 5.4, 8.1, 5.4)

# Row 1 continued: Training
draw_step(ax, 8.1, 4.5, 3.5, 1.8, '💻 QLoRA Training', 'Unsloth + Google Colab T4\n4-bit Quantization', '#3B82F6', '3')
arrow_right(ax, 11.6, 5.4, 12.4, 5.4)
draw_step(ax, 12.4, 4.5, 3, 1.8, '📦 LoRA Adapter', 'Trained Weights\n~160 MB only', '#6366F1', '4')

# Arrow down from LoRA to Row 2
ax.annotate('', xy=(13.9, 3.3), xytext=(13.9, 4.5),
            arrowprops=dict(arrowstyle='->', color='#F59E0B', lw=2.5))

# Row 2: Conversion & Deployment
draw_step(ax, 12.4, 1.5, 3, 1.8, '🔄 GGUF Conversion', 'llama.cpp Quantization\nCPU-Optimized Format', '#0F766E', '5')

ax.annotate('', xy=(12.4, 2.4), xytext=(11.4, 2.4),
            arrowprops=dict(arrowstyle='->', color='#F59E0B', lw=2.5))

draw_step(ax, 8.1, 1.5, 3.3, 1.8, '⚙️ Ollama Registration', 'Custom Modelfile\n+ System Prompt', '#0E7490', '6')

ax.annotate('', xy=(8.1, 2.4), xytext=(7.1, 2.4),
            arrowprops=dict(arrowstyle='->', color='#F59E0B', lw=2.5))

draw_step(ax, 3.8, 1.5, 3.3, 1.8, '🚀 Ready for Use!', 'cybersec-assistant\nmodel on Ollama', '#10B981', '7')

# Base Model note
draw_step(ax, 0.5, 1.5, 2.8, 1.8, '🤖 Llama-2 7B Base', 'NousResearch\nOpen-Source LLM', '#7C3AED', '')
ax.annotate('', xy=(8.1, 5.9), xytext=(3.3, 2.9),
            arrowprops=dict(arrowstyle='->', color='#A78BFA', lw=1.5, linestyle='dashed'))
ax.text(5.2, 4.6, 'Base weights', fontsize=7, color='#A78BFA', rotation=30)

plt.tight_layout()
plt.savefig('diagrams/02_finetuning_pipeline.png', dpi=200, bbox_inches='tight',
            facecolor='#0B0F19', edgecolor='none')
plt.close()
print("Created: diagrams/02_finetuning_pipeline.png")
