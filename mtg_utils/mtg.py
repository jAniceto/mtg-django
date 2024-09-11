"""
Utility functions for MtG
"""

import collections


def color_families():
    """Dictionary to convert deck family to a list of color codes"""
    return collections.OrderedDict(
        white=['w'],
        blue=['u'],
        black=['b'],
        red=['r'],
        green=['g'],
        selesnya=['w', 'g'],
        orzhov=['w', 'b'],
        boros=['w', 'r'],
        azorius=['w', 'u'],
        dimir=['u', 'b'],
        rakdos=['b', 'r'],
        golgari=['b', 'g'],
        izzet=['u', 'r'],
        simic=['u', 'g'],
        gruul=['r', 'g'],
        naya=['w', 'r', 'g'],
        esper=['w', 'u', 'b'],
        grixis=['u', 'b', 'r'],
        jund=['b', 'r', 'g'],
        bant=['w', 'u', 'g'],
        abzan=['w', 'b', 'g'],
        temur=['u', 'r', 'g'],
        jeskai=['w', 'u', 'r'],
        mardu=['w', 'b', 'r'],
        sultai=['u', 'b', 'g'],
        glint=['u', 'b', 'r', 'g'],
        dune=['w', 'b', 'r', 'g'],
        ink=['w', 'u', 'r', 'g'],
        whitch=['w', 'u', 'b', 'g'],
        yore=['w', 'u', 'b', 'r'],
        domain=['w', 'u', 'b', 'r', 'g'],
        colorless=['c'],
    )


def symbols_html():
    """Dictionary of MtG symbols to HTML using Mana font (mana.andrewgioia.com)"""
    return {
        '{0}': '<i class="ms ms-0 ms-cost"></i>',
        '{1}': '<i class="ms ms-1 ms-cost"></i>',
        '{2}': '<i class="ms ms-2 ms-cost"></i>',
        '{3}': '<i class="ms ms-3 ms-cost"></i>',
        '{4}': '<i class="ms ms-4 ms-cost"></i>',
        '{5}': '<i class="ms ms-5 ms-cost"></i>',
        '{6}': '<i class="ms ms-6 ms-cost"></i>',
        '{7}': '<i class="ms ms-7 ms-cost"></i>',
        '{8}': '<i class="ms ms-8 ms-cost"></i>',
        '{9}': '<i class="ms ms-9 ms-cost"></i>',
        '{10}': '<i class="ms ms-10 ms-cost"></i>',
        '{11}': '<i class="ms ms-11 ms-cost"></i>',
        '{12}': '<i class="ms ms-12 ms-cost"></i>',
        '{13}': '<i class="ms ms-13 ms-cost"></i>',
        '{14}': '<i class="ms ms-14 ms-cost"></i>',
        '{15}': '<i class="ms ms-15 ms-cost"></i>',
        '{16}': '<i class="ms ms-16 ms-cost"></i>',
        '{17}': '<i class="ms ms-17 ms-cost"></i>',
        '{18}': '<i class="ms ms-18 ms-cost"></i>',
        '{19}': '<i class="ms ms-19 ms-cost"></i>',
        '{20}': '<i class="ms ms-20 ms-cost"></i>',
        '{G}': '<i class="ms ms-g ms-cost"></i>',
        '{R}': '<i class="ms ms-r ms-cost"></i>',
        '{B}': '<i class="ms ms-b ms-cost"></i>',
        '{U}': '<i class="ms ms-u ms-cost"></i>',
        '{W}': '<i class="ms ms-w ms-cost"></i>',
        '{C}': '<i class="ms ms-c ms-cost"></i>',
        '{X}': '<i class="ms ms-x ms-cost"></i>',
        '{S}': '<i class="ms ms-s ms-cost"></i>',
        '{E}': '<i class="ms ms-e ms-cost"></i>',
        '{G/P}': '<i class="ms ms-cost ms-p ms-g"></i>',
        '{R/P}': '<i class="ms ms-cost ms-p ms-r"></i>',
        '{B/P}': '<i class="ms ms-cost ms-p ms-b"></i>',
        '{U/P}': '<i class="ms ms-cost ms-p ms-u"></i>',
        '{W/P}': '<i class="ms ms-cost ms-p ms-w"></i>',
        '{G/R}': '<i class="ms ms-rg ms-split ms-cost"></i>',
        '{G/B}': '<i class="ms ms-gb ms-split ms-cost"></i>',
        '{G/U}': '<i class="ms ms-gu ms-split ms-cost"></i>',
        '{G/W}': '<i class="ms ms-gw ms-split ms-cost"></i>',
        '{R/G}': '<i class="ms ms-rg ms-split ms-cost"></i>',
        '{R/B}': '<i class="ms ms-rb ms-split ms-cost"></i>',
        '{R/U}': '<i class="ms ms-ru ms-split ms-cost"></i>',
        '{R/W}': '<i class="ms ms-rw ms-split ms-cost"></i>',
        '{B/R}': '<i class="ms ms-br ms-split ms-cost"></i>',
        '{B/G}': '<i class="ms ms-bg ms-split ms-cost"></i>',
        '{B/U}': '<i class="ms ms-bu ms-split ms-cost"></i>',
        '{B/W}': '<i class="ms ms-bw ms-split ms-cost"></i>',
        '{U/R}': '<i class="ms ms-ur ms-split ms-cost"></i>',
        '{U/B}': '<i class="ms ms-ub ms-split ms-cost"></i>',
        '{U/G}': '<i class="ms ms-ug ms-split ms-cost"></i>',
        '{U/W}': '<i class="ms ms-uw ms-split ms-cost"></i>',
        '{W/R}': '<i class="ms ms-wr ms-split ms-cost"></i>',
        '{W/B}': '<i class="ms ms-wb ms-split ms-cost"></i>',
        '{W/U}': '<i class="ms ms-wu ms-split ms-cost"></i>',
        '{W/G}': '<i class="ms ms-wg ms-split ms-cost"></i>',
        '{T}': '<i class="ms ms-tap"></i>',
        '{Q}': '<i class="ms ms-untap"></i>',
    }


def mana_cost_html(mana_cost):
    """Funtion to convert mana cost symbols into HTML"""
    mana_dict = symbols_html()
    code = ''
    if mana_cost is not None:
        mana_list = [e + '}' for e in mana_cost.split('}') if e]  # split symbols
        mana_list2 = []
        [
            mana_list2.extend(idx.split(' // ')) for idx in mana_list
        ]  # detect double-faced cards and split on ' // '
        for symbol in mana_list2:
            if symbol == '':
                code += ' // '
            else:
                code += mana_dict[symbol]
    return code
