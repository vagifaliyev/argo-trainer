Independent Research Project
============================

Due **5pm BST on 28th August**.

Place any code developed during this project in this directory, using git/version control as normal.

Use the `Documentation` folder for any documentation/manuals you write. You are otherwise free to develop your own file structures as appropriate to your project.

You may edit this README.md if you choose.

============================

## data_downloader.py

Contains a list of known float numbers, which are used to access the online database and dowloaded to the local machine as csv files for faster access. The list can be updated by the user, the programme will also avoid redowloading files already in the path directed by the user.

### Run
```
  python3 data_downloader.py
```

### Requirement(s)

Argo.py library is required to access the database and the instructions to download it can be found [argo.py](https://pypi.org/project/argopy/)

Also for faster and easie data analysis and manipulation, Pandas have been used and can be installed with these [instructions](https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html)

## data_labeler.py

Gives the user platform to label data that will be used for training the mahcine learning. 
Instructions to the user are provided within the programme.

### Run
```
  python3 data_labeler.py
```

### Requirement(s)

Matplotlib is a widely used graphing library, and can be installed via [instructions](https://matplotlib.org/3.1.1/users/installing.html)

Geographical map data is recieved from Basemap and that can be install by following these [instructions](https://matplotlib.org/basemap/users/installing.html)

This also requires Pandas for data manipulation.


