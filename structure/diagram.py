import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import numpy as np
from matplotlib import font_manager
import matplotlib as mpl

# Set high-quality rendering
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

# Add professional font if available, otherwise use default
try:
    # For Windows
    font_path = 'C:/Windows/Fonts/segoeui.ttf'  
    prop = font_manager.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = prop.get_name()
except:
    plt.rcParams['font.family'] = 'sans-serif'
    
# Set modern style
plt.style.use('seaborn-v0_8-whitegrid')
mpl.rcParams['axes.grid'] = False

def draw_rounded_rectangle(ax, x, y, width, height, radius=0.1, color='white', alpha=1.0, linewidth=1.5):
    """Draw a rectangle with rounded corners."""
    # Define the path
    verts = [
        (x, y + radius),
        (x, y + height - radius),
        (x + radius, y + height),
        (x + width - radius, y + height),
        (x + width, y + height - radius),
        (x + width, y + radius),
        (x + width - radius, y),
        (x + radius, y),
        (x, y + radius),
    ]
    
    codes = [Path.MOVETO] + [Path.LINETO] * 7 + [Path.CLOSEPOLY]
    path = Path(verts, codes)
    
    # Draw the path
    patch = patches.PathPatch(path, facecolor=color, alpha=alpha, linewidth=linewidth, edgecolor='black')
    ax.add_patch(patch)
    
    return patch

def draw_fancy_arrow(ax, x1, y1, x2, y2, color='#505050', width=0.02, head_width=0.1, head_length=0.1, alpha=0.8):
    """Draw a fancy arrow from (x1, y1) to (x2, y2)."""
    ax.arrow(x1, y1, x2-x1, y2-y1, 
             width=width, head_width=head_width, head_length=head_length, 
             fc=color, ec=color, length_includes_head=True, alpha=alpha,
             shape='full')

