import plotly.express as px


def plot_deck_cmc_curve(deck):
    # mainboard = CardMainboard.objects.filter(mainboard=deck)
    # mainboard = deck.cardmainboard_set.all()
    mainboard = deck.cardmainboard_set.exclude(card__type_line__icontains='Land')  # exclude Lands
    quantities = list(mainboard.values_list('quantity', flat=True))
    cmcs = list(mainboard.values_list('card__cmc', flat=True))
    cmcs = [int(cmc) for cmc in cmcs]
    
    x_cmc = []
    y_n_cards = []
    for i in range(max(cmcs)+1):
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
        margin=dict(l=0, r=0, t=5, b=0),  # Remove margins
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=250,
        xaxis = dict(
            tickmode = 'linear',
            # tick0 = 0,
            dtick = 1,
            showline=True,
            linecolor='black'
        ),
        yaxis=dict(visible=False),
    )

    fig.update_traces(textposition='outside', cliponaxis=False)

    return fig
