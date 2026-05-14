import streamlit as st
import pandas as pd
import joblib

# Load trained model
model = joblib.load("coffee_demand_model.pkl")

# Page config
st.set_page_config(
    page_title="Coffee Demand Forecasting",
    page_icon="☕",
    layout="wide"
)

# -----------------------------
# Custom Styling
# -----------------------------
st.markdown("""
<style>
.stApp {
    background: #f5eee6;
    color: #2b160d;
}

.block-container {
    padding-top: 2.5rem;
    max-width: 1150px;
}

.hero-title {
    font-size: 2.8rem;
    font-weight: 800;
    color: #5a2d16;
    margin-bottom: 0.3rem;
}

.hero-subtitle {
    color: #8a5a3c;
    font-size: 1.05rem;
    margin-bottom: 3rem;
}

h1, h2, h3, label, p {
    color: #2b160d !important;
}

/* Inputs */
div[data-baseweb="select"] > div,
div[data-baseweb="base-input"] {
    background-color: #fffaf4 !important;
    border: 1px solid #d1aa86 !important;
    border-radius: 16px !important;
    color: #2b160d !important;
    box-shadow: none !important;
}

/* Input text */
div[data-baseweb="select"] span,
div[data-baseweb="base-input"] input {
    color: #2b160d !important;
}

/* Dropdown */
ul[role="listbox"] {
    background-color: #fffaf4 !important;
    border: 1px solid #d1aa86 !important;
    border-radius: 12px !important;
}

li[role="option"] {
    color: #2b160d !important;
    background-color: #fffaf4 !important;
}

li[role="option"]:hover {
    background-color: #ead6c1 !important;
}

/* Slider styling */
.stSlider [data-baseweb="slider"] > div > div {
    background: #d8c7b8 !important;
}

.stSlider [data-baseweb="slider"] div[role="slider"] {
    background-color: #8b451f !important;
    border-color: #8b451f !important;
}

.stSlider [data-baseweb="slider"] > div > div > div {
    background: #8b451f !important;
}

/* Button */
.stButton button {
    background: linear-gradient(135deg, #7b3f1d, #a65f2b) !important;
    color: #fffaf4 !important;
    border-radius: 18px !important;
    border: none !important;
    height: 3.4rem !important;
    font-weight: 800 !important;
    font-size: 1.05rem !important;
    box-shadow: 0 8px 18px rgba(90,45,20,0.18);
}

.stButton button p {
    color: #fffaf4 !important;
    font-weight: 800 !important;
}

.stButton button:hover {
    background: #5a2d16 !important;
}

.stButton button:hover p {
    color: #ffffff !important;
}

/* Result cards */
.result-card {
    background: linear-gradient(135deg, #7b3f1d, #b46a35);
    padding: 2rem;
    border-radius: 24px;
    color: white;
    text-align: center;
    box-shadow: 0 10px 24px rgba(90,45,20,0.18);
}

.metric-card {
    background: #fffaf4;
    padding: 1.4rem;
    border-radius: 20px;
    border: 1px solid #e0c3a8;
    box-shadow: 0 6px 16px rgba(90,45,20,0.10);
}

.small-label {
    color: #e7c4a3;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1.2px;
}

.big-number {
    font-size: 2.4rem;
    font-weight: 800;
}
            
/* Restore dropdown arrow */
div[data-baseweb="select"] svg {
    display: block !important;
    color: #8b451f !important;
}
            
header[data-testid="stHeader"] {
    background: transparent !important;
}

div[data-testid="stToolbar"] {
    right: 1rem;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown(
    '<div class="hero-title">☕ Coffee Demand Forecasting</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-subtitle">Predict expected coffee demand using origin, roast profile, quality, pricing, and seasonality.</div>',
    unsafe_allow_html=True
)


st.markdown(
    """
<div style="
position: fixed;
top: 20px;
right: 130px;
display: flex;
gap: 14px;
z-index: 9999;
">

<a href="https://github.com/YOUR_GITHUB" target="_blank">
    <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png"
         width="20">
</a>

<a href="https://linkedin.com/in/YOUR_LINKEDIN" target="_blank">
    <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png"
         width="20">
</a>

</div>
    """,
    unsafe_allow_html=True
)
# -----------------------------
# Layout
# -----------------------------
left, right = st.columns([1.4, 1])

# -----------------------------
# LEFT SIDE - INPUTS
# -----------------------------
with left:

    st.subheader("Coffee Profile")

    c1, c2 = st.columns(2)

    # LEFT COLUMN
    with c1:

        origin = st.selectbox(
            "Coffee Origin",
            [
                "Brazil",
                "Colombia",
                "Ethiopia",
                "Guatemala",
                "Kenya",
                "Honduras",
                "Costa Rica"
            ]
        )

        roast_level = st.selectbox(
            "Roast Level",
            ["Light", "Medium", "Dark"]
        )

        process_method = st.selectbox(
            "Process Method",
            ["Washed", "Natural", "Honey", "Pulped Natural"]
        )

        months = {
            "January": 1,
            "February": 2,
            "March": 3,
            "April": 4,
            "May": 5,
            "June": 6,
            "July": 7,
            "August": 8,
            "September": 9,
            "October": 10,
            "November": 11,
            "December": 12
        }

        selected_month = st.selectbox(
            "Order Month",
            list(months.keys())
        )

        order_month = months[selected_month]

    # RIGHT COLUMN
    with c2:

        altitude = st.slider(
            "Altitude",
            min_value=1000,
            max_value=2500,
            value=1600,
            step=50
        )

        quality_score = st.slider(
            "Quality Score",
            min_value=80.0,
            max_value=95.0,
            value=87.0,
            step=0.1
        )

        cost_per_kg = st.slider(
            "Cost per kg",
            min_value=1.0,
            max_value=20.0,
            value=8.0,
            step=0.1
        )

        selling_price = st.slider(
            "Selling Price",
            min_value=5.0,
            max_value=40.0,
            value=18.99,
            step=0.1
        )

    predict_clicked = st.button(
        "Generate Forecast",
        use_container_width=True
    )

# -----------------------------
# INPUT DATAFRAME
# -----------------------------
input_data = pd.DataFrame({
    "origin": [origin],
    "roast_level": [roast_level],
    "process_method": [process_method],
    "altitude": [altitude],
    "quality_score": [quality_score],
    "cost_per_kg": [cost_per_kg],
    "selling_price": [selling_price],
    "order_month": [order_month]
})

# -----------------------------
# RIGHT SIDE - OUTPUT
# -----------------------------
with right:

    st.subheader("Forecast Output")

    if predict_clicked:

        prediction = model.predict(input_data)[0]

        demand = round(prediction)

        estimated_revenue = prediction * selling_price

        estimated_profit = prediction * (
            selling_price - cost_per_kg
        )

        margin = (
            estimated_profit / estimated_revenue
        ) * 100 if estimated_revenue > 0 else 0

        # Demand Card
        st.markdown(f"""
        <div class="result-card">
            <div class="small-label">Predicted Demand</div>
            <div class="big-number">{demand} units</div>
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        m1, m2 = st.columns(2)

        # Revenue Card
        with m1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="small-label">Revenue</div>
                <div class="big-number">${estimated_revenue:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)

        # Profit Card
        with m2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="small-label">Profit</div>
                <div class="big-number">${estimated_profit:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)

        st.write("")

        # Margin Card
        st.markdown(f"""
        <div class="metric-card">
            <div class="small-label">Estimated Profit Margin</div>
            <div class="big-number">{margin:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        # Recommendation
        if demand >= 60:
            st.success(
                "Recommendation: High demand expected — strong candidate for sourcing priority."
            )

        elif demand >= 45:
            st.info(
                "Recommendation: Moderate demand expected — maintain stable inventory."
            )

        else:
            st.warning(
                "Recommendation: Lower demand expected — monitor before increasing sourcing."
            )

    else:
        st.info("Enter coffee details and generate a forecast.")

