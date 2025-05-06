import os
from tabulate import tabulate  # Optional: for better table formatting

# ========The beginning of the class==========
class Shoe:
    """
    Represents a single shoe item in the inventory.

    Attributes:
        country (str): The country of origin.
        code (str): The unique code for the shoe.
        product (str): The name of the shoe model.
        cost (float): The cost of one unit of the shoe.
        quantity (int): The number of units currently in stock.
    """

    def __init__(self, country, code, product, cost, quantity):
        """Initialises the Shoe object."""
        self.country = country
        self.code = code
        self.product = product
        # Ensure cost and quantity are stored as appropriate numeric types
        try:
            self.cost = float(cost)
        except ValueError:
            print(
                f"Error: Invalid cost '{cost}' for shoe {code}. Setting cost to 0.0."
            )
            self.cost = 0.0
        try:
            self.quantity = int(quantity)
        except ValueError:
            print(
                f"Error: Invalid quantity '{quantity}' for shoe {code}. Setting quantity to 0."
            )
            self.quantity = 0

    def get_cost(self):
        """Returns the cost of the shoe."""
        return self.cost

    def get_quantity(self):
        """Returns the quantity of the shoes."""
        return self.quantity

    def __str__(self):
        """Returns a string representation of the Shoe object."""
        return (
            f"Country:  {self.country}\n"
            f"Code:     {self.code}\n"
            f"Product:  {self.product}\n"
            f"Cost:     {self.cost:.2f}\n"
            f"Quantity: {self.quantity}"
        )

    def to_file_string(self):
        """Returns a comma-separated string for writing to the file."""
        return f"{self.country},{self.code},{self.product},{self.cost},{self.quantity}"


# =============Shoe list===========
# The list will be used to store a list of objects of shoes.
shoe_list = []
INVENTORY_FILE = "inventory.txt"


# ==========Functions outside the class==============
def read_shoes_data():
    """
    Reads shoe data from inventory.txt, creates Shoe objects,
    and appends them to the global shoe_list.
    Skips the header row and handles potential errors.
    """
    global shoe_list
    shoe_list = (
        []
    )  # Clear the list before reading to avoid duplicates if called again
    try:
        with open(INVENTORY_FILE, "r") as f:
            # Skip the header line
            next(f)
            for line in f:
                try:
                    # Strip whitespace and split by comma
                    data = line.strip().split(",")
                    # Check if the line has the correct number of elements
                    if len(data) == 5:
                        country, code, product, cost, quantity = data
                        # Create Shoe object and add to list
                        shoe_list.append(Shoe(country, code, product, cost, quantity))
                    else:
                        print(f"Warning: Skipping malformed line: {line.strip()}")
                except ValueError as e:
                    print(
                        f"Warning: Skipping line due to data error: {line.strip()} - {e}"
                    )
                except Exception as e:
                    print(
                        f"Warning: An unexpected error occurred processing line: {line.strip()} - {e}"
                    )
        print(f"Successfully loaded {len(shoe_list)} shoes from {INVENTORY_FILE}.")
    except FileNotFoundError:
        print(f"Error: The file {INVENTORY_FILE} was not found.")
        # Optional: Create the file with headers if it doesn't exist
        try:
            with open(INVENTORY_FILE, "w") as f:
                f.write("Country,Code,Product,Cost,Quantity\n")
            print(f"{INVENTORY_FILE} created with headers.")
        except IOError:
            print(f"Error: Could not create {INVENTORY_FILE}.")
    except Exception as e:
        print(f"An unexpected error occurred while reading the file: {e}")



def write_shoes_data():
    """
    Writes the current shoe_list data back to inventory.txt,
    overwriting the existing content.
    """
    try:
        with open(INVENTORY_FILE, "w") as f:
            f.write("Country,Code,Product,Cost,Quantity\n")  # Write header
            for shoe in shoe_list:
                f.write(shoe.to_file_string() + "\n")
        # print(f"Inventory data successfully written to {INVENTORY_FILE}.") # Optional confirmation
    except IOError:
        print(f"Error: Could not write data to {INVENTORY_FILE}.")
    except Exception as e:
        print(f"An unexpected error occurred while writing to the file: {e}")



