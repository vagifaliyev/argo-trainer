# va719 - Vagif R. Aliyev
import random 
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.widgets import RectangleSelector
from mpl_toolkits.basemap import Basemap
import matplotlib.patches as patches
import matplotlib.colors
from matplotlib import gridspec
import csv
import pickle
import glob # get file names 
from matplotlib import style
from pandas.api.types import is_numeric_dtype

online = None
onlinee = input('Use online (y) or local data base (n) ? ')

if onlinee == 'y':
    print("Using online data base")
    online = True 
else:
    print("Using local data base")
    online = False 
    print("----------------------")


#if online requested use argopy
if online == True:
    print("--------ARGOPY---------")
    #only importing library if online requested by user 
    from argopy import DataFetcher as ArgoDataFetcher
    argo_loader = ArgoDataFetcher()
    print("-----------------------")


style.use("Solarize_Light2")

colour = None
feature = None


def line_select_callback(eclick, erelease):
    'eclick and erelease are the press and release events'
    global x1,y1,x2,y2
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata

def toggle_selector(event):
    global colour
    print(' Key pressed.')
    # Good data
    if event.key in ['G', 'g'] and toggle_selector.RS.active:
        print('> Good Data selected')
        print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (x1, y1, x2, y2))
        colour = 'green'
        toggle_selector.RS.set_active(False) 

    #good prediction
    if event.key in ['B', 'b'] and toggle_selector.RS.active:
        print('> Prediction is good')
        #print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (x1, y1, x2, y2))
        colour = 'blue'
        toggle_selector.RS.set_active(False) 

    # enable user to activate the selector again     
    if event.key in ['T', 't'] and not toggle_selector.RS.active:
        print(' RectangleSelector activated.')
        toggle_selector.RS.set_active(True)
    
    txt = "— Selection —"+ "\n" + "Colour: " + colour + "\n" +"Salinity [PSU]: "+ str(round(x1,3)) + " — " + str(round(x2,3)) + '\n' + "Temperature [°C]: "+ str(round(y1,3)) + " — " + str(round(y2,2)) 
    plt.figtext(0.6, 0.01, txt, wrap=True, ha='left',va="bottom", fontsize=8)

def normalize(array, value):
    norm = float((value - min(array)) / (max(array) - min(array)))
    return norm

def de_normalize(array, norm):
    denorm = (norm * (max(array) - min(array)) + min(array))
    return denorm

# get avarage normalized values 

# get avarage normalized values 
def train(feature):
    # USER SELECTION DATA
    global online 
    print("-> training started")

    path = r'./laballed_data/' # use your path
    all_files = glob.glob(path + "/*.csv") #only use csv file formats

    li = []
    #combine all the user entries 
    for filename in all_files:
        df_y = pd.read_csv(filename, index_col=None, header=0)
        li.append(df_y)

    df_y = pd.concat(li, axis=0, ignore_index=True)

    #only use feature data interested in 
    df_y = df_y[df_y.Feature == feature]

    #Reset index
    df_y = df_y.reset_index(drop=True)

    #if given feature exist train
    if not df_y.empty:
        #remove unneeded columns
        df_y = df_y.drop(columns=['lat', 'long'])

        argos = df_y['Float']

        profiles = df_y['Profile']

        df_normie = pd.DataFrame(columns=['x1', 'x2', 'y1', 'y2'])
        path = r'./argo_data/' # use your path
        for i in range(len(df_y.index)):
            #access the random float  from database
            if online == False:
                data = pd.read_csv(path+(str(argos[i])+".csv")) #access right float 
            if online == True:
                #access certain data and profile 
                ds = argo_loader.float(int(argos[i])).to_xarray()
                #conver to pandas
                data = ds.to_dataframe()

                # entries with qc flag of 1 for Pressure and Temo
                # if not 1, remove row
                data = data[data.PSAL_QC == 1]
                data = data[data.TEMP_QC == 1]

            data = data.loc[data['CYCLE_NUMBER'] == profiles[i]] # access right profile
            #normalize the values between -1 and 1 
            TEMP = data[['TEMP']].to_numpy()
            PSAL = data[['PSAL']].to_numpy()

            #if data exists 
            if data.empty == False:
                x1 = normalize(PSAL, df_y['x1'][i])
                x2 = normalize(PSAL, df_y['x2'][i])
                y1 = normalize(TEMP, df_y['y1'][i])
                y2 = normalize(TEMP, df_y['y2'][i])

                df_normie = df_normie.append({'x1': x1, 'x2': x2, 'y1': y1, 'y2': y2},ignore_index=True)  

        x_1 = df_normie["x1"].mean()
        x_2 = df_normie["x2"].mean()
        y_1 = df_normie["y1"].mean()
        y_2 = df_normie["y2"].mean()
        
        print("-> training finished")
    else:
        # if given feature does not exist ask again
        print("Given feature " + feature + " does not exist. \n Try again")
        feature = input("Feature interested: ")
        x_1, x_2, y_1 ,y_2, feature = train(feature)
    return x_1, x_2, y_1 ,y_2, feature

