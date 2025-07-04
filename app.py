import pandas as pd
import streamlit as st
import plotly.express as px
import folium
from streamlit_folium import st_folium


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
    

    # Select y variable for the boxplot
    y_variable = st.selectbox("Select Y Variable", ['grain_kg_ha','stalk_kg_ha', 'stand_pl_ha'])

    # Generate boxplot using seaborn
    # Optional: orientation toggle
    orientation = st.sidebar.radio("Boxplot Orientation:",["Vertical","Horizontal"])

    # Build interactive boxplot using Plotly
    if orientation == "Vertical":
        fig = px.box(
            filtered_data,
            x='treatment',
            y=y_variable,
            color='treatment',
            color_discrete_sequence=px.colors.sequential.Viridis,
            points="all",
            hover_data=filtered_data.columns
        )
    else:
        fig = px.box(
            filtered_data,
            x=y_variable,
            y='treatment',
            color='treatment',
            color_discrete_sequence=px.colors.sequential.Viridis,
            orientation="h",
            points="all",
            hover_data=filtered_data.columns
        )

    # Adjust individual box widths (in categorical units)
    fig.update_traces(width=0.6)

    fig.update_layout(
        title=f"Interactive Boxplot of {y_variable} by Treatment",
        boxmode="group"
    )

    # Display in Streamlit
    st.plotly_chart(fig, use_container_width=True)

    # display the data
    if st.sidebar.checkbox("Show raw data"):
        st.write(f"Data for {crop} in {year} with {trial_type} in {village}:")
        # Display the filtered data
        st.dataframe(filtered_data)
    
    # Display the map
    # Display map if latitude/longitude present and box checked
    if st.sidebar.checkbox("Show the map"):
        if "latitude" in filtered_data.columns and "longitude" in filtered_data.columns:
            map_data = filtered_data.dropna(subset=["latitude", "longitude"]).drop_duplicates()
            if not map_data.empty:
                # Initialize folium map at mean coordinate
                center = [map_data["latitude"].mean(), map_data["longitude"].mean()]
                m = folium.Map(location=center, zoom_start=2)
                for _, row in map_data.iterrows():
                    folium.CircleMarker(
                        location=[row["latitude"], row["longitude"]],
                        radius=5,
                        color="blue",
                        fill=True,
                        fill_opacity=0.7
                        #popup=f"{category_feature}: {row[category_feature]}\n{numeric_feature}: {row[numeric_feature]}"
                    ).add_to(m)
                st_folium(m, width=700, height=500)
            else:
                st.warning("No valid latitude/longitude data to display.")  
        else:
            st.warning("Latitude/longitude columns not found in data.")

    


if __name__ == "__main__":
    main()
    

