import random

# Function to create the customers table
def create_customers(num_customers):
    customers = []
    time_of_arrival = 0
    total_waiting_time = 0
    total_idle_time = 0
    server_busy_time = 0
    num_customers_with_wait = 0
    total_service_time = 0
    for i in range(num_customers):
        customer_id = i + 1
        
        if i == 0:
            time_since_last_arrival = None
            waiting_time = 0
        else:
            time_since_last_arrival = random.randint(1, 10)
            waiting_time = time_since_last_arrival
            if waiting_time > 0:
                num_customers_with_wait += 1
        
        service_time = random.randint(1, 10)
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
    
    total_time = time_of_arrival + waiting_time
    fraction_idle_time = total_idle_time / total_time
    fraction_busy_time = 1 - fraction_idle_time
    
    return customers, total_waiting_time / num_customers, num_customers_with_wait / num_customers, fraction_idle_time, fraction_busy_time, total_service_time / num_customers

# Generate the table data and calculate metrics
customer_data, average_waiting_time, probability_of_waiting, fraction_idle_time, fraction_busy_time, average_service_time = create_customers(20)

# Calculate the probability of the server being idle
total_idle_time = sum([customer[3] for customer in customer_data if customer[1] is not None])
total_run_time = customer_data[-1][2] + customer_data[-1][3]
probability_idle_server = total_idle_time / total_run_time

# Print the metrics
print("Average Waiting Time for a Customer:", average_waiting_time)
print("Probability that a Customer has to Wait in the Queue:", probability_of_waiting)
print("Fraction of Idle Time of the Server:", fraction_idle_time)
print("Fraction of Busy Time of the Server:", fraction_busy_time)
print("Average Service Time for a Customer:", average_service_time)
print("Probability of the Server Being Idle:", probability_idle_server)