import tkinter as tk
import random

SIMULATION_TIME = 480
AVERAGE_INTERARRIVAL_TIME = 10
AVERAGE_SERVICE_TIME = 5

class Customer:
    def __init__(self, id, arrival_time):
        self.id = id
        self.arrival_time = arrival_time
        self.service_time = random.expovariate(1.0 / AVERAGE_SERVICE_TIME)
        self.cumulative_probability = random.random()

root = tk.Tk()
root.title("Carhop Service Simulation")
root.geometry("800x800")

label_customers_served = tk.Label(root, text="Customers Served: 0")
label_customers_served.pack()

label_able_utilization = tk.Label(root, text="Able's Utilization: 0%")
label_able_utilization.pack()

label_baker_utilization = tk.Label(root, text="Baker's Utilization: 0%")
label_baker_utilization.pack()

canvas = tk.Canvas(root, width=10, height=10, bg='white')
canvas.pack()

text_details = tk.Text(root, height=50, width=100)
text_details.pack()

scrollbar = tk.Scrollbar(root, command=text_details.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_details.config(yscrollcommand=scrollbar.set)

def simulate():
    global next_customer_arrival, service_completion_able, service_completion_baker, customers_served, able_idle_time, baker_idle_time, current_time, customer_queue

    while current_time < SIMULATION_TIME and customers_served < 20:
        next_event_time = min(next_customer_arrival, service_completion_able, service_completion_baker)

        if next_event_time == next_customer_arrival:
            customers_served += 1
            current_time = next_customer_arrival
            next_customer_arrival = current_time + random.expovariate(1.0 / AVERAGE_INTERARRIVAL_TIME)

            if service_completion_able == float('inf'):
                service_completion_able = current_time + random.expovariate(1.0 / AVERAGE_SERVICE_TIME)
            elif service_completion_baker == float('inf'):
                service_completion_baker = current_time + random.expovariate(1.0 / AVERAGE_SERVICE_TIME)
            else:
                customer_queue.append(current_time)

            customer = Customer(customers_served, current_time)
            text_details.insert(tk.END, f"Customer {customer.id} - Arrival Time: {customer.arrival_time:.2f} min\n")
            text_details.insert(tk.END, f"Service Time: {customer.service_time:.2f} min\n")
            text_details.insert(tk.END, f"Cumulative Probability: {customer.cumulative_probability:.2f}\n\n")

        elif next_event_time in [service_completion_able, service_completion_baker]:
            if next_event_time == service_completion_able:
                service_completion_able = float('inf')
                able_idle_time += (next_customer_arrival - current_time)
            else:
                service_completion_baker = float('inf')
                baker_idle_time += (next_customer_arrival - current_time)

            current_time = next_event_time

        update_gui()

def update_gui():
    canvas.delete("all")

    canvas.create_text(50, 50, text="Customer Queue:", anchor=tk.W)
    for i, customer_time in enumerate(customer_queue):
        canvas.create_text(50, 70 + 20 * i, text=f"Customer {i + 1}: {customer_time:.2f} min", anchor=tk.W)

    canvas.create_text(50, 300, text="Service Status:", anchor=tk.W)
    canvas.create_text(50, 320, text=f"Able: {'Busy' if service_completion_able != float('inf') else 'Idle'}", anchor=tk.W)
    canvas.create_text(50, 340, text=f"Baker: {'Busy' if service_completion_baker != float('inf') else 'Idle'}", anchor=tk.W)

    total_idle_time = able_idle_time + baker_idle_time
    utilization_able = (SIMULATION_TIME - able_idle_time) / SIMULATION_TIME * 100
    utilization_baker = (SIMULATION_TIME - baker_idle_time) / SIMULATION_TIME * 100

    label_customers_served.config(text=f"Customers Served: {customers_served}")
    label_able_utilization.config(text=f"Able's Utilization: {utilization_able:.2f}%")
    label_baker_utilization.config(text=f"Baker's Utilization: {utilization_baker:.2f}%")

start_button = tk.Button(root, text="Start Simulation", command=simulate)
start_button.pack()

next_customer_arrival = 0
service_completion_able = float('inf')
service_completion_baker = float('inf')
customers_served = 0
able_idle_time = 0
baker_idle_time = 0
current_time = 0
customer_queue = []

root.mainloop()