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

            # Извлекаем данные с помощью регулярного выражения
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
        mod_poly = conway[p][n]

    return gf.GFpn(p, mod_poly)

def ElementIsInversible(elem: gf.ElementInGFpn):
    prod = elem * elem.inverse()
    return prod.coeffs == [1]