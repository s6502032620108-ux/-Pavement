import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Pavement Design & ESAL Calculator", layout="wide")

html_full_system = """
<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700&family=IBM+Plex+Mono&display=swap" rel="stylesheet">
<style>
    :root {
        --bg: #0d1117; --card: #161b22; --border: #30363d; --accent: #f0a500; --text: #e6edf3;
        --ac: #374151; --base: #854d0e; --sb: #a16207; --sg: #166534;
    }
    body { font-family: 'Sarabun', sans-serif; background: var(--bg); color: var(--text); padding: 20px; }
    .container { max-width: 1200px; margin: auto; }
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
    .card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 20px; margin-bottom: 20px; }
    h2, h3 { color: var(--accent); margin-top: 0; border-bottom: 1px solid var(--border); padding-bottom: 8px; }
    
    table { width: 100%; border-collapse: collapse; margin-bottom: 15px; font-size: 0.85rem; }
    th { text-align: left; color: #8b949e; padding: 8px; border-bottom: 1px solid var(--border); }
    td { padding: 8px; border-bottom: 1px solid #21262d; }
    
    input { width: 90%; padding: 6px; background: #0d1117; border: 1px solid var(--border); color: #fff; border-radius: 4px; font-family: 'IBM Plex Mono'; }
    .btn { width: 100%; padding: 15px; background: var(--accent); border: none; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 1rem; color: #000; }
    
    .diagram-area { background: #010409; border: 1px solid var(--border); border-radius: 10px; padding: 20px; min-height: 400px; }
    .layer { margin: 0 auto; width: 70%; display: flex; align-items: center; justify-content: center; font-weight: bold; color: white; transition: 0.5s; border: 1px solid rgba(255,255,255,0.1); position: relative; font-size: 0.75rem; }
    .layer-label { position: absolute; left: 105%; white-space: nowrap; color: var(--accent); font-family: 'IBM Plex Mono'; font-size: 0.8rem; }
</style>
</head>
<body>
<div class="container">
    <div class="grid">
        <div>
            <div class="card">
                <h3>1. คำนวณปริมาณจราจรสะสม (ESAL)</h3>
                <table>
                    <thead>
                        <tr>
                            <th>ประเภทรถ (Vehicle Type)</th>
                            <th>AADT (คัน/วัน)</th>
                            <th>Truck Factor (TF)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td>รถกระบะ/รถส่วนบุคคล</td><td><input type="number" id="v1_n" value="1500"></td><td><input type="number" id="v1_tf" value="0.0007" step="0.0001"></td></tr>
                        <tr><td>รถบรรทุก 6 ล้อ</td><td><input type="number" id="v2_n" value="300"></td><td><input type="number" id="v2_tf" value="0.28"></td></tr>
                        <tr><td>รถบรรทุก 10 ล้อ</td><td><input type="number" id="v3_n" value="150"></td><td><input type="number" id="v3_tf" value="1.08"></td></tr>
                        <tr><td>รถพ่วง/รถกึ่งพ่วง</td><td><input type="number" id="v4_n" value="80"></td><td><input type="number" id="v4_tf" value="2.25"></td></tr>
                    </tbody>
                </table>
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
                    <div><label style="font-size:0.7rem">อายุการใช้งาน (ปี)</label><input type="number" id="design_period" value="15"></div>
                    <div><label style="font-size:0.7rem">อัตราเติบโต (%)</label><input type="number" id="growth_rate" value="3"></div>
                </div>
            </div>

            <div class="card">
                <h3>2. คุณสมบัติวัสดุและดิน</h3>
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
                    <div><label style="font-size:0.7rem">Subgrade MR (psi)</label><input type="number" id="mr" value="7500"></div>
                    <div><label style="font-size:0.7rem">Reliability (Zr)</label><input type="number" id="zr" value="-1.282"></div>
                    <div><label style="font-size:0.7rem">a1 (Surface)</label><input type="number" id="a1" value="0.44"></div>
                    <div><label style="font-size:0.7rem">a2 (Base)</label><input type="number" id="a2" value="0.14"></div>
                    <div><label style="font-size:0.7rem">D2 (Base - นิ้ว)</label><input type="number" id="d2" value="8"></div>
                    <div><label style="font-size:0.7rem">a3 (Subbase)</label><input type="number" id="a3" value="0.11"></div>
                    <div><label style="font-size:0.7rem">D3 (Subbase - นิ้ว)</label><input type="number" id="d3" value="6"></div>
                </div>
                <button class="btn" style="margin-top:15px;" onclick="calculateAll()">⚡ คำนวณทั้งหมด</button>
            </div>
        </div>

        <div>
            <div class="card" id="res_card" style="display:none; background:#010409;">
                <h3 style="border:none;">สรุปผลการคำนวณ</h3>
                <p>ปริมาณจราจรสะสม (W18): <span id="w18_res" style="color:var(--accent); font-weight:bold;"></span> ESALs</p>
                <p>ความหนาที่ต้องการ (D1): <span id="d1_res" style="color:#3fb950; font-size:1.5rem; font-weight:bold;"></span></p>
            </div>
            
            <div class="diagram-area">
                <h4 style="text-align:center; color:#8b949e;">Cross-Section Visualizer</h4>
                <div id="v_ac" class="layer" style="background:var(--ac); height:40px;">SURFACE (AC)<div class="layer-label" id="lbl_ac">D1 = ?</div></div>
                <div id="v_base" class="layer" style="background:var(--base); height:80px;">BASE COURSE<div class="layer-label" id="lbl_base">D2 = 8"</div></div>
                <div id="v_sb" class="layer" style="background:var(--sb); height:60px;">SUBBASE<div class="layer-label" id="lbl_sb">D3 = 6"</div></div>
                <div class="layer" style="background:var(--sg); height:40px;">SUBGRADE (ดินเดิม)</div>
            </div>
        </div>
    </div>
</div>

<script>
function calculateAll() {
    // 1. คำนวณ ESAL (W18)
    const n = parseFloat(document.getElementById('design_period').value);
    const r = parseFloat(document.getElementById('growth_rate').value) / 100;
    const g_factor = r > 0 ? (Math.pow(1 + r, n) - 1) / r : n; // Growth Factor

    const v1 = parseFloat(document.getElementById('v1_n').value) * parseFloat(document.getElementById('v1_tf').value);
    const v2 = parseFloat(document.getElementById('v2_n').value) * parseFloat(document.getElementById('v2_tf').value);
    const v3 = parseFloat(document.getElementById('v3_n').value) * parseFloat(document.getElementById('v3_tf').value);
    const v4 = parseFloat(document.getElementById('v4_n').value) * parseFloat(document.getElementById('v4_tf').value);
    
    const w18 = (v1 + v2 + v3 + v4) * 365 * g_factor * 0.5; // คูณ 0.5 สำหรับ Lane Distribution (สมมติ 2 เลน)
    
    // 2. คำนวณ SN Required (AASHTO Iteration)
    const mr = parseFloat(document.getElementById('mr').value);
    const zr = parseFloat(document.getElementById('zr').value);
    const so = 0.45;
    const dpsi = 1.9;
    
    let sn_req = 1.0;
    const target = Math.log10(w18);
    for(let i=0; i<200; i++) {
        let logW = zr * so + 9.36 * Math.log10(sn_req + 1) - 0.2 + Math.log10(dpsi/2.7)/(0.4 + 1094/Math.pow(sn_req+1, 5.19)) + 2.32*Math.log10(mr) - 8.07;
        sn_req += (target - logW) * 0.1;
    }

    // 3. หา D1
    const a1 = parseFloat(document.getElementById('a1').value);
    const a2 = parseFloat(document.getElementById('a2').value);
    const a3 = parseFloat(document.getElementById('a3').value);
    const d2 = parseFloat(document.getElementById('d2').value);
    const d3 = parseFloat(document.getElementById('d3').value);
    
    const sn_sub = (a2 * d2) + (a3 * d3);
    let d1 = (sn_req - sn_sub) / a1;
    d1 = Math.max(2, Math.ceil(d1 * 2) / 2); // ปัดขึ้นทุก 0.5 นิ้ว

    // 4. แสดงผล
    document.getElementById('res_card').style.display = 'block';
    document.getElementById('w18_res').innerText = w18.toLocaleString(undefined, {maximumFractionDigits: 0});
    document.getElementById('d1_res').innerText = d1 + '" (' + (d1*2.54).toFixed(1) + ' cm)';
    
    // 5. อัปเดตกราฟิก
    document.getElementById('v_ac').style.height = (d1 * 12) + 'px';
    document.getElementById('v_base').style.height = (d2 * 10) + 'px';
    document.getElementById('v_sb').style.height = (d3 * 10) + 'px';
    document.getElementById('lbl_ac').innerText = 'D1 = ' + d1 + '"';
    document.getElementById('lbl_base').innerText = 'D2 = ' + d2 + '"';
    document.getElementById('lbl_sb').innerText = 'D3 = ' + d3 + '"';
}
</script>
</body>
</html>
"""

components.html(html_full_system, height=950, scrolling=True)
