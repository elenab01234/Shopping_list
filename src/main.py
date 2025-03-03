import pandas as pd
import streamlit as st
from sqlalchemy.util import NoneType
from models import ShoppingListDb


if 'df' not in st.session_state:
    all_items = ShoppingListDb.get_all_items()
    if all_items == NoneType:
        data = []
    else:
        data = [item.to_dict() for item in ShoppingListDb.get_all_items()]
    st.session_state.df = pd.DataFrame(
        columns=["Item", "Price", "Quantity", "Bought", "Remove", "Category"],
        data = data
    )

with st.sidebar:
    st.header("Add Item to Shopping List")
    categ_list = ShoppingListDb.get_all_categories()
    category_options = [categ.Category for categ in categ_list]
    category = st.selectbox("Select Category", category_options)

    item_name = st.text_input("Item Name")
    price = st.number_input("Price", min_value=0.0, step=1.0)
    quantity = st.number_input("Quantity", min_value=1.0, step=1.0)
    submit_button = st.button(label="Add Item")

    # st.sidebar.image(f'{WORK_DIR}/src/shopping-trolley.jpg')

    if submit_button:
        new_item = pd.DataFrame(
            {"Item": [item_name],
             "Price": [price],
             "Quantity": [quantity],
             "Bought": [False],
             "Remove": [False],
             "Category": [category]
             }
        )
        st.session_state.df = pd.concat([st.session_state.df, new_item], ignore_index=True)
        st.sidebar.success(f"Added {item_name} to the shopping list!")

st.title("Shopping List")


col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 1, 1])
with col1:
    st.write("**Item**")
with col2:
    st.write("**Price**")
with col3:
    st.write("**Quantity**")
with col4:
    st.write("**Bought**")
with col5:
    st.write("**Remove**")


categories = st.session_state.df['Category'].unique()


for category in categories:
    st.write(f"**{category}**")

    category_df = st.session_state.df[st.session_state.df['Category'] == category]


    updated_rows = []
    for index, row in category_df.iterrows():
        col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 1, 1])

        with col1:
            item_text = st.text_input(" ", value=row['Item'], key=f"item_{index}",
                                      disabled=True, label_visibility="collapsed")

        with col2:
            price_input = st.number_input(" ", value=row['Price'], step = 1.0, key=f"price_{index}",
                                          label_visibility="collapsed")

        with col3:
            quantity_input = st.number_input(" ", value=row['Quantity'], step = 1.0, key=f"quantity_{index}",
                                             label_visibility="collapsed")

        with col4:
            bought_state = st.checkbox(" ", value=row['Bought'], key=f"checkbox_{index}", label_visibility="collapsed")

        with col5:
            remove_state = st.checkbox(" ", value=row['Remove'], key=f"remove_{index}", label_visibility="collapsed")

        updated_rows.append((index, item_text, bought_state, price_input, quantity_input, remove_state))


    for index, item_text, bought_state, price_input, quantity_input, remove_state in updated_rows:
        st.session_state.df.at[index, 'Bought'] = bought_state
        st.session_state.df.at[index, 'Price'] = price_input
        st.session_state.df.at[index, 'Quantity'] = quantity_input
        st.session_state.df.at[index, 'Remove'] = remove_state

    st.session_state.df = st.session_state.df[st.session_state.df['Remove']==False]


total_button = st.button(label="Total price (bought items)")
if total_button:
    bought_items = st.session_state.df[st.session_state.df['Bought'] == True]
    total_price_bought = (bought_items['Price'] * bought_items['Quantity']).sum()
    st.text_input(" ", value=f"{total_price_bought:.2f}", disabled=True, label_visibility="collapsed")


ShoppingListDb.save_items(st.session_state.df)
