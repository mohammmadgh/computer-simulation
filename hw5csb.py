import tkinter as tk
from tkinter import ttk, messagebox

# Combined Linear Congruential Generator function
def combined_linear_congruential(m1, c1, a1, X1, m2, c2, a2, X2, n):
    ui_values = []
    for _ in range(n):
        X1 = (a1 * X1 + c1) % m1
        X2 = (a2 * X2 + c2) % m2
        ui = X1 / m1 + X2 / m2
        ui_values.append(ui)
    return ui_values

# K-S test function
def ks_test(ui_values):
    n = len(ui_values)
    sorted_ui_values = sorted(ui_values)
    D_plus = max((i + 1) / n - u for i, u in enumerate(sorted_ui_values))
    D_minus = max(u - i / n for i, u in enumerate(sorted_ui_values))
    D = max(D_plus, D_minus)
    D_alpha = 0.294  # Critical value for N = 20 and alpha = 0.05
    return D, D_alpha

# Function to generate random numbers and perform K-S test
def generate_and_test():
    # Clear previous entries in the Treeview
    for i in tree.get_children():
        tree.delete(i)
    
    m1, c1, a1, X1 = 100, 43, 23, 13
    m2, c2, a2, X2 = 99, 47, 27, 17
    n = 20
    
    ui_values = combined_linear_congruential(m1, c1, a1, X1, m2, c2, a2, X2, n)
    
    for i in range(n):
        tree.insert("", tk.END, values=(i + 1, ui_values[i]))

    D, D_alpha = ks_test(ui_values)
    
    if D <= D_alpha:
        result_message = "The null hypothesis is not rejected. The sample appears to be uniformly distributed."
    else:
        result_message = "The null hypothesis is rejected. The sample does not appear to be uniformly distributed."
    
    # Display results in a message box
    messagebox.showinfo("K-S Test Result", f"K-S Statistic: {D:.3f}\nCritical Value: {D_alpha}\n{result_message}")
    
    # Display results in the main window
    result_label.config(text=f"K-S Statistic: {D:.3f}\nCritical Value: {D_alpha}\n{result_message}")

# Create the main window
root = tk.Tk()
root.title("Random Number Generator and K-S Test")
root.geometry("800x600")

# Create a Treeview widget with columns
tree = ttk.Treeview(root, columns=("Index", "ui Value"), show="headings")
tree.heading("Index", text="Index")
tree.heading("ui Value", text="ui Value")
tree.pack(padx=10, pady=10, fill="both", expand=True)

# Button to generate random numbers and perform K-S test
generate_button = tk.Button(root, text="Generate and Test Random Numbers", command=generate_and_test)
generate_button.pack(pady=10)

# Label to display K-S test results
result_label = tk.Label(root, text="", justify=tk.LEFT)
result_label.pack(pady=10)

# Start the main loop
root.mainloop()
