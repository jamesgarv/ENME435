"""
======
Slider
======
=== Version 0 ===
In this example, sliders are used to control the frequency and amplitude of
a sine wave.
See :doc:`/gallery/widgets/slider_snap_demo` for an example of having
the ``Slider`` snap to discrete values.
See :doc:`/gallery/widgets/range_slider` for an example of using
a ``RangeSlider`` to define a range of values.
=== Version 1 ===
Adapted for laser alignment calibration
"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button, Slider
# The parametrized function to be plotted - aka distance to target
def getD(pfc,rpc,ro):
D = np.empty((0))
for i in range(pfc.shape[0]):
D = np.append(D, H/( np.tan(pfc[i]*rpc + ro) ))
D = np.flip(D,0)
D = 3.28*D
return D
pfc = np.arange(0,640,2)
H = 0.3048
# Define initial parameters
init_ro = -0.0019
init_rpc = 0.00008
# Create the figure and the line that we will manipulate
fig, ax = plt.subplots()
points, = ax.plot(pfc, getD(pfc, init_rpc, init_ro), 'ro') # <== CHANGE THIS to:
ax.plot(x_plot, y_plot, 'ro'), where x_plot and y_plot are your data from the laser
points
line, = ax.plot(pfc, getD(pfc, init_rpc, init_ro), lw=3, c='b')
ax.set_xlabel('Pixel')
ax.set_ylabel('Distance to Target')
ax.set_ylim([0,120])
# adjust the main plot to make room for the sliders
fig.subplots_adjust(left=0.25, bottom=0.25)
# Make a horizontal slider to control rpc (radians per pixel pitch)
axrpc = fig.add_axes([0.25, 0.1, 0.65, 0.03])
rpc_slider = Slider(
ax=axrpc,
label='rpc',
valmin=0,
valmax=0.001,
valinit=init_rpc,
)
# Make a vertically oriented slider to control the ro (radian offset)
axro = fig.add_axes([0.1, 0.25, 0.0225, 0.63])
ro_slider = Slider(
ax=axro,
label="ro",
valmin=-0.03,
valmax=0.01,
valinit=init_ro,
orientation="vertical"
)
# The function to be called anytime a slider's value changes
def update(val):
line.set_ydata(getD(pfc, rpc_slider.val, ro_slider.val))
fig.canvas.draw_idle()
# register the update function with each slider
rpc_slider.on_changed(update)
ro_slider.on_changed(update)
# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
resetax = fig.add_axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.975')
def reset(event):
rpc_slider.reset()
ro_slider.reset()
button.on_clicked(reset)
plt.show()
