import pandas as pd
import numpy as np

def generate_cycling_data(num_samples=1000):
    np.random.seed(42)
    
    # User Segments
    segments = ['Commuter', 'Fitness/Recreational', 'Enthusiast/Pro']
    segment_probs = [0.5, 0.35, 0.15]
    
    user_segments = np.random.choice(segments, num_samples, p=segment_probs)
    
    # Primary Needs based on segment
    needs_map = {
        'Commuter': ['Safety/Dashcam', 'Evidence', 'Battery Life'],
        'Fitness/Recreational': ['Social Sharing', 'Scenery', 'Ease of Use'],
        'Enthusiast/Pro': ['Data Overlay', 'Image Quality', 'Stabilization']
    }
    
    primary_needs = []
    preferred_devices = []
    budget_inr = []
    
    for segment in user_segments:
        # Needs
        needs_options = needs_map[segment]
        primary_needs.append(np.random.choice(needs_options))
        
        # Devices
        if segment == 'Commuter':
            device = np.random.choice(['Smartphone Mount', 'Budget Action Cam'], p=[0.7, 0.3])
            budget = np.random.randint(500, 5000)
        elif segment == 'Fitness/Recreational':
            device = np.random.choice(['Smartphone Mount', 'Mid-range Action Cam', '360 Cam'], p=[0.5, 0.4, 0.1])
            budget = np.random.randint(5000, 20000)
        else: # Pro
            device = np.random.choice(['High-end Action Cam', '360 Cam', 'Drone'], p=[0.6, 0.3, 0.1])
            budget = np.random.randint(20000, 50000)
            
        preferred_devices.append(device)
        budget_inr.append(budget)
    
    data = {
        'User_ID': range(1, num_samples + 1),
        'Segment': user_segments,
        'Primary_Need': primary_needs,
        'Preferred_Device': preferred_devices,
        'Budget_INR': budget_inr,
        'Location': np.random.choice(['Mumbai', 'Bangalore', 'Delhi', 'Pune', 'Chennai', 'Tier-2 City'], num_samples)
    }
    
    df = pd.DataFrame(data)
    df.to_csv('cycling_survey_data.csv', index=False)
    print("Mock data generated: cycling_survey_data.csv")

if __name__ == "__main__":
    generate_cycling_data()
