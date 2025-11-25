import { API_BASE_URL } from "../config/constants";

export const checkHealth = async () => {
  const response = await fetch(`${API_BASE_URL}/health`);
  return await response.json();
};

export const synthesizeZeroShot = async (text, promptText, audioFile) => {
  const formData = new FormData();
  formData.append("text", text);
  formData.append("prompt_text", promptText);
  formData.append("prompt_audio", audioFile);

  const response = await fetch(
    `${API_BASE_URL}/synthesize/zero-shot?text=${encodeURIComponent(
      text
    )}&prompt_text=${encodeURIComponent(promptText)}`,
    {
      method: "POST",
      body: formData,
    }
  );

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || "Synthesis failed");
  }

  return await response.blob();
};

export const synthesizeSFT = async (text, speaker) => {
  const response = await fetch(`${API_BASE_URL}/synthesize/sft`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text, speaker }),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || "Synthesis failed");
  }

  return await response.blob();
};
