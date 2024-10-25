import random
import math
from tkinter import Tk, Label, Button, Canvas, Toplevel, Text, Scrollbar, RIGHT, LEFT, Y, END

def generate_random_numbers():
    return [random.random() for _ in range(100)]

def poisson_pmf(k, alpha):
    return (alpha**k * math.exp(-alpha)) / math.factorial(k)

def poisson_acceptance_rejection(alpha=2):
    pois_variates = []
    for _ in range(100):
        while True:
            y = int(random.expovariate(1 / alpha))
            u = random.random()
            if u <= poisson_pmf(y, alpha):
                pois_variates.append(y)
                break
    return pois_variates

def qq_plot(canvas, theoretical_quantiles, sample_quantiles):
    max_theoretical = max(theoretical_quantiles)
    max_sample = max(sample_quantiles)
    max_value = max(max_theoretical, max_sample)
    
    margin = 50
    plot_size = 500
    canvas.delete("all")
    canvas.create_rectangle(margin, margin, margin + plot_size, margin + plot_size, outline='black')
    
    # Draw points
    for tq, sq in zip(theoretical_quantiles, sample_quantiles):
        x = tq / max_value * plot_size + margin
        y = (1 - sq / max_value) * plot_size + margin
        canvas.create_oval(x-3, y-3, x+3, y+3, fill='blue')
    
    # Draw the y=x line
    canvas.create_line(margin, margin + plot_size, margin + plot_size, margin, fill='red', dash=(4, 2))
    
    # Add labels
    canvas.create_text(margin + plot_size / 2, margin / 2, text="Q-Q Plot", font=("Arial", 16))
    canvas.create_text(margin / 2, margin + plot_size / 2, text="Sample Quantiles", font=("Arial", 12), angle=90)
    canvas.create_text(margin + plot_size / 2, margin + plot_size + margin / 2, text="Theoretical Quantiles", font=("Arial", 12))
    
    # Add ticks and tick labels
    for i in range(11):
        x = i / 10 * plot_size + margin
        y = (1 - i / 10) * plot_size + margin
        canvas.create_line(x, margin + plot_size, x, margin + plot_size + 5)
        canvas.create_text(x, margin + plot_size + 15, text=f"{i / 10 * max_value:.1f}", font=("Arial", 10))
        canvas.create_line(margin - 5, y, margin, y)
        canvas.create_text(margin - 15, y, text=f"{i / 10 * max_value:.1f}", font=("Arial", 10))

def display_random_numbers(title, random_numbers):
    top = Toplevel(root)
    top.title(title)
    
    scrollbar = Scrollbar(top)
    scrollbar.pack(side=RIGHT, fill=Y)
    
    text = Text(top, wrap='none', yscrollcommand=scrollbar.set)
    text.pack(side=LEFT, fill='both', expand=True)
    
    scrollbar.config(command=text.yview)
    
    for number in random_numbers:
        text.insert(END, f"{number:.4f}\n" if isinstance(number, float) else f"{number}\n")

def empirical_cdf(data):
    data_sorted = sorted(data)
    cdf_values = [(data_sorted.index(x) + 1) / len(data_sorted) for x in data_sorted]
    return data_sorted, cdf_values

def theoretical_poisson_cdf(x, alpha):
    cdf = sum(poisson_pmf(k, alpha) for k in range(0, x + 1))
    return cdf

def ks_test(empirical_data, alpha):
    n = len(empirical_data)
    empirical_data_sorted, empirical_cdf_values = empirical_cdf(empirical_data)
    
    D_statistic = max(abs(empirical_cdf_values[i] - theoretical_poisson_cdf(empirical_data_sorted[i], alpha)) for i in range(n))
    
    # Kolmogorov-Smirnov critical value for alpha=0.05
    ks_critical_value = 1.36 / math.sqrt(n)
    reject_null = D_statistic > ks_critical_value
    
    return D_statistic, ks_critical_value, reject_null

