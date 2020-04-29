from PIL import Image
import numpy as np

def getPixels(filename):
    image = Image.open(filename)
    pixels = np.asarray(image)/255
    image.close()
    return pixels

def k_means(image, nClusters, nIters):

    image = np.reshape(image,(image.shape[0]*image.shape[1],3))
    means = image[np.random.choice(image.shape[0], nClusters, replace=False), :]
    idx = np.zeros(image.shape[0])
    dist = np.zeros(nClusters)
    
    for i in range(nIters):
        # assignment step
        for j in range(len(image)):
            
            for k in range(nClusters):
                dist[k] = np.linalg.norm(image[j] - means[k])
                
            idx[j] = np.argmin(dist)
    
        # compute mean of each cluster 
        for i in range(nClusters):
            cluster = np.empty((0,3))
            for j in range(len(image)):
                
                if(idx[j] == i):
                    cluster = np.append(cluster,np.array([image[j]]),axis=0)
            means[i] = np.array([np.mean(cluster[:,0]),np.mean(cluster[:,1]),np.mean(cluster[:,2])])        
    return means, idx


image_list = ['dupont.jpg','green.jpg','spencer.jpg','udel_logo.jpg']
cluster_list = [1,2,5,10,20]

nIters = 5

for image in image_list:
    for nClusters in cluster_list:
        image_pixels = getPixels(image)
        
        # pixels of the means of the clusters and indices denoting the cluster a pixel belongs to
        means, idx = k_means(image_pixels, nClusters, nIters)
        image_new = means[idx.astype('uint8')]
        image_new = (255*image_new).astype('uint8')
        
        # reshaping to the original image size
        image_new = np.reshape(image_new,(image_pixels.shape[0], image_pixels.shape[1], image_pixels.shape[2]))
        image_new = Image.fromarray(image_new)
        image_new_name = image[:-4]+'_k='+str(nClusters)+'_new.jpg'
        image_new.save(image_new_name)
        im = Image.open(image_new_name)
        im.show()






























































