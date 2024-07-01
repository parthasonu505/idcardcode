import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
from io import BytesIO
import mysql.connector
import ftplib
import os
# Load the Excel file
st.set_page_config(layout="wide")

ipcode=""
ipname=""
ipsection=''
ipclass=''
r1c1,_,r1c2 = st.columns([4,0.5,4])
section_set=()
class_set=()
if 'go' not in st.session_state:
    st.session_state.go = False
if 'df' not in st.session_state:
    st.session_state.df = None
def change_go():
    st.session_state.go = True

with r1c1:
    st.title('Data Entry')
    school_name = st.text_input("Please Enter The School Code", "JH2010")
    uploaded_file = st.file_uploader("Choose a file", type = 'xlsx')
    
    if uploaded_file is not None:
        if st.session_state.df is None:
            print("****************hi*****************")
            st.session_state.df = pd.read_excel(uploaded_file, sheet_name='Sheet1')
        section_set=tuple(set(list(st.session_state.df['Section'])))
        class_set=tuple(set(list(st.session_state.df['Class'])))
        uploaded_file=None
        
        if 'photo_taken' not in st.session_state.df.columns:
            st.session_state.df['photo_taken'] = 'No'
    r1lc1,r1lc2 = st.columns([2,2])
    with r1lc1:
        class_name=st.selectbox( "Select Class",class_set)
        Section_name= st.selectbox( "Select Section",section_set)
        
        if Section_name is not None:
            temp_name= tuple(set(list(st.session_state.df[(st.session_state.df['Section'] == Section_name)&(st.session_state.df['Class'] == class_name)]["Name"])))
            select_name=st.selectbox( "Select Name",temp_name)
    with r1lc2:
        roll_no = st.text_input('Enter Roll Number')
    
    cb0,cb1,cb2,_=st.columns([1,1,1,3])
    with cb2:
        st.button('Go', on_click=change_go)
    with cb1:
        next=st.button('Next >')
    with cb0:
        prev=st.button('< Prev')

    if(st.session_state.go):
        option = st.selectbox('How would you like submit photo',('Capture', 'Upload'))
        if(option == 'Capture'):
            picture = st.camera_input("Take a picture")
        else:
            picture = st.file_uploader("Upload a picture", type = 'jpg')
            if picture:
                st.image(picture, caption='Uploaded Photo')
 
