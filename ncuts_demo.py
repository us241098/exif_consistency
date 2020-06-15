from __future__ import print_function
from __future__ import division

import os, sys, numpy as np, ast
import init_paths
import load_models
from lib.utils import benchmark_utils, util
import tensorflow as tf
import cv2, time, scipy, scipy.misc as scm, sklearn.cluster, skimage.io as skio, numpy as np, argparse
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN

import demo

if __name__ == '__main__':
    plt.switch_backend('agg')
    #parser = argparse.ArgumentParser()
    #parser.add_argument("--im_path", type=str, help="path_to_image")
    #cfg = parser.parse_args()
    
    #assert os.path.exists(cfg.im_path)
    
    import glob
    import os
    
    im_path_results=glob.glob("./images_test_result/*.png")
    
    import re
    
    for j in range (0, len(im_path_results)):
      im_path_results[j] = re.sub('_result.png$', '.jpg', im_path_results[j])
      im_path_results[j]=im_path_results[j].replace('images_test_result','test_results')
    print(len(im_path_results))
    
 
    im_path = glob.glob("./test_results/*")
    filepaths=set(im_path) - set(im_path_results)
    filepaths=list(filepaths)
        # Re-populate list with filename, size tuples
    for i in range(len(filepaths)):
        filepaths[i] = (filepaths[i], os.path.getsize(filepaths[i]))

    # Sort list by file size
    # If reverse=True sort from largest to smallest
    # If reverse=False sort from smallest to largest
    filepaths.sort(key=lambda filename: filename[1], reverse=True)

    # Re-populate list with just filenames
    for i in range(len(filepaths)):
        filepaths[i] = filepaths[i][0]
        
    print(filepaths)
    print(len(filepaths)) 
    
    print("loading model")
    ckpt_path = './ckpt/exif_final/exif_final.ckpt'
    exif_demo = Demo(ckpt_path=ckpt_path, use_gpu=0, quality=2.0, num_per_dim=20)
    print("model loaded")
    #assert os.path.exists(cfg.im_path)
    
    for i in filepaths:    
        imid = i.split('/')[-1].split('.')[0]
        save_path = os.path.join('./images_test_result', imid + '_ncuts_result.png')
        print('Running image %s' % i)
        ms_st = time.time()
        im_path = i
        im1 = skio.imread(im_path)[:,:,:3].astype(np.float32)
        res = exif_demo.run(im1, use_ncuts=True, blue_high=True)
        print('MeanShift run time: %.3f' % (time.time() - ms_st))

        plt.subplots(figsize=(16, 8))
        plt.subplot(1, 3, 1)
        plt.title('Input Image')
        plt.imshow(im1.astype(np.uint8))
        plt.axis('off')

        plt.subplot(1, 3, 2)
        plt.title('Cluster w/ MeanShift')
        plt.axis('off')
        plt.imshow(res[0], cmap='jet', vmin=0.0, vmax=1.0)

        plt.subplot(1, 3, 3)
        plt.title('Segment with NCuts')
        plt.axis('off')
        plt.imshow(res[1], vmin=0.0, vmax=1.0)
        
        plt.savefig(save_path)
        print('Result saved %s' % save_path)