from pathlib import Path

import joblib
import pandas as pd
import streamlit as st


# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Coffee Demand Forecasting",
    page_icon="☕",
    layout="wide",
)


# -----------------------------
# Load trained model safely
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "coffee_demand_model.pkl"

model = joblib.load(MODEL_PATH)


# -----------------------------
# Custom styling
# -----------------------------
st.markdown(
    """
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
    line-height: 1.1;
}

.hero-subtitle {
    color: #8a5a3c;
    font-size: 1.05rem;
    margin-bottom: 2.3rem;
}

h1, h2, h3, label, p {
    color: #2b160d !important;
}

/* Header social links */
.social-links {
    display: flex;
    justify-content: flex-end;
    align-items: center;
    gap: 14px;
    padding-top: 18px;
}

.social-link {
    width: 38px;
    height: 38px;
    border-radius: 12px;
    background: #fffaf4;
    border: 1px solid #d1aa86;
    display: flex;
    align-items: center;
    justify-content: center;
    text-decoration: none;
    box-shadow: 0 4px 12px rgba(90, 45, 20, 0.08);
    transition: transform 0.2s ease, background 0.2s ease;
}

.social-link:hover {
    transform: translateY(-2px);
    background: #ead6c1;
}

.social-link img {
    width: 21px;
    height: 21px;
    object-fit: contain;
}


.dashboard-link {
    background: #7b3f1d;
    color: #fffaf4 !important;
    text-decoration: none;
    padding: 9px 14px;
    border-radius: 12px;
    font-size: 0.85rem;
    font-weight: 700;
    white-space: nowrap;
}

.dashboard-link:hover {
    background: #5a2d16;
    color: white !important;
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

/* Dropdown arrow */
div[data-baseweb="select"] svg {
    display: block !important;
    color: #8b451f !important;
}

/* Dropdown menu */
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

/* Generate button */
.stButton button {
    background: linear-gradient(135deg, #7b3f1d, #a65f2b) !important;
    color: #fffaf4 !important;
    border-radius: 18px !important;
    border: none !important;
    height: 3.4rem !important;
    font-weight: 800 !important;
    font-size: 1.05rem !important;
    box-shadow: 0 8px 18px rgba(90, 45, 20, 0.18);
    transition: transform 0.2s ease;
}

.stButton button p {
    color: #fffaf4 !important;
    font-weight: 800 !important;
}

.stButton button:hover {
    background: #5a2d16 !important;
    transform: translateY(-1px);
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
    box-shadow: 0 10px 24px rgba(90, 45, 20, 0.18);
}

.metric-card {
    background: #fffaf4;
    padding: 1.4rem;
    border-radius: 20px;
    border: 1px solid #e0c3a8;
    box-shadow: 0 6px 16px rgba(90, 45, 20, 0.10);
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
    color: inherit;
}

/* Streamlit top toolbar */
header[data-testid="stHeader"] {
    background: transparent !important;
}

div[data-testid="stToolbar"] {
    right: 1rem;
}

/* Mobile adjustments */
@media (max-width: 768px) {
    .hero-title {
        font-size: 2rem;
    }

    .hero-subtitle {
        margin-bottom: 1rem;
    }

    .social-links {
        justify-content: flex-start;
        padding-top: 0;
        padding-bottom: 1rem;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


# -----------------------------
# Header
# -----------------------------
header_left, header_right = st.columns([8, 1.4])

with header_left:
    st.markdown(
        '<div class="hero-title">☕ Coffee Demand Forecasting</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="hero-subtitle">
            Predict expected coffee demand using origin, roast profile,
            quality, pricing, and seasonality.
        </div>
        """,
        unsafe_allow_html=True,
    )

