# Homework 3: K-means algorithm for image segmentation

## How to run the code

This code can be run as a python script or using the command:

$ python hw3_group3.py


## Functions within the code


`getPixels(filename)`

	Input: string(name of the image)

	Output: array(pixels)

	This function takes the name of the image and returns an array which contains the RGB values of each pixel.

	Calls: None

	Called by: Main


`def k_means(image, nClusters, nIters)`

	Input: array(image_pixels), int(nClusters), int(nIters)

	Output: array(pixels)

	This function takes the array returned by getPixels, the k(= number of clusters) and the number of iterations we will repeating the process. It returns the pixels of the means of the clusters and indices denoting the cluster a pixel belongs to.

	Calls: None

	Called by: Main


`Main`

	The main part of the code we create a list with all the names of the images we will process and another list with all the values of k we are willing to try. For each image and for each k we find the best centers of the clusters and we replace the RGB values of each pixel belongs in the cluster with the RGB values of the center. Finally we save the produced images to the folder. 



