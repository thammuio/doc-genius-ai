export const CONVERSATION_START = ['Hello', 'Good', 'I want'];
export const CONVERSATION_END = 'Goodbye';

export const ASSISTANT_QUESTIONS = ['Is a pleasure! What is your username?', 'What is your password?'];

export const LOAN_OPTIONS = [
];

export const HELP_START_OPTIONS = CONVERSATION_START.map((option, index) => ({
  id: index + 1,
  option,
  response: option,
  description: ASSISTANT_QUESTIONS[index],
}));
