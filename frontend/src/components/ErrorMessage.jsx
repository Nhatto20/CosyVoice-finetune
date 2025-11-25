import React from "react";
import { XCircle } from "lucide-react";

const ErrorMessage = ({ error }) =>
  error && (
    <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl flex items-start gap-3">
      <XCircle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
      <div className="text-sm text-red-700">{error}</div>
    </div>
  );

export default ErrorMessage;
