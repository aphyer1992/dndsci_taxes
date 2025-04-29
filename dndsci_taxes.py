import math
import random

goods_list = [
    
    {'long_name' : 'Cockatrice Eye', 'short_name' : 'C', 'value' : 6},
    {'long_name' : 'Dragon Head', 'short_name' : 'D', 'value' : 14},
    {'long_name' : 'Lich Skull', 'short_name' : 'L', 'value' : 10},
    {'long_name' : 'Unicorn Horn', 'short_name' : 'U', 'value' : 7},
    {'long_name' : 'Zombie Hand', 'short_name' : 'Z', 'value' : 2},
]

goods_lookup = {}
for g in goods_list:
    goods_lookup[g['short_name']] = g

tax_brackets = [
    {'threshold' : 0, 'rate' : 0.2},
    {'threshold' : 30, 'rate' : 0.3},
    {'threshold' : 60, 'rate' : 0.4},
    {'threshold' : 100, 'rate' : 0.5},
    {'threshold' : 300, 'rate' : 0.6},
    ]

global_file_loc = 'dndsci_tax.csv'

def calc_tax(taxed_goods):
    total_value = sum([taxed_goods[g['short_name']] * g['value'] for g in goods_list])
    tax_rate = max([b['rate'] for b in tax_brackets if b['threshold'] <= total_value])

    if taxed_goods['C'] == 0 and taxed_goods['D'] == 0 and taxed_goods['U'] == 0:
        tax_rate = 0.1

    if taxed_goods['U'] >= 5:
        tax_rate = min(tax_rate, 0.25)

    tax = total_value * tax_rate

    if taxed_goods['D'] > 1:
        tax = tax + (tax_rate * goods_lookup['D']['value'] * (taxed_goods['D'] - 1))

    tax = tax - (math.ceil(taxed_goods['C'] / 2) * 6)

    tax = max(tax, 0 )

    return(tax)

def write_row(row, mode='a'):
        row_string = ','.join([str(e) for e in row])+"\n"
        f = open(global_file_loc, mode)
        f.write(row_string)

def setup_csv():
    row = [g['long_name'] for g in goods_list]
    row.append('Tax Assessed')
    write_row(row, mode='w')

def tax_string(taxes):
    gold = math.floor(taxes)
    silver = round((taxes - gold) * 10)

    string = '{} gp {} sp'.format(gold, silver)
    return(string)

def gen_dataset():
    for i in range(18188):
        if i%1000 == 0:
            print(i)
        overall = {
            'C' : max(0, random.choice(list(range(-4, 12)))),
            'D' : max(0, random.choice(list(range(-4, 8)))),
            'L' : max(0, random.choice(list(range(-4, 10)))),
            'U' : max(0, random.choice(list(range(-4, 16)))),
            'Z' : max(0, random.choice(list(range(-8, 30)))),
        }
        num_adventurers = random.choice(list(range(1, 6)))
        loots = []
        for a in range(num_adventurers):
            loots.append({'C' : 0, 'D': 0, 'L': 0, 'U': 0, 'Z' : 0})
        for g in ['C', 'D', 'L', 'U', 'Z']:
            num = overall[g]
            random.shuffle(loots)
            while num >= num_adventurers:
                num -= num_adventurers
                for l in loots:
                    l[g] += 1
            for i in range(num):
                loots[i][g] += 1
        for l in loots:
            if sum(l.values()) > 0:
                taxes = calc_tax(l)
                row = [l['C'], l['D'], l['L'], l['U'], l['Z'], tax_string(taxes)]
                write_row(row)

random.seed("IRS")
setup_csv()
gen_dataset()
