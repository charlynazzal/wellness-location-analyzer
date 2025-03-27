#Import libraries we installed
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Check our environment using a function
def check_environment():
    print("Welcome to the Wellness LocationAnalyzer")
    print(f"Current date and time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    #Check pandas version
    print(f"Using matplotlib version: {matplotlib.__version__}")

    #Print project structure
    print("\nProject folders:")
    folders = ["data/raw", "data/processed", "scripts", "results/figures"]
    for folder in folders:
        exists = os.path.exists(folder)
        status = "✓ exists" if exists else "✗ missing"
        print(f" - {folder}: {status}")

# this line of code only runs when this file is executed directly
if __name__ == "__main__":
    check_environment()

    # Create a simple visualization to test matplotlib
    print("\nCreating a simple test visualization...")

    # Sample data for wellness scores (1-10) for three locations
    locations = ["Location A", "Location B", "Location C"]
    scores = [7, 8, 6]

    # Make a barchart
    plt.figure(figsize=(8,4))
    plt.bar(locations, scores, color=['#5DA5DA', '#FAA43A', '#60BD68'])
    plt.title("Sample Wellness Scores by Location")
    plt.ylabel("Wellness Score (1-10)")
    plt.ylim(0, 10)

     # Save the visualization
    os.makedirs("results/figures", exist_ok=True)
    plt.savefig("results/figures/test_visualization.png")
    print("Visualization saved to results/figures/test_visualization.png")
    
    print("\nEnvironment check complete!")