import plotly.express as px
import pandas as pd
from django.db.models import Count
from mtg_utils.mtg import color_families


def plot_deck_cmc_curve(deck):
    """Creates a Plotly barplot to display the mana curve."""
    mainboard = deck.cardmainboard_set.exclude(card__type_line__icontains='Land')  # exclude Lands
    quantities = list(mainboard.values_list('quantity', flat=True))
    cmcs = list(mainboard.values_list('card__cmc', flat=True))
    cmcs = [int(cmc) for cmc in cmcs]

    x_cmc = []
    y_n_cards = []
    for i in range(max(cmcs) + 1):
        x_cmc.append(i)

        n_card = 0
        for qty, cmc in zip(quantities, cmcs):
            if i == cmc:
                n_card += qty
        y_n_cards.append(n_card)

    fig = px.bar(x=x_cmc, y=y_n_cards, text_auto=True, color_discrete_sequence=['#7B8A8B'])

    fig.update_layout(
        # title='CMC Distribution',
        xaxis_title='Converted mana cost',
        margin=dict(l=0, r=0, t=8, b=0),  # Remove margins
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=250,
        xaxis=dict(
            tickmode='linear',
            # tick0 = 0,
            dtick=1,
            showline=True,
            linecolor='black',
        ),
        yaxis=dict(visible=False),
    )

    fig.update_traces(textposition='outside', cliponaxis=False)

    return fig


def plot_deck_color_distribution(decks):
    """Creates a Plotly pie chart to display the deck colors."""
    color_dict = color_families()
    deck_colors = [color_dict[d.family.lower()] for d in decks if d.family is not None]

    COLORS = ['w', 'u', 'b', 'r', 'g']
    COLOR_LABELS = ['White', 'Blue', 'Black', 'Red', 'Green']

    counts = []
    for c in COLORS:
        count = 0
        for d in deck_colors:
            if c in d:
                count += 1
        counts.append(count)

    df = pd.DataFrame({
        'Color': COLOR_LABELS,
        'Count': counts,
    }).sort_values('Count')

    fig = px.pie(df, values='Count', names='Color', color='Color', color_discrete_map={'White':'#F8E7B9', 'Blue':'#B3CEEA', 'Black':'#150B00', 'Red':'#EB9F82', 'Green':'#C4D3CA'})
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        uniformtext_minsize=12, 
        uniformtext_mode='hide',
        margin=dict(l=0, r=0, t=16, b=0),  # Remove margins
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
    )
    return fig


def plot_deck_family_distribution(decks):
    """Creates a Plotly barplot to display the deck families."""
    family_counts = decks.values('family').annotate(count=Count('family'))
    counts = [f['count'] for f in family_counts if f['family'] is not None]
    families = [f['family'] for f in family_counts if f['family'] is not None]

    decks_with_no_family_count = decks.filter(family__isnull=True).count()
    counts.append(decks_with_no_family_count)
    families.append('Missing')

    df = pd.DataFrame({
        'Family': families,
        'Count': counts,
    }).sort_values('Count')
    
    fig = px.bar(df, x='Count', y='Family', text_auto=True, orientation='h', color_discrete_sequence=['#3394D5'])

    fig.update_layout(
        xaxis_title='Number of decks',
        yaxis_title=None,
        margin=dict(l=0, r=0, t=16, b=0),  # Remove margins
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=800,
        xaxis=dict(
            tickmode='linear',
            dtick=5,
            showline=True,
            linecolor='black',
        ),
    )
    fig.update_traces(textposition='outside', cliponaxis=False)
    return fig