with header_right:
    st.markdown(
        (
            '<div class="social-links">'
            '<a class="dashboard-link" '
            'href="https://github.com/Drasti24/coffee-sourcing-analytics-dashboard" '
            'target="_blank" '
            'rel="noopener noreferrer">'
            'GitHub'
            '</a>'
            '<a class="dashboard-link" '
            'href="https://www.linkedin.com/in/pateldrasti" '
            'target="_blank" '
            'rel="noopener noreferrer">'
            'LinkedIn'
            '</a>'
            '<a class="dashboard-link" '
            'href="https://github.com/Drasti24/coffee-sourcing-analytics-dashboard/blob/main/Coffee_Sourcing_Analytics_Dashboard.pdf" '
            'target="_blank" '
            'rel="noopener noreferrer">'
            'Dashboard'
            '</a>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )

# -----------------------------
# Month mapping
# -----------------------------
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
    "December": 12,
}


# -----------------------------
# Main layout
# -----------------------------
left, right = st.columns([1.4, 1])


# -----------------------------
# Left side: inputs
# -----------------------------
with left:
    st.subheader("Coffee Profile")

    c1, c2 = st.columns(2)

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
                "Costa Rica",
            ],
        )

        roast_level = st.selectbox(
            "Roast Level",
            ["Light", "Medium", "Dark"],
        )

        process_method = st.selectbox(
            "Process Method",
            ["Washed", "Natural", "Honey", "Pulped Natural"],
        )

        selected_month = st.selectbox(
            "Order Month",
            list(months.keys()),
        )

        order_month = months[selected_month]

    with c2:
        altitude = st.slider(
            "Altitude",
            min_value=1000,
            max_value=2500,
            value=1600,
            step=50,
        )

        quality_score = st.slider(
            "Quality Score",
            min_value=80.0,
            max_value=95.0,
            value=87.0,
            step=0.1,
        )

        cost_per_kg = st.slider(
            "Cost per kg",
            min_value=1.0,
            max_value=20.0,
            value=8.0,
            step=0.1,
        )

        selling_price = st.slider(
            "Selling Price",
            min_value=5.0,
            max_value=40.0,
            value=18.99,
            step=0.1,
        )

    predict_clicked = st.button(
        "Generate Forecast",
        use_container_width=True,
    )


# -----------------------------
# Prepare model input
# -----------------------------
input_data = pd.DataFrame(
    {
        "origin": [origin],
        "roast_level": [roast_level],
        "process_method": [process_method],
        "altitude": [altitude],
        "quality_score": [quality_score],
        "cost_per_kg": [cost_per_kg],
        "selling_price": [selling_price],
        "order_month": [order_month],
    }
)


# -----------------------------
# Right side: output
# -----------------------------
with right:
    st.subheader("Forecast Output")

    if predict_clicked:
        prediction = float(model.predict(input_data)[0])

        demand = round(prediction)
        estimated_revenue = prediction * selling_price
        estimated_profit = prediction * (
            selling_price - cost_per_kg
        )

        margin = (
            estimated_profit / estimated_revenue
        ) * 100 if estimated_revenue > 0 else 0

        st.markdown(
            f"""
            <div class="result-card">
                <div class="small-label">Predicted Demand</div>
                <div class="big-number">{demand} units</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")

        m1, m2 = st.columns(2)

        with m1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="small-label">Revenue</div>
                    <div class="big-number">
                        ${estimated_revenue:,.0f}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with m2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="small-label">Profit</div>
                    <div class="big-number">
                        ${estimated_profit:,.0f}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.write("")

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="small-label">
                    Estimated Profit Margin
                </div>
                <div class="big-number">{margin:.1f}%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")

        if demand >= 60:
            st.success(
                "Recommendation: High demand expected — "
                "strong candidate for sourcing priority."
            )
        elif demand >= 45:
            st.info(
                "Recommendation: Moderate demand expected — "
                "maintain stable inventory."
            )
        else:
            st.warning(
                "Recommendation: Lower demand expected — "
                "monitor before increasing sourcing."
            )

    else:
        st.info("Enter coffee details and generate a forecast.")