def create_financebot_architecture():
    # Create figure and axis with higher resolution
    fig, ax = plt.subplots(figsize=(14, 12), constrained_layout=True)
    
    # Set axis limits
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    
    # Remove axes
    ax.axis('off')
    
    # Define colors with higher saturation
    colors = {
        'onboarding': '#FFD180',      # Light orange
        'main': '#A5D6A7',            # Light green
        'intent': '#90CAF9',          # Light blue
        'handler': '#D1C4E9',         # Light purple
        'error': '#FFAB91',           # Light coral
        'end': '#CFD8DC',             # Light gray
        'external': '#FFF59D'         # Light yellow
    }
    
    # Title and subtitle with shadow effect
    ax.text(5, 9.8, 'FinanceBot Architecture Diagram', 
            horizontalalignment='center', fontsize=22, fontweight='bold',
            bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.5', edgecolor='none'))
    
    # Draw main components with rounded corners and shadow effects
    
    # Onboarding
    draw_rounded_rectangle(ax, 3.5, 8.3, 3, 1.1, radius=0.2, color=colors['onboarding'])
    ax.text(5, 9.05, 'Onboarding Page', horizontalalignment='center', 
            fontsize=14, fontweight='bold')
    ax.text(3.75, 8.8, "• Welcome message", fontsize=11)
    ax.text(3.75, 8.6, "• User info collection", fontsize=11)
    ax.text(3.75, 8.4, "• Input validation", fontsize=11)
    
    # Main Chat Interface
    draw_rounded_rectangle(ax, 3.5, 6.6, 3, 1.1, radius=0.2, color=colors['main'])
    ax.text(5, 7.35, 'Main Chat Interface', horizontalalignment='center', 
            fontsize=14, fontweight='bold')
    ax.text(3.75, 7.1, "• User input processing", fontsize=11)
    ax.text(3.75, 6.9, "• Chat history display", fontsize=11)
    ax.text(3.75, 6.7, "• Message submission", fontsize=11)
    
    # External Services
    draw_rounded_rectangle(ax, 0.5, 6.6, 2.3, 1.1, radius=0.2, color=colors['external'])
    ax.text(1.65, 7.35, 'External Services', horizontalalignment='center', 
            fontsize=14, fontweight='bold')
    ax.text(0.75, 7.1, "• OpenAI API", fontsize=11)
    ax.text(0.75, 6.9, "• Cryptocurrency API", fontsize=11)
    
    # Session State
    draw_rounded_rectangle(ax, 7.2, 6.6, 2.3, 1.1, radius=0.2, color=colors['external'])
    ax.text(8.35, 7.35, 'Session State', horizontalalignment='center', 
            fontsize=14, fontweight='bold')
    ax.text(7.45, 7.1, "• User data", fontsize=11)
    ax.text(7.45, 6.9, "• Chat history", fontsize=11)
    ax.text(7.45, 6.7, "• Expenses", fontsize=11)
    
    # Intent Classification
    draw_rounded_rectangle(ax, 3.5, 5.1, 3, 1, radius=0.2, color=colors['intent'])
    ax.text(5, 5.8, 'Intent Classification', horizontalalignment='center', 
            fontsize=14, fontweight='bold')
    ax.text(3.75, 5.5, "• AI-powered classification", fontsize=11)
    ax.text(3.75, 5.3, "• Intent routing", fontsize=11)
    
    # Intent Handlers
    # Budget Setup
    draw_rounded_rectangle(ax, 0.8, 3.2, 2, 1.4, radius=0.2, color=colors['handler'])
    ax.text(1.8, 4.3, 'Budget Setup', horizontalalignment='center', 
            fontsize=14, fontweight='bold')
    ax.text(1.0, 4.0, "• 50/30/20 rule", fontsize=11)
    ax.text(1.0, 3.7, "• Personalized", fontsize=11)
    ax.text(1.0, 3.5, "  recommendations", fontsize=11)
    
    # Expense Tracking
    draw_rounded_rectangle(ax, 3, 3.2, 2, 1.4, radius=0.2, color=colors['handler'])
    ax.text(4, 4.3, 'Expense Tracking', horizontalalignment='center', 
            fontsize=14, fontweight='bold')
    ax.text(3.2, 4.0, "• Category selection", fontsize=11)
    ax.text(3.2, 3.7, "• Amount tracking", fontsize=11)
    ax.text(3.2, 3.4, "• Data storage", fontsize=11)
    
    # Investment Tips
    draw_rounded_rectangle(ax, 5.2, 3.2, 2, 1.4, radius=0.2, color=colors['handler'])
    ax.text(6.2, 4.3, 'Investment Tips', horizontalalignment='center', 
            fontsize=14, fontweight='bold')
    ax.text(5.4, 4.0, "• Income-based advice", fontsize=11)
    ax.text(5.4, 3.7, "• Crypto price info", fontsize=11)
    ax.text(5.4, 3.4, "• AI-generated tips", fontsize=11)
    
    # Reports & Help
    draw_rounded_rectangle(ax, 7.4, 3.2, 2, 1.4, radius=0.2, color=colors['handler'])
    ax.text(8.4, 4.3, 'Reports & Help', horizontalalignment='center', 
            fontsize=14, fontweight='bold')
    ax.text(7.6, 4.0, "• Expense summary", fontsize=11)
    ax.text(7.6, 3.7, "• Visualizations", fontsize=11)
    ax.text(7.6, 3.4, "• Guidance", fontsize=11)
    
    # Error & Fallback
    draw_rounded_rectangle(ax, 3.5, 1.6, 3, 1.1, radius=0.2, color=colors['error'])
    ax.text(5, 2.35, 'Error & Fallback Handling', horizontalalignment='center', 
            fontsize=14, fontweight='bold')
    ax.text(3.75, 2.1, "• Error tracking", fontsize=11)
    ax.text(3.75, 1.9, "• Guidance", fontsize=11)
    ax.text(3.75, 1.7, "• Redirection", fontsize=11)
    
    # End Session
    draw_rounded_rectangle(ax, 3.5, 0.1, 3, 1.1, radius=0.2, color=colors['end'])
    ax.text(5, 0.85, 'End Session Page', horizontalalignment='center', 
            fontsize=14, fontweight='bold')
    ax.text(3.75, 0.6, "• Summary", fontsize=11)
    ax.text(3.75, 0.4, "• Financial tips", fontsize=11)
    ax.text(3.75, 0.2, "• Restart options", fontsize=11)
    
    # Draw arrows with better styling
    # Onboarding to Chat Interface
    draw_fancy_arrow(ax, 5, 8.3, 5, 7.7)
    
    # External Services to Chat Interface
    draw_fancy_arrow(ax, 2.8, 7.15, 3.5, 7.15)
    
    # Chat Interface to Session State
    draw_fancy_arrow(ax, 6.5, 7.15, 7.2, 7.15)
    
    # Chat Interface to Intent Classification
    draw_fancy_arrow(ax, 5, 6.6, 5, 6.1)
    
    # Intent Classification to Handlers
    # Central vertical line
    draw_fancy_arrow(ax, 5, 5.1, 5, 4.6)
    
    # Horizontal connectors
    ax.plot([1.8, 8.4], [4.6, 4.6], 'k-', linewidth=1.5, alpha=0.8)
    
    # Vertical connectors to each handler
    draw_fancy_arrow(ax, 1.8, 4.6, 1.8, 4.6)
    draw_fancy_arrow(ax, 4, 4.6, 4, 4.6)
    draw_fancy_arrow(ax, 6.2, 4.6, 6.2, 4.6)
    draw_fancy_arrow(ax, 8.4, 4.6, 8.4, 4.6)
    
    # Error Handling
    draw_fancy_arrow(ax, 5, 3.2, 5, 2.7)
    
    # End Session
    draw_fancy_arrow(ax, 5, 1.6, 5, 1.2)
    
    # Add legend with color coding
    legend_height = 0.25
    legend_width = 0.35
    legend_items = [
        {"label": "Onboarding", "color": colors['onboarding']},
        {"label": "Main Interface", "color": colors['main']},
        {"label": "Intent Processing", "color": colors['intent']},
        {"label": "Intent Handlers", "color": colors['handler']},
        {"label": "Error Handling", "color": colors['error']},
        {"label": "Session End", "color": colors['end']},
        {"label": "External Components", "color": colors['external']}
    ]
    
    # Create legend at bottom
    for i, item in enumerate(legend_items):
        x_pos = 0.75 + (i * 1.2)
        y_pos = 0.25
        rect = patches.Rectangle((x_pos, y_pos-0.15), legend_width, legend_height, 
                                 facecolor=item["color"], edgecolor='black',
                                 linewidth=1, alpha=0.7)
        ax.add_patch(rect)
        ax.text(x_pos + 0.4, y_pos, item["label"], fontsize=9, 
                horizontalalignment='center', verticalalignment='center')
    
    # Save with transparent background and high resolution
    plt.tight_layout()
    plt.savefig('financebot_architecture_revised.png', dpi=300, bbox_inches='tight', transparent=False)
    plt.close()
    
    print("Enhanced architecture diagram saved as 'financebot_architecture.png'")

if __name__ == "__main__":
    create_financebot_architecture()




