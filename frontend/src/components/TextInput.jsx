import React from 'react';

const TextInput = ({ text, setText }) => (
  <div className="mb-6">
    <label className="block text-sm font-semibold text-gray-700 mb-2">
      Văn bản cần tổng hợp *
    </label>
    <textarea
      value={text}
      onChange={(e) => setText(e.target.value)}
      placeholder="Nhập văn bản tiếng Việt..."
      className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:outline-none resize-none"
      rows="4"
    />
    <div className="text-xs text-gray-500 mt-1">
      {text.length} ký tự
    </div>
  </div>
);

export default TextInput;