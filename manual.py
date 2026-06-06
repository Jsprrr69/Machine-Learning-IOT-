import streamlit as st

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Fire Detection System Manual",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

/* Sidebar */
[data-testid="stSidebar"]{
    background: linear-gradient(
        180deg,
        #0f172a 0%,
        #1e293b 50%,
        #111827 100%
    );
}

/* Sidebar title */
.sidebar-title{
    text-align:center;
    color:white;
    font-size:24px;
    font-weight:bold;
    margin-bottom:20px;
}

/* Radio buttons */
div[role="radiogroup"] > label{
    background: rgba(255,255,255,0.05);
    border-radius:12px;
    padding:10px;
    margin-bottom:8px;
    transition:0.3s;
}

div[role="radiogroup"] > label:hover{
    background: rgba(255,140,66,0.25);
    transform:translateX(5px);
}

/* Selected menu */
div[role="radiogroup"] label[data-selected="true"]{
    background: rgba(255,140,66,0.35);
}

/* Sidebar text */
[data-testid="stSidebar"] *{
    color:white;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* ===================================================== */
/* MAIN BACKGROUND */
/* ===================================================== */

.stApp {
    background: linear-gradient(
        135deg,
        #090909,
        #121212,
        #1a0f0a
    );
    color: white;
}

/* ===================================================== */
/* EMBER ANIMATION */
/* ===================================================== */

.fire-bg {
    position: fixed;
    width: 100%;
    height: 100%;
    overflow: hidden;
    top: 0;
    left: 0;
    z-index: -1;
}

.ember {
    position: absolute;
    width: 6px;
    height: 6px;
    background: orange;
    border-radius: 50%;
    opacity: 0.7;
    animation: floatUp 10s linear infinite;
}

@keyframes floatUp {
    0% {
        transform: translateY(100vh);
        opacity: 0;
    }

    10% {
        opacity: 1;
    }

    100% {
        transform: translateY(-120px);
        opacity: 0;
    }
}

/* ========================================= */
/* FADE IN ANIMATION */
/* ========================================= */

.fade-in {
    animation: fadeIn 1.2s ease-in-out;
}

@keyframes fadeIn {

    from {
        opacity: 0;
        transform: translateY(20px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* ========================================= */
/* HERO GLOW */
/* ========================================= */

.hero h1 {
    text-shadow:
        0 0 10px rgba(255,140,66,0.4),
        0 0 20px rgba(255,140,66,0.3),
        0 0 30px rgba(255,140,66,0.2);
}

/* ========================================= */
/* TIMELINE */
/* ========================================= */

.timeline-card {
    background: rgba(255,255,255,0.04);
    border-left: 4px solid #ff8c42;
    padding: 20px;
    margin-bottom: 15px;
    border-radius: 10px;
}

/* ========================================= */
/* FOOTER */
/* ========================================= */

.footer {
    text-align:center;
    padding:40px;
    color:#999;
    margin-top:50px;
}

/* ========================================= */
/* TEAM CARD */
/* ========================================= */

.team-card {

    background: rgba(255,255,255,0.05);

    padding:20px;

    border-radius:15px;

    text-align:center;

    transition:0.3s;
}

.team-card:hover {

    transform:translateY(-8px);

    box-shadow:0 0 25px rgba(
        255,
        140,
        66,
        0.3
    );
}
            
/* ===================================================== */
/* HERO */
/* ===================================================== */

.hero {
    text-align: center;
    padding-top: 80px;
    padding-bottom: 80px;
}

.hero h1 {
    font-size: 3.5rem;
    color: #ff8c42;
}

.hero h3 {
    color: #d9d9d9;
    font-weight: 300;
}

.hero p {
    color: #bbbbbb;
    max-width: 900px;
    margin: auto;
    font-size: 18px;
}    

/* ===================================================== */
/* GLASS CARD */
/* ===================================================== */

.glass {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);

    border: 1px solid rgba(
        255,
        255,
        255,
        0.1
    );

    border-radius: 20px;

    padding: 30px;

    margin-top: 20px;
    margin-bottom: 20px;

    transition: 0.3s;
}

.glass:hover {
    transform: translateY(-5px);
}

/* ===================================================== */
/* METRIC CARDS */
/* ===================================================== */

.metric-card {
    background: rgba(255,140,66,0.08);
    border-radius: 20px;
    text-align: center;
    padding: 25px;
}

.metric-card h1 {
    color: #ff8c42;
}

.metric-card p {
    color: #cccccc;
}

/* ===================================================== */
/* SIDEBAR */
/* ===================================================== */

section[data-testid="stSidebar"] {
    background-color: #111111;
}

section[data-testid="stSidebar"] * {
    color: white;
}

/* ===================================================== */
/* SCROLLBAR */
/* ===================================================== */

::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-track {
    background: #111;
}

::-webkit-scrollbar-thumb {
    background: #ff8c42;
    border-radius: 20px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# EMBERS
# ==========================================================

st.markdown("""
<div class="fire-bg">
    <div class="ember" style="left:10%;animation-delay:0s;"></div>
    <div class="ember" style="left:20%;animation-delay:2s;"></div>
    <div class="ember" style="left:35%;animation-delay:4s;"></div>
    <div class="ember" style="left:50%;animation-delay:1s;"></div>
    <div class="ember" style="left:65%;animation-delay:3s;"></div>
    <div class="ember" style="left:80%;animation-delay:5s;"></div>
    <div class="ember" style="left:90%;animation-delay:6s;"></div>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# SIDEBAR MENU
# ==========================================================

st.sidebar.markdown("""
<div class="sidebar-title">

🔥 FIREGUARD AI 🔥

</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<p style='text-align:center;color:#bbbbbb;'>
Smart Fire Detection System
</p>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "",
    [
        "🏠 Home",
        "📖 About Project",
        "⚙️ How It Works",
        "🏗️ Architecture",
        "📚 User Manual",
        "📊 Performance",
        "📱 SMS Alerts",
        "🎥 Demonstration",
        "❓ FAQ",
        "👨‍💻 Developers"
    ]
)

# ==========================================================
# HOME PAGE
# ==========================================================

if page == "🏠 Home":

    st.markdown("""
    <div class='hero'>

    <h1>
    IoT-Based Fire Detection
    and Classification System
    </h1>

    <h3>
    with Automatic Breaker Isolation
    and SMS Notification
    </h3>

    <br>

    <p>
    An intelligent residential fire
    safety solution powered by
    IoT technology, Machine Learning,
    Automated Breaker Isolation,
    and Real-Time SMS Notification.
    </p>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
<div class='glass fade-in'>

<h2>🔥 Why This Project Matters</h2>

<p>
Traditional smoke alarms may generate false
alarms from cooking, cigarette smoke,
or steam.

Our system uses Machine Learning and
multiple sensors to intelligently classify
conditions and provide the appropriate
response.
</p>

</div>
""", unsafe_allow_html=True)

    st.markdown("""
    <div class='glass'>

    <h2>🔥 Project Overview</h2>

    <p>
    This project was developed to
    improve residential fire safety
    by combining environmental sensors,
    machine learning classification,
    cloud monitoring, GSM notification,
    and automatic breaker isolation.
    </p>

    <p>
    The system classifies conditions into:
    Non-Fire, Potential Fire, and Fire.
    Appropriate responses are then
    executed automatically.
    </p>

    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class='metric-card'>
        <h1>98.80%</h1>
        <p>Model Accuracy</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='metric-card'>
        <h1>100%</h1>
        <p>SMS Reliability</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class='metric-card'>
        <h1>100%</h1>
        <p>Breaker Reliability</p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================================
# PLACEHOLDERS
# ==========================================================

elif page == "📖 About Project":

    st.markdown("""
    <div class='glass'>

    <h1>📖 About the Project</h1>

    <p>
    Fire incidents remain one of the leading causes
    of property damage and loss of life in residential
    environments.
    </p>

    <p>
    Traditional fire alarms often rely on a single
    sensing mechanism and may generate false alarms
    due to cooking smoke, cigarette smoke,
    humidifiers, and other household activities.
    </p>

    <p>
    To address this problem, this project integrates
    multiple sensors, machine learning,
    cloud monitoring, SMS notification,
    and automatic breaker isolation.
    </p>

    <p>
    The system classifies conditions into:
    </p>

    <ul>
    <li>🟢 Non-Fire</li>
    <li>🟡 Potential Fire</li>
    <li>🔴 Fire</li>
    </ul>

    <p>
    Appropriate responses are automatically executed
    depending on the detected condition.
    </p>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='glass'>

    <h2>🎯 Objectives</h2>

    <ul>
    <li>Detect fire-related conditions in real time.</li>
    <li>Reduce false alarms.</li>
    <li>Provide early warning notifications.</li>
    <li>Automatically isolate electrical power.</li>
    <li>Improve residential fire safety.</li>
    </ul>

    </div>
    """, unsafe_allow_html=True)

elif page == "⚙️ How It Works":

    st.divider()

    st.subheader("📌 Complete Workflow")

    st.markdown("""
    <div class='timeline-card'>
    1️⃣ Sensors collect environmental data
    </div>

    <div class='timeline-card'>
    2️⃣ ESP32 transmits readings
    </div>

    <div class='timeline-card'>
    3️⃣ Cloud database stores information
    </div>

    <div class='timeline-card'>
    4️⃣ Random Forest analyzes data
    </div>

    <div class='timeline-card'>
    5️⃣ System classifies condition
    </div>

    <div class='timeline-card'>
    6️⃣ Dashboard updates in real time
    </div>

    <div class='timeline-card'>
    7️⃣ SMS notifications are sent
    </div>

    <div class='timeline-card'>
    8️⃣ Breaker isolation activates during Fire
    </div>
    """, unsafe_allow_html=True)

    st.title("⚙️ How The System Works")

    st.markdown("""
    ### 🔥 Step 1 — Data Collection
    """)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.success("🌫️ MQ2\n\nSmoke")

    with c2:
        st.success("☠️ MQ7\n\nCarbon Monoxide")

    with c3:
        st.success("🌬️ MQ135\n\nAir Quality")

    with c4:
        st.success("🌡️ MCP9808\n\nTemperature")

    st.divider()

    st.markdown("""
    ### ⚡ Step 2 — ESP32 Processing

    The ESP32 continuously gathers data from all
    sensors and transmits the information to
    the cloud database.
    """)

    st.divider()

    st.markdown("""
    ### 🧠 Step 3 — Machine Learning Classification
    """)

    st.code("""
Sensor Readings
       ↓
Random Forest
       ↓
Classification
    """, language="text")

    st.markdown("""
    The Random Forest model analyzes the sensor
    readings and determines the current condition.
    """)

    st.divider()

    st.markdown("""
    ### 🚦 Step 4 — Classification Result
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.success("""
🟢 NON-FIRE

Normal Conditions

No Action Required
""")

    with col2:
        st.warning("""
🟡 POTENTIAL FIRE

Warning Condition

SMS Sent
""")

    with col3:
        st.error("""
🔴 FIRE

Emergency Condition

SMS Sent
+
Breaker Trip
""")

    st.divider()

    st.markdown("""
    ### 📱 Step 5 — Automated Response

    Depending on the classification,
    the system automatically performs:

    • Dashboard Update

    • SMS Notification

    • Alarm Activation

    • Breaker Isolation
    """)

    

elif page == "📚 User Manual":

    st.title("📚 User Manual")

    st.markdown("""
    ## 🚀 Getting Started
    """)

    st.markdown("""
    ### Step 1

    Supply power to the system.
    Ensure that the ESP32,
    sensors, GSM module,
    and relay are properly powered.
    """)

    st.divider()

    st.markdown("""
    ### Step 2

    Connect the ESP32
    to the configured WiFi network.
    """)

    st.divider()

    st.markdown("""
    ### Step 3

    Verify sensor initialization.
    """)

    st.code("""
MQ2      ✓
MQ7      ✓
MQ135    ✓
MCP9808  ✓
    """)

    st.divider()

    st.markdown("""
    ### Step 4

    Open the monitoring dashboard.
    Observe the current status.
    """)

    st.divider()

    st.markdown("""
    ### Step 5

    Interpret the classification result.
    """)

    tab1, tab2, tab3 = st.tabs(
        [
            "🟢 Non-Fire",
            "🟡 Potential Fire",
            "🔴 Fire"
        ]
    )

    with tab1:

        st.success("""
Examples:

• Cooking

• Cigarette Smoke

• Humidifier

• Solder Smoke

• Boiling Water
""")

    with tab2:

        st.warning("""
Examples:

• Methane Gas

• Smoldering Cartons

• Early Smoke Buildup

Warning SMS will be sent.
""")

    with tab3:

        st.error("""
Examples:

• Burning Paper

• Burning Leaves

• Burning Clothes

• Open Flame

Actions:

✓ SMS Sent

✓ Alarm Activated

✓ Breaker Isolation
""")

    st.divider()

    st.markdown("""
    ## ⚠️ Important Reminders

    • Do not cover sensors.

    • Ensure internet connectivity.

    • Verify GSM signal strength.

    • Regularly inspect wiring.

    • Test the system periodically.
    """)

elif page == "🏗️ Architecture":

    st.title("🏗️ System Architecture")

    st.markdown("""
    ## Overall Workflow
    """)

    st.image(
        "assets/arki.jfif",
        use_container_width=True
)

    st.info("""
The ESP32 collects sensor readings and sends them
to the cloud database.

The Random Forest model analyzes the data and
classifies the condition.

The system then performs automated responses.
""")

elif page == "📊 Performance":

    st.title("📊 System Performance")

    c1,c2,c3 = st.columns(3)

    with c1:
        st.metric(
            "Model Accuracy",
            "98.80%"
        )

    with c2:
        st.metric(
            "SMS Reliability",
            "100%"
        )

    with c3:
        st.metric(
            "Breaker Reliability",
            "100%"
        )

    st.divider()

    st.subheader("🧠 Random Forest Results")

    st.success("""
The machine learning model achieved
98.80% overall accuracy.

The model successfully classified:

• Non-Fire

• Potential Fire

• Fire

conditions using four environmental sensors.
""")

    st.divider()

    st.subheader("📈 Class Performance")

    st.table({
        "Class":[
            "Non-Fire",
            "Potential Fire",
            "Fire"
        ],

        "Description":[
            "Normal Conditions",
            "Early Warning",
            "Emergency"
        ]
    })

    st.divider()

    st.subheader("🔥 Dataset")

    st.info("""
Approximately 13,000 sensor readings were
collected from various residential scenarios.

These include:

• Cooking

• Cigarette Smoke

• Humidifier

• Methane Gas

• Burning Paper

• Burning Leaves

• Burning Clothes

and other fire-related conditions.
""")

elif page == "📱 SMS Alerts":

    st.title("📱 SMS Notification System")

    st.markdown("""
    ## Potential Fire Alert
    """)

    st.warning("""
WARNING

Potential Fire Detected

Please inspect the area immediately.
    """)

    st.markdown("""
    ## Fire Alert
    """)

    st.error("""
EMERGENCY ALERT

Fire Detected

Breaker Isolation Activated

Please evacuate immediately.
    """)

    st.success("""
The GSM module automatically sends SMS
notifications whenever the system detects
Potential Fire or Fire conditions.
""")
    
elif page == "🎥 Demonstration":

    st.title("🎥 System Demonstration")

    st.video("assets/demo.mp4")
    
elif page == "❓ FAQ":

    st.title("❓ Frequently Asked Questions")

    with st.expander(
        "How does the system detect fire?"
    ):
        st.write("""
The system analyzes smoke,
temperature, carbon monoxide,
and air quality data.
        """)

    with st.expander(
        "What is Potential Fire?"
    ):
        st.write("""
Potential Fire is an early warning
condition before an actual fire occurs.
        """)

    with st.expander(
        "Why use Machine Learning?"
    ):
        st.write("""
Machine Learning reduces false alarms
and improves classification accuracy.
        """)

    with st.expander(
        "What happens during Fire?"
    ):
        st.write("""
The system sends SMS alerts,
activates alarms,
and trips the breaker.
        """)

elif page == "👨‍💻 Developers":

    st.title("👨‍💻 Development Team")

    st.markdown("""
    ### Research Team

    Bachelor of Science in Electrical Engineering

    Group 5
    """)

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.markdown("""
    <div class='team-card'>
    👨‍💻<br><br>
    Latuga
    </div>
    """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
    <div class='team-card'>
    👨‍💻<br><br>
    Padilla
    </div>
    """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
    <div class='team-card'>
    👨‍💻<br><br>
    Reyes
    </div>
    """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
    <div class='team-card'>
    👨‍💻<br><br>
    Wenceslao
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.success("""
IoT-Based Fire Detection and Classification System

with Automatic Breaker Isolation
and SMS Notification
""")

# FOOTER #
st.markdown("""
    
<div class='footer'>

🔥 IoT-Based Fire Detection and Classification System

with Automatic Breaker Isolation
and SMS Notification

<br><br>

Bachelor of Science in Electrical Engineering

</div>
""", unsafe_allow_html=True)
