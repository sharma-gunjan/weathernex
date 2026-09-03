import streamlit as st
import pandas as pd
import requests
from sklearn.ensemble import RandomForestRegressor
import plotly.express as px


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="WeatherNex",
    page_icon="🌦️",
    layout="wide"
)
# ---------------- WEBSITE STYLING ----------------

st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

h1 {
    font-size: 42px !important;
    font-weight: 700 !important;
}

h2 {
    font-size: 28px !important;
}

h3 {
    font-size: 22px !important;
}

[data-testid="stMetric"] {
    padding: 15px;
    border-radius: 12px;
    border: 1px solid rgba(128,128,128,0.25);
}

[data-testid="stMetricValue"] {
    font-size: 28px;
}

div[data-testid="stVerticalBlock"] > div {
    gap: 0.7rem;
}

</style>
""", unsafe_allow_html=True)
# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.markdown("## 🌦️ WeatherNex")

    st.caption("National Weather Intelligence Platform")

    st.divider()

    st.markdown("### 📊 Dashboard")
    st.markdown("Live weather & AI insights")

    st.markdown("### 🌧️ Forecast")
    st.markdown("5-day weather forecast")

    st.markdown("### ⚠️ Risk Analysis")
    st.markdown("Rainfall & weather risk")

    st.markdown("### 🗺️ Risk Map")
    st.markdown("Regional risk visualization")

    st.markdown("### 🚨 Early Warning")
    st.markdown("Weather alerts & warnings")

    st.divider()

    st.caption("WeatherNex Prototype")
    st.caption("AI • Data • Risk Intelligence")
# ---------------- HEADER ----------------

st.title("🌦️ WeatherNex")

st.subheader("National Weather Intelligence Platform")

st.write(
    "From weather data to prediction, risk analysis and early warnings."
)

st.divider()



# =========================================================
# LOCATIONS
# =========================================================

locations = {
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Chennai": (13.0827, 80.2707),
    "Kolkata": (22.5726, 88.3639),
    "Bengaluru": (12.9716, 77.5946)
}


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 🌦️ WeatherNex")
    st.write("National Weather Intelligence Platform")

    st.divider()

    st.markdown("### 📍 Location")
    st.write("Select a city from the main dashboard.")

    st.divider()

    st.markdown("### 🧠 Intelligence Modules")

    st.write("✅ Live Weather")
    st.write("✅ Historical Analysis")
    st.write("✅ AI Rainfall Prediction")
    st.write("✅ Risk Assessment")
    st.write("✅ Risk Map")
    st.write("✅ 5-Day Forecast")
    st.write("✅ Anomaly Detection")
    st.write("✅ Early Warning")
    st.write("✅ Intelligence Score")


# =========================================================
# LOCATION SELECTION
# =========================================================

st.divider()

st.subheader("📍 Select Location for Weather Intelligence")

location = st.selectbox(
    "Location",
    list(locations.keys())
)

latitude, longitude = locations[location]

st.write("Selected Location:", location)


# =========================================================
# WEATHER API
# =========================================================

def get_weather(latitude, longitude):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,

        "current":
        "temperature_2m,"
        "relative_humidity_2m,"
        "precipitation,"
        "wind_speed_10m",

        "daily":
        "temperature_2m_max,"
        "temperature_2m_min,"
        "precipitation_sum,"
        "rain_sum",

        "forecast_days": 5,

        "timezone": "auto"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        if response.status_code == 200:
            return response.json()

        return None

    except Exception:
        return None


weather_data = get_weather(
    latitude,
    longitude
)


# =========================================================
# CHECK API
# =========================================================

if not weather_data:

    st.error(
        "Unable to fetch weather data. "
        "Please check your internet connection."
    )

    st.stop()


# =========================================================
# CURRENT WEATHER
# =========================================================

current = weather_data["current"]

temperature = current["temperature_2m"]
humidity = current["relative_humidity_2m"]
rainfall = current["precipitation"]
wind_speed = current["wind_speed_10m"]


# =========================================================
# 5 DAY FORECAST DATA
# =========================================================

daily = weather_data["daily"]

forecast_df = pd.DataFrame({

    "Date": pd.to_datetime(
        daily["time"]
    ),

    "Max Temperature (°C)":
    daily["temperature_2m_max"],

    "Min Temperature (°C)":
    daily["temperature_2m_min"],

    "Rainfall (mm)":
    daily["precipitation_sum"],

    "Rain (mm)":
    daily["rain_sum"]
})


# =========================================================
# LIVE WEATHER
# =========================================================

st.divider()

st.subheader("🌤️ Live Weather")

st.caption(
    f"Real-time weather conditions for {location}"
)

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "🌡️ Temperature",
        f"{temperature} °C"
    )


with col2:

    st.metric(
        "💧 Humidity",
        f"{humidity} %"
    )


with col3:

    st.metric(
        "🌧️ Current Precipitation",
        f"{rainfall} mm"
    )


with col4:

    st.metric(
        "💨 Wind Speed",
        f"{wind_speed} km/h"
    )


# =========================================================
# HISTORICAL DATA
# =========================================================

df = pd.read_csv(
    "data/weather.csv"
)

df["date"] = pd.to_datetime(
    df["date"]
)

location_data = df[
    df["location"] == location
]


if location_data.empty:

    st.warning(
        "No historical data available for this location."
    )

    st.stop()


# =========================================================
# AI RAINFALL PREDICTION
# =========================================================

features = [
    "temperature",
    "humidity",
    "wind_speed"
]

X = df[features]

y = df["rainfall"]


model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(
    X,
    y
)


current_input = pd.DataFrame({

    "temperature": [temperature],

    "humidity": [humidity],

    "wind_speed": [wind_speed]

})


predicted_rainfall = model.predict(
    current_input
)[0]


# =========================================================
# HISTORICAL RAINFALL
# =========================================================

st.divider()

st.subheader("📊 Historical Rainfall")

st.line_chart(
    location_data
    .set_index("date")["rainfall"]
)


# =========================================================
# HISTORICAL AVERAGE
# =========================================================

historical_avg = location_data[
    "rainfall"
].mean()


st.metric(
    "📊 Historical Average Rainfall",
    f"{historical_avg:.1f} mm"
)


# =========================================================
# AI RAINFALL PREDICTION
# =========================================================

st.divider()

st.subheader("🤖 AI Rainfall Prediction")

pred_col1, pred_col2, pred_col3 = st.columns(3)


with pred_col1:

    st.metric(
        "🌧️ Predicted Rainfall",
        f"{predicted_rainfall:.1f} mm"
    )


with pred_col2:

    st.metric(
        "📊 Historical Average",
        f"{historical_avg:.1f} mm"
    )


# Avoid division by zero

if historical_avg != 0:

    deviation = (
        (predicted_rainfall - historical_avg)
        / historical_avg
    ) * 100

else:

    deviation = 0


with pred_col3:

    st.metric(
        "📈 Deviation from Average",
        f"{deviation:.1f}%"
    )


# =========================================================
# RISK ASSESSMENT
# =========================================================

if predicted_rainfall < 25:

    risk_level = "LOW"

    warning_message = (
        "Weather conditions are normal."
    )


elif predicted_rainfall < 50:

    risk_level = "MODERATE"

    warning_message = (
        "Moderate rainfall expected. Stay alert."
    )


elif predicted_rainfall < 80:

    risk_level = "HIGH"

    warning_message = (
        "Heavy rainfall expected. "
        "Prepare for possible waterlogging."
    )


else:

    risk_level = "VERY HIGH"

    warning_message = (
        "Very heavy rainfall expected. "
        "Flood risk may increase."
    )


# =========================================================
# WEATHER RISK ASSESSMENT
# =========================================================

st.divider()

st.subheader("⚠️ Weather Risk Assessment")

risk_col1, risk_col2 = st.columns(2)


with risk_col1:

    st.metric(
        "🌧️ Rainfall Risk",
        risk_level
    )


with risk_col2:

    if risk_level == "LOW":

        st.success(
            "✅ " + warning_message
        )

    elif risk_level == "MODERATE":

        st.warning(
            "⚠️ " + warning_message
        )

    else:

        st.error(
            "🚨 " + warning_message
        )


# =========================================================
# REGIONAL RISK MAP
# =========================================================

st.divider()

st.subheader("🗺️ Regional Weather Risk Intelligence")

map_data = []


for city, (lat, lon) in locations.items():

    city_data = df[
        df["location"] == city
    ]

    if not city_data.empty:

        avg_rainfall = city_data[
            "rainfall"
        ].mean()


        if avg_rainfall < 25:

            city_risk = "LOW"


        elif avg_rainfall < 50:

            city_risk = "MODERATE"


        elif avg_rainfall < 80:

            city_risk = "HIGH"


        else:

            city_risk = "VERY HIGH"


        map_data.append({

            "City": city,

            "Latitude": lat,

            "Longitude": lon,

            "Historical Rainfall":
            avg_rainfall,

            "Risk":
            city_risk

        })


map_df = pd.DataFrame(
    map_data
)


fig = px.scatter_map(
    map_df,

    lat="Latitude",

    lon="Longitude",

    hover_name="City",

    hover_data={

        "Historical Rainfall": ":.1f",

        "Risk": True,

        "Latitude": False,

        "Longitude": False

    },

    color="Risk",

    zoom=4.5,

    center={
        "lat": 22.5,
        "lon": 79.0
    },

    height=550,

    title="Weather Risk Across Selected Regions"
)


fig.update_layout(

    map_style="open-street-map",

    margin={
        "r": 0,
        "t": 50,
        "l": 0,
        "b": 0
    }

)


st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# 5 DAY WEATHER FORECAST
# =========================================================

st.divider()

st.subheader("📅 5-Day Weather Forecast")

st.dataframe(

    forecast_df,

    use_container_width=True,

    hide_index=True
)


# =========================================================
# 5 DAY RAINFALL FORECAST
# =========================================================

st.subheader(
    "🌧️ 5-Day Rainfall Forecast"
)

forecast_chart = forecast_df.set_index(
    "Date"
)[["Rainfall (mm)"]]


st.line_chart(
    forecast_chart
)


# =========================================================
# SMART EARLY WARNING
# =========================================================

max_forecast_rainfall = forecast_df[
    "Rainfall (mm)"
].max()


max_rainfall_date = forecast_df.loc[

    forecast_df[
        "Rainfall (mm)"
    ].idxmax(),

    "Date"

]


if max_forecast_rainfall > historical_avg * 2:

    alert_level = "CRITICAL"

    alert_message = (

        f"Very heavy rainfall is expected around "
        f"{max_rainfall_date.strftime('%d %b')}. "
        f"Potential waterlogging risk."

    )


elif max_forecast_rainfall > historical_avg * 1.5:

    alert_level = "HIGH"

    alert_message = (

        f"Heavy rainfall is expected around "
        f"{max_rainfall_date.strftime('%d %b')}. "
        f"Residents should remain alert."

    )


elif max_forecast_rainfall > historical_avg:

    alert_level = "MODERATE"

    alert_message = (

        f"Rainfall may be above the historical average "
        f"around {max_rainfall_date.strftime('%d %b')}."

    )


else:

    alert_level = "LOW"

    alert_message = (

        "No significant rainfall anomaly detected "
        "in the forecast period."

    )


# =========================================================
# EARLY WARNING UI
# =========================================================

st.divider()

st.subheader(
    "🚨 Smart Early Warning System"
)

warning_col1, warning_col2 = st.columns(2)


with warning_col1:

    st.metric(

        "🌧️ Maximum Forecast Rainfall",

        f"{max_forecast_rainfall:.1f} mm"

    )


with warning_col2:

    st.metric(

        "⚠️ Alert Level",

        alert_level

    )


if alert_level == "CRITICAL":

    st.error(
        "🚨 CRITICAL ALERT\n\n"
        + alert_message
    )


elif alert_level == "HIGH":

    st.warning(
        "⚠️ HIGH ALERT\n\n"
        + alert_message
    )


elif alert_level == "MODERATE":

    st.info(
        "ℹ️ MODERATE ALERT\n\n"
        + alert_message
    )


else:

    st.success(
        "✅ LOW RISK\n\n"
        + alert_message
    )


# =========================================================
# WEATHER ANOMALY DETECTION
# =========================================================

st.divider()

st.subheader(
    "🔎 Weather Anomaly Detection"
)


if predicted_rainfall > historical_avg * 1.5:

    anomaly_status = "⚠️ Anomaly Detected"

    anomaly_message = (
        "Predicted rainfall is significantly "
        "above the historical range."
    )


elif predicted_rainfall < historical_avg * 0.5:

    anomaly_status = "⚠️ Anomaly Detected"

    anomaly_message = (
        "Predicted rainfall is significantly "
        "below the historical range."
    )


else:

    anomaly_status = "✅ Normal"

    anomaly_message = (
        "Predicted rainfall is within the "
        "expected historical range."
    )


anomaly_col1, anomaly_col2 = st.columns(2)


with anomaly_col1:

    st.metric(
        "Anomaly Status",
        anomaly_status
    )


with anomaly_col2:

    if "Anomaly Detected" in anomaly_status:

        st.warning(
            anomaly_message
        )

    else:

        st.info(
            anomaly_message
        )


# =========================================================
# RECOMMENDED ACTIONS
# =========================================================

st.divider()

st.subheader(
    "🎯 Recommended Actions"
)


if risk_level in ["HIGH", "VERY HIGH"]:

    st.error(
        "🚨 Immediate Attention Recommended"
    )

    st.markdown(
        """
        **Recommended Actions:**

        - Monitor rainfall and weather conditions closely
        - Prepare for possible waterlogging
        - Avoid unnecessary travel during heavy rainfall
        - Keep emergency contacts ready
        - Local authorities should monitor vulnerable areas
        """
    )


elif risk_level == "MODERATE":

    st.warning(
        "⚠️ Stay Alert"
    )

    st.markdown(
        """
        **Recommended Actions:**

        - Continue monitoring weather conditions
        - Stay updated with rainfall forecasts
        - Be prepared for moderate rainfall
        """ 
    )


else:

    st.success(
        "✅ No Immediate Action Required"
    )

    st.markdown(
        """
        **Recommended Actions:**

        - Continue monitoring weather conditions
        - No significant weather anomaly detected
        """ 
    )


# =========================================================
# WEATHER INTELLIGENCE SCORE
# =========================================================

st.divider()

st.subheader(
    "🧠 Weather Intelligence Score"
)


rainfall_factor = min(

    predicted_rainfall /
    max(historical_avg, 1),

    3

)


forecast_factor = min(

    max_forecast_rainfall /
    max(historical_avg, 1),

    3

)


score = (

    (rainfall_factor / 3) * 50

    +

    (forecast_factor / 3) * 50

)


score = min(
    round(score),
    100
)


if score < 30:

    score_status = "LOW RISK"


elif score < 60:

    score_status = "MODERATE RISK"


elif score < 80:

    score_status = "HIGH RISK"


else:

    score_status = "CRITICAL RISK"


score_col1, score_col2 = st.columns(2)


with score_col1:

    st.metric(
        "🧠 Intelligence Score",
        f"{score}/100"
    )


with score_col2:

    st.metric(
        "⚠️ Overall Status",
        score_status
    )


# =========================================================
# WEATHER SITUATION OVERVIEW
# =========================================================

st.divider()

st.subheader(
    "📋 Weather Situation Overview"
)


overview_col1, overview_col2, overview_col3 = st.columns(3)


with overview_col1:

    if deviation > 20:

        st.error(
            "🌧️ Rainfall\n\n"
            "Above normal range"
        )

    elif deviation < -20:

        st.info(
            "🌧️ Rainfall\n\n"
            "Below normal range"
        )

    else:

        st.success(
            "🌧️ Rainfall\n\n"
            "Within normal range"
        )


with overview_col2:

    if risk_level in ["HIGH", "VERY HIGH"]:

        st.error(
            "⚠️ Risk\n\n"
            f"{risk_level}"
        )

    elif risk_level == "MODERATE":

        st.warning(
            "⚠️ Risk\n\n"
            f"{risk_level}"
        )

    else:

        st.success(
            "⚠️ Risk\n\n"
            f"{risk_level}"
        )


with overview_col3:

    if alert_level in ["CRITICAL", "HIGH"]:

        st.error(
            "🚨 Alert\n\n"
            f"{alert_level}"
        )

    elif alert_level == "MODERATE":

        st.warning(
            "🚨 Alert\n\n"
            f"{alert_level}"
        )

    else:

        st.success(
            "🚨 Alert\n\n"
            "No immediate threat"
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🌦️ WeatherNex | Weather Intelligence & Early Warning Prototype"
)
