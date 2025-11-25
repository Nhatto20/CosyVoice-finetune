import React from "react";
import { Volume2, Loader } from "lucide-react";

const SynthesizeButton = ({ onClick, isLoading, disabled }) => (
  <button
    onClick={onClick}
    disabled={disabled}
    className={`w-full py-4 rounded-xl font-semibold text-white transition-all flex items-center justify-center gap-2 ${
      disabled
        ? "bg-gray-300 cursor-not-allowed"
        : "bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 shadow-lg hover:shadow-xl"
    }`}
  >
    {isLoading ? (
      <>
        <Loader className="w-5 h-5 animate-spin" />
        Đang tổng hợp...
      </>
    ) : (
      <>
        <Volume2 className="w-5 h-5" />
        Tổng hợp giọng nói
      </>
    )}
  </button>
);

export default SynthesizeButton;
