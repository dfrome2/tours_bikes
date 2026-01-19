"""
Streamlit application for bike count prediction in Tours, France.
Made by Denis Froment, Value Discovery SASU.

Multi-page app with:
- Documentation page (README with images)
- Prediction page (single and batch predictions)
- Bilingual interface (French/English)

Run with: streamlit run streamlit_app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from predictor import BikeCountPredictor
import re

# Page configuration
st.set_page_config(
    page_title="Tours bike predictor",
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
    img {
        max-width: 100%;
        height: auto;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==================== INTERNATIONALIZATION ====================

TRANSLATIONS = {
    "fr": {
        # Pages
        "page_doc": "Info projet",
        "page_pred": "Prédiction",
        "language": "Langue",
        "title": "Tours Bike Predictor",
        
        # Prediction page
        "pred_title": "Prédiction de comptage de vélos",
        "pred_subtitle": "Prédisez la fréquentation des pistes cyclables de Tours",
        "single_pred": "Prédiction simple",
        "batch_pred": "Prédictions par lots",
        
        # Sections
        "temp_section": "Température (°C)",
        "precip_wind_section": "Précipitation et vent",
        "snowfall_depth_section": "Neige et profondeur",
        "day_section": "Type de jour",
        
        # Temperature fields
        "temp_min": "Température minimale",
        "temp_min_desc": "Température mini attendue pour la journée (°C)",
        "temp_max": "Température maximale",
        "temp_max_desc": "Température maxi attendue pour la journée (°C)",
        
        # Precipitation & Wind fields
        "precip": "Précipitation totale",
        "precip_desc": "Quantité totale d'eau tombée en journée (en m ! exemple 0.001 pour 1 mm)",
        "wind_gust": "Rafales de vent",
        "wind_gust_desc": "Vitesse maxi des rafales de vent (en m/s)",
        
        # Snowfall & Snow depth fields
        "snow_fall": "Chutes de neige totale",
        "snow_fall_desc": "Quantité de neige attendue (m)",
        "snow_depth": "Profondeur de neige",
        "snow_depth_desc": "Couche max de neige tenant au sol (m)",
        
        # Day type fields
        "weekend": "Weekend",
        "weekend_desc": "Jour de weekend (samedi ou dimanche)",
        "holiday": "Jour férié",
        "holiday_desc": "Jour férié officiel national",
        "vacation": "Vacances scolaires",
        "vacation_desc": "Période de vacances scolaires de l'académie",
        
        # Buttons and messages
        "predict_btn": "Prédire",
        "success": "Prédiction réussie!",
        "predicted": "Nombre de vélos prédits",
        "error": "Erreur lors de la prédiction:",
        "input_summary": "Résumé des paramètres",
        
        # Batch prediction
        "batch_title": "Prédictions par lots",
        "csv_upload": "Téléchargez un fichier CSV",
        "csv_help": "Le CSV doit contenir: t2m_min, t2m_max, tp_total, sd_total, i10fg_max, sf_max, is_weekend, is_holiday, is_school_vacation",
        "loaded_rows": "Lignes chargées",
        "missing_columns": "Colonnes manquantes:",
        "csv_error": "Erreur lors de la lecture:",
        "download_btn": "Télécharger les prédictions (CSV)",
        
        # Display helpers
        "temp_range": "Température:",
        "to": "à",
        "precip_short": "Précip:",
        "wind_short": "Vent:",
        "yes": "Oui",
        "no": "Non",
        
        # Footer
        "footer": "Denis Froment | contact@valuediscovery.fr | Données: Copernicus et Syndicat des Mobilités de Tours",
        
        # Readme status
        "readme_error": "Erreur lors du chargement du README",
    },
    "en": {
        # Pages
        "page_doc": "Project info",
        "page_pred": "Prediction",
        "language": "Language",
        "title": "Tours Bike Predictor",
        
        # Prediction page
        "pred_title": "Bike count prediction",
        "pred_subtitle": "Predict bike traffic on Tours cycling lanes",
        "single_pred": "Single prediction",
        "batch_pred": "Batch predictions",
        
        # Sections
        "temp_section": "Temperature (°C)",
        "precip_wind_section": "Precipitation & Wind",
        "snowfall_depth_section": "Snowfall & Snow depth",
        "day_section": "Day type",
        
        # Temperature fields
        "temp_min": "Minimum temperature",
        "temp_min_desc": "Minimum temperature expected for the day (°C)",
        "temp_max": "Maximum temperature",
        "temp_max_desc": "Maximum temperature expected for the day (°C)",
        
        # Precipitation & Wind fields
        "precip": "Total precipitation",
        "precip_desc": "Amount of water expected to fall (m)",
        "wind_gust": "Max wind gusts",
        "wind_gust_desc": "Maximum wind gust speed (m/s)",
        
        # Snowfall & Snow depth fields
        "snow_fall": "Max snowfall",
        "snow_fall_desc": "Maximum amount of snow fallen (m)",
        "snow_depth": "Snow depth",
        "snow_depth_desc": "Max height of snow on ground (m)",
        
        # Day type fields
        "weekend": "Weekend",
        "weekend_desc": "you predict for a saturday or sunday",
        "holiday": "Holiday",
        "holiday_desc": "Is it a public holiday",
        "vacation": "School vacation",
        "vacation_desc": "Is it a school vacation period",
        
        # Buttons and messages
        "predict_btn": "Predict",
        "success": "Prediction successful!",
        "predicted": "Predicted bike count",
        "error": "Error during prediction:",
        "input_summary": "Parameter summary",
        
        # Batch prediction
        "batch_title": "Batch predictions",
        "csv_upload": "Upload a CSV file",
        "csv_help": "CSV must contain: t2m_min, t2m_max, tp_total, sd_total, i10fg_max, sf_max, is_weekend, is_holiday, is_school_vacation",
        "loaded_rows": "Rows loaded",
        "missing_columns": "Missing columns:",
        "csv_error": "Error reading file:",
        "download_btn": "Download predictions (CSV)",
        
        # Display helpers
        "temp_range": "Temperature:",
        "to": "to",
        "precip_short": "Precip:",
        "wind_short": "Wind:",
        "yes": "Yes",
        "no": "No",
        
        # Footer
        "footer": "Built with Streamlit | Tours Bike Counting | Data: Copernicus & Syndicat des Mobilites",
        
        # Readme status
        "readme_error": "Error loading README",
    },
}


@st.cache_resource
def load_predictor():
    """Load the model once and cache it."""
    model_path = Path(__file__).parent / "data" / "bike_count_model.pkl"
    return BikeCountPredictor(model_path)


@st.cache_data
def load_readme():
    """Load and process README content."""
    # Try multiple possible paths
    possible_paths = [
        Path(__file__).parent.parent / "doc" / "README.md",
        Path(__file__).parent / ".." / "doc" / "README.md",
        Path(__file__).resolve().parent.parent / "doc" / "README.md",
    ]
    
    for readme_path in possible_paths:
        if readme_path.exists():
            try:
                with open(readme_path, "r", encoding="utf-8") as f:
                    content = f.read()
                return content
            except Exception as e:
                continue
    
    return None


def process_markdown_images(content):
    """Replace markdown image paths to work with doc/captures folder."""
    # Replace ![...](captures/...) with ![...](...doc/captures/...)
    content = re.sub(
        r'!\[(.*?)\]\(captures/(.*?)\)',
        lambda m: f'![{m.group(1)}](../doc/captures/{m.group(2)})',
        content
    )
    return content


def get_text(key, lang):
    """Get translated text by key."""
    if lang not in TRANSLATIONS:
        lang = "en"
    return TRANSLATIONS[lang].get(key, key)


def page_documentation(lang):
    """Documentation page with README and images."""
    t = lambda key: get_text(key, lang)
    
    readme_content = load_readme()
    if readme_content:
        # Process image paths
        readme_content = process_markdown_images(readme_content)
        st.markdown(readme_content)
    else:
        st.error(t("readme_error"))
        st.info("README.md should be located in: `../doc/README.md`")


def page_prediction(lang):
    """Prediction page with single and batch predictions."""
    t = lambda key: get_text(key, lang)
    
    st.title(t("pred_title"))
    st.markdown(t("pred_subtitle"))
    
    # Create tabs for single and batch
    tab_single, tab_batch = st.tabs([t("single_pred"), t("batch_pred")])
    
    # ==================== SINGLE PREDICTION ====================
    with tab_single:
        st.subheader(t("single_pred"))

        # ========== Line 1: Temperature ==========
        st.markdown(f"### {t('temp_section')}")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**{t('temp_min')}**")
            st.caption(t('temp_min_desc'))
            t2m_min = st.number_input(
                t("temp_min"),
                value=-5.0,
                min_value=-40.0,
                max_value=50.0,
                step=0.5,
                label_visibility="collapsed",
                key="temp_min_input"
            )
        
        with col2:
            st.markdown(f"**{t('temp_max')}**")
            st.caption(t('temp_max_desc'))
            t2m_max = st.number_input(
                t("temp_max"),
                value=10.0,
                min_value=-40.0,
                max_value=50.0,
                step=0.5,
                label_visibility="collapsed",
                key="temp_max_input"
            )

        st.divider()

        # ========== Line 2: Precipitation & Wind ==========
        st.markdown(f"### {t('precip_wind_section')}")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**{t('precip')}**")
            st.caption(t('precip_desc'))
            tp_total = st.number_input(
                t("precip"),
                value=0.001,
                min_value=0.0,
                max_value=0.5,
                step=0.001,
                label_visibility="collapsed",
                key="precip_input"
            )
        
        with col2:
            st.markdown(f"**{t('wind_gust')}**")
            st.caption(t('wind_gust_desc'))
            i10fg_max = st.number_input(
                t("wind_gust"),
                value=5.0,
                min_value=0.0,
                max_value=50.0,
                step=0.5,
                label_visibility="collapsed",
                key="wind_input"
            )

        st.divider()

        # ========== Line 3: Snowfall & Snow depth ==========
        st.markdown(f"### {t('snowfall_depth_section')}")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**{t('snow_fall')}**")
            st.caption(t('snow_fall_desc'))
            sf_max = st.number_input(
                t("snow_fall"),
                value=0.0,
                min_value=0.0,
                max_value=5.0,
                step=0.01,
                label_visibility="collapsed",
                key="snowfall_input"
            )
        
        with col2:
            st.markdown(f"**{t('snow_depth')}**")
            st.caption(t('snow_depth_desc'))
            sd_total = st.number_input(
                t("snow_depth"),
                value=0.0,
                min_value=0.0,
                max_value=5.0,
                step=0.01,
                label_visibility="collapsed",
                key="snowdepth_input"
            )

        st.divider()

        # ========== Line 4: Day type ==========
        st.markdown(f"### {t('day_section')}")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"**{t('weekend')}**")
            st.caption(t('weekend_desc'))
            is_weekend = st.checkbox(
                t("weekend"),
                value=False,
                label_visibility="collapsed",
                key="weekend_check"
            )
        
        with col2:
            st.markdown(f"**{t('holiday')}**")
            st.caption(t('holiday_desc'))
            is_holiday = st.checkbox(
                t("holiday"),
                value=False,
                label_visibility="collapsed",
                key="holiday_check"
            )
        
        with col3:
            st.markdown(f"**{t('vacation')}**")
            st.caption(t('vacation_desc'))
            is_school_vacation = st.checkbox(
                t("vacation"),
                value=False,
                label_visibility="collapsed",
                key="vacation_check"
            )

        st.divider()

        # Predict button
        if st.button(t("predict_btn"), use_container_width=True, type="primary", key="single_pred_btn"):
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

                st.success(t("success"))
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(
                        label=t("predicted"),
                        value=f"{prediction:,}",
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

    # ==================== BATCH PREDICTION ====================
    with tab_batch:
        st.subheader(t("batch_title"))

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
                    if st.button(t("predict_btn"), use_container_width=True, type="primary", key="batch_pred_btn"):
                        try:
                            predictor = load_predictor()
                            predictions = predictor.predict_batch(df[required_cols])
                            df["predicted_bikes"] = predictions

                            st.success(t("success"))
                            st.dataframe(
                                df[["predicted_bikes"] + required_cols],
                                use_container_width=True,
                            )

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


def main():
    """Main application with page navigation."""
    
    # Initialize session state
    if "lang" not in st.session_state:
        st.session_state.lang = "fr"
    if "page" not in st.session_state:
        st.session_state.page = "doc"

    # ==================== SIDEBAR NAVIGATION ====================
    with st.sidebar:
        st.title(get_text("title", st.session_state.lang))
        st.markdown("---")
        
        # Language selection with flags
        st.markdown("**" + get_text("language", st.session_state.lang) + "**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Francais", use_container_width=True, key="lang_fr"):
                st.session_state.lang = "fr"
        with col2:
            if st.button("English", use_container_width=True, key="lang_en"):
                st.session_state.lang = "en"
        
        st.markdown("---")
        
        # Page navigation
        st.markdown("**Pages**")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(
                get_text("page_doc", st.session_state.lang),
                use_container_width=True,
                type="primary",
                key="btn_doc"
            ):
                st.session_state.page = "doc"
        
        with col2:
            if st.button(
                get_text("page_pred", st.session_state.lang),
                use_container_width=True,
                type="primary",
                key="btn_pred"
            ):
                st.session_state.page = "pred"
        
        st.markdown("---")
        st.caption(get_text("footer", st.session_state.lang))

    # ==================== MAIN CONTENT ====================
    if st.session_state.page == "doc":
        page_documentation(st.session_state.lang)
    else:
        page_prediction(st.session_state.lang)


if __name__ == "__main__":
    main()
