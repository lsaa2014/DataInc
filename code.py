import numpy as np
import os
import matplotlib.pyplot as plt
from pandas import Series, DataFrame
import pandas as pd
import json
from flask import Flask

app = Flask(__name__)

if __name__ == '__main__':
    app.run(port=33507)

import requests
url = 'https://chronicdata.cdc.gov/api/views/dttw-5yxu/rows.json?accessType=DOWNLOAD'
resp = requests.get(url)
resp

print(len(resp.text))
print (resp.headers['content-type'])

## file type {'data': [[3639,'2FD4E5E9-4694-47BB-9EFB-E421E46C041A',3639,1457698824,'716424',1457698824,'716424',
## None,'2014','AK', 'Alaska', 'Alcohol Consumption', 'Alcohol Consumption', 'Adults who have had at 
##least one drink of alcohol within the past 30 days', 'Yes','Overall','Overall','2385','56.7','54.6', '58.8', '1','%',
 ##  'Crude Prevalence',None,None,'BRFSS','CLASS01','Topic03','02','BO1','CAT1','DRNKANY5', 'RESP046',[None, '64.84507995700051',
##'-147.72205903599973', None, False]]

data = json.loads(resp.text)
prams = DataFrame(data['data'])

prams = prams.drop(prams.columns[:8], axis = 1)
prams_set = prams.copy()

## Select my columns
subset = prams_set[[8,9,11,12,13,14,15,16,17,18,19,20,27,28,32,33]]

## Rename the columns with the correct name
myCol = {8:'Year',9:'Location',11:'Class',12:'Topic',13:'Question',14:'Response',15:'Break_Out',16:'Break_Out_Category',
    17:'Sample_Size',18:'Data_Value',19:'ConfidenceL', 20:'ConfidenceH',27:'ClassId',28:'TopicId',32:'QuestionId',33:'ResponseId'}
    
subset = subset.rename(columns = myCol)
subset.head(n=3)

subset['Class'].unique()

subset1 = subset[(subset['Class']== 'Chronic Health Indicators') | (subset['Class']== 'Colorectal Cancer Screening')
    | (subset['Class'] == 'Overweight and Obesity (BMI)') | (subset['Class']== 'Cholesterol Awareness') | 
                 (subset['Class']== 'Fruits and Vegetables')]
                 

## find the frequency based on class and topic
res = subset1.groupby('Class')['Topic'].value_counts() 
subset1.groupby('Topic')['Class'].value_counts().plot(kind = 'barh') 
 
## find the class frequency 
subset1['Class'].value_counts().plot(kind='barh')
plt.title('Disease Class on BRFSS')    

## find the class frequency 
subset1['Topic'].value_counts().plot(kind='barh')
plt.title('Disease Topic on BRFSS')   

## choose the 2014 year
subset_2014 = subset1[subset1['Year']== '2014']
subset_2014.groupby('Class')['Location'].value_counts()

## choose the chronic health class
subset_2014_chronic = subset_2014[subset_2014['Class']== 'Chronic Health Indicators']
subset_2014_chronic.groupby('Topic')['Location'].value_counts()
sub = subset_2014_chronic[subset_2014_chronic['Response']== 'Yes']

sub['Data_Value'] = sub['Data_Value'].astype('float')
sub['Data_Value'].dtypes
sub.groupby(['Topic', 'Location'])['Data_Value'].quantile(0.5)

sub.groupby('Topic')['Data_Value'].mean().plot(kind = 'barh')
plt.title('Disease Topic on BRFSS d based on the data value mean')
plt.xlabel('Data Value mean')

sub.groupby('Break_Out')['Data_Value'].mean().plot(kind = 'barh')
plt.title('Break Out Type on BRFSS based on the data value mean')
plt.xlabel('Data Value mean')
