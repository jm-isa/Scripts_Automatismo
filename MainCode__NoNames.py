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
from datetime import *

from read_comtrade import ReadAllComtrade 
from scipy.ndimage import gaussian_filter1d
from math import ceil
from sklearn import svm
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime
from Functions import *
# from Auto_TestBed_Hypersim import *
 
#print( Test_Time )

#time.sleep(120)


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



Test_Time3 = {'Caso_01': datetime(2022, 3, 10, 16, 32, 47, 338114), 
 'Caso_02': datetime(2022, 3, 10, 16, 33, 33, 118916), 
 'Caso_03': datetime(2022, 3, 10, 16, 34, 18, 721434), 
 'Caso_06': datetime(2022, 3, 10, 16, 35, 4, 383485), 
 'Caso_07': datetime(2022, 3, 10, 16, 35, 50, 247382), 
 'Caso_08': datetime(2022, 3, 10, 16, 36, 35, 735222), 
 'Caso_09': datetime(2022, 3, 10, 16, 37, 21, 299688), 
 'Caso_10': datetime(2022, 3, 10, 16, 38, 6, 800653), 
 'Caso_11': datetime(2022, 3, 10, 16, 38, 52, 440520), 
 'Caso_12': datetime(2022, 3, 10, 16, 39, 38, 203827), 
 'Caso_13': datetime(2022, 3, 10, 16, 40, 24, 249374), 
 'Caso_14': datetime(2022, 3, 10, 16, 41, 9, 871243), 
 'Caso_15': datetime(2022, 3, 10, 16, 41, 55, 398712), 
 'Caso_16': datetime(2022, 3, 10, 16, 42, 40, 972905), 
 'Caso_04': datetime(2022, 3, 10, 16, 43, 26, 490161), 
 'Caso_05': datetime(2022, 3, 10, 16, 44, 11, 936479)}



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

  

"""
Main code start here
This code is for the relay testing protection 

There are two algorithms for the classification 

Decision Tree and k-Nearest Neighbors

"""

#time.sleep(60)


# Ensayando para asignar el tipo de caso a cada comtrade leído con el nombre por defecto que asigna el relé

Carpeta= 'Ensayo SinPOTT_2_NN'
pathh= 'd:/ambiente/escritorio/Comtrades' 
# path2= pathh + "\\" + Carpeta
allF2= []
date_com= []
allnames2=[]
N_dict= {}

for root, dirs, files in os.walk( pathh, topdown= False ):
  for name in files:
    if name.find('.cfg') > -1 or name.find('.CFG') > -1:
      print( name )
      allnames2.append(name)
      allF2.append(os.path.join(root, name))
      
      pos1= name.find('_')
      #date_com= int( name[ (pos1 + 1) : name.find('_', (pos1 + 1) ) ] ) 
      #N_dict[ os.path.join(root, name) ]= date_com


NN= {}
NNn= {}
DO2= []

for file in allF2:
  ComtradeObjec2= ReadAllComtrade( file )                                                 # Firts step, create instance for the comtrade class
  ComtradeObjec2.ReadDataFile()                                                           # Next, read the data file
  Time= ComtradeObjec2.getTimeChannel()/1000000                                           # Time in us
  
  # D1, T1= Digital( ComtradeObjec2.getDigitalASCCI(1), Time )                              # Trip A
  # D2, T2= Digital( ComtradeObjec2.getDigitalASCCI(2), Time )                              # Trip B
  # D3, T3= Digital( ComtradeObjec2.getDigitalASCCI(3), Time )                              # Trip C
  # D4, T4= Digital( ComtradeObjec2.getDigitalASCCI(4), Time )                              # 21 Dir Forward
  # D5, T5= Digital( ComtradeObjec2.getDigitalASCCI(5), Time )                              # 21 Dir Backward
  # D6, T6= Digital( ComtradeObjec2.getDigitalASCCI(6), Time )                              # Trip Z4 reversal
  # D7, T7= Digital( ComtradeObjec2.getDigitalASCCI(7), Time )                              # Trip Z2
  # D8, T8= Digital( ComtradeObjec2.getDigitalASCCI(8), Time )                              # Trip Z1
  # D9, T9= Digital( ComtradeObjec2.getDigitalASCCI(9), Time )                              # Trip 67N
  # D10, T10= Digital( ComtradeObjec2.getDigitalASCCI(10), Time )                           # Trip O 85 - 67N  POTT
  # D11, T11= Digital( ComtradeObjec2.getDigitalASCCI(11), Time )                           # Send O 85 - 67N  POTT
  # D12, T12= Digital( ComtradeObjec2.getDigitalASCCI(12), Time )                           # Trip O 85 - 21  POTT
  # D13, T13= Digital( ComtradeObjec2.getDigitalASCCI(13), Time )                           # Send O 85 - 21  POTT
 
  # Digital_Out= [D1, D2, D3, D4, D5, D6, D7, D8, D9, D10, D11, D12, D13]                   # Construye el vector de 
  # DO2.append( Digital_Out )
  
  NN[ file ]= ComtradeObjec2.start                                                        # Crea un dict con los archivos como "keys" y los tiempos de captura de los comtrade como "values"
  NNn[ file ]= ComtradeObjec2.templistt


