export async function askIma(message) {
  const response = await fetch('/ima-api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message }),
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.error || `chat HTTP ${response.status}`);
  if (!data.response) throw new Error('IMA returned no response');
  return data.response;
}
