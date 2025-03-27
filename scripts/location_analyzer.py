# scripts/location_analyzer.py
import pandas as pd
import matplotlib.pyplot as plt
import os

# Define our wellness factor categories and specific factors
WELLNESS_CATEGORIES = {
    "Health & Wellbeing": [
        "Healthcare Quality", 
        "Sunlight/Climate", 
        "Mental Health & Happiness"
    ],
    "Food & Nutrition": [
        "Food Quality (Natural/Traditional)",
        "Whole Foods Availability",
        "Traditional Cuisine"
    ],
    "Lifestyle & Activities": [
        "Fitness Opportunities",
        "Beach/Coastal Access",
        "Outdoor Recreation"
    ],
    "Community & Social": [
        "Family-Friendliness",
        "Community Cohesion",
        "Dating Scene/Romance"
    ],
    "Economic Factors": [
        "Cost of Living",
        "Average Salary",
        "Economic Stability"
    ],
    "Infrastructure & Services": [
        "Safety and Security",
        "Educational Opportunities",
        "Transportation Options"
    ],
    "Culture & Environment": [
        "Nightlife and Entertainment",
        "Religious Tolerance",
        "Political Environment"
    ]
}

# Flatten the factors for easier access
ALL_FACTORS = []
for category, factors in WELLNESS_CATEGORIES.items():
    ALL_FACTORS.extend(factors)

class Location:
    """
    Represents a location with wellness scores across different factors.
    """
    def __init__(self, name, country, location_type):
        """
        Initialize a location with basic information.
        
        Parameters:
        - name: Name of the location (city, town, etc.)
        - country: Country where the location is situated
        - location_type: Type of location (Coastal City, Small Town, etc.)
        """
        self.name = name
        self.country = country
        self.location_type = location_type
        self.scores = {}
        self.notes = {}
        
    def add_score(self, factor, score, note=None):
        """
        Add a score for a specific wellness factor.
        
        Parameters:
        - factor: The wellness factor being scored
        - score: Score value (1-10)
        - note: Optional note explaining the score
        """
        if factor not in ALL_FACTORS:
            raise ValueError(f"Unknown factor: {factor}. Must be one of {ALL_FACTORS}")
            
        if not 1 <= score <= 10:
            raise ValueError("Score must be between 1 and 10")
            
        self.scores[factor] = score
        if note:
            self.notes[factor] = note
            
    def get_score(self, factor):
        """Get score for a specific factor."""
        return self.scores.get(factor, None)
        
    def get_category_average(self, category):
        """Calculate average score for a category."""
        if category not in WELLNESS_CATEGORIES:
            raise ValueError(f"Unknown category: {category}")
            
        factors = WELLNESS_CATEGORIES[category]
        scores = [self.scores.get(factor, 0) for factor in factors]
        
        if not scores or all(score == 0 for score in scores):
            return 0
            
        return sum(scores) / len([s for s in scores if s > 0])
        
    def get_overall_score(self):
        """Calculate overall wellness score."""
        if not self.scores:
            return 0
            
        return sum(self.scores.values()) / len(self.scores)
        
    def __str__(self):
        """String representation of the location."""
        return f"{self.name}, {self.country} ({self.location_type})"


