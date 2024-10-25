import tkinter as tk
from tkinter import messagebox
import math

window = tk.Tk()
window.title("Random Number Generator and Testing Tool")
window.geometry("600x600")

# Function to generate random numbers and perform tests
def generate_random_numbers(a1, c1, m1, X10, a2, c2, m2, X20, count, num_intervals, i, alpha):
    random_numbers = []
    x1 = X10
    x2 = X20

    for _ in range(count):
        x1 = (a1 * x1 + c1) % m1
        x2 = (a2 * x2 + c2) % m2

        random_number = (x1 - x2) % m2
        random_numbers.append(random_number)

    ecdf = [i / len(random_numbers) for i in range(1, len(random_numbers) + 1)]
    d = max([abs(ecdf[i] - (i+1)/len(random_numbers)) for i in range(len(random_numbers))])
    ks_stat = math.sqrt(len(random_numbers)) * d
    is_uniform_ks = ks_stat < 1.36  # Critical value for alpha=0.05

    observed_freq = [0] * num_intervals
    for num in random_numbers:
        interval = num // (m1 // num_intervals)
        observed_freq[interval] += 1

    expected_freq = len(random_numbers) / num_intervals
    chi_stat = sum([(observed_freq[i] - expected_freq)**2 / expected_freq for i in range(num_intervals)])
    is_uniform_chi_square = chi_stat < 16.92  # Critical value for alpha=0.05 and 10 intervals

    observed_freq_independence = [[0 for _ in range(m1)] for _ in range(m1)]
    n = len(random_numbers) - i
    for j in range(n):
        idx1 = random_numbers[j]
        idx2 = random_numbers[j + i]
        observed_freq_independence[idx1][idx2] += 1

    expected_freq_independence = n / (m1 * m1)
    chi_stat_independence = sum([(observed_freq_independence[idx1][idx2] - expected_freq_independence)**2 / expected_freq_independence for idx1 in range(m1) for idx2 in range(m1)])
    is_independent = chi_stat_independence < 23.68  # Critical value for alpha=0.05 and 5x5 table

    return random_numbers, is_uniform_ks, is_uniform_chi_square, is_independent

def run_program():
    try:
        a1 = int(entry_a1.get())
        c1 = int(entry_c1.get())
        m1 = int(entry_m1.get())
        X10 = int(entry_X10.get())
        a2 = int(entry_a2.get())
        c2 = int(entry_c2.get())
        m2 = int(entry_m2.get())
        X20 = int(entry_X20.get())
        count = int(entry_count.get())
        num_intervals = int(entry_num_intervals.get())
        i = int(entry_i.get())
        alpha = float(entry_alpha.get())

        random_numbers, is_uniform_ks, is_uniform_chi_square, is_independent = generate_random_numbers(a1, c1, m1, X10, a2, c2, m2, X20, count, num_intervals, i, alpha)

        text_generated_numbers.configure(state="normal")
        text_generated_numbers.delete(1.0, tk.END)
        text_generated_numbers.insert(tk.END, " ".join(map(str, random_numbers)))
        text_generated_numbers.configure(state="disabled")

        text_uniformity_ks.configure(state="normal")
        text_uniformity_ks.delete(1.0, tk.END)
        text_uniformity_ks.insert(tk.END, "Passed" if is_uniform_ks else "Failed")
        text_uniformity_ks.configure(state="disabled")

        text_uniformity_chi_square.configure(state="normal")
        text_uniformity_chi_square.delete(1.0, tk.END)
        text_uniformity_chi_square.insert(tk.END, "Passed" if is_uniform_chi_square else "Failed")
        text_uniformity_chi_square.configure(state="disabled")

        text_independence.configure(state="normal")
        text_independence.delete(1.0, tk.END)
        text_independence.insert(tk.END, "Passed" if is_independent else "Failed")
        text_independence.configure(state="disabled")

    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter numeric values.")

# Create entry fields for input parameters
entry_a1 = tk.Entry(window)
entry_a1.pack()

entry_c1 = tk.Entry(window)
entry_c1.pack()

entry_m1 = tk.Entry(window)
entry_m1.pack()

entry_X10 = tk.Entry(window)
entry_X10.pack()

entry_a2 = tk.Entry(window)
entry_a2.pack()

entry_c2 = tk.Entry(window)
entry_c2.pack()

entry_m2 = tk.Entry(window)
entry_m2.pack()

entry_X20 = tk.Entry(window)
entry_X20.pack()

entry_count = tk.Entry(window)
entry_count.pack()

entry_num_intervals = tk.Entry(window)
entry_num_intervals.pack()

entry_i = tk.Entry(window)
entry_i.pack()

entry_alpha = tk.Entry(window)
entry_alpha.pack()

# Create buttons for running the program and clearing the results
button_run = tk.Button(window, text="Run", command=run_program)
button_run.pack()

# Create text boxes to display the generated numbers and analysis results
label_generated_numbers = tk.Label(window, text="Generated Numbers:")
label_generated_numbers.pack()
text_generated_numbers = tk.Text(window, height=5, width=50)
text_generated_numbers.configure(state="disabled")
text_generated_numbers.pack()

label_uniformity_ks = tk.Label(window, text="Uniformity (K-S test):")
label_uniformity_ks.pack()
text_uniformity_ks = tk.Text(window, height=1, width=25)
text_uniformity_ks.configure(state="disabled")
text_uniformity_ks.pack()

label_uniformity_chi_square = tk.Label(window, text="Uniformity (Chi-Square test):")
label_uniformity_chi_square.pack()
text_uniformity_chi_square = tk.Text(window, height=1, width=25)
text_uniformity_chi_square.configure(state="disabled")
text_uniformity_chi_square.pack()

label_independence = tk.Label(window, text="Independence (Chi-Square test):")
label_independence.pack()
text_independence = tk.Text(window, height=1, width=25)
text_independence.configure(state="disabled")
text_independence.pack()

# Start the Tkinter event loop
window.mainloop()