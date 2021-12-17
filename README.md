# Drawing (almost) Anything with the Fourier Series
For this project, I created a program that can break down any image into its component signals then use those same signals to plot an approximation of the original image. By deconstructing any arbitrary image, or signal, into component signals can allow for simpler image manipulation and could also lead to better storage methods. The reconstructed signal can never be exactly equal to the original image (unless it was decomposed into an infinite number of signals), but there exists a finite number of "building block" signals that, when summed together, create an adequate representation of the original. This idea becomes weaker when looking at different types of signals, such as ones with many sharp corners, but it still holds strong for essentially every other type of signal. 

This program takes in SVG format image files, reads the paths in that image to some degree, then takes the discrete Fourier transform. In the first version of this project, I also used the DFT's output to calculate the Fourier series coefficients of that signal, then used those coefficients to calculate an approximation of the signal using the Fourier series' synthesis equation. I've tested the code using a variety of different images, some simple and some more complex, in order to see just how accurately it can recreate varying inputs.

# My Approach
The Fourier series/transform allows for an image to be represented in the frequency domain. It's widely held true that the Fourier transform of any real/complex valued signal can be represented as a sum of sinusoids. The Fourier series is similar in that it can represent any function as long as it is periodic or as long as it's bounded on a certain interval (and as long as it passes the Dirichlet conditions). See the synthesis and analysis equations below:

