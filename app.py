import streamlit as st
import joblib
import pandas as pd


# ================= LOAD MODELS =================

crop_model = joblib.load("models/crop_model.pkl")
crop_columns = joblib.load("models/crop_columns.pkl")

fert_model = joblib.load("models/fert_model.pkl")
fert_columns = joblib.load("models/fert_columns.pkl")


# ================= FERTILIZER FULL FORM =================

fertilizer_names = {
    "DAP": "Diammonium Phosphate (DAP)",
    "Urea": "Urea (Nitrogen Fertilizer)",
    "MOP": "Muriate of Potash (MOP)",
    "SSP": "Single Super Phosphate (SSP)",
    "NPK": "Nitrogen Phosphorus Potassium (NPK)",
    "10-26-26": "NPK Fertilizer (10-26-26)",
    "14-35-14": "NPK Fertilizer (14-35-14)",
    "17-17-17": "Balanced NPK Fertilizer (17-17-17)",
    "20-20-0": "Nitrogen Phosphorus Fertilizer (20-20-0)"
}


# ================= CROP LOCAL NAMES =================

crop_names = {
    "paddy": "Paddy (Dhaan)",
    "wheat": "Wheat (Gehu)",
    "mungbean": "Mungbean (Moong Dal)",
    "millet": "Millet (Bajra)",
    "maize": "Maize (Makka)",
    "lentil": "Lentil (Masoor Dal)",
    "cotton": "Cotton (Kapas)",
    "groundnut": "Groundnut (Moongfali)",
    "sugarcane": "Sugarcane (Ganna)",
    "blackgram": "Blackgram (Urad Dal)",
    "pigeonpeas": "Pigeonpeas (Arhar Dal)",
    "chickpea": "Chickpea (Chana)",
    "grapes": "Grapes (Angoor)"
}


# ================= SUITABILITY =================

def crop_suitability(score):

    if score >= 70:
        return "🟢 Highly suitable conditions for this crop"

    elif score >= 40:
        return "🟡 Moderately suitable conditions"

    else:
        return "🟠 Low suitability under current conditions"



# ================= BACKGROUND =================

st.markdown("""
<style>

[data-testid="stAppViewContainer"] {

background:
linear-gradient(
rgba(255,255,255,0.60),
rgba(255,255,255,0.60)
),
url("https://img.magnific.com/free-photo/nature-product-backdrop-farm-sunlight_53876-147920.jpg");

background-size:cover;
background-position:center;
background-attachment:fixed;

}


[data-testid="stHeader"]{

background:rgba(0,0,0,0);

}

</style>
""", unsafe_allow_html=True)



# ================= HEADER =================

st.markdown("""
<h1 style="text-align:center;color:#2d6a4f;">
🌾 Krishi Kalyan AI
</h1>

<p style="text-align:center;font-size:16px;color:#1b4332;">
AI-based crop and fertilizer prediction system for smarter farming 🪴
</p>

""", unsafe_allow_html=True)



st.write("Enter soil and weather details 👇")



# ================= INPUTS =================

temperature = st.number_input(
    "🌡️ Temperature (°C)",
    0.0,
    50.0,
    25.0
)


humidity = st.number_input(
    "💧 Humidity (%)",
    0.0,
    100.0,
    50.0
)


rainfall = st.number_input(
    "🌧️ Rainfall (mm)",
    0.0,
    2000.0,
    100.0
)


ph = st.number_input(
    "⚗️ Soil pH",
    0.0,
    14.0,
    6.5
)


nitrogen = st.number_input(
    "🌿 Nitrogen (kg/ha)",
    0,
    150,
    50
)


phosphorous = st.number_input(
    "🌸 Phosphorous (kg/ha)",
    0,
    150,
    50
)


potassium = st.number_input(
    "⚡ Potassium (kg/ha)",
    0,
    200,
    50
)


soil = st.selectbox(
    "🧱 Soil Type",
    [
        "Alkaline",
        "Acidic",
        "Loamy",
        "Peaty",
        "Neutral"
    ]
)



# ================= PREDICT =================

