import React from "react";
import PropTypes from "prop-types";

export default function UserMessage({ message }) {
  return (
    <div className="flex text-sm mb-4 justify-end text-[#1a0400] font-medium">
      <div className="bg-[#fae5ca] max-w-xl p-3 rounded-l-xl rounded-t-xl">
        <p className="leading-relaxed">{message.content}</p>
      </div>
    </div>
  );
}

UserMessage.propTypes = {
  message: PropTypes.shape({
    content: PropTypes.string.isRequired,
  }).isRequired,
};
