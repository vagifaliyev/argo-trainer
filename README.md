ARGO TRAINER
============================

![app](https://github.com/vagifaliyev/argo_trainer/blob/master/app.png)


Studying ocean is very essential for Earth as it cover 70 % of its surface, absorbs 1/3 of carbon dioxide emissions and plays the major role in protecting the world from the effects of greenhouse (Le Qu ́er ́e et al. 2012). Thus, obtaining data and understanding it in this field has become more essential as these factors have become more threatening. One of the leading providers of ocean data is ARGO floats with over 3200 floats (growing) reporting with 10,000 profiles per month, providing a range of properties such as water mass, salinity, temperature etc . This data enables scientists to understand how the state of oceans change over time and helps humanity monitor issues such as sea level rise, ocean heat content and warming, ocean circulation and the water cycle 

Having access to more information is beneficial, however it is difficult to go navigate through so much data without assistance. The climate science community is always in need of new set of tools to deal with a very large, ever-increasing volume of observational and computer model data. The target is to aid and facilitate analysis of these data for researchers in this field.

The software created provides automated method of creating a local database for argo data, visual- ization platform for graphical data and geographical mapping of sensor locations. Most importantly, allows the users to freely label data by interacting with graphs via multiple tools such as selector, zooming, panning and saving. Coding has been implemented in a modular way, thus user can insert their own prediction algorithms easily, observe its results through authenticator and further provide more training data till satisfactory results have been achieved. The final software is a product of constant user feed-back provided, matching the needs of researches in oceanography field. Before the publication of this software, there was no platform or mechanism to record knowledge of studies as data as there was no defined architecture to learn from each others analysis other than publication. To combat that problem, the main goal of the project is to provide a platform for researches across the field to share their data analysis and learn from each other in an interactive way.

Please read [report.pdf](https://github.com/vagifaliyev/argo_trainer/blob/master/report.pdf) for more information on code of conduct, development stages and algorthims.

## retrive.py

With the help of argo.py, the downloading of the data has been automated using a script. No other argo related piece of research has been used. Since the data-set of available argo floats is very large, the user can specify which exact float data they would like to download and work on. If any problem occurs, such as due to corrupted files, in successfully downloading the data a notification pops up to notify the user of the argo float id that caused the problem. The addition to the list can be made and already downloaded files will not be attempted to be downloaded again. 

## labeler.py

Data labelling allows the user to create a dataset of the features they are interested in. At startup, user can enter details of their name, feature interested in and number of samples they wish to examine.

Afterwards, two subplots are generated. First one, a salinity against temperature graph of random float and profile is drawn with scatter points colour codded by pressure. Since the behaviour of floats is highly dependent on its location a fully interactive map is also implemented as the second subplot, showing the location of current float and also the ones previously selected. 

The feature interested can then be selected using a rectangular tool which is activated on launch or re-activated by key press of "T". Once the feature is highlighted the user has 2 choices to label the selection as good by pressing the "G" key or as bad by pressing "R" key. Colour coded as Green and red respectively in the map subplot. While the current float examined is labeled with a white dot. The selection made is also displayed on the screen for the user. In the scenario where the user closes the application without making any selection, no data will be entered to the database and the next random one will be presented. 

Once the requested sample size has been reached, the user entries are presented to the user and given an option to name the csv file where the selections will be stored for later usage in training.

## authenticator.py

Authenticator allows the user to observe the prediction made by the algorithm. User can approve the prediction as correct by pressing the "B" key thus increasing the training data set or correct the prediction by making a new selection as previously described. Programme has been writen in a modular way so that the user can replace the predictive algorithm with their own. Once the user is satisfied with the predictions, the training is concluded. 


## Requirement(s)

Matplotlib is a widely used graphing library, and can be installed via [instructions](https://matplotlib.org/3.1.1/users/installing.html)

Geographical map data is recieved from Basemap and that can be install by following these [instructions](https://matplotlib.org/basemap/users/installing.html)

Also for faster and easie data analysis and manipulation, Pandas have been used and can be installed with these [instructions](https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html)

Argo.py library is required to access the database and the instructions to download it can be found [argo.py](https://pypi.org/project/argopy/)

This also requires Pandas for data manipulation.

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/vagifaliyev/argo_trainer/blob/master/LICENSE) file for details.




