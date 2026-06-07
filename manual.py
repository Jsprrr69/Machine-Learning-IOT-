import streamlit as st

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Fire Detection System Manual",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown(
    """
<style>

/* ===================================================== */
/* PREMIUM SIDEBAR */
/* ===================================================== */

[data-testid="stSidebar"]{
    background:
    linear-gradient(
        180deg,
        #081018 0%,
        #0f172a 50%,
        #111827 100%
    );

    border-right:
    1px solid rgba(
        255,
        140,
        66,
        0.15
    );
}

/* Sidebar Content */

[data-testid="stSidebar"] > div:first-child{

    padding-top:20px;
}

/* Logo Card */

.sidebar-logo{

    text-align:center;

    background:
    rgba(255,255,255,0.04);

    border:
    1px solid rgba(
        255,
        255,
        255,
        0.08
    );

    border-radius:20px;

    padding:20px;

    margin-bottom:25px;

    box-shadow:
    0 0 20px rgba(
        255,
        140,
        66,
        0.15
    );
}

.sidebar-logo h1{

    color:#ff8c42;

    margin:0;

    font-size:28px;
}

.sidebar-logo p{

    color:#bdbdbd;

    font-size:13px;

    margin-top:5px;
}

/* Menu Items */

div[role="radiogroup"] > label{

    background:
    rgba(255,255,255,0.03);

    border:
    1px solid rgba(
        255,
        255,
        255,
        0.04
    );

    border-radius:15px;

    padding:14px;

    margin-bottom:10px;

    transition:all .35s ease;

    font-weight:500;
}

/* Hover */

div[role="radiogroup"] > label:hover{

    transform:translateX(8px);

    border-color:#ff8c42;

    box-shadow:
    0 0 18px rgba(
        255,
        140,
        66,
        0.25
    );

    background:
    rgba(255,140,66,0.08);
}

/* Selected */

div[role="radiogroup"] label[data-selected="true"]{

    background:
    rgba(255,140,66,0.15);

    border-left:
    5px solid #ff8c42;

    box-shadow:
    0 0 25px rgba(
        255,
        140,
        66,
        0.35
    );
}

</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
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

.stApp::before {

    content: "";

    position: fixed;

    top: -50%;
    left: -50%;

    width: 200%;
    height: 200%;

    background:
    radial-gradient(
        circle at 20% 20%,
        rgba(255,140,66,0.15),
        transparent 30%
    ),

    radial-gradient(
        circle at 80% 30%,
        rgba(255,69,0,0.12),
        transparent 35%
    ),

    radial-gradient(
        circle at 50% 80%,
        rgba(255,180,80,0.08),
        transparent 40%
    );

    animation: fireGlow 15s ease-in-out infinite;

    z-index: -2;
}

@keyframes fireGlow {

    0%{
        transform: rotate(0deg);
    }

    50%{
        transform: rotate(180deg);
    }

    100%{
        transform: rotate(360deg);
    }
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

    position:absolute;

    width:8px;

    height:8px;

    background:#ff8c42;

    border-radius:50%;

    box-shadow:
        0 0 10px #ff8c42,
        0 0 20px #ff8c42,
        0 0 30px #ff4500;

    animation:
        emberFloat linear infinite;
}

@keyframes emberFloat {

    from {

        transform:
        translateY(100vh)
        translateX(0px);

        opacity:0;
    }

    20%{
        opacity:1;
    }

    100%{

        transform:
        translateY(-150px)
        translateX(120px);

        opacity:0;
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

    animation:
        flameText 2s ease-in-out infinite;

    text-shadow:
        0 0 10px #ff8c42,
        0 0 20px #ff4500,
        0 0 40px #ff8c42;
}

@keyframes flameText {

    0%{
        transform:translateY(0px);
    }

    50%{
        transform:translateY(-3px);
    }

    100%{
        transform:translateY(0px);
    }
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

    transform:
        translateY(-10px)
        scale(1.02);

    box-shadow:
        0 0 20px rgba(255,140,66,0.25),
        0 0 40px rgba(255,69,0,0.15),
        0 0 60px rgba(255,140,66,0.10);
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

/* ========================================= */
/* RESEARCHER PROFILE CARD */
/* ========================================= */

.researcher-name{
    text-align:center;
    color:white;
    font-weight:bold;
    font-size:20px;
    margin-top:10px;
}

.researcher-role{
    text-align:center;
    color:#cccccc;
    margin-bottom:15px;
}

.fb-button{
    display:block;
    text-align:center;
    padding:10px;
    border-radius:10px;
    background:rgba(255,140,66,0.15);
    color:white !important;
    text-decoration:none !important;
    transition:0.3s;
    border:1px solid rgba(255,140,66,0.3);
}

.fb-button:hover{
    background:rgba(255,140,66,0.35);
    transform:translateY(-3px);
}

[data-testid="stImage"] img{
    transition:0.3s;
    border-radius:15px;
}

[data-testid="stImage"] img:hover{
    transform:translateY(-8px);
    box-shadow:0 0 25px rgba(255,140,66,0.4);
}

/* ===================================================== */
/* SIDEBAR */
/* ===================================================== */

section[data-testid="stSidebar"] {
    background-color: #111111;
}

section[data-testid="stSidebar"] * {
    color: white;
    animation:
    sidebarGlow 5s ease infinite;

        @keyframes sidebarGlow {
    
        0%{
            filter:brightness(1);
        }
    
        50%{
            filter:brightness(1.15);
        }
    
        100%{
            filter:brightness(1);
        }
    }
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
""",
    unsafe_allow_html=True,
)

