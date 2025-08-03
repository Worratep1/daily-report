#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
# import tabulate as ta


# In[2]:


df = pd.read_excel("daily_reports/Daily report_20250115_Pattama_Sooksan.xlsx")
# print(df)
df.head()


# In[3]:


df = pd.read_excel("daily_reports/Daily report_20250115_Raewwadee_Jaidee.xlsx") 
# print(df)
df.head()


# In[4]:


df_new = pd.read_excel("New Employee_YYYYMM.xlsx")
# print(df)
df_new.head()


# In[5]:


passed_list = []

for file in os.listdir("daily_reports"):
    if file.endswith(".xlsx"):
        df = pd.read_excel(os.path.join("daily_reports", file))

        # print(f" ไฟล์: {file}")
        # print(" คอลัมน์ในไฟล์นี้:", df.columns)

        parts = file.replace(".xlsx", "").split("_")
        team_member = f"{parts[2]} {parts[3]}"
        # print(team_member)

        #คัดเฉพาะแถวที่มีสถานะ "Pass"
        passed = df[df['Status'] == 'Pass']

        passed["Team Member"] = team_member

        passed_list.append(passed)

df_passed = pd.concat(passed_list, ignore_index=True) #คัดเฉพาะแถวที่มีสถานะ "Pass"
df_passed.head()



# In[6]:


df_passed.rename(columns={
    "Candidate Name": "Employee Name"}, inplace=True)
df_passed.head()


# In[7]:


df_merge = pd.merge(df_new, df_passed, on="Employee Name")
df_merge.head()


# In[8]:


df_result = df_merge[["Employee Name", "Join Date", "Role_x", "Team Member"]].copy()
df_result.rename(columns={ "Role_x":"Role"}, inplace=True)
df_result.head()


# In[12]:


# ฟังก์เเสดงผล Dashboard
st.set_page_config(page_title="Team Member Overview",layout="wide")
st.title("Dashboard: Team Member Overview")

# แสดงตารางผลลัพธ์
st.dataframe(df_result)

#เเสดงกราฟแท่ง
# เลือกตำแหน่ง (Role) 
roles = df_result['Role'].unique()
selected_role = st.selectbox(" Select Position (Role)", options=['All'] + list(roles))

#  กรองตามวันที่เริ่มงาน
df_result['Join Date'] = pd.to_datetime(df_result['Join Date'])  # แปลงเป็น datetime ก่อน
min_date = df_result['Join Date'].min()
max_date = df_result['Join Date'].max()

selected_date = st.date_input(" Select Join Date ", value=min_date, min_value=min_date, max_value=max_date)

# กรองข้อมูลตามตำแหน่งและวันที่
filtered_df = df_result.copy()

if selected_role != 'All':
    filtered_df = filtered_df[filtered_df['Role'] == selected_role]

filtered_df = filtered_df[filtered_df['Join Date'] >= pd.to_datetime(selected_date)]
filtered_df['Join Date'] = filtered_df['Join Date'].dt.strftime('%Y-%m-%d')


# --- แสดงตาราง ---
st.write("Filtered Results:")
st.dataframe(filtered_df)

# --- แสดงกราฟแท่ง ---
if not filtered_df.empty:
    role_counts = filtered_df['Role'].value_counts().reset_index()
    role_counts.columns = ['Role', 'Count']
    fig = px.bar(role_counts, x='Role', y='Count', color='Role',
                 title='Graph of number of employees in each position')
    fig.update_yaxes(dtick=1)
    st.plotly_chart(fig)
else:
    st.warning("ไม่มีข้อมูลที่ตรงกับเงื่อนไขที่เลือก")




