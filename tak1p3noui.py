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

def simulate():
    next_customer_arrival = 0
    service_completion_able = float('inf')
    service_completion_baker = float('inf')
    customers_served = 0
    able_idle_time = 0
    baker_idle_time = 0
    current_time = 0
    customer_queue = []

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

        elif next_event_time in [service_completion_able, service_completion_baker]:
            if next_event_time == service_completion_able:
                service_completion_able = float('inf')
                able_idle_time += (next_customer_arrival - current_time)
            else:
                service_completion_baker = float('inf')
                baker_idle_time += (next_customer_arrival - current_time)

    total_idle_time = able_idle_time + baker_idle_time
    utilization_able = (SIMULATION_TIME - able_idle_time) / SIMULATION_TIME * 100
    utilization_baker = (SIMULATION_TIME - baker_idle_time) / SIMULATION_TIME * 100

    print(f"Customers Served: {customers_served}")
    print(f"Able's Utilization: {utilization_able:.2f}%")
    print(f"Baker's Utilization: {utilization_baker:.2f}%")

simulate()