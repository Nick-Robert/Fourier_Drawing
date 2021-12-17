import numpy as np
import matplotlib.pyplot as plt
from svg.path import parse_path
from svg.path.path import Close
from xml.dom import minidom

# Define a function to generate a Fourier series based on the coefficients determined by the Fast Fourier Transform.
# This also includes a series of phases x to pass through the function.
def make_fourier_series(t, f_coeffs):
    # Generate the approximated signal using the synthesis equation where the fundamental frequency (w0) is 1 since it's in the frequency domain
    # Euler's was used to convert the exponential into its sinusoidal form such that:
    # f(t) ~= a0/2 + summation_{n = 1} ^ N (a_n * cos(2*pi*n*t) + b_n * sin(2*pi*n*t))
    fourier_series_start = f_coeffs[0][0] / 2
    fourier_series = []
    outer_idx = 0
    for t_point in t:
        fourier_series.append(fourier_series_start)
        for n in range(1, n_coeff+1):
            a_n_cos_portion = np.cos(2 * np.pi * n * t_point)
            b_n_sin_portion = np.sin(2 * np.pi * n * t_point)
            fourier_series[outer_idx] += (f_coeffs[n][0] * a_n_cos_portion + f_coeffs[n][1] * b_n_sin_portion)
        outer_idx += 1
    return fourier_series

def make_fs_coeffs(ncoeff, fft_vals):
    fourier_coeffs = []
    for n in range(0, ncoeff+1):
        a = 2 * fft_vals[n].real / len(x)
        b = -2 * fft_vals[n].imag / len(x)
        fourier_coeffs.append([a, b])
    return np.array(fourier_coeffs)


# define how many points on each path object will be taken
# since each path's .point() method takes a value from 0.0 to 1.0, the number will be 1.0 / N
# This affects how good an approximation the svg paths are (which also affects the Fourier approximation)
n_bins = 1500
# number of Fourier coefficients
# This affects how good an approximation the Fourier series is for the svg file
n_coeffs = [5000]
# for loop that was used to generate the slideshows in the readme
# for num in range(1, 201):
#     n_coeffs.append(num)

# load in the svg file as a series of complex numbered points
doc = minidom.parse('C:/Users/nickr/Documents/Programming/Visual_Studio/Fourier_Project/svg_files/homer2.svg')
path_strings = [path.getAttribute('d') for path in doc.getElementsByTagName('path')]
doc.unlink()

pic_points = []
for path_string in path_strings:
    path = parse_path(path_string)
    for e in path:
        if not isinstance(e, Close):
            time_num = 0
            while (time_num <= 1.0):
                pic_points.append(e.point(time_num))
                time_num += (1.0/n_bins)
# ensures that the x and y values are between 0 and 1
scale = 0
for val in pic_points:
    if (val.real > scale):
        scale = val.real + 1
    elif (val.imag > scale):
        scale = val.imag + 1
# defines the x-axis
x = np.array([i.real / scale for i in pic_points])
# defines the y-axis
y = np.array([i.imag / scale for i in pic_points])
# defines the time axis
t = np.linspace(0, 1, n_bins)

for n_coeff in n_coeffs:
    # initialize the plot
    fig, axs = plt.subplots(1, 1, figsize=(12, 12))
    fig.suptitle('n = ' + str(n_coeff))

    # FFT for the x and y values
    fast_fourier_transform_x = np.fft.fft(x)
    fast_fourier_transform_y = np.fft.fft(y)

    # Calculate the corresponding Fourier series coefficients from the FFT
    f_coeffs_x = make_fs_coeffs(n_coeff, fast_fourier_transform_x)
    f_coeffs_y = make_fs_coeffs(n_coeff, fast_fourier_transform_y)

    # Create the Fourier series approximating this data
    fourier_series_x = make_fourier_series(t, f_coeffs_x)
    fourier_series_y = make_fourier_series(t, f_coeffs_y)

    # Create a plot to view the data
    axs.set_xlim(0, 1)
    axs.set_ylim(0, 1)
    axs.scatter(x, y, color="red", s=1)
    axs.plot(fourier_series_x, fourier_series_y, color="blue", linewidth=1)
    # if wanting to save a series of plots, then uncomment the next two lines and comment the plt.show()
    # fig.savefig('C:/Users/nickr/Documents/Programming/Visual_Studio/Fourier_Project/succulent_ss/'+str(n_coeff))
    # plt.close()
    plt.show()