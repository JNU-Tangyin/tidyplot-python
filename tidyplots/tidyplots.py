"""A Python library for creating publication-ready plots with a fluent, chainable interface."""

import pandas as pd
import numpy as np
from plotnine import *
from typing import Optional, List, Union
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import sem
import warnings

@pd.api.extensions.register_dataframe_accessor("tidyplot")
class TidyPlot:
    """A fluent interface for creating publication-ready plots."""
    
    def __init__(self, pandas_obj):
        """Initialize TidyPlot with a pandas DataFrame."""
        self._obj = pandas_obj
        self.plot = None
        
    def __call__(self, x: str, y: str = None, color: Optional[str] = None):
        """Create a new plot with the given aesthetics.
        
        Parameters:
        -----------
        x : str
            Column name for x-axis
        y : str, optional
            Column name for y-axis
        color : str, optional
            Column name for color aesthetic
        """
        mapping = aes(x=x)
        if y is not None:
            mapping = aes(x=x, y=y)
            if color is not None:
                mapping = aes(x=x, y=y, color=color)
        else:
            if color is not None:
                mapping = aes(x=x, fill=color)
            
        self.plot = (ggplot(self._obj, mapping)
                    + theme_minimal())
        return self
    
    def add_scatter(self, alpha: float = 0.6, size: float = 3):
        """Add scatter points to the plot."""
        self.plot = self.plot + geom_point(alpha=alpha, size=size)
        return self
    
    def add_line(self, alpha: float = 0.8, size: float = 1):
        """Add line to the plot."""
        self.plot = self.plot + geom_line(alpha=alpha, size=size)
        return self
    
    def add_smooth(self, method: str = 'lm', se: bool = True, alpha: float = 0.2):
        """Add smoothed conditional means."""
        self.plot = self.plot + stat_smooth(method=method, se=se, alpha=alpha)
        return self
    
    def add_boxplot(self, alpha: float = 0.3, outlier_alpha: float = 0.5):
        """Add boxplot to the plot."""
        self.plot = self.plot + geom_boxplot(alpha=alpha, outlier_alpha=outlier_alpha)
        return self
    
    def add_violin(self, alpha: float = 0.4, draw_quantiles: List[float] = [0.25, 0.5, 0.75]):
        """Add violin plot."""
        self.plot = self.plot + geom_violin(alpha=alpha, draw_quantiles=draw_quantiles)
        return self
    
    def add_density(self, alpha: float = 0.3):
        """Add density plot."""
        self.plot = self.plot + geom_density(alpha=alpha)
        return self
    
    def add_hex(self, bins: int = 20):
        """Add hexagonal binning plot."""
        self.plot = self.plot + stat_bin_2d(bins=bins) + geom_tile()
        return self
    
    def add_errorbar(self, ymin: str, ymax: str, alpha: float = 0.8, width: float = 0.2):
        """Add error bars with explicit min/max values."""
        self.plot = self.plot + geom_errorbar(
            aes(ymin=ymin, ymax=ymax), 
            alpha=alpha, 
            width=width
        )
        return self
    
    def add_data_points_jitter(self, width: float = 0.2, height: float = 0, alpha: float = 0.5):
        """Add jittered points to the plot."""
        self.plot = self.plot + geom_jitter(width=width, height=height, alpha=alpha)
        return self

    def add_mean_bar(self, alpha: float = 0.4, width: float = 0.7):
        """Add bars showing mean values."""
        self.plot = self.plot + stat_summary(fun_y=np.mean, geom='bar', alpha=alpha, width=width)
        return self

    def add_sem_errorbar(self, width: float = 0.2):
        """Add error bars showing standard error of the mean."""
        self.plot = self.plot + stat_summary(fun_data='mean_se', geom='errorbar', width=width)
        return self

    def add_correlation_text(self, method: str = 'pearson', format: str = '.2f'):
        """Add correlation coefficient text."""
        if method not in ['pearson', 'spearman']:
            raise ValueError("method must be 'pearson' or 'spearman'")
        
        mapping = self.plot.mapping
        x = mapping['x']
        y = mapping['y']
        
        if method == 'pearson':
            r, p = stats.pearsonr(self._obj[x], self._obj[y])
        else:
            r, p = stats.spearmanr(self._obj[x], self._obj[y])
        
        y_max = self._obj[y].max()
        x_mean = np.mean(self._obj[x])
        self.plot = self.plot + annotate('text', x=x_mean, y=y_max * 1.1,
                                       label=f'r = {r:{format}}\np = {p:{format}}')
        return self

    def adjust_labels(self, title: str = None, x: str = None, y: str = None):
        """Adjust plot labels."""
        self.plot = self.plot + labs(title=title, x=x, y=y)
        return self
    
    def adjust_colors(self, palette: str = 'Set2'):
        """Change color palette."""
        mapping = self.plot.mapping
        if 'y' not in mapping:
            self.plot = self.plot + scale_fill_brewer(type='qual', palette=palette)
        else:
            self.plot = self.plot + scale_color_brewer(type='qual', palette=palette)
        return self
    
    def adjust_axis_text_angle(self, angle: float = 45):
        """Rotate axis text."""
        self.plot = self.plot + theme(axis_text_x=element_text(angle=angle, hjust=1))
        return self
    
    def adjust_legend_position(self, position: str = 'right'):
        """Control legend placement."""
        if position not in ['right', 'left', 'top', 'bottom', 'none']:
            raise ValueError("position must be 'right', 'left', 'top', 'bottom', or 'none'")
        self.plot = self.plot + theme(legend_position=position)
        return self

    def scale_x_log10(self):
        """Apply log10 scale to x-axis."""
        self.plot = self.plot + scale_x_log10()
        return self

    def scale_y_log10(self):
        """Apply log10 scale to y-axis."""
        self.plot = self.plot + scale_y_log10()
        return self
    
    def scale_color_gradient(self, low: str = 'lightblue', high: str = 'darkblue'):
        """Set continuous color gradient."""
        self.plot = self.plot + scale_color_gradient(low=low, high=high)
        return self
    
    def show(self):
        """Display the plot."""
        return self.plot
    
    def save(self, filename: str, **kwargs):
        """Save the plot to a file.
        
        Parameters:
        -----------
        filename : str
            Path to save the plot to
        **kwargs : dict
            Additional arguments to pass to ggsave
        """
        self.plot.save(filename, **kwargs)
        return self