if st.button("🚀 Predict"):


    # ================= CROP PREDICTION =================

    crop_input = {

        "Temperature": temperature,
        "Humidity": humidity,
        "Rainfall": rainfall,
        "PH": ph,
        "Nitrogen": nitrogen,
        "Phosphorous": phosphorous,
        "Potassium": potassium,
        "Soil": soil

    }



    crop_df = pd.get_dummies(
        pd.DataFrame([crop_input])
    )



    for col in crop_columns:

        if col not in crop_df.columns:
            crop_df[col] = 0



    crop_df = crop_df[crop_columns]



    crop_prob = crop_model.predict_proba(crop_df)[0]

    crop_classes = crop_model.classes_



    crop_results = sorted(
        zip(crop_classes, crop_prob),
        key=lambda x:x[1],
        reverse=True
    )



    top_crop, top_crop_prob = crop_results[0]


    top_crop_display = crop_names.get(
        top_crop.lower(),
        top_crop.title()
    )


    suitability = crop_suitability(
        top_crop_prob*100
    )



    # ================= FERTILIZER INPUT =================


    fert_input = {

        "Soil": soil,
        "Nitrogen": nitrogen,
        "Phosphorous": phosphorous,
        "Potassium": potassium,
        "PH": ph,
        "Rainfall": rainfall,
        "Temperature": temperature,
        "Crop": top_crop

    }


    fert_df = pd.get_dummies(
        pd.DataFrame([fert_input])
    )


    for col in fert_columns:

        if col not in fert_df.columns:
            fert_df[col] = 0


    fert_df = fert_df[fert_columns]



    # ================= TOP 2 FERTILIZER =================


    fert_prob = fert_model.predict_proba(fert_df)[0]

    fert_classes = fert_model.classes_


    fert_results = sorted(
        zip(fert_classes, fert_prob),
        key=lambda x:x[1],
        reverse=True
    )


    top_fertilizers = fert_results[:2]


    fert_display = []


    for fert, prob in top_fertilizers:

        fert_display.append(
            fertilizer_names.get(
                fert,
                fert
            )
        )


    fert_recommendation = "<br>".join(
        [
            f"🌿 {fert}"
            for fert in fert_display
        ]
    )
        # ================= RESULT =================

    st.markdown(
        "<h2 style='color:#2d6a4f;'>🌱 Krishi Kalyan AI Result</h2>",
        unsafe_allow_html=True
    )


    col1, col2 = st.columns(2)



    # ================= CROP CARD =================

    with col1:

        st.markdown(f"""

        <div style="
        background:linear-gradient(135deg,#1b4332,#2d6a4f);
        padding:20px;
        border-radius:18px;
        color:white;
        height:240px;
        display:flex;
        flex-direction:column;
        justify-content:flex-start;
        align-items:center;
        text-align:center;
        font-family:'Segoe UI',sans-serif;
        box-shadow:0px 6px 18px rgba(0,0,0,0.25);
        overflow:hidden;
        ">


        <h3 style="
        color:#95d5b2;
        font-size:18px;
        margin:0;
        ">
        🌾 Crop Recommendation
        </h3>


        <h1 style="
        font-size:26px;
        margin:10px 0 4px 0;
        ">
        {top_crop_display}
        </h1>


        <p style="
        font-size:15px;
        margin:2px 0;
        ">
        {suitability}
        </p>


        <p style="
        font-size:14px;
        color:#d8f3dc;
        ">
        🎯 Krishi Kalyan Score:
        <b>{top_crop_prob*100:.1f}%</b>
        </p>


        </div>

        """, unsafe_allow_html=True)




    # ================= FERTILIZER CARD =================

    with col2:

        st.markdown(f"""

        <div style="
        background:linear-gradient(135deg,#1b4332,#2d6a4f);
        padding:20px;
        border-radius:18px;
        color:white;
        height:240px;
        display:flex;
        flex-direction:column;
        justify-content:flex-start;
        align-items:center;
        text-align:center;
        font-family:'Segoe UI',sans-serif;
        box-shadow:0px 6px 18px rgba(0,0,0,0.25);
        overflow:hidden;
        ">


        <h3 style="
        color:#95d5b2;
        font-size:18px;
        margin:0;
        ">
        🧪 Fertilizer Recommendation
        </h3>



        <h2 style="
        font-size:18px;
        margin:15px 0;
        line-height:1.5;
        ">
        {fert_recommendation}
        </h2>



        <p style="
        font-size:13px;
        color:#d8f3dc;
        margin:5px 0 0 0;
        line-height:1.4;
        ">

        **Based on soil nutrients and predicted crop requirements

        </p>



        </div>

        """, unsafe_allow_html=True)




    # ================= ALTERNATIVE CROPS =================


    st.markdown(
        "<h3 style='color:#2d6a4f;margin-top:25px;'>🌱 Alternative Crops</h3>",
        unsafe_allow_html=True
    )



    for emoji,(crop,prob) in zip(
        ["🥈","🥉"],
        crop_results[1:3]
    ):


        st.markdown(f"""

        <div style="
        background:rgba(255,255,255,0.85);
        padding:10px 18px;
        border-radius:10px;
        margin-bottom:8px;
        display:flex;
        justify-content:space-between;
        align-items:center;
        font-size:16px;
        box-shadow:0px 2px 8px rgba(0,0,0,0.15);
        ">


        <span>
        {emoji}
        {crop_names.get(crop.lower(),crop.title())}
        </span>


        <b>
        {prob*100:.2f}%
        </b>


        </div>


        """, unsafe_allow_html=True)





    # ================= DISCLAIMER =================


    st.markdown("""

    <br>

    <div style="
    background:rgba(255,255,255,0.85);
    padding:15px;
    border-radius:12px;
    font-size:14px;
    color:#444;
    ">


    <b>Disclaimer:</b><br>

    Krishi Kalyan AI provides crop and fertilizer suggestions based on patterns learned from the dataset.
    This is a prototype decision-support tool and should be used with IoT systems and expert advice.


    </div>


    """, unsafe_allow_html=True)