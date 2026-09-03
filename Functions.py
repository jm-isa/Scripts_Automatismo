# -*- coding: utf-8 -*-

import os
import struct
import numpy
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import export_graphviz
import seaborn as sns
import time
#from datetime import datetime

from read_comtrade import ReadAllComtrade 
from scipy.ndimage import gaussian_filter1d
from math import ceil
from sklearn import svm
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime




class Evaluate:
    #this algorith evaluate  and classifier comtrades acording to the values of the digitals values
    #To do: a algorith with the ability to identify the faul type (Pa-G,Pb-G,Pc-g,Pa-Pb,Pb-Pc,Pc-Pa,Pa-Pb-Pc)
    def __init__(self):
        #print('Starting evaluation decition tree!')
        return


    def training(self):
        
        # Data for trainig the algorithm
#        self.Dir_DataSet= dir_path + "\\" + "DataSet_TestBed.xlsx"                  # Training DataBase Directory 
        self.Data= pd.read_excel( 'DataSet_TestBed__v10_1.xlsx', index_col= None )
                
        cols= self.Data.columns[:17]
        X  = self.Data[ cols ]
        #X= [ list( Xx.loc[ ii ] ) for ii in range( len( Xx ) ) ]
        #Y= list( self.Data['Target'] )
        Y= self.Data['Target']
        decision_tree = DecisionTreeClassifier( random_state= 0, max_depth= None )
        self.decision_tree = decision_tree.fit( X, Y )

        return self.Data


    def Result( self,value ):
        B= int( self.decision_tree.predict( [ value ] ) )

        return B

    def ExportTree(self,name):
        name= name+'.dot'
        export_graphviz(
            self.decision_tree,
            out_file= name,
            filled= True,
            rounded= True)
    


def Digital(Signal,Time):
    # This function return 1 if the binary input change from 0 to 1 in any position
    #returns the activation time
    if numpy.sum(Signal) > 0:
        i, j = numpy.where(Signal == 1)
        TripTime=Time[i[0]]
        Trip=1
    else:
        TripTime=999
        Trip=0

    return Trip,TripTime

  


def DefCaso2( dict_time, DOs ) -> dict:
    # This function assing a 4 bits code depend on the input case     
    
    N= list( dict_time.values() )                                   # Toma los tiempos del diccionario de casos donde están los archivos como 'keys' y los tiempos de los comtrades como 'values'        
    N.sort()                                                        # Organiza los tiempos de orden ascendente (menor a mayor) 

    M= {}
    count= 0
    for j in N:                                                     # Cada tiempo de la lista organizada (para asignarlas en orden)
        for k,filee in enumerate( dict_time.keys() ):               # Saca los 'file'       
            
            if j == dict_time[ filee ]:                             # La idea es en este loop buscar el 'value' igualito al 'j' para asignarlo a un nuevo diccionario 'M' con los datos ordenados
                
                count += 1
                M[ filee ]= { 'Tiempo': j,                          # Diccionario con los archivos organizados cronológicamente, donde cada archivo contiene un diccionario que guarda el 'Tiempo' del evento y define el 'Caso' SEGÚN ORDEN ASCENDENTE
                              'Caso': 'Caso_' + str( count ) }                            
        
                if M[ filee ]['Caso'] == 'Caso_1':
                    A1, A2, A3, A4 = 0, 0, 0, 0
                                    
                elif M[ filee ]['Caso'] == 'Caso_2':
                    A1, A2, A3, A4 = 0, 0, 0, 1
                                    
                elif M[ filee ]['Caso'] == 'Caso_3':
                    A1, A2, A3, A4 = 0, 0, 1, 0
                                        
                elif M[ filee ]['Caso'] == 'Caso_4':
                    A1, A2, A3, A4 = 0, 0, 1, 1 
                elif M[ filee ]['Caso'] == 'Caso_5':
                    A1, A2, A3, A4 = 0, 1, 0, 0
                                         
                elif M[ filee ]['Caso'] == 'Caso_6':
                    A1, A2, A3, A4 = 0, 1, 0, 1
                                        
                elif M[ filee ]['Caso'] == 'Caso_7':
                    A1, A2, A3, A4 = 0, 1, 1, 0
                                        
                elif M[ filee ]['Caso'] == 'Caso_8':
                    A1, A2, A3, A4 = 0, 1, 1, 1
                                        
                elif M[ filee ]['Caso'] == 'Caso_9':
                    A1, A2, A3, A4 = 1, 0, 0, 0
                                        
                elif M[ filee ]['Caso'] == 'Caso_10':
                    A1, A2, A3, A4 = 1, 0, 0, 1
                                        
                elif M[ filee ]['Caso'] == 'Caso_11':
                    A1, A2, A3, A4 = 1, 0, 1, 0
                                       
                elif M[ filee ]['Caso'] == 'Caso_12':
                    A1, A2, A3, A4 = 1, 0, 1, 1
                                       
                elif M[ filee ]['Caso'] == 'Caso_13':
                    A1, A2, A3, A4 = 1, 1, 0, 0
                                        
                elif M[ filee ]['Caso'] == 'Caso_14':
                    A1, A2, A3, A4 = 1, 1, 0, 1
                                        
                elif M[ filee ]['Caso'] == 'Caso_15':
                    A1, A2, A3, A4 = 1, 1, 1, 0
                    
                elif M[ filee ]['Caso'] == 'Caso_16':
                    A1, A2, A3, A4 = 1, 1, 1, 1                     
        
               # M[ filee ]['DO']= [A1, A2, A3, A4] + DOs[ k ]
                M[ filee ]['DO']= DOs[ k ] + [A1, A2, A3, A4]
        
        
    return M
  
    

