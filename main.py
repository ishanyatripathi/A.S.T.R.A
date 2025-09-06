# main.py
import importlib

print("Select a module to launch:")
print("1. H.A.N.D.S")
print("2. IRIS")

choice = input("Enter 1 or 2: ").strip()

if choice == "1":
    hands_module = importlib.import_module("hands")  # Import hands.py
    hands_module.launch()
elif choice == "2":
    iris_module = importlib.import_module("iris")  # Import iris.py
    iris_module.launch()
else:
    print("Invalid choice. Exiting.")
