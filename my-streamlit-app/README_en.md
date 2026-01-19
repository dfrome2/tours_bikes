# Bike traffic in Tours: Power BI visualizations & data science predictions

---

## Why This Project?
**How does weather influence bike traffic in Tours?**
This project explores the correlation between weather conditions (temperature, rain, wind, snow) and bike lane usage, using open data from Tours Métropole and Copernicus records.
**Goal**: Visualize trends, predict daily traffic, and why not: help local authorities optimize their operation on cycling infrastructure.

---

## Key insights

### 1. Temperature and bike traffic
Sample to visualize the influence of temperature variation between 15°C and 22°C: from October 15 to 22, 2023, the bike traffic curve follows the maximum temperature curve.

![Temperature/Bike Traffic Correlation](captures/visual_temperature.png)

### 2. Impact of rain
Precipitation significantly reduces bike traffic. in Power BI, A DAX measure was created to amplify the visibility of low precipitation (initially in m/h).

![Rain in blue vs. Daily bike traffic in purple](captures/visual_pluie.png)

### 3. Interactive visualization
Power BI dashboard allowing filtering by counter, date, and weather conditions, with maps and site photos.

![Main dashboard](captures/report_principal.png)

---

## Methodology & tools

### 1. Data sources
- **Bike Traffic**: [Tours Métropole Open Data](https://data.tours-metropole.fr/explore/dataset/comptage-velo-compteurs-syndicat-des-mobilites-de-touraine/)
- **Weather**: [Copernicus ERA5](https://cds.climate.copernicus.eu/) (temperature, rain, wind, snow)

### 2. Data processing
- **Power Query**: Temperature conversion (K → °C), hourly to daily aggregation.
- **Python**: Cleaning, feature engineering (weekend, holidays), outlier management. DataViz.
![Temperature range](captures/temp_range.png)


### 3. Predictive modeling
- **Model**: LightGBM (MAE = 4010, satisfactory results for daily prediction).
- **Features**: Min/max temperatures, precipitation, wind, weekend, school holidays.
- **Possible Improvements**: Add lag, dichotomize weekdays, special events.

---

## For experts

### Technical details
- **Power BI**: Simple data model, DAX measures for aggregations and visualizations.
- **Python**: Prediction scripts (`predict_bike_count.py`), Copernicus API quota management.
- **Bias Risks**: Missing data (rain), counters activated during the period.

### How to reproduce?
Github project: [tours_bikes](https://github.com/dfrome2/tours_bikes)


---

## Contact
Value Discovery – [contact@valuediscovery.fr](mailto:contact@valuediscovery.fr) | Consulting and training.


**Licence** : GNU3
---