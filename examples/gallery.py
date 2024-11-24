"""
Example gallery for tidyplots package.
"""
import numpy as np
import pandas as pd
from tidyplots import tidyplot
import os

# Create figures directory if it doesn't exist
os.makedirs('../../figures', exist_ok=True)

# Generate sample data
np.random.seed(42)
n = 200

# Time series data
dates = pd.date_range(start='2023-01-01', periods=n)
data = pd.DataFrame({
    'date': dates,
    'value': np.cumsum(np.random.normal(0, 1, n)),
    'group': np.random.choice(['A', 'B', 'C'], n),
    'x': np.random.normal(0, 1, n),
    'y': np.random.normal(0, 1, n),
    'size': np.random.uniform(1, 10, n),
    'category': np.random.choice(['Type 1', 'Type 2', 'Type 3', 'Type 4'], n)
})

# 1. Time series line plot with smooth trend
(tidyplot(data, x='date', y='value')
 .add_line(alpha=0.5)
 .add_smooth(method='loess', se=True)
 .adjust_labels(title='Time Series with Trend',
            x='Date',
            y='Value')
 .save('../../figures/time_series.png'))

# 2. Scatter plot with size mapping
(tidyplot(data, x='x', y='y', color='group')
 .add_scatter(alpha=0.6)
 .adjust_colors('Blues')
 .adjust_labels(title='Scatter Plot with Groups',
            x='X Value',
            y='Y Value')
 .save('../../figures/scatter_groups.png'))

# 3. Box plot with jittered points
(tidyplot(data, x='category', y='value', color='category')
 .add_boxplot(alpha=0.3)
 .add_data_points_jitter(width=0.2, alpha=0.5)
 .adjust_colors('Blues')
 .adjust_axis_text_angle(45)
 .adjust_labels(title='Value Distribution by Category',
            x='Category',
            y='Value')
 .save('../../figures/boxplot_jitter.png'))

# 4. Violin plot with quartiles
(tidyplot(data, x='group', y='value', color='group')
 .add_violin(alpha=0.4, draw_quantiles=[0.25, 0.5, 0.75])
 .adjust_colors('Blues')
 .adjust_labels(title='Value Distribution by Group',
            x='Group',
            y='Value')
 .save('../../figures/violin_quartiles.png'))

# 5. Density plot with multiple groups
(tidyplot(data, x='value', color='group')
 .add_density(alpha=0.3)
 .adjust_colors('Blues')
 .adjust_labels(title='Value Density by Group',
            x='Value',
            y='Density')
 .save('../../figures/density_groups.png'))

# 6. Hexbin plot with color gradient
(tidyplot(data, x='x', y='y')
 .add_hex(bins=20)
 .scale_color_gradient(low='lightblue', high='darkblue')
 .adjust_labels(title='Hexbin Plot',
            x='X Value',
            y='Y Value')
 .save('../../figures/hexbin.png'))

# 7. Bar plot with error bars
group_stats = data.groupby('category').agg({
    'value': ['mean', 'std']
}).reset_index()
group_stats.columns = ['category', 'mean', 'std']

(tidyplot(group_stats, x='category', y='mean')
 .add_mean_bar(alpha=0.6)
 .add_errorbar(ymin='mean-std', ymax='mean+std')
 .adjust_colors('Blues')
 .adjust_axis_text_angle(45)
 .adjust_labels(title='Mean Value by Category',
            x='Category',
            y='Mean Value')
 .save('../../figures/barplot_error.png'))

# 8. Scatter plot with trend line and correlation
(tidyplot(data, x='x', y='y')
 .add_scatter(alpha=0.5)
 .add_smooth(method='lm')
 .add_correlation_text()
 .adjust_labels(title='Correlation Plot',
            x='X Value',
            y='Y Value')
 .save('../../figures/correlation.png'))
