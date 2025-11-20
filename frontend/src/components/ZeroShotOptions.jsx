import React from "react";
import { Upload } from "lucide-react";

const ZeroShotOptions = ({
  promptText,
  setPromptText,
  audioFile,
  fileInputRef,
  handleFileChange,
}) => (
  <div className="space-y-4 mb-6 p-4 bg-purple-50 rounded-xl">
    <div>
      <label className="block text-sm font-semibold text-gray-700 mb-2">
        Transcript audio tham chiếu
      </label>
      <input
        type="text"
        value={promptText}
        onChange={(e) => setPromptText(e.target.value)}
        placeholder="Văn bản trong audio tham chiếu"
        className="w-full px-4 py-2 border-2 border-gray-200 rounded-lg focus:border-purple-500 focus:outline-none"
      />
    </div>

    <div>
      <label className="block text-sm font-semibold text-gray-700 mb-2">
        Audio tham chiếu * (WAV, 16kHz khuyến nghị)
      </label>
      <div
        onClick={() => fileInputRef.current?.click()}
        className="border-2 border-dashed border-gray-300 rounded-xl p-6 text-center cursor-pointer hover:border-purple-500 hover:bg-purple-50 transition-all"
      >
        <input
          ref={fileInputRef}
          type="file"
          accept="audio/*"
          onChange={handleFileChange}
          className="hidden"
        />
        <Upload className="w-8 h-8 mx-auto mb-2 text-gray-400" />
        {audioFile ? (
          <div>
            <div className="font-medium text-purple-600">{audioFile.name}</div>
            <div className="text-xs text-gray-500 mt-1">
              {(audioFile.size / 1024 / 1024).toFixed(2)} MB
            </div>
          </div>
        ) : (
          <div className="text-gray-500">Click để chọn file audio</div>
        )}
      </div>
    </div>
  </div>
);

export default ZeroShotOptions;