# ==========================================================
# EMBERS
# ==========================================================

st.markdown(
    """
<div class="fire-bg">

<div class="ember" style="left:5%;animation-duration:8s;"></div>
<div class="ember" style="left:10%;animation-duration:12s;"></div>
<div class="ember" style="left:15%;animation-duration:9s;"></div>
<div class="ember" style="left:20%;animation-duration:11s;"></div>
<div class="ember" style="left:25%;animation-duration:10s;"></div>

<div class="ember" style="left:30%;animation-duration:13s;"></div>
<div class="ember" style="left:35%;animation-duration:9s;"></div>
<div class="ember" style="left:40%;animation-duration:12s;"></div>
<div class="ember" style="left:45%;animation-duration:8s;"></div>

<div class="ember" style="left:50%;animation-duration:14s;"></div>
<div class="ember" style="left:55%;animation-duration:10s;"></div>
<div class="ember" style="left:60%;animation-duration:11s;"></div>
<div class="ember" style="left:65%;animation-duration:9s;"></div>

<div class="ember" style="left:70%;animation-duration:13s;"></div>
<div class="ember" style="left:75%;animation-duration:8s;"></div>
<div class="ember" style="left:80%;animation-duration:12s;"></div>

<div class="ember" style="left:85%;animation-duration:9s;"></div>
<div class="ember" style="left:90%;animation-duration:11s;"></div>
<div class="ember" style="left:95%;animation-duration:10s;"></div>

</div>
""",
    unsafe_allow_html=True,
)

# ==========================================================
# SIDEBAR MENU
# ==========================================================

st.sidebar.markdown(
    """
<div class="sidebar-logo">

<h1>🔥 MAIN MENU 🔥</h1>

<p>
IoT-Based Fire Detection
and Classification System
</p>

</div>
""",
    unsafe_allow_html=True,
)

st.sidebar.success("🟢 System Online")

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
        "👨‍💻 Developers",
    ],
)

st.sidebar.markdown("---")

st.sidebar.markdown(
    """
<center>

BS Electrical Engineering

4-1

Group 5

</center>
""",
    unsafe_allow_html=True,
)

# ==========================================================
# HOME PAGE
# ==========================================================

