import pandas as pd
import streamlit as st
import altair as alt

# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv('data/crop_mix_intensification.csv')
    return df

# Main function to run the Streamlit app
def main():
    st.title("Crop Mix Intensification Dashboard")
    
    # Load the data
    df = load_data()
    

    # Crop to sidebar
    crop = st.sidebar.selectbox("Select Crop", df['crop'].unique())
    # Filter data based on selected crop
    filtered_data = df[df['crop'] == crop]


    # Add year to sidebar
    year = st.sidebar.selectbox("Select Year", filtered_data['year'].unique())
    # Filter data based on selected year
    filtered_data = filtered_data[filtered_data['year'] == year]


    # Add trial_type to sidebar
    trial_type = st.sidebar.selectbox("Select Trial Type", filtered_data['trial_type'].unique())
    # Filter data based on selected trial type
    filtered_data = filtered_data[filtered_data['trial_type'] == trial_type]


    # add village to sidebar
    village = st.sidebar.selectbox("Select Village", filtered_data['village'].unique())
    # Filter data based on selected village
    filtered_data = filtered_data[filtered_data['village'] == village]
    st.write(f"Data for {crop} in {year} with {trial_type} in {village}:")
    st.dataframe(filtered_data)

    # Select y variable for the boxplot
    y_variable = st.selectbox("Select Y Variable", ['grain_kg_ha.trt','stalk_kg_ha.trt', 'stand_pl_ha.trt'])

    # Generate a boxplot using altair 

    boxplot = alt.Chart(filtered_data).mark_boxplot(extent='min-max').encode(
        x='treatment',
        y=y_variable
    ).interactive()

    # Display the boxplot
    st.altair_chart(boxplot, use_container_width=True)

    


if __name__ == "__main__":
    main()
    

