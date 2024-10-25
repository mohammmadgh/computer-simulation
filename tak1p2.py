import random
import tkinter as tk

# Function to create the customers table
def create_customers(num_customers):
    customers = []
    time_of_arrival = 0  # Initialize the time of arrival for the first customer
    total_waiting_time = 0  # Initialize total waiting time
    total_idle_time = 0  # Initialize total idle time
    server_busy_time = 0  # Initialize total time the server is busy
    num_customers_with_wait = 0  # Initialize the number of customers who have to wait
    total_service_time = 0  # Initialize total service time
    for i in range(num_customers):
        customer_id = i + 1
        
        if i == 0:
            time_since_last_arrival = None  # No arrival time for the first customer
            waiting_time = 0
        else:
            time_since_last_arrival = random.randint(1, 10)  # Generate a random time since last arrival
            waiting_time = time_since_last_arrival
            if waiting_time > 0:
                num_customers_with_wait += 1
        
        service_time = random.randint(1, 10)  # Generate a random service time
        total_service_time += service_time
        
        if time_since_last_arrival is not None:
            time_of_arrival += time_since_last_arrival
            total_waiting_time += waiting_time
            
            if server_busy_time > 0:
                server_busy_time += time_since_last_arrival - waiting_time
            else:
                server_busy_time += time_since_last_arrival
            
            total_idle_time += waiting_time
        
        customers.append((customer_id, time_since_last_arrival, time_of_arrival, waiting_time, service_time))
    
    total_time = time_of_arrival + waiting_time  # Total time the server is operational
    fraction_idle_time = total_idle_time / total_time
    fraction_busy_time = 1 - fraction_idle_time
    
    return customers, total_waiting_time / num_customers, num_customers_with_wait / num_customers, fraction_idle_time, fraction_busy_time, total_service_time / num_customers  # Return the customers data, average waiting time, probability of waiting, fraction of idle time, fraction of busy time, and average service time

# Generate the table data and calculate average waiting time, probability of waiting, fraction of idle time, fraction of busy time, and average service time for 100 customers
customer_data, average_waiting_time, probability_of_waiting, fraction_idle_time, fraction_busy_time, average_service_time = create_customers(100)

# Calculate the probability of the server being idle
total_idle_time = sum([customer[3] for customer in customer_data if customer[1] is not None])
total_run_time = customer_data[-1][2] + customer_data[-1][3]  # Total run time of the simulation

probability_idle_server = total_idle_time / total_run_time

# Create a GUI window
root = tk.Tk()
root.title("Customer Arrival Times Table 100 C")
root.geometry("800x600")  # Set the window size to 800x400

# Create a text widget to display the table
text_widget = tk.Text(root)
text_widget.pack(fill=tk.BOTH, expand=True)

# Insert table data into the text widget
text_widget.insert(tk.END, "Table: Customer Arrival Times\n")
text_widget.insert(tk.END, f"{'Customer':<10}{'Time Since Last Arrival':<30}{'Time of Arrival':<20}{'Waiting Time':<20}{'Service Time':<20}\n")
for customer_id, time_since_last_arrival, time_of_arrival, waiting_time, service_time in customer_data:
    text_widget.insert(tk.END, f"{customer_id:<10}{time_since_last_arrival if time_since_last_arrival is not None else 'N/A':<30}{time_of_arrival:<20}{waiting_time:<20}{service_time:<20}\n")

# Calculate the average waiting time of those who wait
total_waiting_time_of_waiters = sum([customer[3] for customer in customer_data if customer[1] is not None])
num_waiters = len([customer for customer in customer_data if customer[1] is not None])
average_waiting_time_of_waiters = total_waiting_time_of_waiters / num_waiters

# Calculate the average time a customer spends in the system
total_time_in_system = sum([customer[3] + customer[4] for customer in customer_data])
average_time_in_system = total_time_in_system / len(customer_data)

text_widget.insert(tk.END, f"\nAverage Waiting Time for a Customer: {average_waiting_time:.2f} minutes\n")
text_widget.insert(tk.END, f"Probability that a Customer has to Wait in the Queue: {probability_of_waiting:.2%}\n")
text_widget.insert(tk.END, f"Fraction of Idle Time of the Server: {fraction_idle_time:.2%}\n")
text_widget.insert(tk.END, f"Fraction of Busy Time of the Server: {fraction_busy_time:.2%}\n")
text_widget.insert(tk.END, f"Average Service Time for a Customer: {average_service_time:.2f} minutes\n")
text_widget.insert(tk.END, f"Average Waiting Time of Those Who Wait: {average_waiting_time_of_waiters:.2f} minutes\n")
text_widget.insert(tk.END, f"\Probability of the Server Being Idle: {probability_idle_server:.2%}\n")
text_widget.insert(tk.END, f"Average Time a Customer Spends in the System: {average_time_in_system:.2f} minutes\n")
text_widget.insert(tk.END,f'mohammad-gharib ')
root.mainloop()