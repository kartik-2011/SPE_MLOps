const form = document.getElementById("prediction-form");
const sampleBtn = document.getElementById("sample-btn");
const refreshBtn = document.getElementById("refresh-btn");
const predictionValue = document.getElementById("prediction-value");
const predictionSubtext = document.getElementById("prediction-subtext");
const resultModelVersion = document.getElementById("result-model-version");
const resultStatus = document.getElementById("result-status");
const statusPill = document.getElementById("status-pill");
const errorMessage = document.getElementById("error-message");
const healthStatus = document.getElementById("health-status");
const healthModelLoaded = document.getElementById("health-model-loaded");
const infoVersion = document.getElementById("info-version");
const infoSource = document.getElementById("info-source");

function setStatus(label, tone) {
  statusPill.textContent = label;
  statusPill.className = `status-pill ${tone}`;
}

function setError(message) {
  errorMessage.hidden = !message;
  errorMessage.textContent = message || "";
}

function fillSampleData() {
  const sampleInput = window.APP_CONFIG.sampleInput;
  Object.entries(sampleInput).forEach(([key, value]) => {
    const input = form.elements.namedItem(key);
    if (input) {
      input.value = value;
    }
  });
}

async function refreshStatus() {
  try {
    const [healthResponse, infoResponse] = await Promise.all([
      fetch("/health"),
      fetch("/model/info"),
    ]);
    const health = await healthResponse.json();
    const info = await infoResponse.json();

    healthStatus.textContent = health.status.toUpperCase();
    healthModelLoaded.textContent = health.model_loaded ? "Yes" : "No";
    infoVersion.textContent = info.current_version || "Unavailable";
    infoSource.textContent = info.data_source || "Unavailable";
  } catch (error) {
    healthStatus.textContent = "Unavailable";
    healthModelLoaded.textContent = "Unavailable";
    infoVersion.textContent = "Unavailable";
    infoSource.textContent = "Unavailable";
  }
}

async function submitPrediction(event) {
  event.preventDefault();
  setError("");
  setStatus("Predicting...", "loading");
  resultStatus.textContent = "Request in progress";

  const payload = {};
  new FormData(form).forEach((value, key) => {
    payload[key] = Number(value);
  });

  try {
    const response = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const detail = await response.text();
      throw new Error(detail || "Prediction failed");
    }

    const data = await response.json();
    predictionValue.textContent = `$${Number(data.prediction).toFixed(3)}`;
    predictionSubtext.textContent = "Prediction completed successfully using the currently deployed production model.";
    resultModelVersion.textContent = data.model_version;
    resultStatus.textContent = "200 OK";
    setStatus("Prediction ready", "success");
  } catch (error) {
    predictionValue.textContent = "--";
    predictionSubtext.textContent = "The API could not complete the prediction.";
    resultStatus.textContent = "Request failed";
    setError(error.message.replaceAll('"', ""));
    setStatus("Prediction failed", "error");
  }
}

sampleBtn.addEventListener("click", fillSampleData);
refreshBtn.addEventListener("click", refreshStatus);
form.addEventListener("submit", submitPrediction);
refreshStatus();
