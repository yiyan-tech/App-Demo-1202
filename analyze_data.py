import pandas as pd

def analyze_cycling_data():
    try:
        df = pd.read_csv('cycling_survey_data.csv')
    except FileNotFoundError:
        print("Error: cycling_survey_data.csv not found. Run generate_mock_data.py first.")
        return

    report = []
    report.append("# Data Analysis Report: Indian Cyclist Photography Preferences\n")
    
    # 1. Segment Distribution
    segment_dist = df['Segment'].value_counts(normalize=True) * 100
    report.append("## 1. User Segment Distribution")
    for segment, pct in segment_dist.items():
        report.append(f"- **{segment}**: {pct:.1f}%")
    report.append("")

    # 2. Average Budget by Segment
    avg_budget = df.groupby('Segment')['Budget_INR'].mean().sort_values(ascending=False)
    report.append("## 2. Average Budget by Segment (INR)")
    for segment, budget in avg_budget.items():
        report.append(f"- **{segment}**: ₹{budget:,.0f}")
    report.append("")

    # 3. Top Needs per Segment
    report.append("## 3. Top Photography Needs per Segment")
    for segment in df['Segment'].unique():
        top_need = df[df['Segment'] == segment]['Primary_Need'].mode()[0]
        report.append(f"- **{segment}**: {top_need}")
    report.append("")

    # 4. Device Preference
    report.append("## 4. Device Preference Overview")
    device_dist = df['Preferred_Device'].value_counts(normalize=True) * 100
    for device, pct in device_dist.items():
        report.append(f"- **{device}**: {pct:.1f}%")
    
    # Write report to file
    with open('DATA_ANALYSIS_SUMMARY.md', 'w') as f:
        f.write('\n'.join(report))
    
    print("Analysis complete. Summary saved to DATA_ANALYSIS_SUMMARY.md")
    print('\n'.join(report))

if __name__ == "__main__":
    analyze_cycling_data()