class WellnessAnalyzer:
    """
    Analyzes and compares wellness factors across different locations.
    """
    def __init__(self):
        """Initialize the wellness analyzer."""
        self.locations = {}
        
    def add_location(self, location):
        """Add a location to the analyzer."""
        self.locations[location.name] = location
        
    def get_location(self, name):
        """Get a location by name."""
        return self.locations.get(name)
        
    def compare_locations(self, factor=None, category=None):
        """
        Compare locations by factor or category.
        
        Parameters:
        - factor: Specific factor to compare
        - category: Category to compare (average of factors)
        
        Returns a pandas DataFrame with comparison data.
        """
        if not self.locations:
            return pd.DataFrame()
            
        if factor and category:
            raise ValueError("Specify either factor or category, not both")
            
        if factor:
            if factor not in ALL_FACTORS:
                raise ValueError(f"Unknown factor: {factor}")
                
            data = {
                'Location': [],
                'Country': [],
                'Type': [],
                factor: []
            }
            
            for name, location in self.locations.items():
                data['Location'].append(name)
                data['Country'].append(location.country)
                data['Type'].append(location.location_type)
                data[factor].append(location.get_score(factor) or 0)
                
            return pd.DataFrame(data)
            
        elif category:
            if category not in WELLNESS_CATEGORIES:
                raise ValueError(f"Unknown category: {category}")
                
            data = {
                'Location': [],
                'Country': [],
                'Type': [],
                f'{category} (Average)': []
            }
            
            for name, location in self.locations.items():
                data['Location'].append(name)
                data['Country'].append(location.country)
                data['Type'].append(location.location_type)
                data[f'{category} (Average)'].append(location.get_category_average(category))
                
            return pd.DataFrame(data)
            
        else:
            # Compare overall scores
            data = {
                'Location': [],
                'Country': [],
                'Type': [],
                'Overall Score': []
            }
            
            for name, location in self.locations.items():
                data['Location'].append(name)
                data['Country'].append(location.country)
                data['Type'].append(location.location_type)
                data['Overall Score'].append(location.get_overall_score())
                
            return pd.DataFrame(data)
    
    def visualize_comparison(self, factor=None, category=None, save_path=None):
        """
        Create a bar chart comparing locations by factor or category.
        
        Parameters:
        - factor: Specific factor to compare
        - category: Category to compare (average of factors)
        - save_path: Optional path to save the visualization
        """
        df = self.compare_locations(factor, category)
        
        if df.empty:
            print("No data available for visualization")
            return
            
        # Get the metric name (last column)
        metric = df.columns[-1]
        
        # Create the visualization
        plt.figure(figsize=(10, 6))
        
        # Create bars with different colors based on location type
        bars = plt.bar(df['Location'], df[metric])
        
        # Add location type as color
        location_types = df['Type'].unique()
        colors = plt.cm.tab10(range(len(location_types)))
        color_map = dict(zip(location_types, colors))
        
        for i, bar in enumerate(bars):
            location_type = df.iloc[i]['Type']
            bar.set_color(color_map[location_type])
        
        # Add labels and title
        plt.xlabel('Location')
        plt.ylabel('Score (1-10)')
        plt.title(f'Comparison of {metric} Across Locations')
        plt.ylim(0, 10)
        
        # Add a legend for location types
        from matplotlib.lines import Line2D
        legend_elements = [Line2D([0], [0], color=color, lw=4, label=loc_type) 
                          for loc_type, color in color_map.items()]
        plt.legend(handles=legend_elements, title='Location Type')
        
        # Rotate x-labels for better readability
        plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout()
        
        # Save if requested
        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            plt.savefig(save_path)
            print(f"Visualization saved to {save_path}")
            
        plt.show()
        
    def create_radar_chart(self, location_names, category=None, save_path=None):
        """
        Create a radar chart to compare locations across multiple factors.
        
        Parameters:
        - location_names: List of location names to compare
        - category: Optional category to limit factors (if None, uses all factors)
        - save_path: Optional path to save the visualization
        """
        import numpy as np
        
        # Validate locations
        locations = []
        for name in location_names:
            loc = self.get_location(name)
            if loc:
                locations.append(loc)
            else:
                print(f"Warning: Location '{name}' not found")
                
        if not locations:
            print("No valid locations for radar chart")
            return
            
        # Determine factors to plot
        if category:
            if category not in WELLNESS_CATEGORIES:
                raise ValueError(f"Unknown category: {category}")
            factors = WELLNESS_CATEGORIES[category]
        else:
            # Use all factors that have data for any location
            all_scored_factors = set()
            for loc in locations:
                all_scored_factors.update(loc.scores.keys())
            factors = list(all_scored_factors)
            
        if not factors:
            print("No factors with data available")
            return
            
        # Number of variables
        N = len(factors)
        
        # Create angle for each factor
        angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
        angles += angles[:1]  # Close the loop
        
        # Initialize the figure
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
        
        # Add each location
        for i, loc in enumerate(locations):
            values = [loc.get_score(factor) or 0 for factor in factors]
            values += values[:1]  # Close the loop
            
            color = plt.cm.tab10(i)
            ax.plot(angles, values, color=color, linewidth=2, label=loc.name)
            ax.fill(angles, values, color=color, alpha=0.25)
        
        # Fix axis to go from 0 to 10
        ax.set_ylim(0, 10)
        
        # Set factor labels
        plt.xticks(angles[:-1], factors, size=10)
        
        # Add legend
        plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
        
        # Add title
        title = f"Comparison of {category} Factors" if category else "Wellness Factor Comparison"
        plt.title(title, size=15, y=1.1)
        
        # Save if requested
        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            plt.savefig(save_path)
            print(f"Radar chart saved to {save_path}")
            
        plt.tight_layout()
        plt.show()


