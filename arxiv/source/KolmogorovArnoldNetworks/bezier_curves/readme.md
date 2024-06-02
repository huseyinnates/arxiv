# Bezier Curve with Control Points

This project demonstrates how to create and interact with a Bézier curve using Pygame. Users can add control points, move them, and visualize a moving object that follows the curve. The speed of the moving object can be controlled using a slider.

## Features
- Add control points with a right-click.
- Move control points by dragging them with the left mouse button.
- Toggle between looping and non-looping curve with a toggle button.
- Adjust the speed of the moving object with a slider.
- Display the current speed value next to the slider.

## Screenshot
![Screenshot](./bezier-curve.png)

## Mathematical Background

A Bézier curve is defined by a set of control points \( P_0, P_1, \ldots, P_n \). The curve is calculated using the Bernstein polynomial basis as follows:

### Bézier Curve Formula

\[ B(t) = \sum_{i=0}^{n} b_{i,n}(t) \cdot P_i \]

Where:
- \( B(t) \) is the point on the Bézier curve at parameter \( t \).
- \( P_i \) are the control points.
- \( b_{i,n}(t) \) is the Bernstein polynomial defined as:

\[ b_{i,n}(t) = \binom{n}{i} \cdot t^i \cdot (1 - t)^{n-i} \]

And the binomial coefficient \( \binom{n}{i} \) is calculated as:

\[ \binom{n}{i} = \frac{n!}{i!(n-i)!} \]