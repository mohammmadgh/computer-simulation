import random
import math
from tkinter import Tk, Label, Button, Canvas, Toplevel, Text, Scrollbar, RIGHT, LEFT, Y, END

def generate_random_numbers():
    return [random.random() for _ in range(100)]

def inverse_transform(random_numbers, lambda_param=2):
    return [-math.log(1 - u) / lambda_param for u in random_numbers]

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

def display_random_numbers(random_numbers):
    top = Toplevel(root)
    top.title("Generated Random Numbers")
    
    scrollbar = Scrollbar(top)
    scrollbar.pack(side=RIGHT, fill=Y)
    
    text = Text(top, wrap='none', yscrollcommand=scrollbar.set)
    text.pack(side=LEFT, fill='both', expand=True)
    
    scrollbar.config(command=text.yview)
    
    for number in random_numbers:
        text.insert(END, f"{number:.4f}\n")

def perform_analysis():
    # Generate random numbers
    random_numbers = generate_random_numbers()
    
    # Display the generated random numbers
    display_random_numbers(random_numbers)
    
    # Generate Exponential variates
    lambda_param = 2
    exponential_variates = inverse_transform(random_numbers, lambda_param)
    
    # Theoretical quantiles
    theoretical_quantiles = [-math.log(1 - (i + 0.5) / len(exponential_variates)) / lambda_param for i in range(len(exponential_variates))]
    sample_quantiles = sorted(exponential_variates)
    
    # Create Q-Q plot
    qq_plot(canvas, theoretical_quantiles, sample_quantiles)
    
    # Calculate correlation coefficient
    correlation_coefficient = sum((x - theoretical_quantiles[0]) * (y - sample_quantiles[0]) for x, y in zip(theoretical_quantiles, sample_quantiles)) / math.sqrt(sum((x - theoretical_quantiles[0])**2 for x in theoretical_quantiles) * sum((y - sample_quantiles[0])**2 for y in sample_quantiles))
    
    # Determine if Exponential distribution is a good fit
    fit_msg = "Yes" if correlation_coefficient > 0.95 else "No"
    
    # Estimate lambda
    if fit_msg == "Yes":
        estimated_lambda = 1 / (sum(exponential_variates) / len(exponential_variates))
    else:
        estimated_lambda = None
    
    # Display results
    results = (
        f"Correlation Coefficient: {correlation_coefficient:.4f}\n"
        f"Is Exponential distribution a good fit? {fit_msg}\n"
        f"Estimated λ: {estimated_lambda}\n"
    )
    results_label.config(text=results)

# Create the main window
root = Tk()
root.title("Exponential Distribution Analysis")

# Create a label
label = Label(root, text="Click the button to generate random numbers and analyze them.")
label.pack(pady=20)

# Create a button to perform the analysis
button = Button(root, text="Perform Analysis", command=perform_analysis)
button.pack(pady=20)

# Create a canvas for the Q-Q plot
canvas = Canvas(root, width=700, height=700)
canvas.pack(pady=20)

# Label for displaying results
results_label = Label(root, text="", justify='left', font=("Arial", 12))
results_label.pack(pady=20)

# Run the application
root.mainloop()
