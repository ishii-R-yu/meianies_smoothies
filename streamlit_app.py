# Import python packages
import streamlit as st
import pandas as ps
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f"🥤Customize Your Smoothie🥤")
st.write(
  """choose the fruits you want in your custom Smoothie!
  """
)


name_on_order = st.text_input('Name on Smoothie')
st.write('the name on your smoothie will be',name_on_order)

# st.write("Your favorite fruit is:", option)

cnx= st.connection("snowflake")
session=cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()
pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string =''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
      
        #st.write('The search value for ', fruit_chosen,' is ', search_on, '.') 
        st.subheader(fruit_chosen + 'Nutrition Information')
        fruityvicefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+search_on)
        fv_df = st.dataframe(data=fruityvicefroot_response.json(),use_container_width=True)

    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER,ORDER_FILLED)
            values ('""" + ingredients_string + """','""" + name_on_order + """','False')"""
    time_to_insert = st.button('Submit Order')
    if time_to_insert: 
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

