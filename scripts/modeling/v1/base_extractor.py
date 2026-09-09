"""
Base extractor class with common metrics for all datalogger types.
Handles: structural profiling, reliability metrics, temporal analysis.
"""
import pandas as pd
import numpy as np
from abc import ABC, abstractmethod


class BaseExtractor(ABC):
    """Abstract base class for datalogger extractors."""
    
    def __init__(self):
        """Initialize with common parameters."""
        self.INTERVAL_MINUTES = 5  # Standard interval
        self.BLACKOUT_THRESHOLD = 7  # 7 minutes = 1+ missed readings
        self.POWER_THRESHOLD = 0.5  # 0.5W minimum to consider "on"
        self.MAX_POWER_W = 100  # Default max power threshold (override in subclasses)
    
    def detect_power_anomalies(self, df):
        """Detect and report power readings exceeding MAX_POWER_W threshold.
        
        Returns:
            dict: Statistics about anomalies (count, percentage, max value, examples)
        """
        anomalies = df[df['p_total'] > self.MAX_POWER_W]
        
        if len(anomalies) == 0:
            return {
                'anomaly_count': 0,
                'anomaly_percentage': 0.0,
                'status': f'✓ CLEAN: All readings ≤ {self.MAX_POWER_W}W (max: {df["p_total"].max():.2f}W)'
            }
        
        anomaly_percentage = (len(anomalies) / len(df)) * 100 if len(df) > 0 else 0.0
        top_anomalies = anomalies.nlargest(5, 'p_total')[['corrected_timestamp', 'p_total']].values.tolist() if 'corrected_timestamp' in anomalies.columns else []
        
        return {
            'anomaly_count': len(anomalies),
            'anomaly_percentage': round(anomaly_percentage, 2),
            'max_power_reading': round(df['p_total'].max(), 2),
            'anomaly_threshold': self.MAX_POWER_W,
            'status': f'⚠ WARNING: {len(anomalies)} readings ({anomaly_percentage:.2f}%) exceed {self.MAX_POWER_W}W',
            'top_anomalies': top_anomalies
        }
        
    @abstractmethod
    def preprocess(self, filename):
        """Preprocess and standardize dataframe. Must return df with p_total, v_pv."""
        pass
    
    @abstractmethod
    def extract_hardware(self, df):
        """Extract appliance wattages. Returns dict."""
        pass
    
    @abstractmethod
    def extract_hourly_probs(self, df):
        """Extract hourly usage probabilities. Returns dict."""
        pass
    
    @abstractmethod
    def extract_ramp_params(self, df):
        """Extract RAMP parameters. Returns dict."""
        pass
    
    @abstractmethod
    def extract_power_variation(self, df):
        """Extract power variation metrics. Returns dict."""
        pass
    
    # --- COMMON METRICS (inherited by all extractors) ---
    
    def extract_structural_metrics(self, df):
        """Extract structural profiling & resilience metrics (TIER 2)."""
        total_power = df['p_total']
        
        # Modal Peak Hour: hour with highest MEAN power (when active)
        # Use mean instead of median to handle sparse/zero data better
        hourly_means = df.groupby(df['timestamp'].dt.hour)['p_total'].mean()
        
        # Find peak hour: prioritize hours with actual usage (not just zeros)
        # If multiple hours tie at max, pick the one with most variance (most active)
        if len(hourly_means) > 0:
            max_power = hourly_means.max()
            if max_power > 0:
                # Normal case: pick hour with highest mean power
                modal_peak_hour = int(hourly_means.idxmax())
            else:
                # All hours have zero mean (data is all NaN) - use median as fallback
                hourly_medians = df.groupby(df['timestamp'].dt.hour)['p_total'].median()
                modal_peak_hour = int(hourly_medians.idxmax()) if hourly_medians.max() > 0 else 0
        else:
            modal_peak_hour = 0
        
        # Safety Lights Probability: likelihood of lights on during midnight-4am (security/safety)
        # Filter data for hours 0-4 (midnight to 4am)
        night_hours_df = df[(df['timestamp'].dt.hour >= 0) & (df['timestamp'].dt.hour < 4)]
        
        if len(night_hours_df) > 0:
            # Count days where lights are on during this period (power > threshold)
            nights_with_lights = night_hours_df[night_hours_df['p_total'] > self.POWER_THRESHOLD]['date_only'].nunique()
            total_nights = night_hours_df['date_only'].nunique()
            safety_lights_probability = round(nights_with_lights / total_nights, 3) if total_nights > 0 else 0.0
        else:
            safety_lights_probability = 0.0
        
        # MRSD (Mean Relative Standard Deviation) - Chaos Index
        # Using "Monthly MRSD" approach: calculate MRSD for each 30-day chunk,
        # then take the median. This prevents seasonal variations from inflating
        # the metric and allows fair comparison between users with different
        # dataset lengths (2 months vs 12 months).
        monthly_mrsd_values = []
        unique_dates = sorted(df['date_only'].unique())
        
        if len(unique_dates) > 0:
            start_date = unique_dates[0]
            
            while start_date <= unique_dates[-1]:
                # 30-day window
                end_date = start_date + pd.Timedelta(days=30)
                
                # Get data for this month
                month_data = df[(df['date_only'] >= start_date) & (df['date_only'] < end_date)]
                
                if len(month_data) > 0:
                    # Calculate daily CVs for this month only
                    daily_cv_month = []
                    for date in month_data['date_only'].unique():
                        day_power = month_data[month_data['date_only'] == date]['p_total']
                        day_mean = day_power.mean()
                        day_std = day_power.std()
                        if day_mean > 0:
                            daily_cv_month.append(day_std / day_mean)
                    
                    # Monthly MRSD = mean of daily CVs in this 30-day chunk
                    if daily_cv_month:
                        monthly_mrsd_values.append(np.mean(daily_cv_month))
                
                # Move to next month
                start_date = end_date
        
        # Chaos Index = median of monthly MRSDs (level playing field across dataset lengths)
        mrsd_chaos_index = round(np.median(monthly_mrsd_values), 3) if monthly_mrsd_values else 0.0
        
        # Relative Mean Power by time-of-day
        time_periods = {
            'morning': df[(df['timestamp'].dt.hour >= 6) & (df['timestamp'].dt.hour < 12)]['p_total'].mean(),
            'daytime': df[(df['timestamp'].dt.hour >= 12) & (df['timestamp'].dt.hour < 18)]['p_total'].mean(),
            'evening': df[(df['timestamp'].dt.hour >= 18) & (df['timestamp'].dt.hour < 24)]['p_total'].mean(),
            'night': df[(df['timestamp'].dt.hour >= 0) & (df['timestamp'].dt.hour < 6)]['p_total'].mean()
        }
        
        overall_mean_power = df['p_total'].mean()
        relative_mean_power = {}
        for period, mean_val in time_periods.items():
            if overall_mean_power > 0:
                relative_mean_power[period] = round(mean_val / overall_mean_power, 3)
            else:
                relative_mean_power[period] = 0.0
        
        return {
            'modal_peak_hour': modal_peak_hour,
            'safety_lights_probability': safety_lights_probability,
            'mrsd_chaos_index': mrsd_chaos_index,
            'relative_mean_power': relative_mean_power,
            'overall_mean_power_W': round(overall_mean_power, 2)
        }
    
    def extract_stacking_index(self, df, datalogger_type):
        """Extract Appliance Stacking Index by detecting simultaneous device activation.
        
        For TPDIN: Detects when 2+ separate devices have power > 0 simultaneously.
        For OLD: Detects stacking of LEDs or LED+USB combination.
            - p_led > 3W: Both LEDs are on (LED stacking)
            - 0 < p_led < 3W AND p_usb > 0: One LED + USB on
        For BLUE: Not computed (single appliance).
        
        Args:
            df: Dataframe with individual appliance power columns
            datalogger_type: 'old', 'tpdin', or 'blue'
        
        Returns:
            dict: Stacking metrics based on device-level activation
        """
        if datalogger_type == 'tpdin':
            # TPDIN has 3 separate devices
            appliance_names = 'LED_1, LED_2, USB'
            
            # Count devices active per row (power > POWER_THRESHOLD)
            devices_active = (
                (df['p_led_1'] > self.POWER_THRESHOLD).astype(int) +
                (df['p_led_2'] > self.POWER_THRESHOLD).astype(int) +
                (df['p_usb'] > self.POWER_THRESHOLD).astype(int)
            )
            
            # Stacking = rows where 2+ devices are active
            stacking_events = (devices_active >= 2).sum()
            total_active_rows = (devices_active >= 1).sum()
            
            if total_active_rows == 0:
                stacking_index = 0.0
            else:
                stacking_index = (stacking_events / total_active_rows) * 100
            
            return {
                'stacking_index': round(stacking_index, 1),
                'stacking_threshold_W': 0.0,
                'stacking_events_count': stacking_events,
                'total_active_rows': total_active_rows,
                'appliance_names': appliance_names,
                'stacking_interpretation': 'Periods where 2+ devices simultaneously active (power > 0W)'
            }
            
        elif datalogger_type == 'old':
            # OLD has combined LED and separate USB measurements
            appliance_names = 'LED (combined), USB'
            
            # Stacking cases:
            # 1. p_led > 3W: Both LEDs are on (LED stacking)
            # 2. 0 < p_led <= 3W AND p_usb > 0: One LED + USB on
            both_leds_on = df['p_led'] > 3.0
            one_led_and_usb = ((df['p_led'] > 0) & (df['p_led'] <= 3.0) & (df['p_usb'] > 0))
            
            stacking_events = (both_leds_on | one_led_and_usb).sum()
            
            # Total active rows: at least one device is on
            total_active_rows = ((df['p_led'] > 0) | (df['p_usb'] > 0)).sum()
            
            if total_active_rows == 0:
                stacking_index = 0.0
            else:
                stacking_index = (stacking_events / total_active_rows) * 100
            
            return {
                'stacking_index': round(stacking_index, 1),
                'stacking_threshold_W': 0.0,
                'stacking_events_count': stacking_events,
                'total_active_rows': total_active_rows,
                'appliance_names': appliance_names,
                'stacking_interpretation': 'Periods where: both LEDs on (p_led > 3W) OR one LED + USB both on (0 < p_led <= 3W AND p_usb > 0)'
            }
            
        else:  # blue
            # Single appliance - stacking not computed
            return {
                'stacking_index': None,
                'stacking_threshold_W': 0.0,
                'stacking_events_count': 0,
                'total_active_rows': 0,
                'appliance_names': 'CONS',
                'stacking_interpretation': 'Single appliance system (stacking not computed)'
            }
    
    def extract_reliability_metrics(self, df):
        """Extract blackout and reliability metrics."""
        df_copy = df.copy()
        df_copy['time_diff_minutes'] = df_copy['timestamp'].diff().dt.total_seconds() / 60
        
        # Detect blackouts from two sources:
        # 1. Timestamp gaps > BLACKOUT_THRESHOLD
        gap_blackouts = df_copy['time_diff_minutes'] > self.BLACKOUT_THRESHOLD
        
        # 2. Rows where all power measurements are NaN (no data recorded)
        # Find all voltage and current columns
        voltage_cols = [col for col in df_copy.columns if col.startswith('v_') and col != 'v_pv']
        current_cols = [col for col in df_copy.columns if col.startswith('c_')]
        measurement_cols = voltage_cols + current_cols
        
        if measurement_cols:
            nan_blackouts = df_copy[measurement_cols].isna().all(axis=1)
        else:
            nan_blackouts = pd.Series([False] * len(df_copy), index=df_copy.index)
        
        # Combine both blackout indicators
        df_copy['is_blackout'] = gap_blackouts | nan_blackouts
        
        # Group consecutive blackouts
        df_copy['blackout_block'] = (df_copy['is_blackout'] != df_copy['is_blackout'].shift()).cumsum()
        bo_blocks = df_copy[df_copy['is_blackout'] == True].groupby('blackout_block')
        
        total_bo_events = bo_blocks.ngroups
        
        # Mean Outage Duration
        mean_outage_duration = 0.0
        if total_bo_events > 0:
            outage_durations = []
            for _, group in bo_blocks:
                # For gap-based blackouts, use time_diff from first row
                # For NaN-based blackouts, count number of consecutive NaN rows
                if group['time_diff_minutes'].iloc[0] > self.BLACKOUT_THRESHOLD:
                    outage_durations.append(group['time_diff_minutes'].iloc[0])
                else:
                    # NaN-based blackout: duration = number of missing samples * interval
                    outage_durations.append(len(group) * self.INTERVAL_MINUTES)
            mean_outage_duration = round(np.mean(outage_durations), 1)
        
        # Reliability Index
        total_time_minutes = (df['timestamp'].max() - df['timestamp'].min()).total_seconds() / 60
        if total_time_minutes > 0:
            # Sum of all blackout durations
            total_blackout_minutes = sum(outage_durations) if total_bo_events > 0 else 0
            ri_percent = ((total_time_minutes - total_blackout_minutes) / total_time_minutes) * 100
        else:
            ri_percent = 0.0
        
        # Climatic vs Behavioral Blackout Rate
        climatic_events = 0
        df_copy['hour'] = df_copy['timestamp'].dt.hour
        
        for _, group in bo_blocks:
            blackout_start = group['timestamp'].min()
            lookback_start = blackout_start - pd.Timedelta(hours=24)
            prev_data = df[(df['timestamp'] >= lookback_start) & (df['timestamp'] < blackout_start)]
            
            if len(prev_data) > 0 and 'v_pv' in prev_data.columns:
                sun_hours = prev_data[(prev_data['timestamp'].dt.hour >= 10) & (prev_data['timestamp'].dt.hour <= 15)]
                if len(sun_hours) > 0 and sun_hours['v_pv'].mean() < 15.0:
                    climatic_events += 1
        
        behavioral_events = total_bo_events - climatic_events
        
        # Rates per 100 days
        num_days = max((df['timestamp'].max() - df['timestamp'].min()).days, 1)
        cbr = round((climatic_events / num_days) * 100, 2) if num_days > 0 else 0.0
        bbr = round((behavioral_events / num_days) * 100, 2) if num_days > 0 else 0.0
        bo_freq_per_100days = round((total_bo_events / num_days) * 100, 2) if num_days > 0 else 0.0
        
        return {
            'num_measurement_days': num_days,
            'bo_freq_events': total_bo_events,
            'bo_freq_events_per_100days': bo_freq_per_100days,
            'mean_outage_duration_min': mean_outage_duration,
            'ri_percent': round(ri_percent, 2),
            'climatic_blackout_events': climatic_events,
            'behavioral_blackout_events': behavioral_events,
            'cbr_events_per_100days': cbr,
            'bbr_events_per_100days': bbr
        }
