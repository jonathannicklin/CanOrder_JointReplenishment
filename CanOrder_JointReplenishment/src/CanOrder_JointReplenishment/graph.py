import matplotlib.pyplot as plt

def static_plot(cost_progression, service_level_progression, num_generations):
    """
    Plot the cost and service level progression over generations.
    
    Parameters:
        cost_progression (list): List of costs for each generation.
        service_level_progression (list): List of service levels for each generation.
        num_generations (int): Total number of generations.
    """
    fig, ax1 = plt.subplots(figsize=(10, 6))  # Increase figure size to accommodate the legends

    # Plot cost progression on the left y-axis
    ax1.set_xlabel('Generation')
    ax1.set_ylabel('Average Cost', color='black')
    cost_line, = ax1.plot(range(1, num_generations + 1), cost_progression, color='black', label='Cost')
    ax1.tick_params(axis='y', labelcolor='black')

    # Create a second y-axis to plot service level on the right side (light green)
    ax2 = ax1.twinx()
    ax2.set_ylabel('Service Level (%)', color='black', labelpad=15)  # Move label to the right and adjust padding
    service_level_line, = ax2.plot(range(1, num_generations + 1), service_level_progression, color='lightgreen', label='Service Level')
    ax2.tick_params(axis='y', labelcolor='black')

    # Explicitly set label position for ax2 on the right
    ax2.yaxis.set_label_position('right')

    plt.title('(s, c, S) Policy Tuning')

    # Combine legends into a single one with a white background and no border
    ax1.legend(handles=[cost_line, service_level_line], loc='upper right', frameon=True, facecolor='white', edgecolor='none')

    plt.grid(True)
    plt.tight_layout(pad=2.0)  # Increase padding to accommodate right label
    plt.show()

def live_plot(cost_progression, service_level_progression, num_generations, ax=None):
    """
    Plot the cost and service level progression live during the algorithm execution.
    
    Parameters:
        cost_progression (list): List of costs for each generation.
        service_level_progression (list): List of service levels for each generation.
        num_generations (int): Total number of generations.
        ax (matplotlib.axes._axes.Axes, optional): The axis to plot on. Defaults to None.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))  # Increase figure size to accommodate the legends

    # Create a secondary axis only once
    if not hasattr(ax, 'ax2'):
        ax.ax2 = ax.twinx()

    # Clear the plot to update it correctly
    ax.clear()
    ax.ax2.clear()

    # Plot cost progression on the left y-axis
    cost_line, = ax.plot(range(1, len(cost_progression) + 1), cost_progression, color='darkgreen', label='Cost')
    ax.set_xlabel('Generation')
    ax.set_ylabel('Average Cost', color='black')
    ax.tick_params(axis='y', labelcolor='black')

    # Plot service level progression on the right y-axis (light green)
    service_level_line, = ax.ax2.plot(range(1, len(service_level_progression) + 1), service_level_progression, color='lightgreen', label='Service Level')
    ax.ax2.set_ylabel('Service Level (%)', color='black', labelpad=15)
    ax.ax2.tick_params(axis='y', labelcolor='black')

    # Explicitly set label position for ax2 on the right
    ax.ax2.yaxis.set_label_position('right')

    ax.set_title('(s, c, S) Policy Tuning')

    # Combine legends into a single one with a white background and no border
    ax.legend(handles=[cost_line, service_level_line], loc='upper right', frameon=True, facecolor='white', edgecolor='none')

    ax.grid(True)
    plt.tight_layout(pad=2.0)  # Increase padding to accommodate right label
    plt.pause(0.1)  # Pause to allow the plot to update
