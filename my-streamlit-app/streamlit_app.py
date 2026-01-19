"""
Streamlit application for bike count prediction in Tours, France.

This app allows users to predict the number of bikes counted based on weather
and temporal features using a pre-trained RandomForest model.

Run with: streamlit run streamlit_app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from predictor import BikeCountPredictor

# Page configuration
st.set_page_config(
    page_title="Tours Bike Count Predictor",
    page_icon="🚴",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply custom styling
st.markdown(
    """
    <style>
    .main {
        padding-top: 0rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def load_predictor():
    """Load the model once and cache it."""
    model_path = Path(__file__).parent / "data" / "bike_count_model.pkl"
    return BikeCountPredictor(model_path)


def main():
    """Main application."""
    st.title("🚴 Tours Bike Count Predictor")
    st.markdown(
        "Predict the number of bikes counted at counting stations in Tours based on weather and temporal features."
    )

    # Sidebar with information
    with st.sidebar:
        st.header("About")
        st.markdown(
            """
            This application predicts bike counts using a **RandomForest** model
            trained on historical data from Tours, France.
            
            **Features used:**
            - Temperature (min/max)
            - Precipitation
            - Snow depth
            - Wind gusts
            - Day type (weekend, holiday, school vacation)
            """
        )

    # Create tabs for different input methods
    tab1, tab2 = st.tabs(["📊 Single Prediction", "📈 Batch Prediction"])

    with tab1:
        st.subheader("Make a Single Prediction")

        # Create three columns for better layout
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**Temperature (°C)**")
            t2m_min = st.number_input(
                "Min Temperature",
                value=-5.0,
                min_value=-40.0,
                max_value=50.0,
                step=0.5,
                label_visibility="collapsed",
            )
            t2m_max = st.number_input(
                "Max Temperature",
                value=10.0,
                min_value=-40.0,
                max_value=50.0,
                step=0.5,
                label_visibility="collapsed",
            )

        with col2:
            st.markdown("**Precipitation & Snow (m)**")
            tp_total = st.number_input(
                "Total Precipitation",
                value=0.001,
                min_value=0.0,
                max_value=0.5,
                step=0.001,
                label_visibility="collapsed",
            )
            sd_total = st.number_input(
                "Snow Depth",
                value=0.0,
                min_value=0.0,
                max_value=5.0,
                step=0.01,
                label_visibility="collapsed",
            )

        with col3:
            st.markdown("**Wind & Snow Fall (m)**")
            i10fg_max = st.number_input(
                "Max Wind Gust (m/s)",
                value=5.0,
                min_value=0.0,
                max_value=50.0,
                step=0.5,
                label_visibility="collapsed",
            )
            sf_max = st.number_input(
                "Max Snow Fall",
                value=0.0,
                min_value=0.0,
                max_value=5.0,
                step=0.01,
                label_visibility="collapsed",
            )

        st.markdown("---")

        col1, col2, col3 = st.columns(3)

        with col1:
            is_weekend = st.checkbox("🏖️ Weekend", value=False)

        with col2:
            is_holiday = st.checkbox("🎉 Holiday", value=False)

        with col3:
            is_school_vacation = st.checkbox("📚 School Vacation", value=False)

        # Make prediction
        if st.button("🔮 Predict", use_container_width=True, type="primary"):
            try:
                predictor = load_predictor()
                prediction = predictor.predict(
                    t2m_min=t2m_min,
                    t2m_max=t2m_max,
                    tp_total=tp_total,
                    sd_total=sd_total,
                    i10fg_max=i10fg_max,
                    sf_max=sf_max,
                    is_weekend=int(is_weekend),
                    is_holiday=int(is_holiday),
                    is_school_vacation=int(is_school_vacation),
                )

                # Display result
                st.success("✅ Prediction successful!")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(
                        label="Predicted Bike Count",
                        value=f"{prediction:,}",
                        delta=None,
                    )

                with col2:
                    st.info(
                        f"""
                        **Input Summary:**
                        - Temp: {t2m_min}°C to {t2m_max}°C
                        - Precip: {tp_total}m, Wind: {i10fg_max}m/s
                        - Weekend: {'Yes' if is_weekend else 'No'}
                        - Holiday: {'Yes' if is_holiday else 'No'}
                        - School Vacation: {'Yes' if is_school_vacation else 'No'}
                        """
                    )

            except Exception as e:
                st.error(f"❌ Error during prediction: {str(e)}")

    with tab2:
        st.subheader("Batch Prediction from CSV")

        uploaded_file = st.file_uploader(
            "Upload a CSV file with feature columns",
            type="csv",
            help="CSV must contain columns: t2m_min, t2m_max, tp_total, sd_total, i10fg_max, sf_max, is_weekend, is_holiday, is_school_vacation",
        )

        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)

                st.info(f"📊 Loaded {len(df)} rows")
                st.dataframe(df.head(), use_container_width=True)

                # Check required columns
                required_cols = [
                    "t2m_min",
                    "t2m_max",
                    "tp_total",
                    "sd_total",
                    "i10fg_max",
                    "sf_max",
                    "is_weekend",
                    "is_holiday",
                    "is_school_vacation",
                ]
                missing_cols = [col for col in required_cols if col not in df.columns]

                if missing_cols:
                    st.error(f"❌ Missing columns: {', '.join(missing_cols)}")
                else:
                    if st.button(
                        "🔮 Predict All", use_container_width=True, type="primary"
                    ):
                        try:
                            predictor = load_predictor()
                            predictions = predictor.predict_batch(df[required_cols])

                            # Add predictions to dataframe
                            df["predicted_bikes"] = predictions

                            st.success("✅ Predictions completed!")
                            st.dataframe(
                                df[["predicted_bikes"] + required_cols],
                                use_container_width=True,
                            )

                            # Download button
                            csv = df.to_csv(index=False)
                            st.download_button(
                                label="📥 Download predictions as CSV",
                                data=csv,
                                file_name="predictions.csv",
                                mime="text/csv",
                                use_container_width=True,
                            )

                        except Exception as e:
                            st.error(f"❌ Error during batch prediction: {str(e)}")

            except Exception as e:
                st.error(f"❌ Error reading file: {str(e)}")

    # Footer
    st.markdown("---")
    st.markdown(
        "🔧 Built with Streamlit | 🚴 Tours Bike Counting Project | Data: Copernicus & Syndicat des Mobilités"
    )


if __name__ == "__main__":
    main()
