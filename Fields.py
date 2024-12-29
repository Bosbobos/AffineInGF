import re
from collections import defaultdict
import galois_field as gf

conway = defaultdict(lambda: defaultdict(list))

def ReadConwayFromFile():
    global conway
    with open('ConwayPolinomials.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line == "0;":
                continue

            if line.endswith(","):
                line = line[:-1]

            # Regular expression to extract data
            match = re.match(r"\[(\d+),(\d+),\[(.*?)\]\]", line)
            if match:
                p = int(match.group(1))
                n = int(match.group(2))
                coefficients = [int(x) for x in match.group(3).split(",")]
                conway[p][n] = coefficients[::-1]

def CreateGFpn(p, n = None, mod_poly = None):
    if mod_poly is None:
        if n is None: raise ValueError('Either n or mod_poly must be specified')
        if len(conway) == 0:
            ReadConwayFromFile()
        if len(conway[p][n]) == 0:
            raise ValueError(f'No Conway for the given p ({p}) and n ({n}). Please create a polinomial of your own or choose other values')
        mod_poly = conway[p][n]

    return gf.GFpn(p, mod_poly)