NN= TimeFormat3( NN )

DD= {}
for ii, caso in enumerate( Test_Time.keys() ):
    
  for jj, file in enumerate( NN.keys() ):               
      
    A= NN[ file ]
    B= Test_Time3[ caso ]
    
    if ( Test_Time[ caso ] - NN[ file ] ) <= timedelta( seconds= 3 ):
      DD[ caso  ]= { 'Tiempo Ejecución': Test_Time[ caso ], 
                     'Tiempo Comtrade': NN[ file ], 
                     'Comtrade File': file }
            
print( [ list( DD.values())[ i ] for i in range( len( DD ) ) ] )
            

        
MM= DefCaso2( NN, DO2 )     
        




    
DO= [ MM[ i ][ 'DO' ] for i in MM.keys() ]   
Test_Timee= [ TimeFormat( i )  for i in Test_Time2 ]
"""
EvaluateObject2= Evaluate()                                                                 # Create instance for Evaluation
Data2= EvaluateObject2.training()
Estimated2= [ EvaluateObject2.Result( DO[ii] ) for ii in range( len( DO ) ) ]               # Evaluate each DO 
cols_Re= list( Data2.columns[18:-4] )                                                       # Cath the columns with the information for the results 
Re2= [ Data2[ cols_Re ].loc[ Data2['Target']== ii ].values[0] for ii in Estimated2 ]        # Create a matrix with the ordered information results 
Ree2= [ numpy.append( numpy.array( DO[i] ), r ) for i, r in enumerate( Re2 ) ]
print( Re2 )
"""


"""

# Export Tree
#EvaluateObject.ExportTree( 'ElArbolito' )


#Export excel file result
df = pd.DataFrame( Re, columns= cols_Re )
folder= os.getcwd()
File_exp= os.getcwd() + '\\' + 'Resultados.xlsx'
export_excel = df.to_excel ( File_exp, index= None, header= True)




#plot matrix
Cal= Data['Calificación'].unique()
#Res= numpy.concatenate( ( Res, ['OK'] ), axis= 0 )
Res= df['Calificación']
Caso= df['Caso']
matrix= numpy.zeros( ( len(Caso), len(Cal) ) ) - 1



pos= []
for i, res in enumerate( Res ):    
  for j, cal in enumerate(Cal):
      
    if res == cal:
      matrix[ i, j ] = 1            
      #pos.append( numpy.where( Res == aa )[0][0] )
    else:
      matrix[ i, j ] = -1


for i,cal in enumerate( Cal ):    
    matrix[ numpy.where( Res == cal )[0] , i ]= 1
"""    
    

                            


"""


#plot bar plot

Count= df['Caso'].value_counts()
plt.rcParams.update({'font.size': 12})
sns.barplot( Count.index, Count.values, alpha=0.8,)
plt.title('Resultados',fontsize=20)
plt.ylabel('Numero de ocurrencia', fontsize=20)
plt.xlabel('Diagnostico', fontsize=20)
plt.show()



#plot matrix
Res=df['Resultado'].unique()
Res=numpy.concatenate((Res,['OK']),axis=0)
Res1=df['Resultado']
Esp= df['Esperado']
matrix=numpy.zeros((len(Esp),len(Res)))

pos=[]
for i,z in enumerate(Esp):
  aa=Res1[i]
  if z==aa:
    matrix[i,numpy.where(Res=='OK')[0][0]]=1
    pos.append(numpy.where(Res==aa)[0][0])
  else:
    matrix[i,numpy.where(Res==aa)[0][0]] =-1

matrix=numpy.delete(matrix,pos,1)
Res=numpy.delete(Res,pos,0)

fig, ax = plt.subplots()
startcolor ='#FF0000'
midcolor = '#FFFFFF'
endcolor = '#008000'
othercolor = '#0080f0'



own_cmap1 = matplotlib.colors.LinearSegmentedColormap.from_list( 'own2', [startcolor, midcolor, endcolor, othercolor] )
mat = ax.imshow(matrix, cmap=own_cmap1, interpolation='nearest',vmin=-1, vmax=1)
plt.yticks(range(matrix.shape[0]), Caso )
plt.xticks(range(matrix.shape[1]), Res )
plt.xticks(rotation='vertical')
plt.tight_layout()
plt.show()
plt.savefig("output.png", bbox_inches="tight")
"""


