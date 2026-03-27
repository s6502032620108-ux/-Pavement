<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Pavement Design Pro</title>

<style>
body {
  font-family: sans-serif;
  background:#0d1117;
  color:#e6edf3;
  padding:20px;
}
.card {
  background:#161b22;
  padding:20px;
  border-radius:10px;
  margin-bottom:20px;
}
input {
  width:100%;
  padding:8px;
  margin-bottom:10px;
  background:#0d1117;
  border:1px solid #30363d;
  color:white;
}
button {
  width:100%;
  padding:12px;
  background:orange;
  border:none;
  cursor:pointer;
}
.result {
  margin-top:15px;
  padding:15px;
  background:#0d1117;
}
.layer {
  padding:8px;
  margin:5px 0;
  background:#161b22;
}
</style>
</head>

<body>

<h2>🛣️ Pavement Design (AASHTO 1993)</h2>

<div class="card">

<h3>Input</h3>

<label>W18 (ล้าน ESAL)</label>
<input id="w18" type="number" value="2.5">

<label>ZR</label>
<input id="zr" type="number" value="-1.282">

<label>So</label>
<input id="so" type="number" value="0.45">

<label>ΔPSI</label>
<input id="dpsi" type="number" value="1.7">

<label>MR (psi)</label>
<input id="mr" type="number" value="8000">

<hr>

<h3>Material Coefficient</h3>

<label>a1 (AC)</label>
<input id="a1" type="number" value="0.44">

<label>a2 (Base)</label>
<input id="a2" type="number" value="0.14">

<label>a3 (Subbase)</label>
<input id="a3" type="number" value="0.11">

<label>m2 (Base drainage)</label>
<input id="m2" type="number" value="1">

<label>m3 (Subbase drainage)</label>
<input id="m3" type="number" value="1">

<button onclick="calculate()">คำนวณ</button>

<div id="output" class="result"></div>

</div>

<script>

function calculate() {

  let W18 = parseFloat(document.getElementById("w18").value) * 1e6;
  let ZR = parseFloat(document.getElementById("zr").value);
  let So = parseFloat(document.getElementById("so").value);
  let dpsi = parseFloat(document.getElementById("dpsi").value);
  let MR = parseFloat(document.getElementById("mr").value);

  let a1 = parseFloat(document.getElementById("a1").value);
  let a2 = parseFloat(document.getElementById("a2").value);
  let a3 = parseFloat(document.getElementById("a3").value);
  let m2 = parseFloat(document.getElementById("m2").value);
  let m3 = parseFloat(document.getElementById("m3").value);

  // ====== AASHTO SN ======
  let logW = Math.log10(W18);

  let SN = (logW + ZR*So - Math.log10(dpsi/2.7)) / 0.4;

  // ====== Design Layer ======
  // กำหนดขั้นต่ำ
  let D1 = 5; // inch AC
  let SN1 = a1 * D1;

  let remainingSN = SN - SN1;

  let D2 = remainingSN / (a2 * m2);

  // limit base
  if (D2 > 10) {
    D2 = 10;
  }

  let SN2 = a1*D1 + a2*m2*D2;

  let D3 = (SN - SN2) / (a3 * m3);

  if (D3 < 4) D3 = 4;

  // convert to cm
  let cm = 2.54;

  document.getElementById("output").innerHTML = `
    <b>Structural Number (SN) = ${SN.toFixed(2)}</b>

    <div class="layer">AC = ${D1.toFixed(2)} in (${(D1*cm).toFixed(1)} cm)</div>
    <div class="layer">Base = ${D2.toFixed(2)} in (${(D2*cm).toFixed(1)} cm)</div>
    <div class="layer">Subbase = ${D3.toFixed(2)} in (${(D3*cm).toFixed(1)} cm)</div>
  `;
}

</script>

</body>
</html>
