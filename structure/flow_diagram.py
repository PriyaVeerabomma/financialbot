import graphviz

def create_conversation_flow_diagram():
    # Create a new directed graph with improved styling
    dot = graphviz.Digraph('FinanceBot Conversation Flow', format='png')
    
    # Set graph attributes for better appearance
    dot.attr(
        rankdir='TB',  # Top to Bottom layout
        size='12,10',
        dpi='300',
        bgcolor='white',
        fontname='Arial',
        fontsize='16',
        label='FinanceBot Conversation Flow',
        labelloc='t',  # Place label at top
        concentrate='true',  # Merge edges where possible for cleaner look
        compound='true',
        splines='true',
        nodesep='0.5',
        ranksep='0.7'
    )
    
    # Create clusters for different stages of the conversation
    with dot.subgraph(name='cluster_onboarding') as c:
        c.attr(
            label='Onboarding Process',
            style='rounded,filled',
            color='#FFD180',
            fillcolor='#FFD180:white',
            gradientangle='90',
            fontname='Arial Bold',
            fontsize='14'
        )
        # Onboarding nodes
        c.node('start', 'Start', shape='oval', style='filled', fillcolor='#E8E8E8', fontname='Arial', fontsize='12')
        c.node('welcome', 'Welcome Page\n(Introduction)', shape='box', style='rounded,filled', fillcolor='#FFD180', fontname='Arial', fontsize='12', penwidth='1.5')
        c.node('user_info', 'Collect User Info\n(Name, Email, Income)', shape='box', style='rounded,filled', fillcolor='#FFD180', fontname='Arial', fontsize='12', penwidth='1.5')
        c.node('validate', 'Validate User Input', shape='box', style='rounded,filled', fillcolor='#FFD180', fontname='Arial', fontsize='12', penwidth='1.5')
    
    with dot.subgraph(name='cluster_main_interface') as c:
        c.attr(
            label='Main Interface',
            style='rounded,filled',
            color='#A5D6A7',
            fillcolor='#A5D6A7:white',
            gradientangle='90',
            fontname='Arial Bold',
            fontsize='14'
        )
        # Main interface nodes
        c.node('chat', 'Main Chat Interface', shape='box', style='rounded,filled', fillcolor='#A5D6A7', fontname='Arial', fontsize='12', penwidth='1.5')
        c.node('consent', 'Email Marketing Consent\n(Yes/No)', shape='box', style='rounded,filled', fillcolor='#A5D6A7', fontname='Arial', fontsize='12', penwidth='1.5')
        c.node('intent', 'Intent Classification', shape='box', style='rounded,filled', fillcolor='#90CAF9', fontname='Arial', fontsize='12', penwidth='1.5')
    
    with dot.subgraph(name='cluster_intent_handlers') as c:
        c.attr(
            label='Intent Handlers',
            style='rounded,filled',
            color='#D1C4E9',
            fillcolor='#D1C4E9:white',
            gradientangle='90',
            fontname='Arial Bold',
            fontsize='14'
        )
        # Intent handler nodes
        c.node('budget', 'Budget Setup\n(50/30/20 Rule)', shape='box', style='rounded,filled', fillcolor='#D1C4E9', fontname='Arial', fontsize='12', penwidth='1.5')
        c.node('expense', 'Expense Tracking\n(Add Expenses)', shape='box', style='rounded,filled', fillcolor='#D1C4E9', fontname='Arial', fontsize='12', penwidth='1.5')
        c.node('investment', 'Investment Tips\n(AI Generated Advice)', shape='box', style='rounded,filled', fillcolor='#D1C4E9', fontname='Arial', fontsize='12', penwidth='1.5')
        c.node('report', 'Spending Report\n(Charts & Metrics)', shape='box', style='rounded,filled', fillcolor='#D1C4E9', fontname='Arial', fontsize='12', penwidth='1.5')
        c.node('help', 'Help & Guidance\n(Example Queries)', shape='box', style='rounded,filled', fillcolor='#D1C4E9', fontname='Arial', fontsize='12', penwidth='1.5')
    
    with dot.subgraph(name='cluster_error_end') as c:
        c.attr(
            label='Error Handling & Session End',
            style='rounded,filled',
            color='#FFAB91',
            fillcolor='#FFAB91:white',
            gradientangle='90',
            fontname='Arial Bold',
            fontsize='14'
        )
        # Error and end nodes
        c.node('error', 'Error Handling\n(Fallback)', shape='box', style='rounded,filled', fillcolor='#FFAB91', fontname='Arial', fontsize='12', penwidth='1.5')
        c.node('goodbye', 'End Conversation\n(Farewell)', shape='box', style='rounded,filled', fillcolor='#CFD8DC', fontname='Arial', fontsize='12', penwidth='1.5')
    
    # Create edges with improved styling
    # Onboarding flow
    dot.edge('start', 'welcome', penwidth='1.2')
    dot.edge('welcome', 'user_info', penwidth='1.2')
    dot.edge('user_info', 'validate', penwidth='1.2')
    dot.edge('validate', 'user_info', label='  Invalid Input  ', fontname='Arial', fontsize='10', penwidth='1.2', color='#FF5252')
    dot.edge('validate', 'chat', label='  Valid Input  ', fontname='Arial', fontsize='10', penwidth='1.2', color='#4CAF50')
    
    # Main interface flow
    dot.edge('chat', 'consent', label='  First Time  ', fontname='Arial', fontsize='10', penwidth='1.2')
    dot.edge('consent', 'chat', label='  Response Recorded  ', fontname='Arial', fontsize='10', penwidth='1.2')
    dot.edge('chat', 'intent', label='  Message Submitted  ', fontname='Arial', fontsize='10', penwidth='1.2')
    
    # Intent routing with color-coded edges
    dot.edge('intent', 'budget', label='  budget_setup  ', fontname='Arial', fontsize='10', penwidth='1.2', color='#673AB7')
    dot.edge('intent', 'expense', label='  add_expense  ', fontname='Arial', fontsize='10', penwidth='1.2', color='#2196F3')
    dot.edge('intent', 'investment', label='  investment_tips  ', fontname='Arial', fontsize='10', penwidth='1.2', color='#009688')
    dot.edge('intent', 'report', label='  view_report  ', fontname='Arial', fontsize='10', penwidth='1.2', color='#4CAF50')
    dot.edge('intent', 'help', label='  help  ', fontname='Arial', fontsize='10', penwidth='1.2', color='#FF9800')
    dot.edge('intent', 'goodbye', label='  goodbye  ', fontname='Arial', fontsize='10', penwidth='1.2', color='#795548')
    dot.edge('intent', 'error', label='  other/unknown  ', fontname='Arial', fontsize='10', penwidth='1.2', color='#F44336')
    
    # Return to chat
    dot.edge('budget', 'chat', constraint='false', penwidth='1.2', color='#673AB7:white:white', style='tapered')
    dot.edge('expense', 'chat', constraint='false', penwidth='1.2', color='#2196F3:white:white', style='tapered')
    dot.edge('investment', 'chat', constraint='false', penwidth='1.2', color='#009688:white:white', style='tapered')
    dot.edge('report', 'chat', constraint='false', penwidth='1.2', color='#4CAF50:white:white', style='tapered')
    dot.edge('help', 'chat', constraint='false', penwidth='1.2', color='#FF9800:white:white', style='tapered')
    dot.edge('error', 'chat', constraint='false', penwidth='1.2', color='#F44336:white:white', style='tapered')
    
    # Error tracking
    dot.edge('error', 'error', label='  Error Count++  ', fontname='Arial', fontsize='10', penwidth='1.2', color='#F44336')
    
    # End conversation
    dot.edge('goodbye', 'start', label='  New Session  ', fontname='Arial', fontsize='10', penwidth='1.2', color='#795548')
    
    # Render the diagram with high quality
    try:
        # Set render options
        dot.attr(dpi='300')
        dot.format = 'png'
        
        # Render and save
        dot.render('financebot_conversation_flow', cleanup=True)
        print("Enhanced conversation flow diagram saved as 'financebot_conversation_flow.png'")
        
        # Also save the DOT file for reference
        with open('financebot_conversation_flow.dot', 'w') as f:
            f.write(dot.source)
        print("Diagram source saved as 'financebot_conversation_flow.dot'")
        
    except Exception as e:
        print(f"Error rendering diagram: {e}")
        print("Saving DOT file only...")
        with open('financebot_conversation_flow.dot', 'w') as f:
            f.write(dot.source)
        print("To visualize, go to https://dreampuf.github.io/GraphvizOnline/ and paste the content")

if __name__ == "__main__":
    create_conversation_flow_diagram()



