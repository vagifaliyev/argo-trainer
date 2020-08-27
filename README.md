ARGO TRAINER
============================

Studying ocean is very essential for Earth as it cover 70 \% of its surface, absorbs 1/3 of carbon dioxide emissions and plays the major role in protecting us from the effects of greenhouse. Thus, obtaining data and understanding it in this field has become more essential as these factors have become more threatening. One of the leading providers of ocean data is ARGO floats with over 3200 floats (growing) reporting with 10,000 profiles per month, providing a range of properties such as water mass, salinity, temperature etc (Argo Research use, n.d.). This data enables scientists to understand how the state of oceans change over time and helps humanity monitor issues such as sea level rise, ocean heat content and warming, ocean circulation and the water cycle 

Having access to more information is beneficial, however it is difficult to go through so many without assistance. The climate science community is always in need of new set of tools to deal with a very large, ever-increasing volume of observational and computer model data. (reference Unsupervised Clustering of Southern Ocean Argo Float Temperature Profiles) The goal of the project is to take advantage of this data revolution to apply modern computing techniques to provide new user-friendly software to democratize access to this new ARGO data stream. The target is to aid and facilitate analysis of these data for researchers in this field. Allowing the user to create elements that will assist them in seeing patterns in data. Providing them with platform where they can create their own data for analysis and implement their own prediction algorithms and test their performance.

## retrive.py

With the help of argo.py, the downloading of the data has been automated using a script. No other argo related piece of research has been used. Since the data-set of available argo floats is very large, the user can specify which exact float data they would like to download and work on. If any problem occurs, such as due to corrupted files, in successfully downloading the data a notification pops up to notify the user of the argo float id that caused the problem. The addition to the list can be made and already downloaded files will not be attempted to be downloaded again. 

## labeler.py

Data labelling allows the user to create a dataset of the features they are interested in. At startup, user can enter details of their name, feature interested in and number of samples they wish to examine.

Afterwards, two subplots are generated. First one, a salinity against temperature graph of random float and profile is drawn with scatter points colour codded by pressure. Since the behaviour of floats is highly dependent on its location a fully interactive map is also implemented as the second subplot, showing the location of current float and also the ones previously selected. 

The feature interested can then be selected using a rectangular tool which is activated on launch or re-activated by key press of "T". Once the feature is highlighted the user has 2 choices to label the selection as good by pressing the "G" key or as bad by pressing "R" key. Colour coded as Green and red respectively in the map subplot. While the current float examined is labeled with a white dot. The selection made is also displayed on the screen for the user. In the scenario where the user closes the application without making any selection, no data will be entered to the database and the next random one will be presented. 

Once the requested sample size has been reached, the user entries are presented to the user and given an option to name the csv file where the selections will be stored for later usage in training.

## authenticator.py

Authenticator allows the user to observe the prediction made by the algorithm. User can approve the prediction as correct by pressing the "B"key thus increasing the training data set or correct the prediction by making a new selection as previously described. Once the user is satisfied with the predictions, the training is concluded. 


### Requirement(s)

Matplotlib is a widely used graphing library, and can be installed via [instructions](https://matplotlib.org/3.1.1/users/installing.html)

Geographical map data is recieved from Basemap and that can be install by following these [instructions](https://matplotlib.org/basemap/users/installing.html)

Also for faster and easie data analysis and manipulation, Pandas have been used and can be installed with these [instructions](https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html)

Argo.py library is required to access the database and the instructions to download it can be found [argo.py](https://pypi.org/project/argopy/)

This also requires Pandas for data manipulation.



