import React from "react";
import { CheckCircle, Download, Play, Pause } from "lucide-react";

const AudioPlayer = ({
  generatedAudio,
  audioRef,
  isPlaying,
  togglePlayPause,
  handleDownload,
}) =>
  generatedAudio && (
    <div className="mt-6 p-6 bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl border border-green-200">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <CheckCircle className="w-5 h-5 text-green-600" />
          <span className="font-semibold text-green-800">
            Tổng hợp thành công!
          </span>
        </div>
        <button
          onClick={handleDownload}
          className="flex items-center gap-2 px-4 py-2 bg-white rounded-lg hover:bg-gray-50 transition-colors text-sm font-medium text-gray-700"
        >
          <Download className="w-4 h-4" />
          Tải xuống
        </button>
      </div>

      <div className="flex items-center gap-4">
        <button
          onClick={togglePlayPause}
          className="w-12 h-12 rounded-full bg-green-600 hover:bg-green-700 flex items-center justify-center text-white transition-colors"
        >
          {isPlaying ? (
            <Pause className="w-5 h-5" />
          ) : (
            <Play className="w-5 h-5 ml-0.5" />
          )}
        </button>

        <audio
          ref={audioRef}
          src={generatedAudio}
          onEnded={() => togglePlayPause()}
          className="flex-1"
          controls
        />
      </div>
    </div>
  );

export default AudioPlayer;
