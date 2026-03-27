import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Rigid Pavement Field Design", layout="wide")

html_concrete_system = """
<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700&family=IBM+Plex+Mono&display=swap" rel="stylesheet">
<style>
    :root {
        --bg: #0d1117; --card: #161b22; --border: #30363d; --accent: #00d2ff; --text: #e6edf3;
        --slab: #e2e8f0; --base: #854d0e; --sg: #166534;
    }
    body { font-family: 'Sarabun', sans-serif; background: var(--bg); color: var(--text); padding: 20px; }
    .container { max-width: 1200px; margin: auto; }
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 25px; }
    .card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 20px; margin-bottom: 20px; }
    h2, h3 { color: var(--accent); margin-top: 0; border-bottom: 1px solid var(--border); padding-bottom: 8px; }
    h4 { color: #58a6ff; margin: 15px 0 5px 0; font-size: 0.9rem; border-left: 3px solid var(--accent); padding-left: 10px; }
    
    .input-row { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 10px; }
    label { display: block; font-size: 0.75rem; color: #8b949e; margin-bottom: 3px; }
    input, select { width: 100%; padding: 8px; background: #0d1117; border: 1px solid var(--border); color: #fff; border-radius: 6px; font-family: 'IBM Plex Mono'; }
    
    .btn { width: 100%; padding: 18px; background: var(--accent); border: none; border-radius: 8px; font-weight: bold; cursor: pointer; margin-top: 15px; font-size: 1rem; color: #000; }
    .note-panel { background: #010409; border-left: 4px solid var(--accent); padding: 15px; border-radius: 4px; margin-top: 15px; display: none; font-size: 0.9rem; line-height: 1.6; }
    
    .diagram-area { background: #010409; border: 1px solid var(--border); border-radius: 10px; padding: 40px 20px; min-height: 450px; text-align: center; }
    .slab-layer { margin: 0 auto; width: 75%; background: var(--slab); color: #1e293b; display: flex; align-items: center; justify-content: center; font-weight: bold; border: 2px solid #94a3b8; transition: height 0.5s ease; position: relative; }
    .dim-line { position: absolute; left: calc(100% + 15px); color: var(--accent); font-family: 'IBM Plex Mono'; white-space: nowrap; }
</style>
</head>
<body>
<div class="container">
    <div class="grid">
        <div>
            <div class="card">
                <h3>🛠️ ขั้นตอนที่ 1: ข้อมูลสนาม (Field Data)</h3>
                
                <h4>🚛 ข้อมูลจราจร (Traffic Analysis)</h4>
                <div class="input-row">
                    <div><label>จำนวนรถบรรทุก (คัน/วัน/ทิศทาง)</label><input type="number" id="f_truck" value="800"></div>
                    <div><label>อายุออกแบบ (ปี)</label><input type="number" id="f_years" value="20"></div>
                </div>
                <div class="input-row">
                    <div>
                        <label>ประเภทรถ (TF)</label>
                        <select id="f_tf">
                            <option value="1.2">รถบรรทุก 10 ล้อ (TF=1.2)</option>
                            <option value="2.5">รถพ่วง/เทรลเลอร์ (TF=2.5)</option>
                            <option value="0.4">รถ 6 ล้อใหญ่ (TF=0.4)</option>
                        </select>
                    </div>
                    <div><label>Growth Rate (%)</label><input type="number" id="f_growth" value="4"></div>
                </div>

                <h4>🌱 ข้อมูลดินฐานราก (Subgrade Data)</h4>
                <div class="input-row">
                    <div><label>ค่า CBR ดินเดิม (%)</label><input type="number" id="f_cbr" value="4"></div>
                    <div><label>k-value (psi/in) - คำนวณให้</label><input type="number" id="f_k" disabled></div>
                </div>
            </div>

            <div class="card">
                <h3>📐 ขั้นตอนที่ 2: เลือกชนิดและวัสดุ</h3>
                <div class="input-row">
                    <div>
                        <label>ประเภทคอนกรีต</label>
                        <select id="f_type">
                            <option value="JPCP">JPCP (มีรอยต่อ+Dowel)</option>
                            <option value="JRCP">JRCP (มีเหล็กตะแกรง)</option>
                            <option value="CRCP">CRCP (เหล็กเสริมต่อเนื่อง)</option>
                        </select>
                    </div>
                    <div><label>กำลังรับแรงดัด (Sc - psi)</label><input type="number" id="f_sc" value="650"></div>
                </div>
                <button class="btn" onclick="calculateRigidField()">⚡ เริ่มคำนวณออกแบบ</button>
            </div>
        </div>

        <div>
            <div id="result_note" class="note-panel">
                <h3 style="border:none; margin-bottom:10px;">📋 สรุปรายการคำนวณ</h3>
                <div id="calc_steps"></div>
            </div>

            <div class="diagram-area">
                <h4 style="text-align:center; border:none; color:#8b949e;">Concrete Cross-Section Visualizer</h4>
                <div id="v_slab" class="slab-layer" style="height: 60px;">
                    CONCRETE SLAB <div id="dim_slab" class="dim-line">D = ?</div>
                </div>
                <div style="margin:0 auto; width:75%; background:var(--base); height:50px; border:1px solid rgba(255,255,255,0.1); display:flex; align-items:center; justify-content:center; color:#fff; font-size:0.8rem;">BASE COURSE (15-20 cm)</div>
                <div style="margin:0 auto; width:75%; background:var(--sg); height:40px; display:flex; align-items:center; justify-content:center; color:#fff; font-size:0.8rem;">SUBGRADE</div>
            </div>
        </div>
    </div>
</div>

<script>
function calculateRigidField() {
    // 1. แปลง CBR เป็น k-value
    const cbr = parseFloat(document.getElementById('f_cbr').value);
    // สูตรโดยประมาณ: k (pci) = CBR * 40 (สำหรับ CBR < 10) หรือตามตารางความสัมพันธ์
    let k_val = cbr * 35; 
    document.getElementById('f_k').value = Math.round(k_val);

    // 2. คำนวณ W18 (ESAL)
    const trucks = parseFloat(document.getElementById('f_truck').value);
    const tf = parseFloat(document.getElementById('f_tf').value);
    const years = parseFloat(document.getElementById('f_years').value);
    const growth = parseFloat(document.getElementById('f_growth').value) / 100;
    const growth_factor = (Math.pow(1 + growth, years) - 1) / growth;
    const w18 = trucks * tf * 365 * growth_factor;

    // 3. กำหนดค่า J ตามประเภทคอนกรีต
    const type = document.getElementById('f_type').value;
    let J = 3.2; // Default for JPCP/JRCP with Dowels
    if (type === 'CRCP') J = 2.6;

    // 4. คำนวณหาความหนา D (AASHTO Rigid Equation Iteration)
    const Sc = parseFloat(document.getElementById('f_sc').value);
    const Ec = 4000000; // Modulus คอนกรีตมาตรฐาน
    const Cd = 1.0;     // การระบายน้ำปกติ
    const Zr = -1.282;  // Reliability 90%
    const So = 0.35;
    const dPSI = 1.7;

    let D = 6.0;
    const target = Math.log10(w18);
    for(let i=0; i<300; i++) {
        let term1 = Zr * So + 7.35 * Math.log10(D + 1) - 0.06;
        let term2 = Math.log10(dPSI / 3.0) / (1 + 1.62e7 / Math.pow(D + 1, 8.46));
        let term3 = (4.22 - 0.32 * 1.5) * Math.log10( (Sc * Cd * (Math.pow(D, 0.75) - 1.132)) / (215.63 * J * (Math.pow(D, 0.75) - 18.42 / Math.pow(Ec/k_val, 0.25))) );
        let logW = term1 + term2 + term3;
        if (Math.abs(logW - target) < 0.001) break;
        D += (target - logW) * 0.1;
    }

    const finalD = Math.max(6, Math.ceil(D * 2) / 2); // ปัดขึ้น 0.5 นิ้ว

    // 5. แสดงผลรายการคำนวณ
    document.getElementById('result_note').style.display = 'block';
    document.getElementById('calc_steps').innerHTML = `
        <b>1. Traffic Analysis:</b> W18 = ${w18.toLocaleString(undefined, {maximumFractionDigits:0})} ESALs<br>
        <b>2. Foundation:</b> CBR ${cbr}% แปลงเป็นค่า k = ${Math.round(k_val)} psi/in<br>
        <b>3. Design Parameter:</b> ใช้ค่า J = ${J} (${type})<br>
        <hr style="border:0.5px solid var(--border)">
        <b style="color:var(--accent)">4. ผลลัพธ์: ความหนา Slab (D) = ${finalD} นิ้ว (${(finalD*2.54).toFixed(1)} ซม.)</b>
    `;

    // 6. อัปเดตกราฟิก
    document.getElementById('v_slab').style.height = (finalD * 12) + 'px';
    document.getElementById('dim_slab').innerText = 'D = ' + finalD + '" (' + (finalD*2.54).toFixed(1) + ' cm)';
}
</script>
</body>
</html>
"""

components.html(html_concrete_system, height=1000, scrolling=True)
