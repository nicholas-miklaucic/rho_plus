# Rho+

## Aesthetic and ergonomic enhancements for common Python data science tools

This is basically the stuff I wish came by default in libraries like `numpy`, `pandas`, and `matplotlib` that doesn't.

### Installation

To ensure that all customizations apply to the correct version, Rho+ does not include `matplotlib`. If you don't have that installed, you can fix that with

```bash
pip install matplotlib
```

Then, run

```bash
pip install rho_plus
```

### Matplotlib Demo

Rho+ includes several custom additions to Matplotlib's functionality, and a custom Matplotlib theme that can be set to either light or dark mode.

```python
import matplotlib.pyplot as plt
import rho_plus

theme, cs = rho_plus.mpl_setup(is_dark=True, setup=True)
```

Now `theme` is the full Matplotlib theme, `cs` is a list of the default plot cycle colors, and Matplotlib has been set up to use a dark theme.

Here's a showcase of what all of the Matplotlib tools in Rho+ do. For code, check the showcase.

Default Matplotlib:

![images/default.png]

Rho+, with light mode:

![images/rho-light.png]

Rho+, with dark mode:

![images/rho-dark.png]

If things don't work as you expect or you have ideas for improvements, please consider filing a pull request!