#normalizing the dataset further using IQR
def df_iqr(q1,q3,df, list_col):
    iqr_df = df
    for i in list_col:
        Q1 = iqr_df[i].quantile(q1)
        Q3 = iqr_df[i].quantile(q3)
        IQR = Q3 - Q1
        iqr_df = iqr_df.query('(@Q1 - 1.5 * @IQR) <= %s <= (@Q3 + 1.5 * @IQR)' % i)
    return iqr_df


def check_inrange(df,x1,x2,y2,y1):
    global x_1, x_2, y_1 ,y_2
    psal = df['PSAL']
    temp = df['TEMP']

    # only select values that are where the temp values lie
    df_c = df[df['TEMP'].between(y2, y1)]

    check_temp = df_c['TEMP'].between(y2,y1,inclusive=False)
    check_psal = df_c['PSAL'].between(x1,x2,inclusive=False)

    if not (check_temp == True).any() == True & (check_psal == True).any() == True :
        df1 = df_iqr(0.25, 0.75, df, ['PSAL','TEMP'])
        psal1 = df['PSAL']
        temp1 = df['TEMP']
        x1,x2,y1,y2 = get_predicts(psal1,temp1,x_1, x_2, y_1 ,y_2)

        df_c = df1[df1['TEMP'].between(y2, y1)]
        #final check
        check_temp = df_c['TEMP'].between(y2,y1,inclusive=False)
        check_psal = df_c['PSAL'].between(x1,x2,inclusive=False)
        if not (check_temp == True).any() == True & (check_psal == True).any() == True :
            df2 = df_iqr(0.2, 0.8, df, ['PSAL','TEMP'])
            psal2 = df2['PSAL']
            temp2 = df2['TEMP']
            x1,x2,y1,y2 = get_predicts(psal2,temp2,x_1, x_2, y_1 ,y_2)
    return x1,x2,y1,y2

def get_predicts(psal,temp, x_1, x_2, y_1 ,y_2):
    global x1,y1,x2,y2
    x1 = float(de_normalize(psal, x_1))
    x2 = float(de_normalize(psal, x_2))
    y1 = float(de_normalize(temp, y_1))
    y2 = float(de_normalize(temp, y_2))
    return x1, x2, y1, y2

