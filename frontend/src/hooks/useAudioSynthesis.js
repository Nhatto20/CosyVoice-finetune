import { useState, useRef } from "react";
import { synthesizeZeroShot, synthesizeSFT } from "../services/api";
import { MODES } from "../config/constants";

export const useAudioSynthesis = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [generatedAudio, setGeneratedAudio] = useState(null);
  const [error, setError] = useState("");
  const [isPlaying, setIsPlaying] = useState(false);
  const audioRef = useRef(null);

  const handleSynthesize = async (
    mode,
    text,
    promptText,
    audioFile,
    speaker
  ) => {
    if (!text.trim()) {
      setError("Vui lòng nhập văn bản cần tổng hợp");
      return;
    }

    if (mode === MODES.ZERO_SHOT && !audioFile) {
      setError("Vui lòng upload file audio tham chiếu");
      return;
    }

    setIsLoading(true);
    setError("");
    setGeneratedAudio(null);

    try {
      let audioBlob;

      if (mode === MODES.ZERO_SHOT) {
        audioBlob = await synthesizeZeroShot(text, promptText, audioFile);
      } else {
        audioBlob = await synthesizeSFT(text, speaker);
      }

      const audioUrl = URL.createObjectURL(audioBlob);
      setGeneratedAudio(audioUrl);
    } catch (err) {
      setError(err.message || "Có lỗi xảy ra khi tổng hợp giọng nói");
      console.error("Synthesis error:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const togglePlayPause = () => {
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.pause();
      } else {
        audioRef.current.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  const handleDownload = (mode) => {
    if (generatedAudio) {
      const a = document.createElement("a");
      a.href = generatedAudio;
      a.download = `cosyvoice_${mode}_${Date.now()}.wav`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    }
  };

  return {
    isLoading,
    generatedAudio,
    error,
    isPlaying,
    audioRef,
    setError,
    handleSynthesize,
    togglePlayPause,
    handleDownload,
  };
};
