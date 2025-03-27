# scripts/add_location.py
import json
import os
import sys
from pathlib import Path
from scoring_metrics import (
    calculate_healthcare_score,
    calculate_climate_score,
    calculate_food_quality_score,
    calculate_cost_of_living_score,
    calculate_beach_access_score
)

# Add the project root to path to enable imports
script_dir = Path(__file__).parent
project_root = script_dir.parent
sys.path.append(str(project_root))

from scripts.location_analyzer import Location, WellnessAnalyzer, WELLNESS_CATEGORIES, ALL_FACTORS

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def load_existing_data(file_path):
    """Load existing location data from a JSON file."""
    if not os.path.exists(file_path):
        return WellnessAnalyzer()
    
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        analyzer = WellnessAnalyzer()
        
        for loc_data in data['locations']:
            location = Location(
                loc_data['name'],
                loc_data['country'],
                loc_data['location_type']
            )
            
            # Add scores
            for factor, score in loc_data['scores'].items():
                note = loc_data['notes'].get(factor)
                location.add_score(factor, score, note)
            
            analyzer.add_location(location)
        
        return analyzer
    except Exception as e:
        print(f"Error loading data: {e}")
        return WellnessAnalyzer()

def save_data(analyzer, file_path):
    """Save location data to a JSON file."""
    data = {'locations': []}
    
    for name, location in analyzer.locations.items():
        loc_data = {
            'name': location.name,
            'country': location.country,
            'location_type': location.location_type,
            'scores': location.scores,
            'notes': location.notes
        }
        data['locations'].append(loc_data)
    
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
    
    print(f"Data saved to {file_path}")

def add_new_location(analyzer):
    """Add a new location with objectively calculated scores."""
    clear_screen()
    print("=== Add New Location ===\n")
    
    name = input("Location name: ")
    country = input("Country: ")
    
    print("\nLocation types: Coastal City, Beach Community, Modern City, Small Town, Village, etc.")
    location_type = input("Location type: ")
    
    location = Location(name, country, location_type)
    
    print("\nNow let's add raw data to calculate wellness scores.")
    print("For each metric, enter the data or press Enter to skip.")
    
    # Healthcare metrics
    print("\n=== Healthcare Metrics ===")
    try:
        healthcare_rank = float(input("Healthcare system rank (lower is better): ") or "0") 
        hospital_beds = float(input("Hospital beds per 1000 people: ") or "0")
        doctors = float(input("Doctors per 1000 people: ") or "0")
        
        if healthcare_rank or hospital_beds or doctors:
            healthcare_score = calculate_healthcare_score(healthcare_rank, hospital_beds, doctors)
            healthcare_note = f"Based on: Rank={healthcare_rank}, Beds={hospital_beds}/1000, Doctors={doctors}/1000"
            location.add_score("Healthcare Quality", healthcare_score, healthcare_note)
            print(f"Calculated Healthcare Score: {healthcare_score}/10")
    except ValueError:
        print("Invalid input. Skipping healthcare score.")
    
    # Climate metrics
    print("\n=== Climate Metrics ===")
    try:
        sunny_days = float(input("Sunny days per year: ") or "0")
        avg_temp = float(input("Average temperature (Celsius): ") or "0")
        rainfall = float(input("Annual rainfall (mm): ") or "0")
        
        if sunny_days or avg_temp or rainfall:
            climate_score = calculate_climate_score(sunny_days, avg_temp, rainfall)
            climate_note = f"Based on: {sunny_days} sunny days, {avg_temp}°C avg temp, {rainfall}mm rainfall"
            location.add_score("Sunlight/Climate", climate_score, climate_note)
            print(f"Calculated Climate Score: {climate_score}/10")
    except ValueError:
        print("Invalid input. Skipping climate score.")
    
    # Food quality metrics
    print("\n=== Food Quality Metrics ===")
    try:
        organic_farms = float(input("Organic farms per 100,000 people: ") or "0")
        cuisine_preservation = float(input("Traditional cuisine preservation (1-10): ") or "0")
        food_safety = float(input("Food safety rating (1-10): ") or "0")
        
        if organic_farms or cuisine_preservation or food_safety:
            food_score = calculate_food_quality_score(organic_farms, cuisine_preservation, food_safety)
            food_note = f"Based on: {organic_farms} organic farms per 100k, cuisine preservation={cuisine_preservation}, safety={food_safety}"
            location.add_score("Food Quality (Natural/Traditional)", food_score, food_note)
            print(f"Calculated Food Quality Score: {food_score}/10")
    except ValueError:
        print("Invalid input. Skipping food quality score.")
    
    # Cost of living metrics
    print("\n=== Cost of Living Metrics ===")
    try:
        monthly_cost = float(input("Monthly costs for single person (USD): ") or "0")
        purchasing_power = float(input("Purchasing power relative to NYC (NYC=100): ") or "0")
        housing_ratio = float(input("Housing price to income ratio: ") or "0")
        
        if monthly_cost or purchasing_power or housing_ratio:
            cost_score = calculate_cost_of_living_score(monthly_cost, purchasing_power, housing_ratio)
            cost_note = f"Based on: ${monthly_cost} monthly costs, {purchasing_power} purchasing power, {housing_ratio} housing ratio"
            location.add_score("Cost of Living", cost_score, cost_note)
            print(f"Calculated Cost of Living Score: {cost_score}/10")
    except ValueError:
        print("Invalid input. Skipping cost of living score.")
    
    # Beach access metrics
    print("\n=== Beach Access Metrics ===")
    try:
        beach_distance = float(input("Distance to nearest beach (km): ") or "-1")
        beach_quality = float(input("Beach quality rating (1-10): ") or "0")
        beach_facilities = float(input("Beach facilities rating (1-10): ") or "0")
        
        if beach_distance >= 0 or beach_quality or beach_facilities:
            beach_score = calculate_beach_access_score(beach_distance, beach_quality, beach_facilities)
            beach_note = f"Based on: {beach_distance}km to beach, quality={beach_quality}, facilities={beach_facilities}"
            location.add_score("Beach/Coastal Access", beach_score, beach_note)
            print(f"Calculated Beach Access Score: {beach_score}/10")
    except ValueError:
        print("Invalid input. Skipping beach access score.")
    
    # Add other metrics as needed...
    
    # Allow manual entry for factors without automated calculation
    print("\n=== Additional Factors ===")
    print("Would you like to manually enter scores for other factors? (y/n)")
    if input("> ").lower() == 'y':
        for category, factors in WELLNESS_CATEGORIES.items():
            for factor in factors:
                if factor not in location.scores:
                    print(f"\n{factor}")
                    score_input = input(f"Score (1-10) or Enter to skip: ")
                    if score_input:
                        try:
                            score = float(score_input)
                            if 1 <= score <= 10:
                                data_source = input("Data source: ")
                                note = f"Source: {data_source}" if data_source else None
                                location.add_score(factor, score, note)
                        except ValueError:
                            print("Invalid input. Skipping.")
    
    analyzer.add_location(location)
    print(f"\nLocation '{name}' added successfully!")
    return analyzer

