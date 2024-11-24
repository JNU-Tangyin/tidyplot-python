# TidyPlot: A Python Implementation of R's Tidyplot

TidyPlot is a Python library that brings the elegant and intuitive plotting capabilities of R's tidyplot to Python. It provides a fluent interface for creating publication-ready plots using pandas DataFrames.

## Installation

```bash
pip install tidyplot
```

## Quick Start

```python
import pandas as pd
import tidyplot  # This adds the .tidyplot() method to pd.DataFrame

# Create a simple plot
(df.tidyplot(x='group', y='value', color='category')
   .add_boxplot()
   .add_data_points_jitter()
   .adjust_colors('Set2')
   .show())
```

## Features

### Basic Plot Types
- `add_boxplot()`: Create box plots with optional notches
- `add_violin()`: Create violin plots
- `add_scatter()`: Create scatter plots
- `add_line()`: Create line plots
- `add_bar()`: Create bar plots
- `add_count()`: Create count/proportion plots
- `add_density_2d()`: Create 2D density plots
- `add_hex()`: Create hexagonal binning plots
- `add_step()`: Create step plots
- `add_dotplot()`: Create dot plots with stacking options

### Statistical Features
- `add_test_pvalue()`: Add statistical test results (t-test, Wilcoxon, ANOVA)
- `add_errorbar()`: Add error bars with explicit min/max values
- `add_smooth()`: Add smoothed conditional means with confidence intervals
- `add_quantiles()`: Add horizontal lines at specified quantiles
- `add_correlation_text()`: Add correlation coefficient text

### Annotations and References
- `add_text()`: Add text annotations at specific coordinates
- `add_hline()`: Add horizontal reference lines
- `add_vline()`: Add vertical reference lines
- `add_ribbon()`: Add ribbons (filled areas between lines)
- `add_rug()`: Add marginal rug plots

### Scale Transformations
- `scale_x_log10()`, `scale_y_log10()`: Log10 scale transformations
- `scale_x_sqrt()`, `scale_y_sqrt()`: Square root scale transformations
- `scale_x_reverse()`, `scale_y_reverse()`: Reverse axis scales
- `scale_x_limits()`, `scale_y_limits()`: Set axis limits
- `scale_color_gradient()`: Continuous color gradients
- `scale_color_gradient2()`: Diverging color gradients

### Customization
- `adjust_colors()`: Change color palettes
- `adjust_labels()`: Modify plot labels and title
- `adjust_axis_text_angle()`: Rotate axis labels
- `adjust_legend_position()`: Control legend placement
- `coord_flip()`: Flip x and y coordinates
- `expand_limits()`: Expand plot limits

## Examples

### Statistical Plot with Error Bars
```python
(df.tidyplot(x='group', y='value', color='group')
   .add_boxplot()
   .add_data_points_jitter()
   .add_errorbar(ymin='value_min', ymax='value_max')
   .adjust_colors('Set2')
   .add_test_pvalue(test='t')
   .show())
```

### Time Series with Confidence Interval
```python
(df.tidyplot(x='time', y='value', color='group')
   .add_line(alpha=0.3)
   .add_ribbon(ymin='lower', ymax='upper')
   .add_smooth(method='loess', se=True)
   .adjust_colors('viridis')
   .scale_y_log10()
   .show())
```

### 2D Density Plot
```python
(df.tidyplot(x='x', y='y', color='category')
   .add_scatter(alpha=0.3)
   .add_density_2d()
   .add_rug()
   .scale_color_gradient2(low='blue', mid='white', high='red')
   .show())
```

### Count Plot with Proportions
```python
(df.tidyplot(x='category', y=None, color='size')
   .add_count(stat='proportion', position='dodge')
   .adjust_colors('Set3')
   .adjust_axis_text_angle(angle=45)
   .show())
```

## Contributing

We welcome contributions! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
