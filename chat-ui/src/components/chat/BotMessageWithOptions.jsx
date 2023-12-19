import React, { useContext } from 'react';
import PropTypes from 'prop-types';
import { ChatContext } from '@/provider';
import BotCardContent from './BotCardContent';

export default function BotMessageWithOptions({ message = '', options }) {
  const { sendMessage } = useContext(ChatContext);

  return (
    <BotCardContent>
      {message.length > 0 && <p className="leading-relaxed">{message}</p>}
      <div className="mt-1 space-y-2 ">
        {options.map(({ id, option, response }) => (
          <button
            className="bg-white py-2 px-4 w-full rounded-xl cursor-pointer hover:bg-zinc-50 text leading-relaxed font-medium text-sm"
            type="button"
            onClick={() => sendMessage(response)}
            key={id}
          >
            {option}
          </button>
        ))}
      </div>
    </BotCardContent>
  );
}

BotMessageWithOptions.propTypes = {
  message: PropTypes.string,
  options: PropTypes.arrayOf(PropTypes.shape({
    option: PropTypes.string.isRequired,
  })),
};
