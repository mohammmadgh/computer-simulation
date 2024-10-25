import tkinter as tk
from tkinter import ttk, messagebox
import math

# Combined Linear Congruential Generator function
def combined_linear_congruential(m1, c1, a1, X1, m2, c2, a2, X2, n):
    ui_values = []
    for _ in range(n):
        X1 = (a1 * X1 + c1) % m1
        X2 = (a2 * X2 + c2) % m2
        ui = (X1 / m1 + X2 / m2) % 1  # Ensure ui is in [0, 1)
        ui_values.append(ui)
    return ui_values

# Chi-Square test function
def chi_square_test(ui_values, k=5):
    n = len(ui_values)
    bin_counts = [0] * k
    for ui in ui_values:
        bin_index = int(ui * k)
        if bin_index == k:  # edge case where ui is exactly 1
            bin_index = k - 1
        bin_counts[bin_index] += 1
    
    expected_count = n / k
    chi_square_stat = sum((obs - expected_count) ** 2 / expected_count for obs in bin_counts)
    
    # Chi-Square critical value for k-1 degrees of freedom and alpha = 0.05
    chi_square_critical = 9.488  # for df = 4, alpha = 0.05
    return chi_square_stat, chi_square_critical

# Serial Correlation test function
def serial_correlation_test(ui_values, m):
    n = len(ui_values)
    mean_ui = sum(ui_values) / n
    numerator = sum((ui_values[i] - mean_ui) * (ui_values[i + m] - mean_ui) for i in range(n - m))
    denominator = sum((ui - mean_ui) ** 2 for ui in ui_values)
    correlation_coefficient = numerator / denominator
    
    # Z value for alpha = 0.02
    z_alpha = 2.326  # for alpha = 0.02
    return correlation_coefficient, z_alpha

# Function to generate random numbers and perform Chi-Square and Serial Correlation tests
def generate_and_test():
    try:
        # Clear previous entries in the Treeview
        for i in tree.get_children():
            tree.delete(i)
        
        m1, c1, a1, X1 = 100, 43, 23, 13
        m2, c2, a2, X2 = 99, 47, 27, 17
        n = 20
        
        ui_values = combined_linear_congruential(m1, c1, a1, X1, m2, c2, a2, X2, n)
        
        for i in range(n):
            tree.insert("", tk.END, values=(i + 1, ui_values[i]))

        chi_square_stat, chi_square_critical = chi_square_test(ui_values)
        
        if chi_square_stat <= chi_square_critical:
            uniformity_result = "The null hypothesis is not rejected. The sample appears to be uniformly distributed."
        else:
            uniformity_result = "The null hypothesis is rejected. The sample does not appear to be uniformly distributed."
        
        # Serial correlation tests for i=3, i=5, i=7
        correlation_results = []
        for i in [3, 5, 7]:
            correlation_coefficient, z_alpha = serial_correlation_test(ui_values, i)
            if abs(correlation_coefficient) <= z_alpha:
                correlation_results.append(f"The null hypothesis is not rejected for i={i}. The sample appears to be independent.")
            else:
                correlation_results.append(f"The null hypothesis is rejected for i={i}. The sample does not appear to be independent.")
        
        # Display results in a message box
        messagebox.showinfo("Test Results", f"Chi-Square Test Result:\nChi-Square Statistic: {chi_square_stat:.3f}\nCritical Value: {chi_square_critical}\n{uniformity_result}\n\n"
                                            f"Serial Correlation Test Results:\n" + "\n".join(correlation_results))
        
        # Display results in the main window
        result_label.config(text=f"Chi-Square Test Result:\nChi-Square Statistic: {chi_square_stat:.3f}\nCritical Value: {chi_square_critical}\n{uniformity_result}\n\n"
                                 f"Serial Correlation Test Results:\n" + "\n".join(correlation_results))
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main window
root = tk.Tk()
root.title("Random Number Generator and Statistical Tests")
root.geometry("800x600")

# Create a Treeview widget with columns
tree = ttk.Treeview(root, columns=("Index", "ui Value"), show="headings")
tree.heading("Index", text="Index")
tree.heading("ui Value", text="ui Value")
tree.pack(padx=10, pady=10, fill="both", expand=True)

# Button to generate random numbers and perform tests
generate_button = tk.Button(root, text="Generate and Test Random Numbers", command=generate_and_test)
generate_button.pack(pady=10)

# Label to display test results
result_label = tk.Label(root, text="", justify=tk.LEFT)
result_label.pack(pady=10)

# Start the main loop
root.mainloop()
