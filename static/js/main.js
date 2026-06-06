document.getElementById('predictionForm').addEventListener('submit', async function (e) {
  e.preventDefault();

  const form = e.target;
  const btn = form.querySelector('button[type="submit"]');
  btn.disabled = true;
  btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Classifying...';

  const formData = new FormData(form);

  try {
    const response = await fetch('/predict', {
      method: 'POST',
      body: formData
    });

    const data = await response.json();

    if (data.error) {
      alert('Error: ' + data.error);
      return;
    }

    showResult(data);

  } catch (err) {
    alert('An error occurred. Please try again.');
    console.error(err);
  } finally {
    btn.disabled = false;
    btn.innerHTML = '<i class="fas fa-search me-2"></i>Classify Mushroom';
  }
});

function showResult(data) {
  const card = document.getElementById('resultCard');
  const icon = document.getElementById('resultIcon');
  const title = document.getElementById('resultTitle');
  const desc = document.getElementById('resultDesc');
  const probEdible = document.getElementById('probEdible');
  const probPoisonous = document.getElementById('probPoisonous');
  const barEdible = document.getElementById('barEdible');
  const barPoisonous = document.getElementById('barPoisonous');
  const confidenceVal = document.getElementById('confidenceVal');

  card.classList.remove('d-none', 'result-poisonous', 'result-edible');

  if (data.is_poisonous) {
    card.classList.add('result-poisonous');
    icon.innerHTML = '<i class="fas fa-skull-crossbones text-danger"></i>';
    title.innerHTML = '<span class="text-danger">⚠️ Poisonous</span>';
    desc.textContent = 'Warning! This mushroom is classified as POISONOUS. Do not consume!';
  } else {
    card.classList.add('result-edible');
    icon.innerHTML = '<i class="fas fa-check-circle text-success"></i>';
    title.innerHTML = '<span class="text-success">✅ Edible</span>';
    desc.textContent = 'This mushroom is classified as EDIBLE based on the provided characteristics.';
  }

  probEdible.textContent = data.prob_edible + '%';
  probPoisonous.textContent = data.prob_poisonous + '%';
  barEdible.style.width = data.prob_edible + '%';
  barPoisonous.style.width = data.prob_poisonous + '%';
  confidenceVal.textContent = data.confidence;

  card.scrollIntoView({ behavior: 'smooth', block: 'start' });
}
