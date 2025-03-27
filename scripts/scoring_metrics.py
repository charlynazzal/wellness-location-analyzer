# scripts/scoring_metrics.py

def calculate_healthcare_score(healthcare_rank, hospital_beds_per_1000, doctors_per_1000):
    """
    Calculate healthcare quality score (1-10) based on objective metrics.
    
    Parameters:
    - healthcare_rank: Country's healthcare system rank (lower is better)
    - hospital_beds_per_1000: Number of hospital beds per 1000 people
    - doctors_per_1000: Number of doctors per 1000 people
    """
    # Convert WHO rank to a 0-5 scale (assuming rank range 1-200)
    rank_score = max(5 - (healthcare_rank / 40), 0) if healthcare_rank else 2.5
    
    # Convert beds per 1000 to a 0-3 scale (worldwide average is around 3 beds/1000)
    beds_score = min(hospital_beds_per_1000 / 1.5, 3) if hospital_beds_per_1000 else 1.5
    
    # Convert doctors per 1000 to a 0-2 scale (worldwide average is around 1.5 doctors/1000)
    doctors_score = min(doctors_per_1000, 2) if doctors_per_1000 else 1
    
    # Combine scores and round to 1 decimal place
    return round(rank_score + beds_score + doctors_score, 1)

def calculate_climate_score(sunny_days_per_year, avg_temperature, rainfall_mm_per_year):
    """
    Calculate climate/sunlight score (1-10).
    
    Parameters:
    - sunny_days_per_year: Number of sunny days annually
    - avg_temperature: Average annual temperature in Celsius
    - rainfall_mm_per_year: Annual rainfall in millimeters
    """
    # Score for sunny days (0-4 points)
    sunny_score = min(sunny_days_per_year / 91.25, 4) if sunny_days_per_year else 2
    
    # Score for temperature (0-4 points) - optimal around 20-25°C
    if avg_temperature:
        if 20 <= avg_temperature <= 25:
            temp_score = 4
        elif 15 <= avg_temperature < 20 or 25 < avg_temperature <= 30:
            temp_score = 3
        elif 10 <= avg_temperature < 15 or 30 < avg_temperature <= 35:
            temp_score = 2
        else:
            temp_score = 1
    else:
        temp_score = 2
    
    # Score for rainfall (0-2 points) - moderate rainfall ideal
    if rainfall_mm_per_year:
        if 500 <= rainfall_mm_per_year <= 1200:
            rain_score = 2
        elif 250 <= rainfall_mm_per_year < 500 or 1200 < rainfall_mm_per_year <= 2000:
            rain_score = 1.5
        else:
            rain_score = 1
    else:
        rain_score = 1
    
    return round(sunny_score + temp_score + rain_score, 1)

def calculate_food_quality_score(organic_farms_per_capita, traditional_cuisine_preservation, food_safety_rating):
    """
    Calculate food quality score (1-10).
    
    Parameters:
    - organic_farms_per_capita: Number of organic farms per 100,000 people (0-100)
    - traditional_cuisine_preservation: Rating of how well traditional food practices are maintained (1-10)
    - food_safety_rating: Food safety rating (1-10)
    """
    # Score for organic food availability (0-3 points)
    organic_score = min(organic_farms_per_capita / 33.33, 3) if organic_farms_per_capita is not None else 1.5
    
    # Score for traditional cuisine (0-4 points)
    tradition_score = min(traditional_cuisine_preservation * 0.4, 4) if traditional_cuisine_preservation else 2
    
    # Score for food safety (0-3 points)
    safety_score = min(food_safety_rating * 0.3, 3) if food_safety_rating else 1.5
    
    return round(organic_score + tradition_score + safety_score, 1)

def calculate_cost_of_living_score(monthly_cost, local_purchasing_power, housing_affordability):
    """
    Calculate cost of living score (1-10) - higher score means more affordable.
    
    Parameters:
    - monthly_cost: Estimated monthly costs for single person (USD)
    - local_purchasing_power: Purchasing power relative to NYC (New York = 100)
    - housing_affordability: Housing price to income ratio (lower is better)
    """
    # Score for monthly costs (0-4 points) - lower costs = higher score
    if monthly_cost:
        if monthly_cost <= 700:
            cost_score = 4
        elif monthly_cost <= 1200:
            cost_score = 3
        elif monthly_cost <= 2000:
            cost_score = 2
        else:
            cost_score = 1
    else:
        cost_score = 2
    
    # Score for purchasing power (0-3 points)
    pp_score = min(local_purchasing_power / 33.33, 3) if local_purchasing_power else 1.5
    
    # Score for housing affordability (0-3 points) - lower ratio = higher score
    if housing_affordability:
        if housing_affordability <= 3:
            housing_score = 3
        elif housing_affordability <= 6:
            housing_score = 2
        elif housing_affordability <= 10:
            housing_score = 1
        else:
            housing_score = 0.5
    else:
        housing_score = 1.5
    
    return round(cost_score + pp_score + housing_score, 1)

def calculate_beach_access_score(distance_to_beach_km, beach_quality, beach_facilities):
    """
    Calculate beach/coastal access score (1-10).
    
    Parameters:
    - distance_to_beach_km: Distance to nearest beach in kilometers
    - beach_quality: Quality rating of beaches (1-10)
    - beach_facilities: Rating of beach facilities and services (1-10)
    """
    # Score for proximity (0-4 points)
    if distance_to_beach_km is not None:
        if distance_to_beach_km <= 1:
            distance_score = 4
        elif distance_to_beach_km <= 5:
            distance_score = 3
        elif distance_to_beach_km <= 20:
            distance_score = 2
        elif distance_to_beach_km <= 50:
            distance_score = 1
        else:
            distance_score = 0
    else:
        distance_score = 2
    
    # Score for beach quality (0-4 points)
    quality_score = min(beach_quality * 0.4, 4) if beach_quality else 2
    
    # Score for facilities (0-2 points)
    facilities_score = min(beach_facilities * 0.2, 2) if beach_facilities else 1
    
    return round(distance_score + quality_score + facilities_score, 1)

# Continue with similar functions for other factors...