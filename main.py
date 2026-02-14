from stock import *

def format_output(price: float, eps: float, eps_growth: float) -> None:
    pe_ratio = calculate_pe_ratio(price, eps)
    print("PE ratio:\t", pe_ratio)
    print("PEG ratio: \t", calculate_peg_ratio(pe_ratio, eps_growth))

def main():
    price = float(input("price: "))
    eps = float(input("eps: "))
    eps_growth = float(input("growth rate (%): "))

    format_output(price, eps, eps_growth)

if __name__ == "__main__":
    main()
