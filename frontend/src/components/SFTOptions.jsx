import React from "react";
import { ChevronDown } from "lucide-react";
import { SPEAKERS } from "../config/constants";

const SFTOptions = ({ speaker, setSpeaker }) => (
  <div className="mb-6 p-4 bg-blue-50 rounded-xl">
    <label className="block text-sm font-semibold text-gray-700 mb-2">
      Speaker
    </label>
    <div className="relative">
      <select
        value={speaker}
        onChange={(e) => setSpeaker(e.target.value)}
        className="w-full px-4 py-2 pr-10 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:outline-none appearance-none bg-white cursor-pointer"
      >
        {SPEAKERS.map((s) => (
          <option key={s.id} value={s.id}>
            {s.name}
          </option>
        ))}
      </select>
      <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 pointer-events-none" />
    </div>
  </div>
);

export default SFTOptions;
