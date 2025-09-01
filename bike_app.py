import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(
    page_title="🏍️ Motorcycle Analysis Dashboard",
    page_icon="🏍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load the data by running the main analysis
@st.cache_data
def load_bike_data():
    import subprocess
    import os
    
    # Run the main script to generate CSV
    subprocess.run(["python", "main.py"], capture_output=True)
    
    # Load the generated CSV
    df = pd.read_csv("faired_bikes_ratings_india_1to10L_aug2025.csv")
    return df

def main():
    st.title("🏍️ Motorcycle Analysis Dashboard")
    st.markdown("**Comprehensive analysis of motorcycles in India with performance ratings and value-for-money calculations**")
    
    # Load data
    df = load_bike_data()
    
    # Sidebar filters
    st.sidebar.header("🔧 Filters")
    
    # Price range filter
    price_range = st.sidebar.slider(
        "Price Range (₹ Lakh)",
        min_value=float(df["Price (₹ Lakh)"].min()),
        max_value=float(df["Price (₹ Lakh)"].max()),
        value=(float(df["Price (₹ Lakh)"].min()), float(df["Price (₹ Lakh)"].max())),
        step=0.5
    )
    
    # Segment filter
    segments = ["All"] + list(df["Segment"].unique())
    selected_segment = st.sidebar.selectbox("Segment", segments)
    
    # Filter data
    filtered_df = df[
        (df["Price (₹ Lakh)"] >= price_range[0]) & 
        (df["Price (₹ Lakh)"] <= price_range[1])
    ]
    
    if selected_segment != "All":
        filtered_df = filtered_df[filtered_df["Segment"] == selected_segment]
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["📊 Data Table", "📈 Interactive Charts", "🏆 Rankings"])
    
    with tab1:
        st.header("📊 Complete Motorcycle Database")
        st.markdown(f"**Showing {len(filtered_df)} motorcycles**")
        
        # Display sortable dataframe
        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Price (₹ Lakh)": st.column_config.NumberColumn(
                    "Price (₹ Lakh)",
                    format="₹%.2f"
                ),
                "Total score": st.column_config.NumberColumn(
                    "Total Score",
                    format="%.1f/60"
                ),
                "Total (out of 10)": st.column_config.NumberColumn(
                    "Total (out of 10)",
                    format="%.2f/10"
                ),
                "VFM score": st.column_config.NumberColumn(
                    "VFM Score",
                    format="%.2f/10"
                )
            }
        )
    
    with tab2:
        st.header("📈 Interactive Visualization")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # X-axis selection
            numeric_columns = [col for col in filtered_df.columns if filtered_df[col].dtype in ['float64', 'int64']]
            x_axis = st.selectbox(
                "Select X-axis",
                numeric_columns,
                index=numeric_columns.index("Price (₹ Lakh)") if "Price (₹ Lakh)" in numeric_columns else 0
            )
        
        with col2:
            # Y-axis selection
            y_axis = st.selectbox(
                "Select Y-axis",
                numeric_columns,
                index=numeric_columns.index("Total (out of 10)") if "Total (out of 10)" in numeric_columns else 1
            )
        
        # Color by segment
        color_by_segment = st.checkbox("Color by Segment", value=True)
        
        # Create the plot
        if color_by_segment:
            fig = px.scatter(
                filtered_df,
                x=x_axis,
                y=y_axis,
                color="Segment",
                hover_name="Bike",
                hover_data=["Price (₹ Lakh)", "Total (out of 10)", "VFM score"],
                title=f"{y_axis} vs {x_axis}",
                width=800,
                height=600
            )
        else:
            fig = px.scatter(
                filtered_df,
                x=x_axis,
                y=y_axis,
                hover_name="Bike",
                hover_data=["Price (₹ Lakh)", "Total (out of 10)", "VFM score"],
                title=f"{y_axis} vs {x_axis}",
                width=800,
                height=600
            )
        
        # Add reference lines and annotations
        x_median = filtered_df[x_axis].median()
        y_median = filtered_df[y_axis].median()
        x_75th = filtered_df[x_axis].quantile(0.75)
        y_75th = filtered_df[y_axis].quantile(0.75)
        
        # Add median reference lines
        fig.add_hline(y=y_median, line_dash="dash", line_color="gray", 
                     annotation_text=f"Median {y_axis}: {y_median:.2f}", 
                     annotation_position="top right")
        fig.add_vline(x=x_median, line_dash="dash", line_color="gray",
                     annotation_text=f"Median {x_axis}: {x_median:.2f}", 
                     annotation_position="top right")
        
        # Add 75th percentile lines for context
        if y_axis != x_axis:  # Only if different axes
            fig.add_hline(y=y_75th, line_dash="dot", line_color="green", opacity=0.7,
                         annotation_text=f"75th percentile: {y_75th:.2f}", 
                         annotation_position="bottom right")
            fig.add_vline(x=x_75th, line_dash="dot", line_color="green", opacity=0.7,
                         annotation_text=f"75th percentile: {x_75th:.2f}", 
                         annotation_position="bottom left")
        
        fig.update_layout(
            xaxis_title=x_axis,
            yaxis_title=y_axis,
            showlegend=color_by_segment
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Intelligent graph interpretation
        st.subheader("🧠 Graph Intelligence")
        
        # Analyze graph quadrants and provide insights
        def analyze_graph_regions(df, x_col, y_col):
            insights = []
            
            # Find bikes in different quadrants
            high_x_high_y = df[(df[x_col] > x_median) & (df[y_col] > y_median)]
            low_x_high_y = df[(df[x_col] <= x_median) & (df[y_col] > y_median)]
            high_x_low_y = df[(df[x_col] > x_median) & (df[y_col] <= y_median)]
            low_x_low_y = df[(df[x_col] <= x_median) & (df[y_col] <= y_median)]
            
            # Top performers in each quadrant
            if len(high_x_high_y) > 0:
                best_hx_hy = high_x_high_y.loc[high_x_high_y[y_col].idxmax()]
                insights.append(f"🏆 **Top-Right (Best Overall)**: {best_hx_hy['Bike']} excels in both {x_col} ({best_hx_hy[x_col]:.2f}) and {y_col} ({best_hx_hy[y_col]:.2f})")
            
            if len(low_x_high_y) > 0:
                best_lx_hy = low_x_high_y.loc[low_x_high_y[y_col].idxmax()]
                if x_col == "Price (₹ Lakh)":
                    insights.append(f"💎 **Top-Left (Great Value)**: {best_lx_hy['Bike']} offers excellent {y_col} ({best_lx_hy[y_col]:.2f}) at low price (₹{best_lx_hy[x_col]:.2f}L)")
                else:
                    insights.append(f"⭐ **Top-Left**: {best_lx_hy['Bike']} has high {y_col} ({best_lx_hy[y_col]:.2f}) with lower {x_col} ({best_lx_hy[x_col]:.2f})")
            
            if len(high_x_low_y) > 0:
                worst_hx_ly = high_x_low_y.loc[high_x_low_y[y_col].idxmin()]
                if x_col == "Price (₹ Lakh)":
                    insights.append(f"⚠️ **Bottom-Right (Expensive but Average)**: {worst_hx_ly['Bike']} is pricey (₹{worst_hx_ly[x_col]:.2f}L) but {y_col} is only {worst_hx_ly[y_col]:.2f}")
                else:
                    insights.append(f"🔄 **Bottom-Right**: {worst_hx_ly['Bike']} has high {x_col} ({worst_hx_ly[x_col]:.2f}) but lower {y_col} ({worst_hx_ly[y_col]:.2f})")
            
            # Overall insights
            if x_col == "Price (₹ Lakh)" and "VFM" in y_col:
                insights.append(f"📊 **Sweet Spot**: Look for bikes in the top-left region - high VFM at reasonable prices")
            elif x_col == "Price (₹ Lakh)" and "Total" in y_col:
                insights.append(f"🎯 **Performance vs Price**: Top-right = premium performance, top-left = budget excellence")
            elif "VFM" in x_col and "Total" in y_col:
                insights.append(f"⚖️ **Balance Point**: Top-right quadrant bikes excel in both value and performance")
            
            return insights
        
        insights = analyze_graph_regions(filtered_df, x_axis, y_axis)
        
        for insight in insights:
            st.markdown(insight)
        
        # Statistical context with detailed tables
        col_stats1, col_stats2 = st.columns(2)
        with col_stats1:
            good_performers = filtered_df[filtered_df[y_axis] > y_75th]
            st.metric("📊 Good Performance Threshold", 
                     f"Above {y_75th:.2f}", 
                     f"{len(good_performers)} bikes")
            
            # Show table of good performers
            if len(good_performers) > 0:
                st.markdown("**Bikes Above Threshold:**")
                good_performers_display = good_performers[["Bike", y_axis, "Price (₹ Lakh)"]].sort_values(by=y_axis, ascending=False)
                st.dataframe(
                    good_performers_display,
                    use_container_width=True,
                    hide_index=True,
                    height=200
                )
        
        with col_stats2:
            if x_axis == "Price (₹ Lakh)":
                budget_bikes = filtered_df[filtered_df[x_axis] <= x_median]
                st.metric("💰 Budget-Friendly Range", 
                         f"Under ₹{x_median:.1f}L", 
                         f"{len(budget_bikes)} bikes")
                
                # Show table of budget bikes
                if len(budget_bikes) > 0:
                    st.markdown("**Budget-Friendly Options:**")
                    budget_display = budget_bikes[["Bike", "Price (₹ Lakh)", y_axis]].sort_values(by=y_axis, ascending=False)
                    st.dataframe(
                        budget_display,
                        use_container_width=True,
                        hide_index=True,
                        height=200
                    )
            else:
                above_avg = filtered_df[filtered_df[x_axis] > x_median]
                st.metric("📈 Above Average", 
                         f"Above {x_median:.2f}", 
                         f"{len(above_avg)} bikes")
                
                # Show table of above average bikes
                if len(above_avg) > 0:
                    st.markdown("**Above Average Performers:**")
                    above_avg_display = above_avg[["Bike", x_axis, y_axis]].sort_values(by=x_axis, ascending=False)
                    st.dataframe(
                        above_avg_display,
                        use_container_width=True,
                        hide_index=True,
                        height=200
                    )
        
        # Additional insights
        st.subheader("💡 Chart Insights")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Highest " + y_axis,
                filtered_df.loc[filtered_df[y_axis].idxmax(), "Bike"],
                f"{filtered_df[y_axis].max():.2f}"
            )
        
        with col2:
            st.metric(
                "Best VFM",
                filtered_df.loc[filtered_df["VFM score"].idxmax(), "Bike"],
                f"{filtered_df['VFM score'].max():.2f}/10"
            )
        
        with col3:
            st.metric(
                "Price Range",
                f"₹{filtered_df['Price (₹ Lakh)'].min():.1f}L - ₹{filtered_df['Price (₹ Lakh)'].max():.1f}L",
                f"{len(filtered_df)} bikes"
            )
    
    with tab3:
        st.header("🏆 Top Rankings")
        
        # Calculate overall ranking (average of performance rank and VFM rank)
        df_ranks = filtered_df.copy()
        df_ranks['Performance_Rank'] = df_ranks['Total (out of 10)'].rank(method='dense', ascending=False)
        df_ranks['VFM_Rank'] = df_ranks['VFM score'].rank(method='dense', ascending=False)
        df_ranks['Overall_Rank'] = (df_ranks['Performance_Rank'] + df_ranks['VFM_Rank']) / 2
        df_ranks = df_ranks.sort_values('Overall_Rank')
        
        # Top Overall Ranked section
        st.subheader("👑 Top Overall Ranked Bikes (Performance + VFM)")
        st.markdown("*Calculated as average of Performance Rank and VFM Rank*")
        
        # Add combined score column
        df_ranks['Combined_Score'] = df_ranks['Total (out of 10)'] + df_ranks['VFM score']
        
        top_overall = df_ranks.head(15)[["Bike", "Total (out of 10)", "VFM score", "Combined_Score", "Price (₹ Lakh)", "Performance_Rank", "VFM_Rank", "Overall_Rank"]]
        top_overall.columns = ["Bike", "Performance (/10)", "VFM (/10)", "Combined Score", "Price (₹L)", "Perf Rank", "VFM Rank", "Overall Rank"]
        
        # Display as formatted table
        st.dataframe(
            top_overall,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Performance (/10)": st.column_config.NumberColumn(format="%.2f"),
                "VFM (/10)": st.column_config.NumberColumn(format="%.2f"),
                "Combined Score": st.column_config.NumberColumn(format="%.2f"),
                "Price (₹L)": st.column_config.NumberColumn(format="₹%.2f"),
                "Overall Rank": st.column_config.NumberColumn(format="%.1f")
            }
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 Top 10 Performance")
            top_performance = filtered_df.nlargest(10, "Total (out of 10)")[["Bike", "Total (out of 10)", "Price (₹ Lakh)"]]
            for i, row in top_performance.iterrows():
                st.write(f"**{row['Bike']}** - {row['Total (out of 10)']:.2f}/10 (₹{row['Price (₹ Lakh)']}L)")
        
        with col2:
            st.subheader("💰 Top 10 Value for Money")
            top_vfm = filtered_df.nlargest(10, "VFM score")[["Bike", "VFM score", "Price (₹ Lakh)"]]
            for i, row in top_vfm.iterrows():
                st.write(f"**{row['Bike']}** - {row['VFM score']:.2f}/10 (₹{row['Price (₹ Lakh)']}L)")
        
        # Segment-wise analysis
        st.subheader("📊 Segment-wise Analysis")
        segment_analysis = filtered_df.groupby("Segment").agg({
            "Total (out of 10)": "mean",
            "VFM score": "mean",
            "Price (₹ Lakh)": "mean",
            "Bike": "count"
        }).round(2)
        segment_analysis.columns = ["Avg Performance", "Avg VFM", "Avg Price (₹L)", "Count"]
        st.dataframe(segment_analysis, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("**📊 Data updated: August 2025** | Built with Streamlit & Plotly")

if __name__ == "__main__":
    main()