def chi_square_test(empirical_data, alpha):
    observed_freq = {k: 0 for k in range(max(empirical_data) + 1)}
    for val in empirical_data:
        observed_freq[val] += 1
    
    expected_freq = {k: 100 * poisson_pmf(k, alpha) for k in observed_freq.keys()}
    
    chi2_stat = sum((observed_freq[k] - expected_freq[k])**2 / expected_freq[k] for k in observed_freq.keys())
    
    # Chi-square critical value for df=len(observed_freq)-1 and alpha=0.05
    df = len(observed_freq) - 1
    chi2_critical_value = 16.92  # For df=9 and alpha=0.05
    
    reject_null = chi2_stat > chi2_critical_value
    
    return chi2_stat, chi2_critical_value, df, reject_null

def display_results(results):
    top = Toplevel(root)
    top.title("Test Results")
    
    scrollbar = Scrollbar(top)
    scrollbar.pack(side=RIGHT, fill=Y)
    
    text = Text(top, wrap='none', yscrollcommand=scrollbar.set)
    text.pack(side=LEFT, fill='both', expand=True)
    
    scrollbar.config(command=text.yview)
    
    text.insert(END, results)

def perform_analysis():
    # Generate random numbers
    random_numbers = generate_random_numbers()
    
    # Display the generated random numbers
    display_random_numbers("Generated Uniform Random Numbers", random_numbers)
    
    # Generate Poisson variates using Acceptance-Rejection method
    alpha = 2
    poisson_variates = poisson_acceptance_rejection(alpha)
    
    # Display the generated Poisson variates
    display_random_numbers("Generated Poisson Variates", poisson_variates)
    
    # Theoretical quantiles
    theoretical_quantiles = [sum(poisson_pmf(k, alpha) for k in range(int((i + 0.5) * len(poisson_variates) / 100))) for i in range(len(poisson_variates))]
    sample_quantiles = sorted(poisson_variates)
    
    # Create Q-Q plot
    qq_plot(canvas, theoretical_quantiles, sample_quantiles)
    
    # Calculate correlation coefficient
    correlation_coefficient = sum((x - theoretical_quantiles[0]) * (y - sample_quantiles[0]) for x, y in zip(theoretical_quantiles, sample_quantiles)) / math.sqrt(sum((x - theoretical_quantiles[0])**2 for x in theoretical_quantiles) * sum((y - sample_quantiles[0])**2 for y in sample_quantiles))
    
    # Determine if Poisson distribution is a good fit
    fit_msg = "Yes" if correlation_coefficient > 0.95 else "No"
    
    # Estimate alpha
    if fit_msg == "Yes":
        estimated_alpha = sum(poisson_variates) / len(poisson_variates)
    else:
        estimated_alpha = None
    
    # Kolmogorov-Smirnov test
    ks_stat, ks_critical_value, ks_reject_null = ks_test(poisson_variates, alpha)
    
    # Chi-square test
    chi2_stat, chi2_critical_value, df, chi2_reject_null = chi_square_test(poisson_variates, alpha)
    
    # Display results
    results = (
        f"Correlation Coefficient: {correlation_coefficient:.4f}\n"
        f"Is Poisson distribution a good fit? {fit_msg}\n"
        f"Estimated α: {estimated_alpha}\n\n"
        f"Kolmogorov-Smirnov Test:\n"
        f"Statistic: {ks_stat:.4f}\n"
        f"Critical Value: {ks_critical_value:.4f}\n"
        f"Reject Null Hypothesis: {'Yes' if ks_reject_null else 'No'}\n\n"
        f"Chi-square Test:\n"
        f"Degrees of Freedom: {df}\n"
        f"Statistic: {chi2_stat:.4f}\n"
        f"Critical Value: {chi2_critical_value:.4f}\n"
        f"Reject Null Hypothesis: {'Yes' if chi2_reject_null else        'No'}\n"
    )
    
    display_results(results)

# Create the main window
root = Tk()
root.title("Poisson Distribution Analysis")

# Create a label
label = Label(root, text="Click the button to generate random numbers and analyze them.")
label.pack(pady=20)

# Create a button to perform the analysis
button = Button(root, text="Perform Analysis", command=perform_analysis)
button.pack(pady=20)

# Create a canvas for the Q-Q plot
canvas = Canvas(root, width=700, height=700)
canvas.pack(pady=20)

# Run the application
root.mainloop()