# Example usage function (for testing purposes)
def create_sample_data():
    """Create sample data for demonstration purposes."""
    analyzer = WellnessAnalyzer()
    
    # Create our selected locations
    athens = Location("Athens", "Greece", "Coastal City")
    brasov = Location("Brasov", "Romania", "Small Town")
    dubai = Location("Dubai", "UAE", "Modern City")
    penang = Location("Penang", "Malaysia", "Beach Community")
    taormina = Location("Taormina", "Italy", "Village")
    
    # Add some sample scores (these are just examples, not based on real data)
    # Athens scores
    athens.add_score("Healthcare Quality", 7, "Good public healthcare with some waiting times")
    athens.add_score("Sunlight/Climate", 9, "Mediterranean climate with abundant sunshine")
    athens.add_score("Food Quality (Natural/Traditional)", 9, "Strong tradition of fresh, local food")
    athens.add_score("Beach/Coastal Access", 8, "Good beaches within reach of the city")
    athens.add_score("Cost of Living", 6, "Moderate costs, affordable by European standards")
    
    # Brasov scores
    brasov.add_score("Healthcare Quality", 6, "Improving healthcare system")
    brasov.add_score("Sunlight/Climate", 5, "Four seasons with cold winters")
    brasov.add_score("Food Quality (Natural/Traditional)", 8, "Strong food traditions and local agriculture")
    brasov.add_score("Beach/Coastal Access", 1, "Landlocked mountain town")
    brasov.add_score("Cost of Living", 8, "Very affordable living costs")
    
    # Dubai scores
    dubai.add_score("Healthcare Quality", 9, "Excellent private healthcare")
    dubai.add_score("Sunlight/Climate", 7, "Abundant sunshine but extreme summer heat")
    dubai.add_score("Food Quality (Natural/Traditional)", 6, "Great international options but less local tradition")
    dubai.add_score("Beach/Coastal Access", 9, "Excellent beaches and water access")
    dubai.add_score("Cost of Living", 3, "Very high cost of living")
    
    # Penang scores
    penang.add_score("Healthcare Quality", 7, "Good quality private hospitals")
    penang.add_score("Sunlight/Climate", 8, "Tropical climate with consistent temperatures")
    penang.add_score("Food Quality (Natural/Traditional)", 9, "Famous for diverse, fresh cuisine")
    penang.add_score("Beach/Coastal Access", 9, "Island with abundant beaches")
    penang.add_score("Cost of Living", 8, "Very affordable for Western standards")
    
    # Taormina scores
    taormina.add_score("Healthcare Quality", 7, "Good access to Italian healthcare system")
    taormina.add_score("Sunlight/Climate", 9, "Mediterranean climate with mild winters")
    taormina.add_score("Food Quality (Natural/Traditional)", 10, "Exceptional Sicilian cuisine and food culture")
    taormina.add_score("Beach/Coastal Access", 10, "Beautiful beaches and coastal scenery")
    taormina.add_score("Cost of Living", 7, "Moderate by Italian standards")
    
    # Add locations to the analyzer
    analyzer.add_location(athens)
    analyzer.add_location(brasov)
    analyzer.add_location(dubai)
    analyzer.add_location(penang)
    analyzer.add_location(taormina)
    
    return analyzer


# Main function to run if this script is executed directly
if __name__ == "__main__":
    print("Creating Wellness Location Analyzer with sample data...")
    analyzer = create_sample_data()
    
    # Compare locations overall
    print("\nOverall Location Comparison:")

    # Main function to run if this script is executed directly
if __name__ == "__main__":
    print("Creating Wellness Location Analyzer with sample data...")
    analyzer = create_sample_data()
    
    # Compare locations overall
    print("\nOverall Location Comparison:")
    comparison_df = analyzer.compare_locations()
    print(comparison_df)
    
    # Visualize a comparison of a specific factor
    print("\nVisualizing Healthcare Quality comparison:")
    analyzer.visualize_comparison(factor="Healthcare Quality", 
                                 save_path="results/figures/healthcare_comparison.png")
    
    # Visualize a category comparison
    print("\nVisualizing Food & Nutrition category comparison:")
    analyzer.visualize_comparison(category="Food & Nutrition",
                                 save_path="results/figures/food_comparison.png")
    
    # Create a radar chart comparing all locations
    print("\nCreating radar chart for coastal locations:")
    coastal_locations = ["Athens", "Penang", "Taormina"]
    analyzer.create_radar_chart(coastal_locations,
                               save_path="results/figures/coastal_radar_chart.png")
    
    print("\nWellness Location Analyzer demo complete!")