if st.session_state.go:
    # Filter the dataframe based on the input
    if(len(roll_no)):
        
        filtered_df = st.session_state.df[(st.session_state.df['Section'] == Section_name) & (st.session_state.df['Roll'] == int(roll_no))]
        index=st.session_state.df.index[(st.session_state.df['Section'] == Section_name) & (st.session_state.df['Roll'] == int(roll_no))].tolist()
    else:
        filtered_df = st.session_state.df[(st.session_state.df['Section'] == Section_name) & (st.session_state.df['Name'] == select_name)]
        index=st.session_state.df.index[(st.session_state.df['Section'] == Section_name) & (st.session_state.df['Name'] == select_name)].tolist()
    
    if not filtered_df.empty:
        with r1c2:
            st.title('Your Data')
            r2c1,r2c2 = st.columns([2,2])
            # Display the data in text fields
            with r2c1:
                ipname=st.text_input('Name', filtered_df['Name'].values[0])
                ipaddress=st.text_input('Address', filtered_df['Address'].values[0])
                ipphone=st.text_input('Phone', filtered_df['Phone'].values[0])
                ipclass=st.text_input('Class', filtered_df['Class'].values[0])
                ipsection=st.text_input('Section', filtered_df['Section'].values[0])
                iproll=st.text_input('Roll', filtered_df['Roll'].values[0])
                if not picture:
                    ipphototaken=st.text_input('Photo Taken', filtered_df['photo_taken'].values[0])
                else:
                    ipphototaken=st.text_input('Photo Taken', "Yes")
            with r2c2:
                ipcode=st.text_input('Code', filtered_df['Code'].values[0])
                if picture:
                    ippic=st.text_input('Picture', f"{school_name}_{ipclass}_{ipsection}_{ipcode}_{ipname}.jpg")
                else:
                    ippic=st.text_input('Picture', filtered_df['Picture'].values[0])
                ipgurno=st.text_input('Guardian Number', filtered_df['Guardian Number'].values[0])
                ipfn=st.text_input('Father\'s Name', filtered_df['Father\'s Name'].values[0])
                inmn=st.text_input('Mother\'s Name', filtered_df['Mother\'s Name'].values[0])
                inbg=st.text_input('Blood Group', filtered_df['Blood Group'].values[0])
                indob=st.text_input('DOB', str(filtered_df['DOB'].values[0]))
            submit=st.button("submit", type="primary")
            if picture:
                st.session_state.df.loc[st.session_state.df.Code == ipcode, 'Picture'] =f"{school_name}_{ipclass}_{ipsection}_{ipcode}_{ipname}.jpg"
                ippic=f"{school_name}_{ipclass}_{ipsection}_{ipcode}_{ipname}.jpg"
                print("Picture name: ",ippic)

                session = ftplib.FTP('ftp.digidemy.in','u669719505.partha','Partha123$#@')
                session.storbinary(f'STOR {ippic}', picture)
                session.quit()
                #with open(os.path.join("Data",ippic),"wb") as f: 
                    #f.write(picture.getvalue())

                
                # with open(f"Photo/{ipclass}/{ipsection}/{ipcode}_{ipname}.jpg", 'wb') as f: 
                #     f.write(picture.getvalue())
        if(submit):
            st.session_state.df['Name'][index]=ipname
            st.session_state.df['Address'][index]=ipaddress
            st.session_state.df['Phone'][index]=ipphone
            st.session_state.df['Class'][index]=ipclass
            st.session_state.df['Section'][index]=ipsection
            st.session_state.df['Roll'][index]=iproll
            st.session_state.df['photo_taken'][index]=ipphototaken
            st.session_state.df['Code'][index]=ipcode
            st.session_state.df['Picture'][index]=ippic
            st.session_state.df['Guardian Number'][index]=ipgurno
            st.session_state.df['Father\'s Name'][index]=ipfn
            st.session_state.df['Mother\'s Name'][index]=inmn
            st.session_state.df['Blood Group'][index]=inbg
            st.session_state.df['DOB'][index]=indob
            st.session_state.df.to_excel(f"Data/temp/{school_name}_{ipclass}_data.xlsx")
            #df = pd.read_excel(f"Data/temp/{school_name}_{ipclass}_data.xlsx", sheet_name='Sheet1')

            myconn = mysql.connector.connect(host = "193.203.184.80", user = "u669719505_school",passwd = "+=I^|BhLc7D", database = "u669719505_school")  
            cur = myconn.cursor()
            del_query = f"""DELETE FROM schooltest WHERE Code ='{ipcode}';"""
            # Execute the query
            cur.execute(del_query)
            
            insert_query = f"""INSERT INTO schooltesttable (OrgId,Name, Address, Phone, Class, Section, Roll, photo_taken, Code, Picture, Guardian_Number, Fathers_Name, Mothers_Name, Blood_Group,DOB)VALUES ('{school_name}','{ipname}', '{ipaddress}', '{ipphone}', '{ipclass}', '{ipsection}', '{iproll}', '{ipphototaken}', '{ipcode}', '{ippic}', '{ipgurno}', '{ipfn}', '{inmn}', '{inbg}', '{indob}');"""
            # Execute the query
            cur.execute(insert_query)
            
            # Commit the transaction
            myconn.commit() 
            cur.close()
            st.success('Data Is Successfully Updated', icon="✅")
            st.session_state.go=False
            
    else:
        with r1c2:
            st.title('Your Data')
            r2c1,r2c2 = st.columns([2,2])
            
            with r2c1:
                st.text_input('Name', '')
                st.text_input('Address', '')
                st.text_input('Phone', '')
                st.text_input('Class', '')
                st.text_input('Section', '')
                st.text_input('Roll', '')
                st.text_input('Photo Taken', '')
            with r2c2:
                st.text_input('Code', '')
                st.text_input('Picture', '')
                st.text_input('Guardian Number','')
                st.text_input('Father\'s Name', '')
                st.text_input('Mother\'s Name', '')
                st.text_input('Blood Group', '')
                st.text_input('DOB', str(''))
        st.success('No Data Found', icon="❌")
else:
    with r1c2:
        st.title('Your Data')
        r2c1,r2c2 = st.columns([2,2])
        with r2c1:
            st.text_input('Name', '')
            st.text_input('Address', '')
            st.text_input('Phone', '')
            st.text_input('Class', '')
            st.text_input('Section', '')
            st.text_input('Roll', '')
            st.text_input('Photo Taken', '')
        with r2c2:
            st.text_input('Code', '')
            st.text_input('Picture', '')
            st.text_input('Guardian Number','')
            st.text_input('Father\'s Name', '')
            st.text_input('Mother\'s Name', '')
            st.text_input('Blood Group', '')
            st.text_input('DOB', str(''))
