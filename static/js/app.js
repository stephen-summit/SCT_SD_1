// client-side validation and fetch-based conversion
const form = document.getElementById('conv-form');
const valueEl = document.getElementById('value');
const fromUnit = document.getElementById('from_unit');
const toUnit = document.getElementById('to_unit');
const msg = document.getElementById('message');
const resultEl = document.getElementById('result');
const swapBtn = document.getElementById('swap-btn');

function showMessage(text, type='success') {
  msg.textContent = text;
  msg.className = 'message ' + (type === 'error' ? 'error' : 'success');
}

function clearMessage() {
  msg.textContent = '';
  msg.className = 'message';
}

function showResult(text) {
  resultEl.textContent = text;
}

swapBtn.addEventListener('click', () => {
  const a = fromUnit.value;
  fromUnit.value = toUnit.value;
  toUnit.value = a;
  clearMessage();
  showResult('');
});

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  clearMessage();
  showResult('processing...');

  const value = valueEl.value.trim();
  const from = fromUnit.value;
  const to = toUnit.value;

  // client-side validation
  if (!value) {
    showMessage('please enter a temperature value', 'error');
    showResult('');
    return;
  }
  const num = Number(value);
  if (Number.isNaN(num)) {
    showMessage('please enter a valid number', 'error');
    showResult('');
    return;
  }
  // basic absolute zero checks
  if (from === 'c' && num < -273.15) {
    showMessage('temperatures below -273.15 °c are invalid', 'error');
    showResult('');
    return;
  }
  if (from === 'k' && num < 0) {
    showMessage('kelvin cannot be negative', 'error');
    showResult('');
    return;
  }
  if (from === 'f' && ( (num - 32) * 5/9 ) < -273.15) {
    showMessage('temperature below absolute zero is invalid', 'error');
    showResult('');
    return;
  }

  try {
    const resp = await fetch('/convert', {
      method: 'POST',
      headers: {'content-type':'application/json'},
      body: JSON.stringify({value, from_unit: from, to_unit: to})
    });
    const data = await resp.json();
    if (!resp.ok) {
      showMessage(data.message || 'conversion failed', 'error');
      showResult('');
      return;
    }
    showMessage('conversion successful');
    showResult(`${value} ${from.toUpperCase()} → ${data.result} ${to.toUpperCase()}`);
  } catch (err) {
    showMessage('network error — please try again', 'error');
    showResult('');
  }
});
