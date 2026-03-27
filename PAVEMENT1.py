import streamlit as st
import streamlit.components.v1 as components

# ตั้งค่าหน้ากระดาษให้กว้างเพื่อความสวยงาม
st.set_page_config(page_title="AC Pavement Design", layout="wide")

html_code = """
<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700&family=IBM+Plex+Mono&display=swap" rel="stylesheet">
<style>
    :root {
        --primary: #f0a500;
        --bg: #0d1117;
        --card: #161b22;
        --border: #30363d;
        --text: #e6edf3;
    }
    body { font-family: 'Sarabun', sans-serif; background: var(--bg); color: var(--text); padding: 20px; }
    .container { max-width: 1000px; margin: auto; }
    .card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 25px; margin-bottom: 20px; }
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
    h2 { color: var(--primary); border-bottom: 2px solid var(--primary); padding-bottom: 10px; }
    label { display: block; margin-top: 10px; font-size: 0.9rem; color: #8b949e; }
    input { width: 100%; padding: 10px; background: #0d1117; border: 1px solid var(--border); color: white; border-radius: 6px; font-family: 'IBM Plex Mono'; }
    .btn { width: 100%; padding: 15px; background: var(--primary); border: none; border-radius: 8px; font-weight: bold; cursor: pointer; margin-top: 20px; transition: 0.3s; }
    .btn:hover { opacity: 0.8; transform: translateY(-2px); }
    .result-section { background: #010409; border-left: 5px solid #3fb950; padding: 20px; border-radius: 8px; display: none; }
    .formula { font-style: italic; color: #58a6ff; background: rgba(88,166,255,0.1); padding: 10px; border-radius: 5px; }
</style>
</head>
<body>
<div class="container">
    <div class="card">
        <h2>🛣️ ออกแบบความหนาชั้นทาง Asphalt Concrete (AC)</h2>
        <p class="formula">โครงสร้างหลัก: SN = (a1 × D1) + (a2 × D2 × m2) + (a3 × D3 × m3)</p>
        
        <div class="grid">
            <div>
                <h3>1. ข้อมูลจราจร & ดิน</h3>
                <label>W18 (ปริมาณจราจรสะสม - ล้าน ESALs)</label>
                <input type="number" id="w18" value="2.5" step="0.1">
                <label>Reliability (ZR) - [90% = -1.282]</label>
                <input type="number" id="zr" value="-1.282">
                <label>Standard Deviation (So)</label>
                <input type="number" id="so" value="0.45">
                <label>Subgrade Resilient Modulus (MR - psi)</label>
                <input type="number" id="mr" value="7500">
            </div>

            <div>
                <h3>2. ค่าสัมประสิทธิ์ชั้นทาง (a, m, D)</h3>
                <label>a1 (Surface - AC) [ปกติ 0.44]</label>
                <input type="number" id="a1" value="0.44" step="0.01">
                
                <label>a2 (Base) & m2 (Drainage) [ปกติ 0.14, 1.0]</label>
                <div style="display:flex; gap:10px;">
                    <input type="number" id="a2" value="0.14" step="0.01">
                    <input type="number" id="m2" value="1.0" step="0.1">
                </div>
                <label>ความหนา Base ที่กำหนด (D2 - นิ้ว)</label>
                <input type="number" id="d2" value="8">

                <label>a3 (Subbase) & m3 (Drainage) [ปกติ 0.11, 1.0]</label>
                <div style="display:flex; gap:10px;">
                    <input type="number" id="a3" value="0.11" step="0.01">
                    <input type="number" id="m3" value="1.0" step="0.1">
                </div>
                <label>ความหนา Subbase ที่กำหนด (D3 - นิ้ว)</label>
                <input type="number" id="d3" value="6">
            </div>
        </div>

        <button class="btn" onclick="calculateDesign()">⚡ คำนวณความหนาผิวทาง AC (D1)</button>
    </div>

    <div id="resultBox" class="result-section">
        <h3>✅ สรุปผลการออกแบบ</h3>
        <div id="resultContent"></div>
    </div>
</div>

<script>
function calculateDesign() {
    // 1. รับค่าจาก Input
    const w18_mil = parseFloat(document.getElementById('w18').value);
    const w18 = w18_mil * 1000000;
    const zr = parseFloat(document.getElementById('zr').value);
    const so = parseFloat(document.getElementById('so').value);
    const mr = parseFloat(document.getElementById('mr').value);
    const dpsi = 1.9; // ค่ากลางสำหรับการสูญเสียความราบเรียบ

    const a1 = parseFloat(document.getElementById('a1').value);
    const a2 = parseFloat(document.getElementById('a2').value);
    const m2 = parseFloat(document.getElementById('m2').value);
    const d2 = parseFloat(document.getElementById('d2').value);
    const a3 = parseFloat(document.getElementById('a3').value);
    const m3 = parseFloat(document.getElementById('m3').value);
    const d3 = parseFloat(document.getElementById('d3').value);

    // 2. คำนวณหา SN ที่ต้องการ (Required SN) ด้วยวิธี Newton-Raphson หรือ Iteration
    let sn_req = 3.0; 
    const target = Math.log10(w18);
    for (let i = 0; i < 200; i++) {
        let log_w18 = zr * so + 9.36 * Math.log10(sn_req + 1) - 0.20 + 
                      Math.log10(dpsi/2.7) / (0.40 + 1094 / Math.pow(sn_req + 1, 5.19)) + 
                      2.32 * Math.log10(mr) - 8.07;
        if (Math.abs(log_w18 - target) < 0.0001) break;
        sn_req += (target - log_w18) * 0.1;
    }

    // 3. คำนวณความแข็งแรงของชั้นพื้นทางและรองพื้นทาง (SN_base + SN_subbase)
    const sn_existing = (a2 * d2 * m2) + (a3 * d3 * m3);

    // 4. หาความหนา D1 (Surface)
    let d1_req = (sn_req - sn_existing) / a1;
    if (d1_req < 2) d1_req = 2; // ความหนาขั้นต่ำตามมาตรฐาน 2 นิ้ว (5 ซม.)

    // ปัดขึ้นเป็นเลขสวยๆ (ทุก 0.5 นิ้ว)
    const d1_final = Math.ceil(d1_req * 2) / 2;
    const sn_provided = (a1 * d1_final) + sn_existing;

    // 5. แสดงผล
    const resBox = document.getElementById('resultBox');
    const resCont = document.getElementById('resultContent');
    
    resBox.style.display = 'block';
    resCont.innerHTML = `
        <p>ค่า SN ที่ต้องการจากจราจร (Required SN): <b>${sn_req.toFixed(3)}</b></p>
        <p>ความแข็งแรงจากชั้นรอง (SN 2+3): <b>${sn_existing.toFixed(3)}</b></p>
        <hr style="border:0.5px solid #30363d">
        <p>ความหนาชั้นผิวทาง AC ที่คำนวณได้: <b>${d1_req.toFixed(2)} นิ้ว</b></p>
        <p style="font-size: 1.2rem;">👉 สรุปความหนา D1 ที่แนะนำ: <span style="color:var(--primary); font-weight:bold;">${d1_final} นิ้ว (${(d1_final * 2.54).toFixed(1)} ซม.)</span></p>
        <p>ค่า SN ที่ได้จริง (Provided SN): <b style="color:#3fb950;">${sn_provided.toFixed(3)}</b> (ต้องมากกว่า Required SN)</p>
    `;
}
</script>
</body>
</html>
"""

# แสดงผลผ่าน Streamlit
components.html(html_code, height=900, scrolling=True)
