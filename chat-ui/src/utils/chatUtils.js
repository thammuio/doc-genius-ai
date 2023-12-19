import { getNextMessageId } from "./messageCounter";

export const createNewAssistantMessage = (
  content,
  options = null,
  reference = null
) => {
  const newMessage = {
    id: getNextMessageId(),
    content: content || "",
    role: "assistant",
  };

  if (options) {
    newMessage.options = options;
  }
  if (reference) {
    newMessage.reference = reference;
  }

  return newMessage;
};

export const createNewUserMessage = (content) => {
  const newMessage = {
    id: getNextMessageId(),
    content,
    role: "user",
  };
  return newMessage;
};

export const firstMessage = {
  id: getNextMessageId(),
  content: "Hello! How can I assist you today?",
  role: "assistant",
};
