# Can Order (s, c, S) Joint Replenishment Policy Generater

## Overview
Using a genetic algorithm, this code uses a cost function to determine efficient feasible (s, c, S) policies. The project samples from an empirical demand distribution and simulates the total cost per period using holding, ordering, and backorder costs.

In the example setup uses intermittent demand lot-sizing problem for ordering loose-loaded containers.

## Installation
Instructions on how to install and set up your project.

```sh
# Clone the repository
git clone https://github.com/jonathannicklin/CanOrder_JointReplenishment.git

# Navigate to the project directory
cd ../CanOrder_JointReplenishment

# Install dependencies
pip install -r requirements.txt

#Usage
1. Edit the parameters in the setup.json file
2. Edit sample_data.csv to show demand per period (columns) of items (rows)
