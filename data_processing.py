import pandas as pd
from pathlib import Path


def load_activity_data():
    """Load activity data from CSV file."""
    # Resolve path relative to the project root
    data_path = Path(__file__).resolve().parent / 'data' / 'activity.csv'
    df = pd.read_csv(data_path)
    return df


def compute_stats(df: pd.DataFrame) -> tuple:
    """Compute mean and max power from dataframe."""
    if 'PowerOriginal' not in df.columns:
        return 0, 0
    mean_power = df['PowerOriginal'].mean()
    max_power = df['PowerOriginal'].max()
    return mean_power, max_power


def compute_zones(df: pd.DataFrame, max_hr: int) -> pd.DataFrame:
    """
    Compute heart rate zones based on max_hr.
    
    Zones:
    - Zone 1: 50-60% of max_hr (Recovery)
    - Zone 2: 60-70% of max_hr (Endurance)
    - Zone 3: 70-80% of max_hr (Tempo)
    - Zone 4: 80-90% of max_hr (Threshold)
    - Zone 5: 90-100% of max_hr (VO2max)
    """
    df = df.copy()
    
    if 'HeartRate' not in df.columns:
        df['Zone'] = 0
        return df
    
    def get_zone(hr):
        if pd.isna(hr):
            return 0
        hr_pct = (hr / max_hr) * 100
        if hr_pct < 60:
            return 1
        elif hr_pct < 70:
            return 2
        elif hr_pct < 80:
            return 3
        elif hr_pct < 90:
            return 4
        else:
            return 5
    
    df['Zone'] = df['HeartRate'].apply(get_zone)
    return df


def compute_time_per_zone(df: pd.DataFrame) -> pd.Series:
    """Compute total time spent in each heart rate zone."""
    if 'Zone' not in df.columns:
        return pd.Series()
    
    zone_time = df['Zone'].value_counts().sort_index()
    zone_labels = {
        1: 'Zone 1 (Recovery)',
        2: 'Zone 2 (Endurance)',
        3: 'Zone 3 (Tempo)',
        4: 'Zone 4 (Threshold)',
        5: 'Zone 5 (VO2max)'
    }
    zone_time.index = zone_time.index.map(lambda x: zone_labels.get(x, f'Zone {x}'))
    return zone_time


def compute_avg_power_per_zone(df: pd.DataFrame) -> pd.Series:
    """Compute average power for each heart rate zone."""
    if 'Zone' not in df.columns or 'PowerOriginal' not in df.columns:
        return pd.Series()
    
    avg_power = df.groupby('Zone')['PowerOriginal'].mean()
    zone_labels = {
        1: 'Zone 1 (Recovery)',
        2: 'Zone 2 (Endurance)',
        3: 'Zone 3 (Tempo)',
        4: 'Zone 4 (Threshold)',
        5: 'Zone 5 (VO2max)'
    }
    avg_power.index = avg_power.index.map(lambda x: zone_labels.get(x, f'Zone {x}'))
    return avg_power
