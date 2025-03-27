## Project Overview

The Wellness Location Analyzer is a Python-based tool designed to objectively compare different locations around the world based on wellness factors. This project helps users make data-driven decisions about potential places to live, travel, or retire by analyzing and visualizing key wellness metrics.

## Motivation

Choosing where to live is one of life's most significant decisions, impacting our health, happiness, and overall quality of life. This project was created to bring objectivity and data to this decision by:

- Quantifying wellness factors across different locations
- Providing consistent scoring methodology
- Enabling visual comparisons between locations
- Highlighting strengths and weaknesses of each place

## Features

- **Comprehensive wellness metrics**: Analyzes 21 different factors across 7 categories
- **Objective scoring methodology**: Uses real-world data to calculate scores
- **Data visualization**: Generates bar charts and radar charts for easy comparison
- **Location database**: Stores and retrieves location data in JSON format
- **Interactive data entry**: Command-line interface for adding new locations
- **Detailed reporting**: Produces comprehensive analysis reports

## Technologies Used

- **Python 3.x**: Core programming language
- **pandas**: Data manipulation and analysis
- **matplotlib**: Data visualization
- **NumPy**: Numerical computations
- **JSON**: Data storage

## Project Structure
wellness_analyzer/
├── data/
│   ├── raw/              # Raw data files (not used in current version)
│   └── processed/        # Processed data files
│       └── locations.json # Database of analyzed locations
├── docs/
│   ├── data_sources.md             # Documentation of data sources
│   ├── location_research_template.md # Template for researching locations
│   └── research/                   # Individual location research files
│       ├── barcelona_research.md
│       ├── london_research.md
│       ├── athens_research.md
│       ├── tuscany_research.md
│       └── dubai_research.md
├── results/
│   ├── figures/          # Generated visualizations
│   └── reports/          # Analysis reports
│       └── location_analysis_report.md
├── scripts/
│   ├── hello_project.py     # Initial test script
│   ├── location_analyzer.py # Core functionality
│   ├── add_location.py      # Interactive data entry tool
│   └── scoring_metrics.py   # Objective scoring functions
├── venv/               # Virtual environment (not tracked in git)
├── .gitignore         # Git ignore file
├── README.md          # This file
└── requirements.txt   # Project dependencies
Copy
## Installation and Setup

1. **Clone the repository**
git clone https://github.com/yourusername/wellness-analyzer.git
cd wellness-analyzer
Copy
2. **Create and activate a virtual environment**
python -m venv venv
On Windows
venv\Scripts\activate
On macOS/Linux
source venv/bin/activate
Copy
3. **Install dependencies**
pip install -r requirements.txt
Copy
## Usage

### Adding a new location

1. Run the add_location.py script:
python scripts/add_location.py
Copy
2. Select option 1 to add a new location

3. Enter the requested metrics when prompted

4. Select option 4 to save and exit when finished

### Viewing and comparing locations

1. Run the add_location.py script:
python scripts/add_location.py
Copy
2. Select option 2 to view all locations or option 3 to compare locations

3. Follow the prompts to select specific locations and metrics for comparison

4. Visualizations will be displayed and saved to the results/figures directory

## Sample Results

The project currently includes analysis of five diverse locations:

1. Barcelona, Spain (Coastal City)
2. London, United Kingdom (Metropolitan City)
3. Athens, Greece (Coastal City)
4. Tuscany, Italy (Rural Region)
5. Dubai, United Arab Emirates (Modern City)

### Overall Rankings

1. Barcelona - 7.9/10
2. Tuscany - 7.7/10
3. Dubai - 7.4/10
4. Athens - 7.3/10
5. London - 7.3/10

### Sample Visualizations

#### Overall Score Comparison
![Overall Score Comparison](results/figures/overall_comparison.png)

#### Wellness Factors Radar Chart
![Wellness Radar Chart](results/figures/wellness_radar_chart.png)

## Wellness Factors Analyzed

- **Health & Wellbeing**: Healthcare Quality, Sunlight/Climate, Mental Health & Happiness
- **Food & Nutrition**: Food Quality, Whole Foods Availability, Traditional Cuisine
- **Lifestyle & Activities**: Fitness Opportunities, Beach/Coastal Access, Outdoor Recreation
- **Community & Social**: Family-Friendliness, Community Cohesion, Dating Scene/Romance
- **Economic Factors**: Cost of Living, Average Salary, Economic Stability
- **Infrastructure & Services**: Safety and Security, Educational Opportunities, Transportation Options
- **Culture & Environment**: Nightlife and Entertainment, Religious Tolerance, Political Environment

## Future Enhancements

- **Personalized weighting**: Allow users to weight factors based on personal priorities
- **More locations**: Expand the database with additional cities and regions
- **API integration**: Automatic data retrieval from public APIs
- **Web interface**: Create a Flask or Streamlit web application
- **Machine learning**: Recommend locations based on user preferences
- **Mobile app**: Develop a mobile version for on-the-go use

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Data sources including WHO, Numbeo, climate databases, and various tourism boards
- Inspiration from quality of life indices and an elegant lifestyle
- Created as a final project for the University of Michigan "Python for Everybody" course on Coursera