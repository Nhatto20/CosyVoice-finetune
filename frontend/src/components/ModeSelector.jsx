import React from "react";
import { Mic, Volume2 } from "lucide-react";
import { MODES } from "../config/constants";

const ModeSelector = ({ mode, setMode }) => (
  <div className="mb-6">
    <label className="block text-sm font-semibold text-gray-700 mb-3">
      Chế độ tổng hợp
    </label>
    <div className="grid grid-cols-2 gap-3">
      <button
        onClick={() => setMode(MODES.ZERO_SHOT)}
        className={`p-4 rounded-xl border-2 transition-all ${
          mode === MODES.ZERO_SHOT
            ? "border-purple-500 bg-purple-50 text-purple-700"
            : "border-gray-200 bg-white text-gray-600 hover:border-purple-300"
        }`}
      >
        <Mic className="w-6 h-6 mx-auto mb-2" />
        <div className="font-semibold">Zero-Shot</div>
        <div className="text-xs mt-1">Cloning giọng nói</div>
      </button>

      <button
        onClick={() => setMode(MODES.SFT)}
        className={`p-4 rounded-xl border-2 transition-all ${
          mode === MODES.SFT
            ? "border-blue-500 bg-blue-50 text-blue-700"
            : "border-gray-200 bg-white text-gray-600 hover:border-blue-300"
        }`}
      >
        <Volume2 className="w-6 h-6 mx-auto mb-2" />
        <div className="font-semibold">SFT Mode</div>
        <div className="text-xs mt-1">Giọng mặc định</div>
      </button>
    </div>
  </div>
);

export default ModeSelector;
