import React from "react";
import PropTypes from "prop-types";
import BotCardContent from "./BotCardContent";
import Link from "next/link";

export default function BotMessageWithReference({ message, reference }) {
  return (
    <BotCardContent>
      <p>{message} To know more:</p>
      <Link
        className="break-all font-semibold underline decoration-primary-black"
        href={reference}
        target="_blank"
        rel="noreferrer"
      >
        {reference}
      </Link>
    </BotCardContent>
  );
}

BotMessageWithReference.propTypes = {
  message: PropTypes.string.isRequired,
  reference: PropTypes.string.isRequired,
};
