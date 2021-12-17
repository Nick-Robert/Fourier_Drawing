import numpy as np
import matplotlib.pyplot as plt
from numpy.core.fromnumeric import sort
from svg.path import parse_path
from svg.path.path import Close
from xml.dom import minidom
from matplotlib import animation
from matplotlib.patches import ConnectionPatch


def make_frame(i, time, coeffs):
    t = time[i]
    x_coeffs, y_coeffs = [], []
    # exponential term to be multiplied with coefficient 
    # this is responsible for making rotation of circle
    exp_term = np.array([np.exp(n*t*1j) for n in range(0, n_coeff+1)])
    coeffs = sort_coeff(coeffs*exp_term)
    x_coeffs = np.real(coeffs)
    y_coeffs = np.imag(coeffs)
    center_x, center_y = 0, 0
    for i, (x_coeff, y_coeff) in enumerate(zip(x_coeffs, y_coeffs)):
        r = np.linalg.norm([x_coeff, y_coeff])
        theta = np.linspace(0, 2*np.pi, num=50)
        x, y = center_x + r * np.cos(theta), center_y + r * np.sin(theta)
        circles[i].set_data(x, y)
        
        # draw a line to indicate the direction of circle
        x, y = [center_x, center_x + x_coeff], [center_y, center_y + y_coeff]
        circle_lines[i].set_data(x, y)
        
        # calculate center for next circle
        center_x, center_y = center_x + x_coeff, center_y + y_coeff
    # center points now are points from last circle
    # these points are used as drawing points
    draw_x.append(center_x)
    draw_y.append(center_y)

    # draw the curve from last point
    drawing.set_data(draw_x, draw_y)

    orig_drawing.set_data(x, y)


def sort_coeff(coeffs):
    idx = n_coeff // 2
    new_coeffs = [coeffs[idx]]
    for i in range(1, idx+1):
        new_coeffs.extend([coeffs[idx+i],coeffs[idx-i]])
    return np.array(new_coeffs)


draw_x, draw_y = [], []

# define how many points on each path object will be taken
# since each path's .point() method takes a value from 0.0 to 1.0, the number will be 1.0 / N
# This affects how good an approximation for the svg paths are
n_bins = 5000
# number of Fourier coefficients
# This affects how good an approximation the Fourier series is for the svg file
n_coeff = 16
# for num in range(101, 300):
#     n_coeffs.append(num)

doc = minidom.parse('C:/Users/nickr/Documents/Programming/Visual_Studio/Fourier_Project/pi_image.svg')
path_strings = [path.getAttribute('d') for path in doc.getElementsByTagName('path')]
doc.unlink()

pic_points = []
# print the line draw commands
for path_string in path_strings:
    path = parse_path(path_string)
    for e in path:
        if not isinstance(e, Close):
            time_num = 0
            while (time_num <= 1.0):
                pic_points.append(e.point(time_num))
                time_num += (1.0/n_bins)
scale = 5000
pic_points = np.array(pic_points)
# don't need to break up the pic_points array into its real and imaginary parts
# but will do it to graph the original picture
# defines the x-axis
x = np.array([i.real / scale for i in pic_points])
# defines the y-axis
y = np.array([i.imag / scale for i in pic_points])
# defines the time axis
t = np.linspace(0, 1, n_bins)
# initialize the plot
# fig, axs = plt.subplots(1, 1, sharex=True, figsize=(12, 12))
# fig.suptitle(r'Convergences of CT Fourier Series for any Arbitrary Image')

# Determine the fast Fourier transform
fast_fourier_transform = np.fft.fft(pic_points)
fourier_coeff = []

# Loop through the FFT and pick out the a and b coefficients, which are the real and imaginary parts of the
# coefficients calculated by the FFT
# Source for this relation: https://stackoverflow.com/questions/64165282/determining-fourier-coefficients-from-time-series-data 
for n in range(0, n_coeff+1):
    a_x = 2 * fast_fourier_transform[n].real / len(pic_points)
    b_x = -2 * fast_fourier_transform[n].imag / len(pic_points)
    fourier_coeff.append(a_x + 1j*b_x)
fourier_coeff = np.array(fourier_coeff)
# sort the coefficients to prepare them for circle animation
# fourier_coeff = sort_coeff(fourier_coeff)

# Create the Fourier series approximating this data
# fourier_series = make_fourier_series(t, fourier_coeff)
# find the approximated points for the inputted function
# f_t = []
fft_freqs = np.fft.fftfreq(n_coeff+1)
# outer_idx = 0
# print(len(fft_freqs))
# print(len(pic_points))
# print(len(fourier_coeff))
# for t_point in t:
#     f_t.append(0)
#     inner_idx = 0
#     for coeff in fourier_coeff:
#         e_term_phase = fft_freqs[inner_idx] * 2 * np.pi * t_point
#         coeff_phase = np.arctan2(coeff[1], coeff[0])
#         coeff_magn = np.hypot(coeff[0], coeff[1])
#         # multiplying two complex numbers. Can put the coeff into polar form, then just need to add the phase and multiply the magnitudes
#         f_t[outer_idx] += coeff_magn * np.e ** (e_term_phase + coeff_phase)
#         inner_idx += 1
#     f_t[outer_idx] = f_t[outer_idx] / scale
#     outer_idx += 1
# # Create a subplot to view the data
# # print(fourier_series)
# print(f_t)
# print(len(t))
# axs.scatter(x, y, color="red", label="Original", s=1)
# axs.scatter(t, f_t, color="blue", label="Fourier Approximation", s=1)
# # fig.savefig('C:/Users/nickr/Documents/Programming/Visual_Studio/Fourier_Project/pi_image_slideshow/'+str(n_coeff))
# # plt.close()
# plt.show()
# make figure for animation
fig, ax = plt.subplots()

# different plots to make epicycle
circles = [ax.plot([], [], 'r-')[0] for i in range(0, n_coeff+1)]
# circle_lines are radius of each circles
circle_lines = [ax.plot([], [], 'b-')[0] for i in range(0, n_coeff+1)]
# drawing is plot of final drawing
drawing, = ax.plot([], [], 'k-', linewidth=2)
orig_drawing, = ax.plot([], [], 'g-', linewidth=0.5)
# to fix the size of figure so that the figure does not get cropped/trimmed
ax.set_xlim(-250000, 250000)
ax.set_ylim(-250000, 250000)

# hide axes
# ax.set_axis_off()

# to have symmetric axes
ax.set_aspect('equal')
# make animation
# Set up formatting for the movie files
Writer = animation.writers['ffmpeg']
writer = Writer(fps=30, metadata=dict(artist='Me'), bitrate=1800)
# time is array from 0 to tau 
frames = 300
time = np.linspace(0, 2*np.pi, num=frames)
anim = animation.FuncAnimation(fig, make_frame, frames=frames, fargs=(time, fourier_coeff),interval=5)
anim.save('epicycle.mp4', writer=writer)
print("completed: epicycle.mp4")