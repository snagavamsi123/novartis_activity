function validating()
    {
    
        contact_name=document.getElementById('c_name').value;
        contact_no=document.getElementById('c_no').value;
        email=document.getElementById('email').value;
        address=document.getElementById('address').value;
       
        var contact_name_regx=/^([a-z A-Z]{3,15})$/
        var contact_no_regx=/^([0-9]{10,12})?$/
        var mail_regx=/^([a-z A-Z 0-9\.-]+)@([a-z A-Z]{2,8})\.([a-z A-Z]{2,8})([\. a-z A-Z]{2,8})?$/;
        

        //This is for first name mandatory warning
        if(contact_name.trim().length<1 || contact_name_regx.test(contact_name) != true)
        {
            ip1.style.border = 'solid 3px red'; 
            if(f_name.trim().length<1)
            {   
                document.getElementById('first_name_warning').innerHTML='* First Name must no be empty'; 
            }
            else if(f_name.trim().length<=4)
            {
                document.getElementById('first_name_warning').innerHTML='* Name length must be greater than 3'; 
            }
            else{
                document.getElementById('first_name_warning').innerHTML= '* Numbers and special characters are not allowed.Name must only contain alphabets.'; 
            }

        return false    
        }
       else if(contact_no_regx.test(contact_no) != true)
        {
            ip2.style.border = 'solid 3px red'; 
            document.getElementById('last_name_warning').innerHTML= '* Numbers and special characters are not allowed. Name must only contain alphabets.'; 
            return false    
            }


        //This is for email mandatory warning    
        else if(email_id.trim().length<1 || mail_regx.test(email_id) != true)
        {
            
            if(email_id.trim().length<1) //checking email id empty or not
            {   ip3.style.border = 'solid 3px red'; 
                document.getElementById('email_warning').innerHTML='* Email must no be empty';
                return false
            }

            else    //checking valid email or not
            {
                ip3.style.border = 'solid 3px red'; 
                document.getElementById('email_warning').innerHTML= 'Not a valid mail';
                return false
            }

        }

    }