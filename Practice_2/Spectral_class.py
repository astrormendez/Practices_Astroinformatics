import sys

def spec_type(T):
    if 30000 <= T <= 60000:
        return 'O'
    elif 10000 <= T < 30000:
        return 'B'
    elif 7500 <= T < 10000:
        return 'A'
    elif 6000 <= T < 7500:
        return 'F'
    elif 5000 <= T < 6000:
        return 'G'
    elif 3500 <= T < 5000:
        return 'K'
    elif 2000 <= T < 3500:
        return 'M'
    else:
        return 'Temperature out of range.'

temp = float(sys.argv[1])

print(f'Spectral class of {temp} is: {spec_type(temp)}')