import streamlit as st
import streamlit.components.v1 as components

# ตั้งค่าหน้ากระดาษ Streamlit
st.set_page_config(page_title="Pavement Design System", layout="wide")

# ส่วนของโค้ด HTML, CSS และ JavaScript ทั้งหมดที่คุณให้มา
html_content = """
<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<style>
  :root {
    --bg: #0d1117;
    --panel: #161b22;
    --border: #30363d;
    --accent: #f0a500;
    --text: #e6edf3;
  }
  body { 
    font-family: 'Sarabun', sans-serif; 
    background: var(--bg); 
    color: var(--text);
    margin: 0;
    padding: 20px;
  }
  /* ก๊อปปี้ CSS ทั้งหมดจากที่คุณให้มาวางตรงนี้ */
  .card { background: var(--panel); border: 1px solid var(--border); padding: 20px; border-radius: 10px; }
  input { width: 100%; background: #0d1117; border: 1px solid var(--border); color: white; padding: 8px; margin-top: 5px; }
  .btn { width: 100%; padding: 12px; background: var(--accent); border: none; cursor: pointer; font-weight: bold; margin-top: 10px; }
  .result-box { background: #0d1117; border: 1px solid var(--border); padding: 15px; margin-top: 15px; display: none; }
  .show { display: block; }
</style>
</head>
<body>

<div class="card">
  <h2 style="color:var(--accent)">🛣️ ออกแบบโครงสร้างชั้นทาง AC (AASHTO 1993)</h2>
  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
    <div>
      <label>W18 (ล้าน ESALs)</label>
      <input type="number" id="w18" value="2.5">
      <label>Subgrade MR (psi)</label>
      <input type="number" id="mr" value="7500">
      <button class="btn" onclick="calculate()">คำนวณความหนา</button>
    </div>
    <div id="result" class="result-box">
      <div id="content"></div>
    </div>
  </div>
</div>

<script>
function calculate() {
  const w18 = parseFloat(document.getElementById('w18').value) * 1e6;
  const mr = parseFloat(document.getElementById('mr').value);
  const zr = -1.282; // 90% Reliability
  const so = 0.45;
  const dpsi = 1.9;

  // สมการ AASHTO 1993 Iteration
  let sn = 3.0;
  for (let i = 0; i < 100; i++) {
    let lhs = zr * so + 9.36 * Math.log10(sn + 1) - 0.20 + 
              Math.log10(dpsi/2.7) / (0.40 + 1094 / Math.pow(sn + 1, 5.19)) + 
              2.32 * Math.log10(mr) - 8.07;
    if (Math.abs(lhs - Math.log10(w18)) < 0.001) break;
    sn += (Math.log10(w18) - lhs) * 0.1;
  }

  // คำนวณความหนา AC (สมมติชั้นอื่นคงที่)
  let d1 = sn / 0.44; 
  let d1_cm = (d1 * 2.54).toFixed(1);

  const res = document.getElementById('result');
  document.getElementById('content').innerHTML = `
    <h3 style="color:#3fb950">ผลการคำนวณ</h3>
    <p>Structural Number (SN): <b>${sn.toFixed(3)}</b></p>
    <p>ความหนาผิวทาง AC แนะนำ: <b style="font-size:1.5rem; color:var(--accent)">${d1_cm} ซม.</b></p>
  `;
  res.classList.add('show');
}
</script>
</body>
</html>
"""

# แสดงผล HTML ใน Streamlit
components.html(html_content, height=600, scrolling=True)
