import React, { useState, useRef, useEffect } from "react";
import Header from "./components/Header";
import ModeSelector from "./components/ModeSelector";
import TextInput from "./components/TextInput";
import ZeroShotOptions from "./components/ZeroShotOptions";
import SFTOptions from "./components/SFTOptions";
import ErrorMessage from "./components/ErrorMessage";
import SynthesizeButton from "./components/SynthesizeButton";
import AudioPlayer from "./components/AudioPlayer";
import Footer from "./components/Footer";
import { useAudioSynthesis } from "./hooks/useAudioSynthesis";
import { checkHealth } from "./services/api";
import { MODES, DEFAULT_VALUES, SPEAKERS } from './config/constants';

export default function App() {
  const [mode, setMode] = useState(MODES.ZERO_SHOT);
  const [text, setText] = useState("");
  const [promptText, setPromptText] = useState(DEFAULT_VALUES.PROMPT_TEXT);
  const [speaker, setSpeaker] = useState(SPEAKERS[0].id);
  const [audioFile, setAudioFile] = useState(null);
  const [health, setHealth] = useState(null);

  const fileInputRef = useRef(null);

  const {
    isLoading,
    generatedAudio,
    error,
    isPlaying,
    audioRef,
    setError,
    handleSynthesize,
    togglePlayPause,
    handleDownload,
  } = useAudioSynthesis();

  useEffect(() => {
    const fetchHealth = async () => {
      try {
        const data = await checkHealth();
        setHealth(data);
      } catch (err) {
        console.error("Health check failed:", err);
      }
    };
    fetchHealth();
  }, []);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (!file.type.includes("audio")) {
        setError("Vui lòng chọn file audio (WAV, MP3, ...)");
        return;
      }
      setAudioFile(file);
      setError("");
    }
  };

  const onSynthesize = () => {
    handleSynthesize(mode, text, promptText, audioFile, speaker);
  };

  const onDownload = () => {
    handleDownload(mode);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-pink-50 p-6">
      <div className="max-w-4xl mx-auto">
        <Header health={health} />

        <div className="bg-white rounded-2xl shadow-xl p-8">
          <ModeSelector mode={mode} setMode={setMode} />

          <TextInput text={text} setText={setText} />

          {mode === MODES.ZERO_SHOT && (
            <ZeroShotOptions
              promptText={promptText}
              setPromptText={setPromptText}
              audioFile={audioFile}
              fileInputRef={fileInputRef}
              handleFileChange={handleFileChange}
            />
          )}

          {mode === MODES.SFT && (
            <SFTOptions speaker={speaker} setSpeaker={setSpeaker} />
          )}

          <ErrorMessage error={error} />

          <SynthesizeButton
            onClick={onSynthesize}
            isLoading={isLoading}
            disabled={
              isLoading ||
              !text.trim() ||
              (mode === MODES.ZERO_SHOT && !audioFile)
            }
          />

          <AudioPlayer
            generatedAudio={generatedAudio}
            audioRef={audioRef}
            isPlaying={isPlaying}
            togglePlayPause={togglePlayPause}
            handleDownload={onDownload}
          />
        </div>

        <Footer />
      </div>
    </div>
  );
}
