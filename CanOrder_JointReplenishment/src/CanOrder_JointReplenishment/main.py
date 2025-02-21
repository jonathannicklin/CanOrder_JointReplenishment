import os
import sys

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from CanOrder_JointReplenishment.demand import load_historic_demand, create_empirical_distribution
from CanOrder_JointReplenishment.simulation import load_setup
from CanOrder_JointReplenishment.genetic_algorithm import genetic_algorithm

def main():
    # Load demand data and setup configuration
    demand_data = load_historic_demand('data/sample_data.csv')
    setup = load_setup('data/setup.json')
    num_cores = os.cpu_count()
    print(f"Number of CPU cores available: {num_cores}")

    # Create the empirical demand distribution
    demand_distribution = create_empirical_distribution(demand_data, setup)
    
    # Run the genetic algorithm to get the best policies
    best_policies = genetic_algorithm(demand_distribution, setup)
    
    # Print the top 10 best policies along with their costs and service levels
    print("Top 10 Best Policies, Costs, and Service Levels:")
    for policies, cost, service_level in best_policies:
        print(f"Policies: {policies}, Cost = {cost:.2f}, Service Level = {service_level:.2f}%")

if __name__ == "__main__":
    main()