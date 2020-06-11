##Install Dependencies
pip install -r requirements.txt

Start App

export FLASK_APP=server.py
export FLASK_ENV=development
flask run

client side can be found at [link](https://github.com/Tobenna-KA/mimeai/)

## Sample report
__________________________________________________________________________________________________
Layer (type)                    Output Shape         Param #     Connected to                     
==================================================================================================
input_1 (InputLayer)            (None, 28, 28, 3)    0                                            
__________________________________________________________________________________________________
conv1 (Conv2D)                  (None, 20, 20, 128)  31232       input_1[0][0]                    
__________________________________________________________________________________________________
primarycap_conv2d (Conv2D)      (None, 6, 6, 256)    2654464     conv1[0][0]                      
__________________________________________________________________________________________________
primarycap_reshape (Reshape)    (None, 1152, 8)      0           primarycap_conv2d[0][0]          
__________________________________________________________________________________________________
primarycap_squash (Lambda)      (None, 1152, 8)      0           primarycap_reshape[0][0]         
__________________________________________________________________________________________________
digitcaps (CapsuleLayer)        (None, 10, 16)       1474560     primarycap_squash[0][0]          
__________________________________________________________________________________________________
mask_2 (Mask)                   (None, 160)          0           digitcaps[0][0]                  
__________________________________________________________________________________________________
capsnet (Length)                (None, 10)           0           digitcaps[0][0]                  
__________________________________________________________________________________________________
decoder (Sequential)            (None, 28, 28, 3)    3018544     mask_2[0][0]                     
==================================================================================================
Total params: 7,178,800
Trainable params: 7,178,800
Non-trainable params: 0

## sample response

```{
    "disease": "Early_blight",
    "accuracy": 92, 
    "image_path": "static/predicted_images/Early_blight/2020-06-11 23:19:46.142173.png",
    "success": true
    }``` 

