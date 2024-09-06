"""
Dream Narratives Page
=====================

This script displays the user's dream narratives in a table format with sorting options, 
a search feature, and narrative management options including deletion.
"""

import pandas as pd
import streamlit as st

from components import auth
from components.api import delete_narrative, get_user_narratives

### --- Page Configuration --- ###

st.set_page_config(page_title="Dream Narratives", page_icon="📚")
st.markdown("# 📚 Dream Narratives")
st.sidebar.header("Dream Narratives")

# Check authentication
if not st.session_state.get("authenticated", False):
    auth.set_st_state_vars()

# Manage mode
if 'manage_mode' not in st.session_state:
    st.session_state.manage_mode = False
if 'delete_stage' not in st.session_state:
    st.session_state.delete_stage = 0
if 'selected_narratives' not in st.session_state:
    st.session_state.selected_narratives = []
if 'deletion_performed' not in st.session_state:
    st.session_state.deletion_performed = False

# Add login/logout button
if st.session_state.get("authenticated", False):
    auth.button_logout()
else:
    auth.button_login()
    st.stop()  # Stop execution if not authenticated

### --- Narrative Management --- ###

def get_narratives_dataframe(user_id):
    """
    Retrieves the user's dream narratives and returns them as a pandas DataFrame.

    Args:
        user_id (str): The ID of the user (email).

    Returns:
        pd.DataFrame or None: A DataFrame containing the narratives or None if no narratives are found.
    """
    narratives = get_user_narratives(user_id)
    if not narratives:
        st.info("You don't have any dream narratives yet.")
        return None
    
    df = pd.DataFrame(narratives)
    df['creation_date'] = pd.to_datetime(df['date']).dt.date
    df = df.rename(columns={
        'session_id': 'Narrative Name',
        'creation_date': 'Creation Date'
    })
    return df

def toggle_manage_mode():
    st.session_state.manage_mode = not st.session_state.manage_mode
    st.session_state.delete_stage = 0
    st.session_state.selected_narratives = []
    st.session_state.deletion_performed = False

def set_delete_stage(stage):
    st.session_state.delete_stage = stage

def update_selected_narratives():
    st.session_state.selected_narratives = st.session_state.multiselect_narratives

def manage_narratives(df, user_id):
    st.write("Select narratives to manage:")
    st.multiselect(
        "Select narratives",
        options=df['Narrative Name'].tolist(),
        key="multiselect_narratives",
        on_change=update_selected_narratives
    )

    if st.session_state.selected_narratives:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("View Narrative"):
                st.info("View Narrative functionality not implemented yet.")
        with col2:
            handle_deletion(user_id)

def handle_deletion(user_id):
    if st.session_state.delete_stage == 0:
        if st.button("Delete Selected Narratives", on_click=set_delete_stage, args=(1,)):
            pass
    elif st.session_state.delete_stage == 1:
        st.write("Are you sure you want to delete the selected narratives? This action is permanent.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Confirm Delete", key="confirm_delete", on_click=set_delete_stage, args=(2,)):
                pass
        with col2:
            if st.button("Cancel", key="cancel_delete", on_click=set_delete_stage, args=(0,)):
                pass
    
    if st.session_state.delete_stage == 2:
        perform_deletion(st.session_state.selected_narratives, user_id)
        st.session_state.deletion_performed = True
        set_delete_stage(0)

def perform_deletion(selected_narratives, user_id):
    deleted_narratives = []
    st.write("Deleting narratives...")
    for narrative in selected_narratives:
        try:
            result = delete_narrative(user_id, narrative)
            if result:
                if 'error' in result and 'No items found' in result['error']:
                    # This likely means the narrative was successfully deleted
                    deleted_narratives.append(narrative)
                    st.success(f"Successfully deleted narrative: {narrative}")
                elif 'message' in result and 'Successfully deleted narrative' in result['message']:
                    deleted_narratives.append(narrative)
                    st.success(f"Successfully deleted narrative: {narrative}")
                    st.rerun()
                else:
                    st.error(f"Unexpected response when deleting narrative '{narrative}'. Response: {result}")
            else:
                st.error(f"Failed to delete narrative '{narrative}'. No response received.")
        except Exception as e:
            st.error(f"An error occurred while deleting narrative '{narrative}': {str(e)}")
    
    if deleted_narratives:
        st.success(f"Successfully deleted {len(deleted_narratives)} narrative(s).")
    else:
        st.warning("No narratives were deleted.")

### --- Search and Sort --- ###

def search_and_sort_narratives(df):
    search_term = st.text_input("Search narratives by name:", "")
    if search_term:
        df = df[df['Narrative Name'].str.contains(search_term, case=False, na=False)]

    sort_by = st.selectbox("Sort by:", ["Creation Date", "Narrative Name"])
    sort_order = st.radio("Sort order:", ["Ascending", "Descending"])

    if sort_by == "Creation Date":
        df = df.sort_values("timestamp", ascending=(sort_order == "Ascending"))
    else:
        df = df.sort_values("Narrative Name", ascending=(sort_order == "Ascending"))

    return df

### --- Main App --- ###

def main():
    if st.session_state.get("authenticated", False):
        user_id = st.session_state.get("user_email", "")
        
        if st.session_state.deletion_performed:
            st.session_state.deletion_performed = False
            st.rerun()
        
        df = get_narratives_dataframe(user_id)
        
        if df is not None:
            st.button(
                "Manage narratives" if not st.session_state.manage_mode else "Exit manage mode",
                on_click=toggle_manage_mode
            )

            if st.session_state.manage_mode:
                manage_narratives(df, user_id)
            else:
                df = search_and_sort_narratives(df)

            st.dataframe(df[['Narrative Name', 'Creation Date']])
    else:
        st.write("Please log in to view your dream narratives.")

if __name__ == "__main__":
    main()