import math


# calculates the array representation form of the continued fraction of the number r
def calculate_continued_fraction(r, iterations):
    result = []
    for i in range(iterations):
        result += [math.floor(r)]
        r -= math.floor(r)
        if r == 0:
            return result
        r = 1 / r
    return result


# returns an integer and 1 if the array representation is just a single integer
# (for consistency)
def calculate_rational_from_continued(array_representation):
    p = 1
    q = array_representation.pop()

    while len(array_representation) > 0:
        c = array_representation.pop()
        p, q = q, c * q + p

    return q, p


# calculates an optimal rational approximation for the given ratio
# limit refers to the maximum value for the denominator
def get_fractional_representation_under_limit(ratio, limit=100):
    c_f = calculate_continued_fraction(ratio, 1)
    r_f = calculate_rational_from_continued(c_f)

    old_result = r_f

    iterations = 2

    while r_f[1] <= limit:
        c_f = calculate_continued_fraction(ratio, iterations)
        r_f = calculate_rational_from_continued(c_f)

        if r_f[1] > limit or r_f == old_result:
            return old_result
        else:
            old_result = r_f

        iterations += 1
