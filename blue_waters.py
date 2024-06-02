import os
import traceback
from model import MonteCarloModel as m

def show_splash_screen():
    os.system('clear')
    print("***************************************************")
    print("*               Welcome to BlueWaters             *")
    print("*         March Madness Portfolio Optimizer       *")
    print("***************************************************")

def show_menu():
    print("\nChoose an option:")
    print("1. Model Validation")
    print("2. Portfolio Optimization")
    print("3. Command Line")
    print("0. Exit")

def model_validation():
    print("You chose Model Validation. Implement your logic here.")

def portfolio_optimization():
    print("You chose Portfolio Optimization. Implement your logic here.")

def command_line():
    while True:
        try:
            exec(input(">"))
        except Exception:
            traceback.print_exc()


def main():
    show_splash_screen()

    while True:
        show_menu()
        choice = input("Enter the number of your choice (0 to exit): ")

        if choice == "1":
            model_validation()
        elif choice == "2":
            portfolio_optimization()
        elif choice == "3":
            command_line()
        elif choice == "0":
            print("Exiting BlueWaters. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()