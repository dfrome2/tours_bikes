"""
Streamlit application for bike count prediction in Tours, France.

This app allows users to predict the number of bikes counted based on weather
and temporal features using a pre-trained RandomForest model.

Features:
- Bilingual interface (French/English)
- Single and batch predictions
- Home page with project documentation
- Detailed field descriptions

Run with: streamlit run streamlit_app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from predictor import BikeCountPredictor

# Page configuration
st.set_page_config(
    page_title="🚴 Tours Bike Predictor",
    page_icon="🚴",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply custom styling
st.markdown(
    """
    <style>
    .metric-container {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==================== INTERNATIONALIZATION ====================

TRANSLATIONS = {
    "fr": {
        # Navigation
        "title": "🚴 Prédicteur de Comptage de Vélos",
        "subtitle": "Prédisez la fréquentation des pistes cyclables de Tours",
        "language": "🌐 Langue",
        "home": "🏠 Accueil",
        "single_pred": "📊 Prédiction Unique",
        "batch_pred": "📈 Prédictions en Batch",
        
        # Home tab
        "about_title": "À Propos du Projet",
        
        # Sections
        "temp_section": "🌡️ Température (°C)",
        "precip_section": "💧 Précipitations & Neige (m)",
        "wind_section": "💨 Vent & Chutes de Neige",
        "day_section": "📅 Type de Jour",
        
        # Temperature fields
        "temp_min": "Température Minimale",
        "temp_min_desc": "Température minimale attendue pour la journée",
        "temp_max": "Température Maximale",
        "temp_max_desc": "Température maximale attendue pour la journée",
        "temp_hint": "Plage: -40 à 50°C",
        
        # Precipitation fields
        "precip": "Précipitations Totales",
        "precip_desc": "Quantité totale d'eau tombée",
        "precip_hint": "En mètres (0 à 0.5m)",
        "snow_depth": "Profondeur de Neige",
        "snow_depth_desc": "Hauteur moyenne de neige sur le sol",
        "snow_depth_hint": "En mètres (0 à 5m)",
        
        # Wind fields
        "wind_gust": "Rafales de Vent Max",
        "wind_gust_desc": "Vitesse maximale des rafales de vent",
        "wind_gust_hint": "En m/s (0 à 50)",
        "snow_fall": "Chutes de Neige Max",
        "snow_fall_desc": "Quantité maximale de neige tombée",
        "snow_fall_hint": "En mètres (0 à 5m)",
        
        # Day type fields
        "weekend": "🏖️ Weekend",
        "weekend_desc": "C'est un jour de weekend (samedi ou dimanche)",
        "holiday": "🎉 Jour Férié",
        "holiday_desc": "C'est un jour férié officiel",
        "vacation": "📚 Vacances Scolaires",
        "vacation_desc": "C'est une période de vacances scolaires",
        
        # Buttons and messages
        "predict_btn": "🔮 Prédire",
        "success": "✅ Prédiction réussie!",
        "predicted": "Nombre de Vélos Prédits",
        "error": "❌ Erreur lors de la prédiction:",
        "input_summary": "📋 Résumé des Paramètres",
        
        # Batch prediction
        "batch_title": "Prédictions par Lots",
        "csv_upload": "Téléchargez un fichier CSV",
        "csv_help": "Le CSV doit contenir les colonnes: t2m_min, t2m_max, tp_total, sd_total, i10fg_max, sf_max, is_weekend, is_holiday, is_school_vacation",
        "loaded_rows": "📊 Lignes chargées",
        "missing_columns": "❌ Colonnes manquantes:",
        "csv_error": "❌ Erreur lors de la lecture du fichier:",
        "download_btn": "📥 Télécharger les prédictions (CSV)",
        
        # Display helpers
        "temp_range": "Température:",
        "to": "à",
        "precip_short": "Précip:",
        "wind_short": "Vent:",
        "yes": "✓ Oui",
        "no": "✗ Non",
        
        # Footer
        "footer": "🔧 Construit avec Streamlit | 🚴 Projet Tours Bike Counting | Données: Copernicus & Syndicat des Mobilités",
    },
    "en": {
        # Navigation
        "title": "🚴 Tours Bike Count Predictor",
        "subtitle": "Predict bike traffic on Tours cycling lanes",
        "language": "🌐 Language",
        "home": "🏠 Home",
        "single_pred": "📊 Single Prediction",
        "batch_pred": "📈 Batch Predictions",
        
        # Home tab
        "about_title": "About The Project",
        
        # Sections
        "temp_section": "🌡️ Temperature (°C)",
        "precip_section": "💧 Precipitation & Snow (m)",
        "wind_section": "💨 Wind & Snowfall",
        "day_section": "📅 Day Type",
        
        # Temperature fields
        "temp_min": "Minimum Temperature",
        "temp_min_desc": "Minimum temperature expected for the day",
        "temp_max": "Maximum Temperature",
        "temp_max_desc": "Maximum temperature expected for the day",
        "temp_hint": "Range: -40 to 50°C",
        
        # Precipitation fields
        "precip": "Total Precipitation",
        "precip_desc": "Total amount of water fallen",
        "precip_hint": "In meters (0 to 0.5m)",
        "snow_depth": "Snow Depth",
        "snow_depth_desc": "Average height of snow on ground",
        "snow_depth_hint": "In meters (0 to 5m)",
        
        # Wind fields
        "wind_gust": "Max Wind Gusts",
        "wind_gust_desc": "Maximum wind gust speed",
        "wind_gust_hint": "In m/s (0 to 50)",
        "snow_fall": "Max Snowfall",
        "snow_fall_desc": "Maximum amount of snow fallen",
        "snow_fall_hint": "In meters (0 to 5m)",
        
        # Day type fields
        "weekend": "🏖️ Weekend",
        "weekend_desc": "Is it a weekend day (Saturday or Sunday)",
        "holiday": "🎉 Holiday",
        "holiday_desc": "Is it a public holiday",
        "vacation": "📚 School Vacation",
        "vacation_desc": "Is it a school vacation period",
        
        # Buttons and messages
        "predict_btn": "🔮 Predict",
        "success": "✅ Prediction successful!",
        "predicted": "Predicted Bike Count",
        "error": "❌ Error during prediction:",
        "input_summary": "📋 Parameter Summary",
        
        # Batch prediction
        "batch_title": "Batch Predictions",
        "csv_upload": "Upload a CSV file",
        "csv_help": "CSV must contain columns: t2m_min, t2m_max, tp_total, sd_total, i10fg_max, sf_max, is_weekend, is_holiday, is_school_vacation",
        "loaded_rows": "📊 Rows loaded",
        "missing_columns": "❌ Missing columns:",
        "csv_error": "❌ Error reading file:",
        "download_btn": "📥 Download predictions (CSV)",
        
        # Display helpers
        "temp_range": "Temperature:",
        "to": "to",
        "precip_short": "Precip:",
        "wind_short": "Wind:",
        "yes": "✓ Yes",
        "no": "✗ No",
        
        # Footer
        "footer": "🔧 Built with Streamlit | 🚴 Tours Bike Counting Project | Data: Copernicus & Syndicat des Mobilités",
    },
}


@st.cache_resource
def load_predictor():
    """Load the model once and cache it."""
    model_path = Path(__file__).parent / "data" / "bike_count_model.pkl"
    return BikeCountPredictor(model_path)


@st.cache_data
def load_readme():
    """Load the README content from doc folder."""
    readme_path = Path(__file__).parent.parent / "doc" / "README.md"
    if readme_path.exists():
        try:
            with open(readme_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"Error loading README: {str(e)}"
    return None


def get_text(key, lang):
    """Get translated text by key."""
    if lang not in TRANSLATIONS:
        lang = "en"
    return TRANSLATIONS[lang].get(key, key)


def main():
    """Main application."""
    
    # Initialize session state for language
    if "lang" not in st.session_state:
        st.session_state.lang = "fr"

    # Sidebar for language selection with flag buttons
    with st.sidebar:
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🇫🇷 Français", use_container_width=True):
                st.session_state.lang = "fr"
        with col2:
            if st.button("🇬🇧 English", use_container_width=True):
                st.session_state.lang = "en"
        st.markdown("---")

    lang = st.session_state.lang
    t = lambda key: get_text(key, lang)

    # Main header
    st.title(t("title"))
    st.markdown(t("subtitle"))

    # Create tabs for different sections
    tab_home, tab_single, tab_batch = st.tabs([t("home"), t("single_pred"), t("batch_pred")])

    # ==================== HOME TAB ====================
    with tab_home:
        st.subheader(t("about_title"))
        
        readme_content = load_readme()
        if readme_content:
            st.markdown(readme_content)
        else:
            st.warning("README content not found")

    # ==================== SINGLE PREDICTION TAB ====================
    with tab_single:
        st.subheader("📊 " + t("single_pred"))

        # Temperature section
        st.markdown(f"### {t('temp_section')}")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**{t('temp_min')}**")
            st.caption(t('temp_min_desc'))
            st.caption(f"*{t('temp_hint')}*")
            t2m_min = st.number_input(
                t("temp_min"),
                value=-5.0,
                min_value=-40.0,
                max_value=50.0,
                step=0.5,
                label_visibility="collapsed",
            )
        
        with col2:
            st.markdown(f"**{t('temp_max')}**")
            st.caption(t('temp_max_desc'))
            st.caption(f"*{t('temp_hint')}*")
            t2m_max = st.number_input(
                t("temp_max"),
                value=10.0,
                min_value=-40.0,
                max_value=50.0,
                step=0.5,
                label_visibility="collapsed",
            )

        st.divider()

        # Precipitation & Snow section
        st.markdown(f"### {t('precip_section')}")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**{t('precip')}**")
            st.caption(t('precip_desc'))
            st.caption(f"*{t('precip_hint')}*")
            tp_total = st.number_input(
                t("precip"),
                value=0.001,
                min_value=0.0,
                max_value=0.5,
                step=0.001,
                label_visibility="collapsed",
            )
        
        with col2:
            st.markdown(f"**{t('snow_depth')}**")
            st.caption(t('snow_depth_desc'))
            st.caption(f"*{t('snow_depth_hint')}*")
            sd_total = st.number_input(
                t("snow_depth"),
                value=0.0,
                min_value=0.0,
                max_value=5.0,
                step=0.01,
                label_visibility="collapsed",
            )

        st.divider()

        # Wind & Snowfall section
        st.markdown(f"### {t('wind_section')}")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**{t('wind_gust')}**")
            st.caption(t('wind_gust_desc'))
            st.caption(f"*{t('wind_gust_hint')}*")
            i10fg_max = st.number_input(
                t("wind_gust"),
                value=5.0,
                min_value=0.0,
                max_value=50.0,
                step=0.5,
                label_visibility="collapsed",
            )
        
        with col2:
            st.markdown(f"**{t('snow_fall')}**")
            st.caption(t('snow_fall_desc'))
            st.caption(f"*{t('snow_fall_hint')}*")
            sf_max = st.number_input(
                t("snow_fall"),
                value=0.0,
                min_value=0.0,
                max_value=5.0,
                step=0.01,
                label_visibility="collapsed",
            )

        st.divider()

        # Day type section
        st.markdown(f"### {t('day_section')}")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"**{t('weekend')}**")
            st.caption(t('weekend_desc'))
            is_weekend = st.checkbox(t("weekend"), value=False, label_visibility="collapsed")
        
        with col2:
            st.markdown(f"**{t('holiday')}**")
            st.caption(t('holiday_desc'))
            is_holiday = st.checkbox(t("holiday"), value=False, label_visibility="collapsed")
        
        with col3:
            st.markdown(f"**{t('vacation')}**")
            st.caption(t('vacation_desc'))
            is_school_vacation = st.checkbox(t("vacation"), value=False, label_visibility="collapsed")

        st.divider()

        # Predict button
        if st.button(t("predict_btn"), use_container_width=True, type="primary", key="single_pred"):
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
                st.success(t("success"))
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(
                        label=t("predicted"),
                        value=f"{prediction:,}",
                        delta=None,
                    )

                with col2:
                    temp_str = f"{t('temp_range')} {t2m_min}°C {t('to')} {t2m_max}°C"
                    precip_str = f"{t('precip_short')} {tp_total}m"
                    wind_str = f"{t('wind_short')} {i10fg_max}m/s"
                    
                    day_flags = []
                    if is_weekend:
                        day_flags.append(t("weekend"))
                    if is_holiday:
                        day_flags.append(t("holiday"))
                    if is_school_vacation:
                        day_flags.append(t("vacation"))
                    
                    flags_str = " • ".join(day_flags) if day_flags else "-"

                    st.info(
                        f"{t('input_summary')}\n\n"
                        f"- {temp_str}\n"
                        f"- {precip_str}\n"
                        f"- {wind_str}\n"
                        f"- {flags_str}"
                    )

            except Exception as e:
                st.error(f"{t('error')} {str(e)}")

    # ==================== BATCH PREDICTION TAB ====================
    with tab_batch:
        st.subheader("📈 " + t("batch_title"))

        uploaded_file = st.file_uploader(
            t("csv_upload"),
            type="csv",
            help=t("csv_help"),
        )

        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)

                st.info(f"{t('loaded_rows')}: {len(df)}")
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
                    st.error(f"{t('missing_columns')} {', '.join(missing_cols)}")
                else:
                    if st.button(t("predict_btn"), use_container_width=True, type="primary", key="batch_pred"):
                        try:
                            predictor = load_predictor()
                            predictions = predictor.predict_batch(df[required_cols])

                            # Add predictions to dataframe
                            df["predicted_bikes"] = predictions

                            st.success(t("success"))
                            st.dataframe(
                                df[["predicted_bikes"] + required_cols],
                                use_container_width=True,
                            )

                            # Download button
                            csv = df.to_csv(index=False)
                            st.download_button(
                                label=t("download_btn"),
                                data=csv,
                                file_name="predictions.csv",
                                mime="text/csv",
                                use_container_width=True,
                            )

                        except Exception as e:
                            st.error(f"{t('error')} {str(e)}")

            except Exception as e:
                st.error(f"{t('csv_error')} {str(e)}")

    # Footer
    st.markdown("---")
    st.markdown(t("footer"))


if __name__ == "__main__":
    main()
