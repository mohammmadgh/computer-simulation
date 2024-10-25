import random
import tkinter as tk

# Function to create the customers table
def create_customers(num_customers):
    customer_data = []
    for i in range(num_customers):
        customer_id = i + 1
        time_since_last_arrival = random.randint(1, 10) if i > 0 else None
        time_of_arrival = random.randint(1, 60)
        waiting_time = max(0, time_of_arrival - 10)
        service_time = random.randint(5, 15)
        customer_data.append((customer_id, time_since_last_arrival, time_of_arrival, waiting_time, service_time))
        
    total_waiting_time = sum(customer[3] for customer in customer_data)
    average_waiting_time = total_waiting_time / num_customers
    probability_of_waiting = sum(1 for customer in customer_data if customer[3] > 0) / num_customers
    total_service_time = sum(customer[4] for customer in customer_data)
    fraction_idle_time = 1 - (total_service_time / (num_customers * 60))
    fraction_busy_time = total_service_time / (num_customers * 60)
    average_service_time = total_service_time / num_customers
    
    return customer_data, average_waiting_time, probability_of_waiting, fraction_idle_time, fraction_busy_time, average_service_time

# Generate the table data for 100 customers
customer_data, average_waiting_time, probability_of_waiting, fraction_idle_time, fraction_busy_time, average_service_time = create_customers(100)

# Create a GUI window
root = tk.Tk()
root.title("Customer Arrival Simulation")
root.geometry("800x600")
root.configure(bg="lightblue")  # Set background color of the GUI window

# Create a frame for the table
table_frame = tk.Frame(root, bg="lightblue")
table_frame.pack()

# Create a table to display the customer data
table = tk.Listbox(table_frame, width=150,height=20, bg="lightyellow")  # Set background color of the table
table.pack()

# Insert table headers
table.insert(0, "Customer ID | Time Since Last Arrival | Time of Arrival | Waiting Time | Service Time")

# Insert table data
for customer in customer_data:
    table.insert(tk.END, f"{customer[0]} | {customer[1] if customer[1] is not None else 'N/A'} | {customer[2]} | {customer[3]} | {customer[4]}")

# Display simulation results
results_label = tk.Label(root, text=f"Avg. Waiting Time: {average_waiting_time:.2f} | Probability of Waiting: {probability_of_waiting:.2%} | Fraction of Idle Time: {fraction_idle_time:.2%} | Fraction of Busy Time: {fraction_busy_time:.2%} | Avg. Service Time: {average_service_time:.2f}", bg="lightblue")  # Set background color of the label
results_label.pack()

root.mainloop()