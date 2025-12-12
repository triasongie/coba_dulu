export async function sendToModel(inputData) {
  const response = await fetch('http://127.0.0.1:8000/predict', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ text: inputData }),
  });
  return await response.json();
}
