import streamlit as st
import math
import pandas as pd

# ========================================
# AASHTO 1993 Pavement Design Calculator
# ========================================

st.set_page_config(page_title="AASHTO 1993 - Structural Number", layout="wide")

st.title("🛣️ AASHTO 1993 Pavement Design Calculator")
st.markdown("### คำนวณ Structural Number สำหรับผิวทางลาดยาง")

# Sidebar for unit selection
st.sidebar.header("⚙️ การตั้งค่า")
unit_system = st.sidebar.radio("ระบบหน่วย", ["Metric (SI)", "Imperial (US)"])

# Tab selection
tab1, tab2, tab3 = st.tabs(["📊 คำนวณ Required SN", "🔍 คำนวณ Existing SN", "ℹ️ คำอธิบาย"])

# ========================================
# TAB 1: Required SN Calculation
# ========================================
with tab1:
    st.header("คำนวณ Structural Number ที่ต้องการ (Required SN)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("ข้อมูลการจราจร")
        
        # ESAL input
        if unit_system == "Metric (SI)":
            w18 = st.number_input(
                "ปริมาณจราจรสะสม (W₁₈) - ESAL",
                min_value=1e4,
                max_value=1e9,
                value=1e6,
                format="%.2e",
                help="Equivalent Single Axle Load สะสมตลอดอายุการใช้งาน"
            )
        else:
            w18 = st.number_input(
                "Cumulative Traffic (W₁₈) - ESAL",
                min_value=1e4,
                max_value=1e9,
                value=1e6,
                format="%.2e",
                help="Equivalent Single Axle Load over design life"
            )
        
        st.subheader("ความน่าเชื่อถือ")
        
        reliability = st.slider(
            "Reliability (R) %",
            min_value=50,
            max_value=99,
            value=90,
            help="ระดับความน่าเชื่อถือของการออกแบบ"
        )
        
        # Standard Normal Deviate (ZR) based on Reliability
        zr_values = {
            50: 0.000, 60: -0.253, 70: -0.524, 75: -0.674,
            80: -0.841, 85: -1.037, 90: -1.282, 95: -1.645,
            99: -2.327, 99.9: -3.090
        }
        
        # Find closest reliability value
        closest_r = min(zr_values.keys(), key=lambda x: abs(x - reliability))
        zr = zr_values[closest_r]
        
        st.info(f"Standard Normal Deviate (Zᵣ) = {zr:.3f}")
        
        so = st.number_input(
            "Overall Standard Deviation (S₀)",
            min_value=0.30,
            max_value=0.50,
            value=0.45,
            step=0.01,
            help="ค่าเบี่ยงเบนมาตรฐานรวม (โดยทั่วไป 0.40-0.50)"
        )
    
    with col2:
        st.subheader("คุณสมบัติดินเดิม")
        
        soil_input_type = st.radio(
            "เลือกวิธีระบุคุณสมบัติดิน",
            ["CBR (%)", "Resilient Modulus (Mᵣ)"]
        )
        
        if soil_input_type == "CBR (%)":
            cbr = st.number_input(
                "CBR ของดินเดิม (%)",
                min_value=1.0,
                max_value=100.0,
                value=5.0,
                step=0.5
            )
            # Convert CBR to Mr (psi) using correlation: Mr (psi) = 1500 × CBR
            mr_psi = 1500 * cbr
            st.info(f"Resilient Modulus (Mᵣ) ≈ {mr_psi:,.0f} psi")
        else:
            if unit_system == "Metric (SI)":
                mr_mpa = st.number_input(
                    "Resilient Modulus (MPa)",
                    min_value=10.0,
                    max_value=300.0,
                    value=50.0,
                    step=5.0
                )
                # Convert MPa to psi (1 MPa = 145.038 psi)
                mr_psi = mr_mpa * 145.038
            else:
                mr_psi = st.number_input(
                    "Resilient Modulus (psi)",
                    min_value=1500.0,
                    max_value=50000.0,
                    value=7500.0,
                    step=500.0
                )
        
        st.subheader("ความสามารถในการรับน้ำหนัก")
        
        psi_initial = st.number_input(
            "Initial Serviceability (p₀)",
            min_value=3.0,
            max_value=5.0,
            value=4.2,
            step=0.1,
            help="ความสามารถในการรับน้ำหนักเริ่มต้น (ทางใหม่ โดยทั่วไป 4.0-4.5)"
        )
        
        psi_terminal = st.number_input(
            "Terminal Serviceability (pₜ)",
            min_value=1.5,
            max_value=3.5,
            value=2.5,
            step=0.1,
            help="ความสามารถในการรับน้ำหนักสุดท้าย (โดยทั่วไป 2.0-3.0)"
        )
        
        delta_psi = psi_initial - psi_terminal
        st.info(f"ΔPSI = {delta_psi:.1f}")
    
    # Calculate Required SN using AASHTO 1993 equation
    st.markdown("---")
    
    if st.button("🧮 คำนวณ Required SN", type="primary"):
        # AASHTO 1993 equation (iterative solution required)
        # log₁₀(W₁₈) = Zᵣ×S₀ + 9.36×log₁₀(SN+1) - 0.20 + [log₁₀(ΔPSI/(4.2-1.5))] / [0.40 + 1094/(SN+1)⁵·¹⁹] + 2.32×log₁₀(Mᵣ) - 8.07
        
        # Iterative solution for SN
        def aashto_equation(sn, w18, zr, so, delta_psi, mr):
            log_w18_calc = (
                zr * so +
                9.36 * math.log10(sn + 1) - 0.20 +
                (math.log10(delta_psi / (4.2 - 1.5)) / 
                 (0.40 + 1094 / ((sn + 1) ** 5.19))) +
                2.32 * math.log10(mr) - 8.07
            )
            return log_w18_calc
        
        # Newton-Raphson iteration
        sn_required = 3.0  # Initial guess
        log_w18_target = math.log10(w18)
        
        for _ in range(100):  # Max iterations
            f = aashto_equation(sn_required, w18, zr, so, delta_psi, mr_psi) - log_w18_target
            
            # Numerical derivative
            h = 0.001
            df = (aashto_equation(sn_required + h, w18, zr, so, delta_psi, mr_psi) - 
                  aashto_equation(sn_required, w18, zr, so, delta_psi, mr_psi)) / h
            
            sn_new = sn_required - f / df
            
            if abs(sn_new - sn_required) < 0.001:
                sn_required = sn_new
                break
            
            sn_required = sn_new
        
        # Display results
        st.success(f"### ✅ Required Structural Number (SN) = **{sn_required:.2f}**")
        
        # Show calculation summary
        st.subheader("สรุปค่าที่ใช้ในการคำนวณ")
        
        results_df = pd.DataFrame({
            "Parameter": [
                "Cumulative ESAL (W₁₈)",
                "Reliability (R)",
                "Standard Normal Deviate (Zᵣ)",
                "Overall Std Deviation (S₀)",
                "Resilient Modulus (Mᵣ)",
                "Initial PSI (p₀)",
                "Terminal PSI (pₜ)",
                "ΔPSI",
                "**Required SN**"
            ],
            "Value": [
                f"{w18:.2e}",
                f"{reliability}%",
                f"{zr:.3f}",
                f"{so:.2f}",
                f"{mr_psi:,.0f} psi",
                f"{psi_initial:.1f}",
                f"{psi_terminal:.1f}",
                f"{delta_psi:.1f}",
                f"**{sn_required:.2f}**"
            ]
        })
        
        st.table(results_df)
        
        # Suggested layer thicknesses
        st.subheader("💡 ตัวอย่างความหนาชั้นทาง")
        st.info("""
        **Layer Coefficients ทั่วไป:**
        - Asphalt Concrete (a₁) = 0.44
        - Base Course (a₂) = 0.14
        - Subbase (a₃) = 0.11
        
        **ตัวอย่างการคำนวณ:**
        - SN = a₁×D₁ + a₂×D₂ + a₃×D₃
        - ตัวอย่าง: SN = 0.44×(100mm) + 0.14×(200mm) + 0.11×(300mm) = {:.2f}
        """.format(0.44*100 + 0.14*200 + 0.11*300))

# ========================================
# TAB 2: Existing SN Calculation
# ========================================
with tab2:
    st.header("คำนวณ Structural Number ที่มีอยู่ (Existing SN)")
    st.markdown("คำนวณจากความหนาและค่า Layer Coefficient ของแต่ละชั้น")
    
    st.markdown("**สูตร:** SN = a₁×D₁×m₁ + a₂×D₂×m₂ + a₃×D₃×m₃")
    st.markdown("- aᵢ = Layer coefficient")
    st.markdown("- Dᵢ = ความหนา (inches หรือ mm)")
    st.markdown("- mᵢ = Drainage coefficient")
    
    st.markdown("---")
    
    # Unit conversion factor
    if unit_system == "Metric (SI)":
        unit_label = "mm"
        conversion_factor = 1.0 / 25.4  # mm to inches
    else:
        unit_label = "inches"
        conversion_factor = 1.0
    
    # Number of layers
    num_layers = st.number_input("จำนวนชั้นทาง", min_value=1, max_value=5, value=3)
    
    st.subheader("ข้อมูลแต่ละชั้นทาง")
    
    layer_data = []
    
    for i in range(num_layers):
        st.markdown(f"### ชั้นที่ {i+1}")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            thickness = st.number_input(
                f"ความหนา D₍{i+1}₎ ({unit_label})",
                min_value=0.0,
                value=100.0 if i == 0 else 200.0,
                step=10.0,
                key=f"thickness_{i}"
            )
        
        with col2:
            # Common layer coefficient values
            default_a = [0.44, 0.14, 0.11, 0.10, 0.08]
            layer_coef = st.number_input(
                f"Layer Coefficient a₍{i+1}₎",
                min_value=0.0,
                max_value=1.0,
                value=default_a[i] if i < len(default_a) else 0.10,
                step=0.01,
                key=f"coef_{i}",
                help="AC=0.44, Base=0.14, Subbase=0.11"
            )
        
        with col3:
            drainage_coef = st.number_input(
                f"Drainage Coefficient m₍{i+1}₎",
                min_value=0.5,
                max_value=1.4,
                value=1.0,
                step=0.05,
                key=f"drainage_{i}",
                help="1.0 = Good drainage, <1.0 = Poor drainage"
            )
        
        layer_data.append({
            "Layer": f"Layer {i+1}",
            "Thickness": thickness,
            "Layer Coef (a)": layer_coef,
            "Drainage Coef (m)": drainage_coef,
            "SN Contribution": thickness * conversion_factor * layer_coef * drainage_coef
        })
    
    st.markdown("---")
    
    if st.button("🧮 คำนวณ Existing SN", type="primary"):
        # Calculate total SN
        total_sn = sum([layer["SN Contribution"] for layer in layer_data])
        
        st.success(f"### ✅ Existing Structural Number (SN) = **{total_sn:.2f}**")
        
        # Show detailed breakdown
        st.subheader("รายละเอียดการคำนวณ")
        
        df = pd.DataFrame(layer_data)
        df["SN Contribution"] = df["SN Contribution"].round(2)
        
        st.dataframe(df, use_container_width=True)
        
        # Add total row
        st.markdown(f"**รวม SN = {total_sn:.2f}**")
        
        # Visualization
        import plotly.graph_objects as go
        
        fig = go.Figure(data=[
            go.Bar(
                x=[layer["Layer"] for layer in layer_data],
                y=[layer["SN Contribution"] for layer in layer_data],
                text=[f"{layer['SN Contribution']:.2f}" for layer in layer_data],
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title="Structural Number Contribution by Layer",
            xaxis_title="Layer",
            yaxis_title="SN Contribution",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

# ========================================
# TAB 3: Information
# ========================================
with tab3:
    st.header("ℹ️ คำอธิบายและข้อมูลอ้างอิง")
    
    st.markdown("""
    ## AASHTO 1993 Pavement Design Method
    
    ### สมการหลัก (Required SN)
    
    ```
    log₁₀(W₁₈) = Zᵣ×S₀ + 9.36×log₁₀(SN+1) - 0.20 + 
                 [log₁₀(ΔPSI/(4.2-1.5))] / [0.40 + 1094/(SN+1)⁵·¹⁹] + 
                 2.32×log₁₀(Mᵣ) - 8.07
    ```
    
    ### ตัวแปรในสมการ
    
    - **W₁₈** = Cumulative 18-kip ESAL (Equivalent Single Axle Load)
    - **Zᵣ** = Standard Normal Deviate (ขึ้นกับ Reliability)
    - **S₀** = Overall Standard Deviation (0.40-0.50)
    - **SN** = Structural Number
    - **ΔPSI** = pᵢ - pₜ (Initial PSI - Terminal PSI)
    - **Mᵣ** = Resilient Modulus ของดินเดิม (psi)
    
    ### Layer Coefficient (aᵢ) ทั่วไป
    
    | ชั้นทาง | Layer Coefficient (aᵢ) |
    |---------|------------------------|
    | Asphalt Concrete | 0.40 - 0.44 |
    | Cement Treated Base | 0.20 - 0.28 |
    | Crushed Stone Base | 0.12 - 0.14 |
    | Soil Cement Subbase | 0.10 - 0.12 |
    | Granular Subbase | 0.08 - 0.11 |
    
    ### Drainage Coefficient (mᵢ)
    
    | Drainage Quality | mᵢ |
    |------------------|-----|
    | Excellent | 1.20 - 1.35 |
    | Good | 1.00 - 1.15 |
    | Fair | 0.80 - 1.00 |
    | Poor | 0.60 - 0.80 |
    | Very Poor | 0.40 - 0.60 |
    
    ### Reliability (R) และ Zᵣ
    
    | Reliability (%) | Zᵣ |
    |----------------|-----|
    | 50 | 0.000 |
    | 80 | -0.841 |
    | 85 | -1.037 |
    | 90 | -1.282 |
    | 95 | -1.645 |
    | 99 | -2.327 |
    
    ### CBR to Resilient Modulus Correlation
    
    ```
    Mᵣ (psi) ≈ 1500 × CBR (%)
    ```
    
    ### อ้างอิง
    
    - AASHTO Guide for Design of Pavement Structures, 1993
    - AASHTO Designation: M 145 (Soil Classification)
    
    ---
    
    **หมายเหตุ:** โปรแกรมนี้เป็นเครื่องมือช่วยคำนวณเบื้องต้น 
    ควรมีวิศวกรผู้เชี่ยวชาญตรวจสอบการออกแบบก่อนนำไปใช้งานจริง
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>AASHTO 1993 Pavement Design Calculator v1.0</p>
    <p>สร้างด้วย Streamlit 🎈</p>
</div>
""", unsafe_allow_html=True)
