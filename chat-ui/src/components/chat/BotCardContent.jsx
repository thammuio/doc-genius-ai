import React, { useContext, useEffect } from "react";
import PropTypes from "prop-types";
import { Avatar, AvatarFallback, AvatarImage } from "@components/ui/avatar";
import { ChatContext } from "@/provider";
import Typing from "react-typing-animation";
import avatar from '../../images/chat.svg';

export default function BotCardContent({ children }) {
  const { setIsTyping } = useContext(ChatContext);

  return (
    <div className="flex gap-2 text-primary-black font-medium text-sm mb-4">
      <Avatar className="self-end h-6 w-6">
        <AvatarFallback>C</AvatarFallback>
        <AvatarImage src={avatar} />
      </Avatar>
      <div className="bg-zinc-100 max-w-xl p-3 rounded-r-2xl rounded-t-2xl leading-relaxed">
        {typeof children === "string" ? (
          <Typing speed={10} onFinishedTyping={() => setIsTyping(false)}>
            {children}
          </Typing>
        ) : (
          children
        )}
      </div>
    </div>
  );
}

BotCardContent.propTypes = {
  children: PropTypes.node.isRequired,
};
