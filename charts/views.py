from io import StringIO
from django.shortcuts import render
import matplotlib.pyplot as plt
import math
import numpy as np
from django.core.files.storage import FileSystemStorage
import pandas as pd
import os

def input(request):
     if request.method=='POST':
        selected_inp = request.POST['select_type']
        if selected_inp == 'manual':
            manual_choice='enabled'
            excel_choice = 'disabled'
            return render(request,'chartsinput.html',{'manual_choice':manual_choice,'excel_choice':excel_choice})
        elif selected_inp == 'excel':
            manual_choice='disabled'
            excel_choice = 'enabled'
            return render(request,'chartsinput.html',{'manual_choice':manual_choice,'excel_choice':excel_choice})
     manual_choice='disabled'
     excel_choice = 'disabled'
     return render(request,'chartsinput.html',{'manual_choice':manual_choice,'excel_choice':excel_choice})


def num_to_radians(cat_4,cat_5,cat_6,cat_7,cat_8,cat_9):
    total_values = max(cat_4,cat_5,cat_6,cat_7,cat_8,cat_9)
    rad_cat4 = (cat_4*360)/total_values
    rad_cat5 = (cat_5*360)/total_values
    rad_cat6 = (cat_6*360)/total_values
    rad_cat7 = (cat_7*360)/total_values
    rad_cat8 = (cat_8*360)/total_values
    rad_cat9 = (cat_9*360)/total_values

    return rad_cat4,rad_cat5,rad_cat6,rad_cat7,rad_cat8,rad_cat9




def output(request):
    if request.method=='POST':
        cat_1=int(request.POST['cat-1'])
        cat_2=int(request.POST['cat-2'])
        cat_3=int(request.POST['cat-3'])
        cat_4=int(request.POST['cat-4'])
        cat_5=int(request.POST['cat-5'])
        cat_6=int(request.POST['cat-6'])
        cat_7=int(request.POST['cat-7'])
        cat_8=int(request.POST['cat-8'])
        cat_9=int(request.POST['cat-9'])
        #pie chart
        total = np.array([cat_1,cat_2,cat_3])
        labels = ['cat_1','cat_2','cat_3']
        fig = plt.figure()
        plt.pie(total,labels=labels)
        imgdata = StringIO()
        fig.savefig(imgdata,format='svg')
        imgdata.seek(0)
        data = imgdata.getvalue()
        #------------

        #Radial bar guage
        rad_cat4,rad_cat5,rad_cat6,rad_cat7,rad_cat8,rad_cat9 = num_to_radians(cat_4,cat_5,cat_6,cat_7,cat_8,cat_9)
        radial_fig=plt.figure()
        ax=plt.subplot(projection='polar')
        ax.barh(0,math.radians(rad_cat4))
        ax.barh(1,math.radians(rad_cat5))
        ax.barh(2,math.radians(rad_cat6))
        ax.barh(3,math.radians(rad_cat7))
        ax.barh(4,math.radians(rad_cat8))
        ax.barh(5,math.radians(rad_cat9))

        ax.yaxis.grid(False)
        ax.xaxis.grid(False)
        #plt.show()
        imgdata = StringIO()
        radial_fig.savefig(imgdata,format='svg')
        imgdata.seek(0)
        radial_data = imgdata.getvalue()
        return render(request,'chartsoutput.html',{'graph':data,'radial':radial_data})
    
    return render(request,'chartsoutput.html')

def excel_output(request):
    if request.method == 'POST' and (request.FILES['pie'] or request.FILES['radial']):
        pie_data = request.FILES['pie']
        radial_data = request.FILES['radial']
        pie_file_path = 'C:/Users/Ganesh vamsi/MY PROJECTS/novartis_casestudy/novartis/exceldata/pie_chart_data.xlsx'
        #radial_file_path = 'C:/Users/Ganesh vamsi/MY PROJECTS/novartis_casestudy/novartis/exceldata/radial_data.xlsx'
    
        fs = FileSystemStorage()
        pie_file = fs.save(pie_file_path,pie_data)
        #radial_file = fs.save(radial_file_path,radial_data)

        #PIE CHART
        pie_values=[]
        pie_category=[]
        pie_file = pd.read_excel(pie_file)
        print('##################1')
        for j in range(len(pie_file)):
            title = pie_file['Pie category'][j]
            values = str(pie_file['Share'][j])       
            pie_category.append(title)
            pie_values.append(int(values))
            
        
        total = np.array(pie_values)
        labels = pie_category
        fig = plt.figure()
        plt.pie(total,labels=labels)
        imgdata = StringIO()
        fig.savefig(imgdata,format='svg')
        imgdata.seek(0)
        pie_data = imgdata.getvalue()
        #pie chart end

        #Radial guage
        radial_values=[]
        radial_category=[]
        index_no = []
        radial_fig=plt.figure()

        for j in range(len(pie_file)):
            title = pie_file['Pie category'][j]
            values = str(pie_file['Share'][j]) 
            index_no.append(j)      
            radial_category.append(title)
            radial_values.append(int(values))
        ax=plt.subplot(projection='polar')

        #--------------converting into radians
        values_in_rads=[]

        for val in radial_values:
            new_val = (val*360)/max(radial_values)
            values_in_rads.append(new_val)


        for i,j in zip(index_no,values_in_rads):
            ax.barh(i,math.radians(int(j)))
        ax.yaxis.grid(False)
        ax.xaxis.grid(False)
        imgdata = StringIO()
        radial_fig.savefig(imgdata,format='svg')
        imgdata.seek(0)
        radial_data = imgdata.getvalue()
        os.remove(pie_file_path,dir_fd=None)
        return render(request,'chartsoutput.html',{'graph':pie_data,'radial':radial_data})
    
    return render(request,'chartsoutput.html')