# datetime.strptime( '21/12/30,7:41:29', '%y/%m/%d,%H:%M:%S' ) - datetime(2021,12,30,7,41,25)
# datetime(2021,12,30,7,42,1) - datetime(2021,12,30,7,41,58)



#"""

Test_Time2= ['2021-12-30 07:39:56.685021',
 '2021-12-30 07:40:42.317202',
 '2021-12-30 07:41:27.569446',
 '2021-12-30 07:42:12.918801',
 '2021-12-30 07:42:58.227926',
 '2021-12-30 07:43:43.244946',
 '2021-12-30 07:44:29.551188',
 '2021-12-30 07:45:15.034094',
 '2021-12-30 07:46:00.373491',
 '2021-12-30 07:46:45.600111',
 '2021-12-30 07:47:30.809361',
 '2021-12-30 07:48:15.845769',
 '2021-12-30 07:49:01.215670',
 '2021-12-30 07:49:46.397857',
 '2021-12-30 07:50:31.451319',
 '2021-12-30 07:51:17.041337']

Test_TimeO={

'Caso_01': Test_Time2[0],
'Caso_02': Test_Time2[1],
'Caso_03': Test_Time2[2],
'Caso_04': Test_Time2[14],
'Caso_05': Test_Time2[15],
'Caso_06': Test_Time2[3],
'Caso_07': Test_Time2[4],
'Caso_08': Test_Time2[5],
'Caso_09': Test_Time2[6],
'Caso_10': Test_Time2[7],
'Caso_11': Test_Time2[8],
'Caso_12': Test_Time2[9],
'Caso_13': Test_Time2[10],
'Caso_14': Test_Time2[11],
'Caso_15': Test_Time2[12],
'Caso_16': Test_Time2[13]

}

#"""



def TimeFormat( Time ) -> str:
    
    y= int( Time.split('-')[0][-2:] )
    m= int( Time.split('-')[1] )
    d= int( Time.split()[0].split('-')[2] )
    h= int( Time.split()[1].split(':')[0] )
    mm= int( Time.split()[1].split(':')[1] )
    s= int( float( Time.split()[1].split(':')[2] ) )
    
    Timee= [y, m, d, h, mm, s]
   
    return Timee



def TimeFormat2( Time ) -> str:
    
    for i in Time.keys():
        
        y= int( Time[i].split('-')[0][-2:] )
        m= int( Time[i].split('-')[1] )
        d= int( Time[i].split()[1].split(':')[0] )
        h= int( Time[i].split()[1].split(':')[0] )
        mm= int( Time[i].split()[1].split(':')[1] )
        s= int( float( Time[i].split()[1].split(':')[2] ) )
    
        Time[i]= [y, m, d, h, mm, s]
    
    return Time


def TimeFormat3( TT ):
    
    DateTime= {}
    
    for ii in TT.keys():
        
        y= TT[ ii ][0]
        m= TT[ ii ][1]
        d= TT[ ii ][2]
        h= TT[ ii ][3]
        mm= TT[ ii ][4]
        s= TT[ ii ][5]
        
        DateTime[ ii ]= datetime.strptime( str(y) + '/' + str(m) + '/' + str(d) + ',' + str(h) + ':' + str(mm) + ':' + str(s), '%y/%m/%d,%H:%M:%S'  )
        
        
    return DateTime
    
    
    
    
    
    
  