![image](https://user-images.githubusercontent.com/77978140/146498670-f8ef8cea-cd47-444a-8257-ec36aa85bdaf.png)

In order to obtain the Fourier series coefficients (which are needed to reconstruct the signal from the frequency domain, as can be seen in the equations above), I used NumPy's Fast Fourier Transform (FFT) function. This function is an efficient version of the discrete Fourier transform (DFT). DFT's essentially sample some discrete number of equally-spaced points into a sequence of equally-spaced samples of the discrete-time Fourier transform (DTFT), which is also a function of frequency. The DTFT is related to the Fourier series such that the Fourier series' coefficients can be calculated from the DTFT. That relation is shown below:

![image](https://user-images.githubusercontent.com/77978140/146499608-4fd1174e-e612-47d3-874f-7bc4c17ce9ed.png)

where c corresponds to the FFT's complex numbered output, n is the number of Fourier coefficients (from 0 to n), a is the real-valued component and b is the imaginary-valued component of the complex number (a + bi) that is the Fourier series coefficient at that value of n. Now that the Fourier series coefficients are known, the approximation of the original signal can be calculated using the Fourier series synthesis equation. Then, that signal was plotted using that approximation and compared to the original to see how accurate of a recreation it was. 

To test these ideas, I first made a program that approximated a square wave signal. The code for this can be found in sw_plotter.py, and a picture showing the different levels of accuracy for differing values of n is shown below (where n = 1, 19, 51, 501 from top to bottom):

![sw_1_19_51_501](https://user-images.githubusercontent.com/77978140/146500224-79e51741-e811-43ed-9a29-0057fdacf8f1.png)

In the final plot, the approximations at the corners of the discontinuities "spike." This is called the Gibbs phenomenon, which is beyond the scope of this project as of now, but still worth mentioning. This phenomenon will continue to show itself in the more complex signals shown later on. Beyond the Gibbs phenomenon, though, the signal becomes increasingly accurate as the number of n (or Fourier coefficients) increases, which is expected. 

In order to approximate any signal, including 2D images, a similar approach is taken. In the general_fs_plotter.py file, FFT's are taken on both the x and y values of the SVG file's inputs. The same logic is done on both sets of transforms such that, at the end, there are two different arrays containing the Fourier series approximations for the x and y values. The x-values and y-values are plotted together to form the approximation for the signal at every point sampled, and simmilar results are found as in the first, 1D file. 

# Results

Before I discuss the problems with the current implementation, I'd like to show a few different approximations for different signals that were successful. First, I'll show the approximation for the Texas A&M logo, which was the first deliverable of this project:

https://user-images.githubusercontent.com/77978140/146501228-41863088-6487-4b51-a38e-019d45d9c417.mp4

Next, an approximation for the symbol pi:

https://user-images.githubusercontent.com/77978140/146501798-1c53a710-1054-46ac-bc6e-51257b2af3ab.mp4

And finally, that of a simple silhouette of a succulent:

https://user-images.githubusercontent.com/77978140/146501823-b554ab5c-8671-49ab-9c64-52ecb01906e2.mp4

As can be seen from every signal above, the more Fourier coefficients are calculated, the better the approximation becomes. It's also worth noting that sharp corners continue to be a nuisance for the Fourier approximations. In the A&M logo, look closely at the sharp corners. The approximation can only yield "curvy" corners, not perfectly straight ones, at least for any finite number of summed signals. 

It's also worth noting how the images need to be prepared. In the A&M logo again, I had to "connect" the letters together and put a slit into the A so that the Fourier approximation didn't have to jump discontinuously. If I did not edit the picture, then it'd look something like this:

![2_tamu_hole_ex](https://user-images.githubusercontent.com/77978140/146502404-d8bb41b1-8409-451e-b435-91f7d8c7b367.png)

where the approximated signal jumps in an ugly way through the A to the left side of the T. When adding a slit, it fixes that jump: 

![2_tamu_fixed_ex](https://user-images.githubusercontent.com/77978140/146502484-7f10eef2-773b-4fc7-bf1e-2c536533867e.png)

More complex signals can also be represented. For example, a picture of Reveille which contains 501 Fourier coefficients:

![rev_500n_2500bins](https://user-images.githubusercontent.com/77978140/146502586-192fc70f-c996-4a96-9550-a06ea99bbf9a.png)

However, the number of Fourier coefficients is not the only deciding variable for how accurate the approximation is. For example, if I try to reconstruct a picture of Reveille with 5001 Fourier coefficients but only 250 points on each SVG path, then this is the result: 

![rev_5000n_250bins](https://user-images.githubusercontent.com/77978140/146502893-c1fe9d87-2ec7-4e66-b07d-3a84caeba527.png)

This is equivalent to this picture, which has 501 Fourier coefficients as the first but only 250 points (called n_bins in the code):

![rev_500n_250bins](https://user-images.githubusercontent.com/77978140/146502991-201137aa-060a-4d18-beaa-a0ae21c82de6.png)

In the first picture, the number of n_bins used was 2500. Comparing all three of these pictures, it's apparent that how well sampled the SVG file is also factors into how accurate the approximation is, which makes sense intuitively. 

Not all images were recreated successfully, though. Below I'll show a few failures:

Homer with 5000 Fourier coefficients and 1500 n_bins:
![2_homer2_5000n](https://user-images.githubusercontent.com/77978140/146503143-a32fd3bd-21f8-4b3f-b7b8-525b17e4c08c.png)

A lion with 5000 Fourier coefficients and 2500 n_bins:
![lion_5000n_2500bins](https://user-images.githubusercontent.com/77978140/146503252-886ffee9-fb56-490a-97d0-ebe03f8063e0.png)

The same lion with 5000 Fourier coefficients and 5000 n_bins:
![lion_5000n_5000bins](https://user-images.githubusercontent.com/77978140/146503284-f1c2fe61-baf0-4640-8f52-653a3f46aba0.png)

And some palm trees
![palm_tree_strangeness](https://user-images.githubusercontent.com/77978140/146503351-908af29e-5fa3-4524-a737-8c27c6a8a59d.png)

The last picture of these (the palm trees) is likely that way due to not prepping the PNG file before converting it to a SVG (the PNG looked like below):

![palm_trees](https://user-images.githubusercontent.com/77978140/146503459-8dae99a0-180b-4d5e-953e-f0d8839f1162.jpg)

The first three, though, are more interesting. It's possible that there was some sort of error with the SVG file conversion (I did use free sites to convert them, after all), but I'm not certain. The picture of Homer is very complex, so I think with some tinkering of the PNG file I could create a more accurate picture without any ugly discontinuous jumps. I'm not sure why the lion has those discontinuous jumps, though. The PNG and SVG files both look clean, and yet there are a couple of jumps in places that seem like they should be continuous. It's possible that, since the jumps seem to occur on sharp parts of the lion's fur, that the SVG file converter or my program somehow got confused on those sharp edges again. 

# Future Steps
In the near future, I want to implement an animation of the Fourier series actually drawing out its approximation using epicycles (or spinning vectors). In the first YouTube video linked below in the references, he does a fantastic job of visualizing the Fourier series and how those sinusoids add together to create the final image. Unfortunately, I have no experience with any animation tools, and so I wasn't able to finish the animation in time. I had attempted to perform the FFT on the whole SVG path instead of breaking it up into its real and imaginary parts and using its result to animate all of the Fourier series (once the coefficients were calculated from the FFT's values). I'm not sure if it's the way I implemented my animation code or if something is wrong with my math, but it failed to animate properly. Those files that contain that code are svg_plot_test.py and epicycle_animator.py.

I think it would also be interesting to allow for PNG, JPG, and other file formats to be used as inputs into the program. I also want to see if other forms of the Fourier transform/series can be used to create the same approximations and which ones are best for this application. 

Yet another interesting idea is somehow determining beforehand how many Fourier series coefficients are necessary to reconstruct an adequately accurate image. The idea is that for more simple or curvy shapes, like the succulent plant, it takes fewer Fourier coefficients to accurately represent them than for more blocky ones, like in the Texas A&M logo. I suspect that the SVG file format could be used for this, since once its path is found in python, the different curves used to define the image are known. For example, the pi image has many different Line and CubicBezier objects. More information can be found at https://pypi.org/project/svg.path/.

See the section below for all the different resources I used to create this project. Most I simply used as intuitive references, but others (like the 3Blue1Brown and Mathologer videos) I used to help create my math and code. Some are also resources that may be useful in implementing the future ideas in this section.

# References/Sources:

https://www.youtube.com/watch?v=r6sGWTCMz2k&t=307s&ab_channel=3Blue1Brown

https://www.youtube.com/watch?v=qS4H6PEcCCA&t=743s&ab_channel=Mathologer

https://en.wikipedia.org/wiki/Fourier_series

https://en.wikipedia.org/wiki/Discrete-time_Fourier_transform

https://stackoverflow.com/questions/64165282/determining-fourier-coefficients-from-time-series-data 

https://github.com/Amritaryal44/drawing-with-DFT-and-epicycle 

https://gitlab.com/giacomogallina/fourier/-/blob/master/fourier.py

https://github.com/MarcPartensky/Fourier

https://www.eecs.umich.edu/courses/eecs206/public/lec/wakefield,fs,dft.pdf

https://convertio.co/