if page == "🏠 Home":

    st.markdown(
        """
    <div class='hero'>

    <h1>
    IoT-Based Fire Detection
    and Classification System
    with Automatic Breaker Isolation
    and SMS Notification
    </h1>

    <br>

    <p>
    An intelligent residential fire
    safety solution powered by
    IoT technology, Machine Learning,
    Automated Breaker Isolation,
    and Real-Time SMS Notification.
    </p>

    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
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
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
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
    """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
        <div class='metric-card'>
        <h1>98.80%</h1>
        <p>Model Accuracy</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
        <div class='metric-card'>
        <h1>100%</h1>
        <p>SMS Reliability</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
        <div class='metric-card'>
        <h1>100%</h1>
        <p>Breaker Reliability</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

# ==========================================================
# PLACEHOLDERS
# ==========================================================

elif page == "📖 About Project":

    st.markdown(
        """
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
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
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
    """,
        unsafe_allow_html=True,
    )

elif page == "⚙️ How It Works":

    st.divider()

    st.subheader("📌 Complete Workflow")

    st.markdown(
        """
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
    """,
        unsafe_allow_html=True,
    )

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

    st.markdown(
        """
<div class='glass fade-in'>

<h2 style='text-align:center; color:#ff8c42;'>

🧠 Step 3 — Machine Learning Classification

</h2>

<br>

<div style="
display:flex;
justify-content:center;
align-items:center;
gap:25px;
flex-wrap:wrap;
">

<div style="
background:rgba(255,255,255,0.05);
padding:20px;
border-radius:15px;
width:220px;
text-align:center;
">

<h3>📡 Sensor Readings</h3>

<p>
MQ2 Smoke Sensor<br>
MQ7 CO Sensor<br>
MQ135 Air Quality<br>
MCP9808 Temperature
</p>

</div>

<div style="
font-size:40px;
color:#ff8c42;
">
➡️
</div>

<div style="
background:rgba(255,140,66,0.08);
padding:20px;
border-radius:15px;
width:220px;
text-align:center;
">

<h3>🌲 Random Forest</h3>

<p>
Machine Learning Model
</p>

</div>

<div style="
font-size:40px;
color:#ff8c42;
">
➡️
</div>

<div style="
background:rgba(255,255,255,0.05);
padding:20px;
border-radius:15px;
width:220px;
text-align:center;
">

<h3>🚦 Classification</h3>

<p>

🟢 Non-Fire<br>

🟡 Potential Fire<br>

🔴 Fire

</p>

</div>

</div>

<br>

<p style='text-align:center; font-size:16px;'>

The Random Forest algorithm receives the combined
sensor readings, analyzes detected patterns, and
classifies the environment into Non-Fire,
Potential Fire, or Fire conditions.

</p>

</div>
""",
        unsafe_allow_html=True,
    )

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
    ## 📖 Introduction

    Welcome to the IoT-Based Fire Detection and Classification System
    with Automatic Breaker Isolation and SMS Notification.

    This system was developed to improve residential fire safety by
    combining multiple environmental sensors, machine learning,
    cloud monitoring, SMS notification, and automatic breaker isolation.

    Unlike traditional smoke alarms that may generate false alarms from
    cooking smoke, cigarette smoke, or steam, this system intelligently
    analyzes environmental conditions and classifies them into
    Non-Fire, Potential Fire, or Fire.
    """)

    st.divider()

    st.markdown("""
    ## 🚀 Getting Started
    """)

    st.markdown("""
    ### Step 1 — Power On the System

    Supply power to the system and ensure that all components are
    properly energized.

    Components include:

    • ESP32 Microcontroller

    • MQ2 Smoke Sensor

    • MQ7 Carbon Monoxide Sensor

    • MQ135 Air Quality Sensor

    • MCP9808 Temperature Sensor

    • SIM900A GSM Module

    • Relay Module

    Allow the sensors a few moments to stabilize after startup.
    """)

    st.divider()

    st.markdown("""
    ### Step 2 — Verify WiFi Connectivity

    The ESP32 automatically connects to the configured WiFi network.

    A stable internet connection is required for:

    • Cloud Database Communication

    • Dashboard Monitoring

    • Real-Time Data Updates

    • Remote Notifications
    """)

    st.divider()

    st.markdown("""
    <div class='glass fade-in'>

    <h2 style='text-align:center; color:#ff8c42;'>
    🔍 Step 3 — Verify Sensor Initialization
    </h2>

    <p style='text-align:center;'>
    Before using the system, ensure that all sensors
    have initialized correctly and are communicating
    with the ESP32.
    </p>

    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.success("""
🌫️ MQ2 Sensor

✓ Smoke Detection Sensor

Status: Initialized
""")

        st.success("""
☠️ MQ7 Sensor

✓ Carbon Monoxide Sensor

Status: Initialized
""")

    with col2:
        st.success("""
🌬️ MQ135 Sensor

✓ Air Quality Sensor

Status: Initialized
""")

        st.success("""
🌡️ MCP9808 Sensor

✓ Temperature Sensor

Status: Initialized
""")

    st.info("""
The system should only proceed to normal operation
once all four sensors have been successfully initialized
and are providing valid readings.
""")

    st.divider()

    st.markdown("""
    ### Step 4 — Open the Monitoring Dashboard

    Access the monitoring dashboard to observe the system status,
    sensor activity, and classification results in real time.

    The dashboard updates automatically whenever new sensor data
    is received.
    """)

    st.divider()

    st.markdown("""
    ### Step 5 — Machine Learning Classification

    The Random Forest model continuously analyzes sensor readings
    and determines the current environmental condition.
    """)

    tab1, tab2, tab3 = st.tabs(["🟢 Non-Fire", "🟡 Potential Fire", "🔴 Fire"])

    with tab1:

        st.success("""
🟢 NON-FIRE

Normal environmental conditions.

Examples:

• Cooking Smoke

• Cigarette or Vape Smoke

• Humidifier Vapor

• Soldering Smoke

• Steam from Boiling Water

System Response:

✓ Dashboard Updates

✓ Monitoring Continues

✓ No Emergency Action
""")

    with tab2:

        st.warning("""
🟡 POTENTIAL FIRE

Conditions that may lead to a fire.

Examples:

• Methane Gas

• Smoldering Cartons

• Early Smoke Accumulation

• Combustible Gas Presence

System Response:

✓ Warning Displayed

✓ SMS Notification Sent

✓ User Inspection Recommended
""")

    with tab3:

        st.error("""
🔴 FIRE

Active fire or dangerous condition.

Examples:

• Burning Paper

• Burning Leaves

• Burning Clothes

• Open Flame

• Significant Smoke and Heat

System Response:

✓ Breaker Isolation Activated

✓ Fire Alert Displayed

✓ SMS Notification Sent

✓ Alarm Activated
""")

    st.divider()

    st.markdown("""
    ## 📱 SMS Notification System

    The SIM900A GSM Module automatically sends SMS alerts whenever
    the system detects Potential Fire or Fire conditions.

    Potential Fire alerts notify users to inspect the area.

    Fire alerts notify users that a dangerous condition has been
    detected and immediate action may be necessary.
    """)

    st.divider()

    st.markdown("""
    ## ⚡ Automatic Breaker Isolation

    During a Fire classification, the relay module activates the
    breaker isolation mechanism.

    This disconnects electrical power from the protected circuit,
    helping reduce the risk of electrical faults and fire propagation.

    Breaker isolation is only activated during confirmed Fire conditions.
    """)

    st.divider()

    st.markdown("""
    ## 🖥️ Dashboard Monitoring

    The dashboard provides real-time monitoring of:

    • Sensor Activity

    • System Status

    • Classification Results

    • Alert Conditions

    • Historical Monitoring Data

    Users can continuously monitor the condition of the protected area
    through the dashboard interface.
    """)

    st.divider()

    st.markdown("""
    ## ⚠️ Important Reminders

    • Do not cover or obstruct the sensors.

    • Keep sensors clean and free from dust.

    • Ensure stable internet connectivity.

    • Verify GSM signal strength.

    • Regularly inspect wiring connections.

    • Test the system periodically.

    • Perform preventive maintenance when necessary.
    """)

    st.divider()

    st.success("""
✅ Normal Operation Summary

1. Sensors collect environmental data.

2. ESP32 transmits data to the cloud.

3. Random Forest analyzes sensor readings.

4. The system classifies the condition.

5. Dashboard updates automatically.

6. SMS notifications are sent when necessary.

7. Breaker isolation activates during confirmed Fire conditions.
""")

elif page == "🏗️ Architecture":

    st.title("🏗️ System Architecture")

    st.markdown("""
    ## Overall Workflow
    """)

    st.image("assets/arki2.jfif", use_container_width=True)

    st.info("""
The ESP32 collects sensor readings and sends them
to the cloud database.

The Random Forest model analyzes the data and
classifies the condition.

The system then performs automated responses.
""")

elif page == "📊 Performance":

    st.markdown(
        """
    <div class='glass'>
    <h1>📊 System Performance</h1>
    <p>
    Performance evaluation of the IoT-Based Fire Detection and Classification System.
    </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            """
        <div class='glass'>
        <h1 style='color:#ff8c42;'>98.80%</h1>
        <h3>🧠 Model Accuracy</h3>
        <p>Random Forest Classification Performance</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            """
        <div class='glass'>
        <h1 style='color:#ff8c42;'>100%</h1>
        <h3>📱 SMS Reliability</h3>
        <p>Notification Delivery Success Rate</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            """
        <div class='glass'>
        <h1 style='color:#ff8c42;'>100%</h1>
        <h3>⚡ Breaker Reliability</h3>
        <p>Automatic Isolation Success Rate</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.divider()

    st.subheader("🧠 Random Forest Results")

    st.success("""
The machine learning model achieved 98.80% overall accuracy.

The model successfully classified:

• Non-Fire

• Potential Fire

• Fire

conditions using four environmental sensors.
""")

    st.divider()

    st.subheader("📈 Class Performance")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.success("🟢 Non-Fire\n\nNormal Conditions")

    with col2:
        st.warning("🟡 Potential Fire\n\nEarly Warning")

    with col3:
        st.error("🔴 Fire\n\nEmergency")

    st.divider()

    st.subheader("🔥 Dataset")

    st.info("""
Approximately 13,000 sensor readings were collected from various residential scenarios.

Examples include:

• Cooking

• Cigarette Smoke

• Humidifier

• Methane Gas

• Burning Paper

• Burning Leaves

• Burning Clothes
""")

elif page == "📱 SMS Alerts":

    st.title("📱 SMS Notification System")

    st.markdown("""
    ## Potential Fire Alert
    """)

    st.warning("""
WARNING ALERT!!!

The system has detected Potential Fire event

Please check immediately.
    """)

    st.markdown("""
    ## Fire Alert
    """)

    st.error("""
EMERGENCY ALERT!!!

A fire incident has been detected!

Immediate response is needed.

(Sample SMS Alert for Homeowners/Tenants)

A fire incident has been detected!

Immediate response is needed.

Immediate response is needed at PUP CEA Manila!

(Sample SMS Alert for BFP)
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

    with st.expander("How does the system detect fire?"):
        st.write("""
The system analyzes smoke,
temperature, carbon monoxide,
and air quality data.
        """)

    with st.expander("What is Potential Fire?"):
        st.write("""
Potential Fire is an early warning
condition before an actual fire occurs.
        """)

    with st.expander("Why use Machine Learning?"):
        st.write("""
Machine Learning reduces false alarms
and improves classification accuracy.
        """)

    with st.expander("What happens during Fire?"):
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

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.image("assets/latuga.jfif", use_container_width=True)

        st.markdown(
            """
        <div class='researcher-name'>
        Jan Rhemle Latuga
        </div>

        <div class='researcher-role'>
        Researcher
        </div>

        <a class='fb-button'
        href='https://www.facebook.com/janrhemle.latuga.35'
        target='_blank'>
        🔗 Visit Facebook Profile
        </a>
        """,
            unsafe_allow_html=True,
        )

    with col2:

        st.image("assets/padilla.jfif", use_container_width=True)

        st.markdown(
            """
        <div class='researcher-name'>
        Mikaela Padilla
        </div>

        <div class='researcher-role'>
        Researcher
        </div>

        <a class='fb-button'
        href='https://www.facebook.com/EngrMika'
        target='_blank'>
        🔗 Visit Facebook Profile
        </a>
        """,
            unsafe_allow_html=True,
        )

    st.divider()

    col3, col4 = st.columns(2)

    with col3:

        st.image("assets/reyes.jfif", use_container_width=True)

        st.markdown(
            """
        <div class='researcher-name'>
        Amiell Reyes
        </div>

        <div class='researcher-role'>
        Researcher
        </div>

        <a class='fb-button'
        href='https://www.facebook.com/Reyessir.Amieeell'
        target='_blank'>
        🔗 Visit Facebook Profile
        </a>
        """,
            unsafe_allow_html=True,
        )

    with col4:

        st.image("assets/wenceslao.jfif", use_container_width=True)

        st.markdown(
            """
        <div class='researcher-name'>
        Allen Jasper Wenceslao
        </div>

        <div class='researcher-role'>
        Researcher
        </div>

        <a class='fb-button'
        href='https://www.facebook.com/jsprrr'
        target='_blank'>
        🔗 Visit Facebook Profile
        </a>
        """,
            unsafe_allow_html=True,
        )

    st.divider()

    st.success("""
    🔥 IoT-Based Fire Detection and Classification System

    with Automatic Breaker Isolation and SMS Notification
    """)

# FOOTER #
st.markdown(
    """
    
<div class='footer'>

🔥 IoT-Based Fire Detection and Classification System
with Automatic Breaker Isolation
and SMS Notification 🔥 

<br><br>

Bachelor of Science in Electrical Engineering

</div>
""",
    unsafe_allow_html=True,
)
