"""
tidyplots is a Python implementation of R's tidyplots package.
https://github.com/jbengler/tidyplots
This module uses monkey patching to add a tidyplot() method to pd.DataFrame.
Users can then use df.tidyplot() in their code.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import sem
from typing import Optional, Union, Literal
import warnings
from plotnine import *
import pandas as pd

class TidyPlot:
    def __init__(self, data: pd.DataFrame, x: str, y: str = None, color: Optional[str] = None):
        """Initialize TidyPlot with data and mapping.
        
        Parameters:
        -----------
        data : pd.DataFrame
            Input data
        x : str
            Column name for x-axis
        y : str, optional
            Column name for y-axis. Not required for count plots.
        color : str, optional
            Column name for color grouping
        """
        self.data = data
        self.x = x
        self.y = y
        self.color = color
        self.mapping = aes(x=x)
        if y is not None:
            self.mapping = aes(x=x, y=y)
        if color:
            if y is not None:
                self.mapping = aes(x=x, y=y, color=color)
            else:
                self.mapping = aes(x=x, fill=color)  # Use fill for discrete color mapping
        self.plot = (ggplot(data, self.mapping)
                    + theme_minimal())
        if color and y is None:
            self.plot = self.plot + aes(fill=color)  # Use fill for discrete color mapping

    # Add data visualization elements
    def add_mean_bar(self, alpha: float = 0.4, width: float = 0.7):
        """Add bars showing mean values."""
        self.plot = self.plot + stat_summary(fun_y=np.mean, geom='bar', 
                                           alpha=alpha, width=width)
        return self

    def add_sem_errorbar(self, width: float = 0.2):
        """Add error bars showing standard error of the mean."""
        self.plot = self.plot + stat_summary(fun_data='mean_se', 
                                           geom='errorbar', width=width)
        return self

    def add_sd_errorbar(self, width: float = 0.2):
        """Add error bars showing standard deviation."""
        def sd_fun(y):
            return {'y': np.mean(y), 'ymin': np.mean(y) - np.std(y), 
                   'ymax': np.mean(y) + np.std(y)}
        self.plot = self.plot + stat_summary(fun_data=sd_fun, 
                                           geom='errorbar', width=width)
        return self

    def add_ci_errorbar(self, width: float = 0.2, ci: float = 0.95):
        """Add error bars showing confidence interval."""
        def ci_fun(y):
            mean = np.mean(y)
            ci_val = stats.t.interval(ci, len(y)-1, loc=mean, scale=stats.sem(y))
            return {'y': mean, 'ymin': ci_val[0], 'ymax': ci_val[1]}
        self.plot = self.plot + stat_summary(fun_data=ci_fun, 
                                           geom='errorbar', width=width)
        return self

    def add_errorbar(self, ymin: str, ymax: str, width: float = 0.2):
        """Add error bars with explicit min/max values."""
        self.plot = self.plot + geom_errorbar(aes(ymin=ymin, ymax=ymax), width=width)
        return self

    def add_data_points_beeswarm(self, size: float = 3, alpha: float = 0.5):
        """Add individual data points in a beeswarm arrangement."""
        self.plot = self.plot + geom_point(position=position_jitter(width=0.2), 
                                         size=size, alpha=alpha)
        return self

    def add_data_points_jitter(self, width: float = 0.2, size: float = 3, 
                              alpha: float = 0.5):
        """Add jittered data points."""
        self.plot = self.plot + geom_jitter(width=width, size=size, alpha=alpha)
        return self

    def add_violin(self, alpha: float = 0.4, draw_quantiles: list = [0.25, 0.5, 0.75]):
        """Add violin plot."""
        self.plot = self.plot + geom_violin(alpha=alpha, draw_quantiles=draw_quantiles)
        return self

    def add_boxplot(self, alpha: float = 0.4, outlier_alpha: float = 0.5):
        """Add box plot."""
        self.plot = self.plot + geom_boxplot(alpha=alpha, 
                                           outlier_alpha=outlier_alpha)
        return self

    def add_density(self, alpha: float = 0.4):
        """Add density plot."""
        self.plot = self.plot + geom_density(alpha=alpha)
        return self

    def add_density_2d(self, alpha: float = 0.4):
        """Add 2D density plot."""
        self.plot = self.plot + geom_density_2d(alpha=alpha)
        return self

    def add_scatter(self, size: float = 3, alpha: float = 0.5):
        """Add scatter plot."""
        self.plot = self.plot + geom_point(size=size, alpha=alpha)
        return self

    def add_line(self, alpha: float = 1.0):
        """Add line plot."""
        self.plot = self.plot + geom_line(alpha=alpha)
        return self

    def add_smooth(self, method: str = 'loess', se: bool = True):
        """Add smoothed conditional mean."""
        self.plot = self.plot + geom_smooth(method=method, se=se)
        return self

    def add_count(self, stat: str = 'count', position: str = 'stack'):
        """Add count or proportion plot."""
        if stat not in ['count', 'proportion']:
            raise ValueError("stat must be 'count' or 'proportion'")
        if position not in ['stack', 'dodge']:
            raise ValueError("position must be 'stack' or 'dodge'")
        
        pos = position_dodge() if position == 'dodge' else position_stack()
        self.plot = self.plot + geom_bar(stat=stat, position=pos)
        return self

    def add_text(self, label: str, x: float = 0, y: float = 0, 
                ha: str = 'center', va: str = 'center'):
        """Add text annotation."""
        self.plot = self.plot + annotate('text', x=x, y=y, label=label, 
                                       ha=ha, va=va)
        return self

    def add_hline(self, yintercept: float, linetype: str = 'solid', 
                 color: str = 'black', alpha: float = 1.0):
        """Add horizontal reference line."""
        self.plot = self.plot + geom_hline(yintercept=yintercept, 
                                         linetype=linetype,
                                         color=color, alpha=alpha)
        return self

    def add_vline(self, xintercept: float, linetype: str = 'solid', 
                 color: str = 'black', alpha: float = 1.0):
        """Add vertical reference line."""
        self.plot = self.plot + geom_vline(xintercept=xintercept, 
                                         linetype=linetype,
                                         color=color, alpha=alpha)
        return self

    def add_ribbon(self, ymin: str, ymax: str, alpha: float = 0.2):
        """Add ribbon (filled area between lines)."""
        self.plot = self.plot + geom_ribbon(aes(ymin=ymin, ymax=ymax), 
                                          alpha=alpha)
        return self

    def add_rug(self, sides: str = 'bl', length: float = 0.03, alpha: float = 0.5):
        """Add marginal rug plot."""
        self.plot = self.plot + geom_rug(sides=sides, length=length, alpha=alpha)
        return self

    def add_step(self, direction: str = 'hv'):
        """Add step plot.
        
        Parameters:
        -----------
        direction : str
            Step direction ("hv" horizontal then vertical, 
            "vh" vertical then horizontal)
        """
        self.plot = self.plot + geom_step(direction=direction)
        return self

    def add_hex(self, bins: int = 20):
        """Add hexagonal binning plot."""
        self.plot = self.plot + stat_bin_2d(bins=[bins, bins]) + \
                   scale_x_continuous() + scale_y_continuous()
        return self

    def add_quantiles(self, quantiles: list = [0.25, 0.5, 0.75]):
        """Add horizontal lines at specified quantiles."""
        for q in quantiles:
            self.plot = self.plot + \
                       geom_hline(yintercept=self.data[self.y].quantile(q),
                                linetype='dashed', alpha=0.5)
        return self

    # Add statistical elements
    def add_test_pvalue(self, test: str = 't', format: str = '.3f'):
        """Add statistical test p-value."""
        groups = sorted(self.data[self.x].unique())
        if len(groups) != 2:
            warnings.warn("P-value calculation requires exactly 2 groups")
            return self
        
        g1 = self.data[self.data[self.x] == groups[0]][self.y]
        g2 = self.data[self.data[self.x] == groups[1]][self.y]
        
        if test == 't':
            stat, p = stats.ttest_ind(g1, g2)
        elif test == 'wilcoxon':
            stat, p = stats.ranksums(g1, g2)
        else:
            raise ValueError("test must be 't' or 'wilcoxon'")
        
        y_max = self.data[self.y].max()
        self.add_text(f'p = {p:{format}}', 
                     x=np.mean([0, 1]), 
                     y=y_max * 1.1)
        return self

    def add_correlation_text(self, method: str = 'pearson', format: str = '.3f'):
        """Add correlation coefficient text."""
        if method not in ['pearson', 'spearman']:
            raise ValueError("method must be 'pearson' or 'spearman'")
        
        if method == 'pearson':
            r, p = stats.pearsonr(self.data[self.x], self.data[self.y])
        else:
            r, p = stats.spearmanr(self.data[self.x], self.data[self.y])
        
        y_max = self.data[self.y].max()
        self.add_text(f'r = {r:{format}}\np = {p:{format}}', 
                     x=np.mean(self.data[self.x]), 
                     y=y_max * 1.1)
        return self

    # Customize appearance
    def adjust_colors(self, palette: str):
        """Change color palette."""
        self.plot = self.plot + scale_color_brewer(palette=palette)
        return self

    def adjust_labels(self, title: str = None, x: str = None, y: str = None):
        """Modify plot labels."""
        self.plot = self.plot + labs(title=title, x=x, y=y)
        return self

    def adjust_axis_text_angle(self, angle: float = 45):
        """Rotate axis text."""
        self.plot = self.plot + theme(axis_text_x=element_text(angle=angle))
        return self

    def adjust_legend_position(self, position: str = 'right'):
        """Control legend placement."""
        if position not in ['right', 'left', 'top', 'bottom', 'none']:
            raise ValueError("position must be 'right', 'left', 'top', 'bottom', or 'none'")
        self.plot = self.plot + theme(legend_position=position)
        return self

    # Scale transformations
    def scale_x_log10(self):
        """Apply log10 scale to x-axis."""
        self.plot = self.plot + scale_x_log10()
        return self

    def scale_y_log10(self):
        """Apply log10 scale to y-axis."""
        self.plot = self.plot + scale_y_log10()
        return self

    def scale_x_sqrt(self):
        """Apply square root scale to x-axis."""
        self.plot = self.plot + scale_x_sqrt()
        return self

    def scale_y_sqrt(self):
        """Apply square root scale to y-axis."""
        self.plot = self.plot + scale_y_sqrt()
        return self

    def scale_x_reverse(self):
        """Reverse x-axis."""
        self.plot = self.plot + scale_x_reverse()
        return self

    def scale_y_reverse(self):
        """Reverse y-axis."""
        self.plot = self.plot + scale_y_reverse()
        return self

    def scale_color_gradient(self, low: str = 'white', high: str = 'blue'):
        """Apply continuous color gradient."""
        self.plot = self.plot + scale_color_gradient(low=low, high=high)
        return self

    def scale_color_gradient2(self, low: str = 'blue', mid: str = 'white', 
                            high: str = 'red'):
        """Apply diverging color gradient."""
        self.plot = self.plot + scale_color_gradient2(low=low, mid=mid, high=high)
        return self

    # Output
    def show(self):
        """Display the plot."""
        return self.plot

    def save(self, filename: str, **kwargs):
        """Save the plot to a file."""
        self.plot.save(filename, **kwargs)
        return self

# Helper function to create TidyPlot object
def tidyplot(data: pd.DataFrame, x: str, y: str = None, color: Optional[str] = None):
    """Create a new TidyPlot object."""
    return TidyPlot(data, x, y, color)

# Add method to DataFrame
pd.DataFrame.tidyplot = lambda self, x, y=None, color=None: tidyplot(self, x, y, color)
