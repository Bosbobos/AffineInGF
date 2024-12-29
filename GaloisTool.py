from galois import GF, irreducible_poly
import galois

def build_galois_field(p, n):
    return GF(p**n, repr='poly')

def generate_irreducible_polynomial(p, n):
    return irreducible_poly(p, n)

def add_polynomials(field, poly1, poly2):
    return poly1 + poly2

def multiply_polynomials(field, poly1, poly2):
    return poly1 * poly2

def find_primitive_elements(field):
    field.repr("poly")
    return field.primitive_elements

def decompose_elements(field, generator):
    res = []
    for i in range(field.order):
        res.append(generator**i)

    return res