def view_locations(analyzer):
    """View all locations and their overall scores."""
    clear_screen()
    print("=== All Locations ===\n")
    
    if not analyzer.locations:
        print("No locations added yet.")
        return
    
    # Get comparison data
    comparison = analyzer.compare_locations()
    
    # Sort by overall score (descending)
    comparison = comparison.sort_values('Overall Score', ascending=False)
    
    # Display with formatting
    for i, row in comparison.iterrows():
        print(f"{row['Location']}, {row['Country']} ({row['Type']})")
        print(f"  Overall Score: {row['Overall Score']:.1f}/10")
    
    input("\nPress Enter to continue...")

def compare_specific_locations(analyzer):
    """Compare specific locations on factors or categories."""
    clear_screen()
    print("=== Compare Locations ===\n")
    
    if len(analyzer.locations) < 2:
        print("You need at least 2 locations to make a comparison.")
        input("\nPress Enter to continue...")
        return
    
    # List available locations
    print("Available locations:")
    for i, name in enumerate(analyzer.locations.keys(), 1):
        print(f"{i}. {name}")
    
    # Get locations to compare
    print("\nEnter location numbers to compare (comma-separated):")
    selection = input("> ")
    
    try:
        indices = [int(idx.strip()) - 1 for idx in selection.split(',')]
        location_names = list(analyzer.locations.keys())
        selected_locations = [location_names[idx] for idx in indices]
    except (ValueError, IndexError):
        print("Invalid selection.")
        input("\nPress Enter to continue...")
        return
    
    # Choose comparison type
    print("\nCompare by:")
    print("1. Specific factor")
    print("2. Category average")
    print("3. Overall score")
    print("4. Radar chart (multiple factors)")
    
    choice = input("> ")
    
    if choice == '1':
        # List factors
        print("\nAvailable factors:")
        for i, factor in enumerate(ALL_FACTORS, 1):
            print(f"{i}. {factor}")
        
        factor_idx = int(input("Select factor number: ")) - 1
        if 0 <= factor_idx < len(ALL_FACTORS):
            factor = ALL_FACTORS[factor_idx]
            analyzer.visualize_comparison(factor=factor)
        else:
            print("Invalid factor selection.")
    
    elif choice == '2':
        # List categories
        print("\nAvailable categories:")
        for i, category in enumerate(WELLNESS_CATEGORIES.keys(), 1):
            print(f"{i}. {category}")
        
        cat_idx = int(input("Select category number: ")) - 1
        categories = list(WELLNESS_CATEGORIES.keys())
        if 0 <= cat_idx < len(categories):
            category = categories[cat_idx]
            analyzer.visualize_comparison(category=category)
        else:
            print("Invalid category selection.")
    
    elif choice == '3':
        analyzer.visualize_comparison()
    
    elif choice == '4':
        # Radar chart for selected locations
        print("\nAvailable categories (or leave blank for all factors):")
        for i, category in enumerate(WELLNESS_CATEGORIES.keys(), 1):
            print(f"{i}. {category}")
        
        cat_input = input("Select category number (or press Enter for all): ")
        
        if cat_input:
            cat_idx = int(cat_input) - 1
            categories = list(WELLNESS_CATEGORIES.keys())
            if 0 <= cat_idx < len(categories):
                category = categories[cat_idx]
                analyzer.create_radar_chart(selected_locations, category=category)
            else:
                print("Invalid category selection.")
        else:
            analyzer.create_radar_chart(selected_locations)
    
    else:
        print("Invalid choice.")
    
    input("\nPress Enter to continue...")

def main():
    """Main function to run the location data manager."""
    data_file = os.path.join(project_root, "data", "processed", "locations.json")
    
    # Load existing data
    analyzer = load_existing_data(data_file)
    
    while True:
        clear_screen()
        print("=== Wellness Location Analyzer ===")
        print("1. Add new location")
        print("2. View all locations")
        print("3. Compare locations")
        print("4. Save and exit")
        
        choice = input("\nChoose an option: ")
        
        if choice == '1':
            analyzer = add_new_location(analyzer)
        elif choice == '2':
            view_locations(analyzer)
        elif choice == '3':
            compare_specific_locations(analyzer)
        elif choice == '4':
            save_data(analyzer, data_file)
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()