def capture_shoes():
    """
    Allows the user to input data for a new shoe, creates a Shoe object,
    adds it to shoe_list, and updates the inventory file.
    """
    print("\n👟 Enter New Shoe Details 👟")
    while True:
        country = input("Enter country: ").strip()
        if country:
            break
        print("Country cannot be empty.")

    while True:
        code = input("Enter unique shoe code (e.g., SKU12345): ").strip().upper()
        if not code:
            print("Code cannot be empty.")
            continue
        # Check if code already exists
        if any(shoe.code == code for shoe in shoe_list):
            print(f"Error: Shoe code '{code}' already exists. Please enter a unique code.")
        else:
            break

    while True:
        product = input("Enter product name: ").strip()
        if product:
            break
        print("Product name cannot be empty.")

    while True:
        try:
            cost_str = input("Enter cost per unit: ").strip()
            cost = float(cost_str)
            if cost >= 0:
                break
            else:
                print("Cost cannot be negative.")
        except ValueError:
            print("Invalid input. Please enter a numeric value for cost.")

    while True:
        try:
            quantity_str = input("Enter quantity in stock: ").strip()
            quantity = int(quantity_str)
            if quantity >= 0:
                break
            else:
                print("Quantity cannot be negative.")
        except ValueError:
            print("Invalid input. Please enter a whole number for quantity.")

    # Create new shoe object and add to list
    new_shoe = Shoe(country, code, product, cost, quantity)
    shoe_list.append(new_shoe)
    print(f"\n✅ Shoe '{product}' ({code}) added successfully.")

    # Update the inventory file
    write_shoes_data()



def view_all():
    """
    Displays all shoes in the inventory using the tabulate module
    for formatted output.
    """
    if not shoe_list:
        print("\nInventory is empty. Please read data or capture shoes first.")
        return

    print("\n👟👟👟 Full Shoe Inventory 👟👟👟")
    headers = ["Country", "Code", "Product", "Cost", "Quantity"]
    # Create a list of lists for tabulate
    table_data = [
        [s.country, s.code, s.product, f"{s.cost:.2f}", s.quantity]
        for s in shoe_list
    ]

    # Print the table
    print(tabulate(table_data, headers=headers, tablefmt="grid"))



def re_stock():
    """
    Finds the shoe with the lowest quantity, prompts the user to restock,
    and updates the quantity in shoe_list and inventory.txt.
    """
    if not shoe_list:
        print("\nInventory is empty. Cannot perform restock.")
        return

    # Find the shoe with the minimum quantity
    try:
        min_shoe = min(shoe_list, key=lambda shoe: shoe.quantity)
    except ValueError:  # Should not happen if shoe_list is not empty, but good practice
        print("Error finding the shoe with the lowest quantity.")
        return

    print(f"\n📉 Shoe with the lowest stock (needs restocking):")
    print("-" * 30)
    print(min_shoe)
    print("-" * 30)

    while True:
        choice = input(
            f"Do you want to add stock for {min_shoe.product} (Code: {min_shoe.code})? (yes/no): "
        ).strip().lower()
        if choice in ["yes", "y"]:
            while True:
                try:
                    add_qty_str = input(
                        f"Enter quantity to add (current: {min_shoe.quantity}): "
                    ).strip()
                    add_qty = int(add_qty_str)
                    if add_qty >= 0:
                        min_shoe.quantity += add_qty
                        print(
                            f"\n✅ Stock updated. New quantity for {min_shoe.code}: {min_shoe.quantity}"
                        )
                        # Update the inventory file
                        write_shoes_data()
                        return  # Exit re_stock function
                    else:
                        print("Quantity to add cannot be negative.")
                except ValueError:
                    print("Invalid input. Please enter a whole number.")
        elif choice in ["no", "n"]:
            print("No changes made to stock.")
            return  # Exit re_stock function
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")



