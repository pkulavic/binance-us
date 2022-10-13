from binance import BinanceUS

def print_profits():
    b = BinanceUS()
    for t in b.triangle_triples():
        try:
            print(t[2] + '|' + t[1] + '|' + t[0] + ': ' + str(b.compute_profit(*t)))
        except IndexError:
            print(t[2] + '|' + t[1] + '|' + t[0] + ': ' + 'indexError')

def main():
    print_profits()

if __name__ == "__main__":
    main()
