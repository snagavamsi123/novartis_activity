from django.shortcuts import redirect, render
from .models import ContactBook
from django.urls import reverse
import pandas as pd
import os
import io
from django.core.files.storage import FileSystemStorage
import re

# Create your views here.

def home(request):
    return render(request,'index.html')


def addcontact(request):
    if request.method=='POST':
        selected_inp = request.POST['select_type']
        if selected_inp == 'manual':
            manual_choice='enabled'
            excel_choice = 'disabled'
            return render(request,'newcontact.html',{'manual_choice':manual_choice,'excel_choice':excel_choice})
        elif selected_inp == 'excel':
            manual_choice='disabled'
            excel_choice = 'enabled'
            return render(request,'newcontact.html',{'manual_choice':manual_choice,'excel_choice':excel_choice})

    manual_choice='disabled'
    excel_choice = 'disabled'
    return render(request,'newcontact.html',{'manual_choice':manual_choice,'excel_choice':excel_choice})

def addmanually(request):
    if request.method=='POST':

        mail_regex = '^[a-z0-9]+[\._]?[ a-z0-9]+[@]\w+[. ]\w{2,3}$'
        contact_name = request.POST['contact_name']
        contact_no = request.POST['contact_no']
        mail_id = request.POST['email']
        address = request.POST['address']
        str_no = [char for char in str(contact_no)]

        if len(contact_name)<2:
            manual_choice='enabled'
            excel_choice = 'disabled'
            context =  {'manual_choice':manual_choice,
                    'excel_choice':excel_choice,
                    'name_info' : 'length of Name must greater than 2',
                    'name':contact_name,
                    'number':contact_no,
                    'mail':mail_id,
                    'address':address
                    }
            return render(request,'newcontact.html',context)
        
        elif (len(str_no)!=10 and int(contact_no).isdigit()):
            manual_choice='enabled'
            excel_choice = 'disabled'
            context =  {'manual_choice':manual_choice,
                    'excel_choice':excel_choice,
                    'no_info' : 'Provide proper No , number Must 10 or 12 digits',
                    'name':contact_name,
                    'number':contact_no,
                    'mail':mail_id,
                    'address':address}
            return render(request,'newcontact.html',context)
        elif not re.search(mail_regex,mail_id):
            manual_choice='enabled'
            excel_choice = 'disabled'
            context =  {'manual_choice':manual_choice,
                    'excel_choice':excel_choice,
                    'mail_info' : 'Provide proper Email',
                    'name':contact_name,
                    'number':contact_no,
                    'mail':mail_id,
                    'address':address}
            return render(request,'newcontact.html',context)
        elif address=='':
            manual_choice='enabled'
            excel_choice = 'disabled'
            context =  {'manual_choice':manual_choice,
                    'excel_choice':excel_choice,
                    'mail_info' : 'Provide proper address, address must not empty',
                    'name':contact_name,
                    'number':contact_no,
                    'mail':mail_id,
                    'address':address}
            return render(request,'newcontact.html',context)
            

        contacts_table = ContactBook(name=contact_name,number=contact_no,email=mail_id,address=address)
        contacts_table.save()

        manual_choice='enabled'
        excel_choice = 'disabled'

        
        context =  {'manual_choice':manual_choice,
                    'excel_choice':excel_choice,
                    'output_text' : 'Contact "'+ contact_name +'" saved Successfully',}
        return render(request,'newcontact.html',context)
        
    manual_choice='disabled'
    excel_choice = 'disabled'
    return render(request,'newcontact.html',{'manual_choice':manual_choice,'excel_choice':excel_choice})

def add_excel_data(request):
    if request.method == 'POST' and request.FILES['upload_file']:
        uploaded_file = request.FILES['upload_file']
        file_path = 'C:/Users/Ganesh vamsi/MY PROJECTS/novartis_casestudy/novartis/exceldata/contacts.xlsx'
        fs = FileSystemStorage()
        file = fs.save(file_path,uploaded_file)

        #file = pd.read_excel(file_path)

        file = pd.read_excel(file)
        for j in range(len(file)):
            contact_name = file['contact name'][j]
            contact_no = str(file['contact number'][j])
            mail_id = file['mail'][j]
            address = file['address'][j]

            #print(file['contact name'][j],file['contact number'][j],file['mail'][j],file['address'][j])
            contacts_table = ContactBook(name=contact_name,number=contact_no,email=mail_id,address=address)
            contacts_table.save()
        
        os.remove(file_path,dir_fd=None)
        manual_choice='disabled'
        excel_choice = 'enabled'

        
        context =  {'manual_choice':manual_choice,
                    'excel_choice':excel_choice,
                    'output_text' : 'Total "'+ str(len(file)) +'" Contacts  saved Successfully',}
        return render(request,'newcontact.html',context)

    manual_choice='disabled'
    excel_choice = 'disabled'
    return render(request,'newcontact.html',{'manual_choice':manual_choice,'excel_choice':excel_choice})





def contact_book(request):

    values = ContactBook.objects.raw('select * from novartisapp_contactbook')
    return render(request,'contactbook.html',{'values':values})

def delete(request,id):
    dlt=ContactBook.objects.get(id=id)
    dlt.delete()
    values = ContactBook.objects.raw('select * from novartisapp_contactbook')
    #return render(request,'contactbook.html',{'values':values})
    return redirect('/contacts')


def edit(request,id):
    if request.method=='POST':
        updated_name = request.POST['contact_name']
        updated_dno = request.POST['contact_no']
        updated_mail_id = request.POST['email']
        updated_address = request.POST['address']

        ContactBook.objects.filter(id=id).update(name=updated_name,number=updated_dno,email=updated_mail_id,address=updated_address)
        return redirect('/contacts')
 
    edit_contact = ContactBook.objects.get(id=id)
    return render(request,'edit.html',{'ContactBook':edit_contact})


'''
if not uploaded_file.name.endswith('.xlsx')

'''