def search_shoe():
    """
    Searches for a shoe by its code and prints its details if found.
    """
    if not shoe_list:
        print("\nInventory is empty. Cannot perform search.")
        return

    search_code = input("\nEnter the shoe code to search for: ").strip().upper()

    found_shoe = None
    for shoe in shoe_list:
        if shoe.code == search_code:
            found_shoe = shoe
            break

    if found_shoe:
        print("\n🔍 Shoe Found:")
        print("-" * 30)
        print(found_shoe)
        print("-" * 30)
    else:
        print(f"\n❌ Shoe with code '{search_code}' not found in inventory.")



def value_per_item():
    """
    Calculates and displays the total value (cost * quantity) for each shoe.
    """
    if not shoe_list:
        print("\nInventory is empty. Cannot calculate values.")
        return

    print("\n💰 Value Per Shoe Item 💰")
    headers = ["Code", "Product", "Cost", "Quantity", "Total Value"]
    table_data = []
    for shoe in shoe_list:
        value = shoe.cost * shoe.quantity
        table_data.append(
            [
                shoe.code,
                shoe.product,
                f"{shoe.cost:.2f}",
                shoe.quantity,
                f"{value:.2f}",
            ]
        )

    print(tabulate(table_data, headers=headers, tablefmt="grid"))



def highest_qty():
    """
    Finds the shoe with the highest quantity and marks it as 'FOR SALE'.
    """
    if not shoe_list:
        print("\nInventory is empty.")
        return

    try:
        max_shoe = max(shoe_list, key=lambda shoe: shoe.quantity)
    except ValueError:
        print("Error finding the shoe with the highest quantity.")
        return

    print("\n✨ FOR SALE (Highest Quantity Item) ✨")
    print("-" * 30)
    print(max_shoe)
    print("-" * 30)
    print(
        f"This item ({max_shoe.product} - {max_shoe.code}) has the highest stock ({max_shoe.quantity}) and is recommended for sale."
    )



# ==========Main Menu=============
def main_menu():
    """Displays the main menu and handles user interaction."""
    # Load data initially when the program starts
    read_shoes_data()

    while True:
        print("\n═════════════════════════════")
        print("   👟 Inventory Menu 👟")
        print("═════════════════════════════")
        print("1. View All Shoes")
        print("2. Capture New Shoe")
        print("3. Re-stock Lowest Quantity Shoe")
        print("4. Search for Shoe by Code")
        print("5. Calculate Value Per Item")
        print("6. Find Highest Quantity Shoe (For Sale)")
        print("7. Reload Data from File")  # Option to refresh data
        print("0. Exit")
        print("─────────────────────────────────")

        choice = input("Please enter your choice (0-7): ").strip()

        if choice == "1":
            view_all()
        elif choice == "2":
            capture_shoes()
        elif choice == "3":
            re_stock()
        elif choice == "4":
            search_shoe()
        elif choice == "5":
            value_per_item()
        elif choice == "6":
            highest_qty()
        elif choice == "7":
            print("\nReloading data from inventory.txt...")
            read_shoes_data()  # Reread data from the file
        elif choice == "0":
            print("\nExiting Inventory Manager. Goodbye! 👋")
            break
        else:
            print("\nInvalid choice. Please enter a number between 0 and 7.")

        input("\nPress Enter to continue...")  # Pause for readability



# Run the main menu when the script is executed
if __name__ == "__main__":
    # Check if tabulate is installed, provide guidance if not
    try:
        import tabulate
    except ImportError:
        print("*" * 60)
        print(" Optional dependency 'tabulate' not found.")
        print(" For nicely formatted tables, please install it:")
        print("   pip install tabulate")
        print(" The program will work without it, but tables won't look as good.")
        print("*" * 60)
        # Create a dummy tabulate function if it's not installed
        def tabulate(data, headers, tablefmt):
            # Simple fallback: print headers and then data rows
            print("\n" + ", ".join(headers))
            print("-" * (len(", ".join(headers)) + 5))
            for row in data:
                print(", ".join(map(str, row)))
            return ""  # Return empty string to avoid errors where print(tabulate(...)) is used

    main_menu()
