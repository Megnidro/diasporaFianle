from django import template
from collections import defaultdict

register = template.Library()


@register.filter
def top_pays(data, args):
    pays_totals = defaultdict(int)
    for juridiction in data.values():
        for pays, pays_data in juridiction['Pays'].items():
            pays_totals[pays] += pays_data['total']
    return sorted(pays_totals.items(), key=lambda x: x[1], reverse=True)[:int(args)]
