import numpy as np
import matplotlib.pyplot as plt
import svgpathtools as svg

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
        a = 2 * fft_vals[n].real / n_bins
        b = -2 * fft_vals[n].imag / n_bins
        fourier_coeffs.append([a, b])
    return np.array(fourier_coeffs)


# number of equal-time bins
n_bins = 1001
# number of Fourier coefficients
n_coeffs = [1, 19, 51, 501]



# initialize the plot
fig, axs = plt.subplots(len(n_coeffs), 1, sharex=True, figsize=(12, 12))
counter = 0

# Define the x-axis (time)
test_array = np.linspace(-0.5, 0.5, n_bins)

# Define the square wave
test_data = []
for time in test_array:
    if (abs(time) < 1.0/4.0):
        test_data.append(1)
    else:
        test_data.append(0)

for n_coeff in n_coeffs:
    # Determine the fast Fourier transform for this test data.
    # fft expects x-values from 0 to 1, so need to rearrange the signal (since it goes from -1/2 to 1/2)
    fast_fourier_transform = np.fft.fft(test_data[n_bins // 2:] + test_data[:n_bins // 2])

    # Calculate the corresponding Fourier series coefficients from the FFT
    fourier_coeff = make_fs_coeffs(n_coeff, fast_fourier_transform)

    # Create the Fourier series approximating this data
    fourier_series = make_fourier_series(test_array, fourier_coeff)

    # Create a subplot to view the data
    axs[counter].plot(test_array, test_data, color="red")
    axs[counter].plot(test_array, fourier_series, color="blue")
    counter += 1
plt.show()