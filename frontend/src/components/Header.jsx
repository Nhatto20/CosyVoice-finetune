import React from "react";
import { Volume2, CheckCircle, XCircle } from "lucide-react";

const Header = ({ health }) => (
  <div className="text-center mb-8">
    <div className="flex items-center justify-center gap-3 mb-3">
      <Volume2 className="w-10 h-10 text-purple-600" />
      <h1 className="text-4xl font-bold text-gray-800">CosyVoice2 TTS</h1>
    </div>
    <p className="text-gray-600">Text-to-Speech với AI Voice Cloning</p>

    {health && (
      <div className="mt-4 inline-flex items-center gap-2 px-4 py-2 bg-white rounded-full shadow-sm">
        {health.status === "healthy" ? (
          <>
            <CheckCircle className="w-4 h-4 text-green-500" />
            <span className="text-sm text-green-700">
              Server đang hoạt động
            </span>
          </>
        ) : (
          <>
            <XCircle className="w-4 h-4 text-red-500" />
            <span className="text-sm text-red-700">Server không khả dụng</span>
          </>
        )}
        <span className="text-xs text-gray-500 ml-2">
          {health.device === "cuda" ? "🚀 GPU" : "💻 CPU"}
        </span>
      </div>
    )}
  </div>
);

export default Header;