def main():
    list_float = [1901155,1901298,1901324,1901341,1901604,1901685,1901689,1901694,1901710,1901711,1901712,1901713,
    1901716,1901717,1901719,1901720,1901721,1901722,1901727,1901730,1901733,1901784,
    1901790,1901806,1901807,1901814,1901815,1901816,1901817,1901818,1901819,1901820,1901822,1901824,1901825,1901826,1901827,
    1901828,1901829,1901830,1901836,1901849,1901851,1901854,1901855,1901856,1901857,1901865,1901866,1901867,1901868,1901870,1901876,
    1901877,1901878,1901879,1901880,1901882,1901883,1901885,1901886,1901887,1901894,1901896,1901915,1901916,1901917,1902060,
    1902061,1902062,1902063,1902064,1902065,1902066,1902067,1902068,1902069,1902070,1902071,1902072,1902073,1902180,1902182,
    1902183,1902184,1902204,1902205,1902206,1902207,1902208,1902209,1902210,1902211,1902220,1902227,1902228,1902274,2901300,
    2901904,2902169,3900559,3901037,3901038,3901039,3901040,3901041,3901064,3901108,3901110,3901111,
    3901116,3901211,3901219,3901220,3901226,3901236,3901237,3901238,3901239,3901240,
    3901241,3901242,3901297,3901310,3901311,3901312,3901496,3901513,3901515,3901519,3901521,3901522,3901523,3901525,3901526,
    3901534,3901536,3901537,3901546,3901547,3901549,3901550,3901551,3901554,3901597,3901598,3901601,
    3901602,3901603,3901604,3901605,3901606,3901607,3901609,3901610,3901611,3901619,3901622,3901623,3901624,
    3901625,3901626,3901627,3901628,3901629,3901630,3901631,3901632,3901633,3901634,3901635,3901637,
    3901640,3901642,3901643,3901644,3901646,3901650,3901651,3901652,3901653,3901654,3901656,3901657,3901658,
    3901659,3901660,3901661,3901662,3901663,3901665,3901666,3901668,3901669,3901670,3901671,3901672,3901673,3901674,
    3901675,3901677,3901679,3901680,3901681,3901683,3901684,3901685,3901686,3901687,3901819,3901820,3901821,
    3901822,3901823,3901827,3901828,3901829,3901830,3901832,3901833,3901834,3901835,3901836,3901838,3901839,
    3901840,3901841,3901843,3901844,3901845,3901846,3901847,3901849,3901850,3901851,3901852,3901853,
    3901854,3901855,3901856,3901857,3901858,3901859,3901860,3901861,3901864,3901865,3901866,3901867,3901868,
    3901869,3901870,3901871,3901872,3901873,3901875,3901876,3901878,3901880,3901881,3901882,3901884,3901887,
    3901888,3901891,3901892,3901893,3901895,3901896,3901898,3901901,3901903,3901908,3901909,
    3901911,3901915,3901918,3901919,3901921,3901922,3901926,3901929,3901930,3901931,3901932,3901933,3901934,
    3901935,3901937,3901938,3901939,3901942,3901943,3901944,3901945,3901946,3901947,3901948,3901949,3901950,
    3901951,3901954,3901955,3901956,3901957,3901961,3901963,3901964,3901965,3901967,3901968,
    3901969,3901970,3901971,3901972,3901975,3901976,3901977,3901978,3901979,3901980,3901982,3901983,
    3901984,3901985,3901986,3901987,3901988,3901989,3901990,3901991,3901992,3902102,3902103,3902106,3902107,
    3902108,3902109,3902110,3902120,3902121,3902122,3902123,3902124,3902125,3902127,3902128,3902131,3902135,
    3902137,3902148,3902149,3902150,3902151,3902152,3902153,3902154,3902155,3902156,3902157,3902159,3902160,
    3902161,3902162,3902163,3902166,3902168,3902169,3902201,3902202,3902203,3902204,3902206,3902207,3902208,
    3902209,3902213,3902214,3902215,3902218,3902235,3902236,3902237,3902238,3902240,3902241,3902243,3902244,
    3902245,3902398,3902399,3902400,3902402,3902403]
    
    #create empty dataframe to store user inputs
    df_main = pd.DataFrame(columns=['Feature','Float', 'Profile', 'Colour', 'x1', 'x2', 'y1', 'y2','lat', 'long'])

    # will create a data set 
    user = input("Enter name: ")

    #print("Welcome "+ user)
    feat = input("Feature interested: ")
    gen = input("Number of samples: ")
    
    global x_1, x_2, y_1 ,y_2
    
    x_1, x_2, y_1 ,y_2, feat = train(feat)

    print('--------- Graph Info ---------')
    print(" White dot represents the current location \n press 'g' to correct the prediction \n press 'b' to label prediction as correct")
    #create Basemap instance
    m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90, 
                llcrnrlon=-180,urcrnrlon=180,resolution='c')

    # pickle the class instance.
    pickle.dump(m,open('map.pickle','wb'),-1)

    #no need to display the saved map 
    plt.close()

    for i in range(int(gen)):
        # t0 = time.time()
        # declare the global colour
        global colour 
        colour = ''
        global x1,y1,x2,y2

        #select random float float 
        argo = random.choice(list_float)
        argo = 3901987
        #access the random float  from database
        if online == False:
            argo_float = pd.read_csv("./argo_data/"+str(argo)+'.csv') 
        if online == True:
            argo_loader = ArgoDataFetcher()

            #access certain data and profile 
            ds = argo_loader.float(argo).to_xarray()
            #conver to pandas
            argo_float = ds.to_dataframe()

            # entries with qc flag of 1 for Pressure and Temo
            # if not 1, remove row
            argo_float = argo_float[argo_float.PSAL_QC == 1]
            argo_float = argo_float[argo_float.TEMP_QC == 1]


        #recieve a list of profiles in the float
        list_prof = list(dict.fromkeys(argo_float['CYCLE_NUMBER']))

        #randomly select a profile 
        prof = random.choice(list_prof)
        prof = 305
        #access the requested profile number datas 
        df = argo_float.loc[argo_float['CYCLE_NUMBER'] == prof]

        # allocate the columns to specific variable names for easier access
        pres = df['PRES']
        psal = df['PSAL']
        temp = df['TEMP']
        lat = df['LATITUDE'].values[0]
        lon = df['LONGITUDE'].values[0]

        # plotting salinity graph
        fig = plt.figure(num='— Authenticator —' ,figsize=(12,6))
        gs = gridspec.GridSpec(1, 2, width_ratios=[2, 1]) 
        ax1= plt.subplot(gs[0])

        # adding a low transperency line to follow the patern more easily
        plt.plot(psal, temp, alpha=0.2)

        # main fature is the scatter plot
        sc = plt.scatter(psal,temp,c=pres, cmap='hsv')

        #labels
        # add colour graded bar
        cbar = plt.colorbar(sc)
        cbar.set_label('Pressure', labelpad=-40, y=1.05, rotation=0)
        plt.title('Float: '+str(argo)+'      Profile: '+str(prof))
        plt.xlabel('Salinity')
        plt.ylabel('Temp')

        # enabling use of selector 
        # drawtype is 'box' or 'line' or 'none'
        toggle_selector.RS = RectangleSelector(ax1, line_select_callback,
                                            drawtype='box', useblit=True,
                                            button=[1, 3],  # don't use middle button
                                            minspanx=5, minspany=5,
                                            spancoords='pixels',
                                            interactive=True)

        plt.connect('key_press_event', toggle_selector)

        # Create a Rectangle patch
        x1,x2,y1,y2 = get_predicts(psal,temp,x_1, x_2, y_1 ,y_2)
        # if the prediction is not within the data range
        # normalize the data further 
        x1,x2,y1,y2 = check_inrange(df,x1,x2,y1,y2)


        rect = patches.Rectangle((x1,y1),(x2-x1),(y2-y1),linewidth=0.5,
                                fc=(0,0,1,0.5), ec=(0,0,0,0.8))

        # add rectnagle to ax 
        ax1.add_patch(rect)

        txt = "— Prediction —"+ "\n" + "Salinity [PSU]: "+ str(round(x1,3)) + " — " + str(round(x2)) + '\n' + "Temperature [°C]: "+ str(round(y1,3)) + " — " + str(round(y2,3)) 
        plt.figtext(0.6, 0.15, txt, wrap=True, horizontalalignment='left', fontsize=8)

        # BASEMAP MAPPING
        ax2 = plt.subplot(gs[1])    
        #load the saved map
        m = pickle.load(open('map.pickle','rb'))

        # make sure extra features are loaded
        m.bluemarble()
        m.drawcountries()
        m.drawcoastlines()
        m.drawrivers(color='#0000ff')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')

        #plot the current float point
        lons, lats = m(lon, lat)
        m.scatter(lons, lats, marker='o',color='w', zorder=5)
        
        #plot the previous points
        lons, lats = m(df_main['long'].values, df_main['lat'].values)
        m.scatter(lons, lats, marker='o',color=df_main['Colour'], zorder=5)
        ax2.set_title("— Map — \n" + "Lat: " + str(round(lat,3)) + ' Long: ' + str(round(lon,3)))

        # zoom in to current float 
        plt.axis([lon-30,lon+30,lat-30,lat+30])

        # Instructions
        txt = "Press B to confirm the prediction \n Press G to correct the prediction \n Press T enable selector again"
        plt.figtext(0.8, 0.05, txt, wrap=True, ha='left',va="bottom", fontsize=8)
        
        # Author info
        txt = "created by Vagif R. Aliyev"
        plt.figtext(0.935, 0.01, txt, color='white',
            ha='center', fontsize=8, 
            bbox={'fc':'navy', 'ec':'white','alpha':0.8, 'pad':4})

        print("—- Prediction -- \n" +"Float: "+ str(argo) +"Profile: " + str(prof))
        print("Salinity [PSU]: "+ str(round(x1,3)) + " — " + str(round(x2)) + '\n' + "Temperature [°C]: "+ str(round(y1,3)) + " — " + str(round(y2,3)) )
        
        plt.show()
        plt.close()

        # at the end of one loop, save all the data to main dataframe
        # if user made no selection do not

        if str(colour) is not '':
            df_main = df_main.append({'Feature': feat,'Float': argo,'Profile': prof, 
                                    'Colour': colour,'x1': x1, 'x2': x2, 'y1': y1, 'y2': y2,'lat': lat, 'long':lon}, 
                                    ignore_index=True)

    print('----------------------DATA AUTHENTICATION FINISHED-------------------------')
    #print dataframe to check 
    print(df_main)
    
    #request filename
    filename = input(user+", insert file name: ")

    #save the data frame as csv
    # if file does not exist write header 
    # else it exists so append without writing the header
    path=r'./laballed_data/'
    with open(path+(user+'_'+filename+'.csv'), 'a') as f:
        df_main.to_csv(f, header=f.tell()==0,index=False)

    print('-----------------------CSV FILE SAVED------------------------')

#call main function
main()