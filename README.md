# Rho+

## Aesthetic and ergonomic enhancements for common Python data science tools

This is basically the stuff I wish came by default in libraries like `numpy`, `pandas`, and `matplotlib` that doesn't.

### Installation

```bash
pip install rho_plus
```

### Matplotlib

A custom Matplotlib theme that can be set to either light or dark mode.

```python
import rho_plus

IS_DARK = True
theme, cs = rho_plus.mpl_setup(IS_DARK)
plt.style.use(theme)
```

Now `cs` is a list of the default plot color cycle, and Matplotlib has been set up to use a dark theme.
