"""
Example gallery for tidyplots.

This script generates example plots to demonstrate the capabilities of tidyplots.
"""

import numpy as np
import pandas as pd
import tidyplots

# Create sample data
np.random.seed(42)
n = 100

# Time series data
dates = pd.date_range(start='2023-01-01', periods=n)
df = pd.DataFrame({
    'date': dates,
    'value': np.random.normal(0, 1, n).cumsum(),
    'group': np.random.choice(['A', 'B', 'C'], n),
    'x': np.random.normal(0, 1, n),
    'y': np.random.normal(0, 1, n),
    'category': np.random.choice(['X', 'Y', 'Z'], n)
})

# Create figures directory if it doesn't exist
import os
os.makedirs('figures', exist_ok=True)

# 1. Time Series with Trend Line
(df.tidyplot(x='date', y='value')
 .add_line(alpha=0.5)
 .add_smooth(method='loess', se=True)
 .adjust_labels(title='Time Series with Trend',
            x='Date',
            y='Value')
 .save('figures/time_series.png'))

# 2. Scatter Plot with Groups
(df.tidyplot(x='x', y='y', color='group')
 .add_scatter(alpha=0.6)
 .adjust_colors('Set2')
 .adjust_labels(title='Scatter Plot with Groups',
            x='X Value',
            y='Y Value')
 .save('figures/scatter_groups.png'))

# 3. Box Plot with Jittered Points
(df.tidyplot(x='category', y='value', color='category')
 .add_boxplot(alpha=0.3)
 .add_data_points_jitter(width=0.2, alpha=0.5)
 .adjust_colors('Set2')
 .adjust_axis_text_angle(45)
 .adjust_labels(title='Value Distribution by Category',
            x='Category',
            y='Value')
 .save('figures/boxplot_jitter.png'))

# 4. Violin Plot with Quartiles
(df.tidyplot(x='group', y='value', color='group')
 .add_violin(alpha=0.4, draw_quantiles=[0.25, 0.5, 0.75])
 .adjust_colors('Set2')
 .adjust_labels(title='Value Distribution by Group',
            x='Group',
            y='Value')
 .save('figures/violin_quartiles.png'))

# 5. Density Plot with Multiple Groups
(df.tidyplot(x='value', color='group')
 .add_density(alpha=0.3)
 .adjust_colors('Set2')
 .adjust_labels(title='Value Density by Group',
            x='Value',
            y='Density')
 .save('figures/density_groups.png'))

# 6. Hexbin Plot with Color Gradient
(df.tidyplot(x='x', y='y')
 .add_hex(bins=20)
 .scale_color_gradient(low='lightblue', high='darkblue')
 .adjust_labels(title='Hexbin Plot',
            x='X Value',
            y='Y Value')
 .save('figures/hexbin.png'))

# 7. Bar Plot with Error Bars
group_stats = df.groupby('category').agg({
    'value': ['mean', 'std']
}).reset_index()
group_stats.columns = ['category', 'mean', 'std']

(group_stats.tidyplot(x='category', y='mean')
 .add_mean_bar(alpha=0.6)
 .add_errorbar(ymin='mean-std', ymax='mean+std')
 .adjust_colors('Set2')
 .adjust_axis_text_angle(45)
 .adjust_labels(title='Mean Value by Category',
            x='Category',
            y='Mean Value')
 .save('figures/barplot_error.png'))

# 8. Scatter Plot with Trend Line and Correlation
(df.tidyplot(x='x', y='y')
 .add_scatter(alpha=0.5)
 .add_smooth(method='lm')
 .add_correlation_text()
 .adjust_labels(title='Correlation Plot',
            x='X Value',
            y='Y Value')
 .save('figures/correlation.png'))
