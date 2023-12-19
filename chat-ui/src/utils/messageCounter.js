let messageIdCounter = 1;

export const getNextMessageId = () => {
  messageIdCounter += 1;
  return messageIdCounter;
};

export const resetMessageIdCounter = () => {
  messageIdCounter = 1;
};
