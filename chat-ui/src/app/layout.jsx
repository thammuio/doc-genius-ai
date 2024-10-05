import React from 'react';
import PropTypes from 'prop-types';
import './globals.css';
import { Inter } from 'next/font/google';
import { ChatProvider } from '../provider';
import favicon from '../images/favicon.ico';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'ChatBot',
  description: 'Web chatbot',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" suppressHydrationWarning>
        <head>
        <title>DocGenius AI | Generative AI Chatbot - powered by Cloudera</title>
        <link rel="shortcut icon" href="https://raw.githubusercontent.com/thammuio/doc-genius-ai/main/chat-ui/src/images/favicon.ico" />
        <meta
          name="description"
          content="Generative AI Chatbot for your Documentation"
        />
        <meta property="og:title" content="DocGenius AI | Generative AI Chatbot - powered by Cloudera" />
        <meta
          property="og:description"
          content="Generative AI Chatbot for your Documentation"
        />
        <meta property="og:image" content="https://raw.githubusercontent.com/thammuio/doc-genius-ai/main/images/doc-genius-ai.png" />
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content="DocGenius AI" />
        <meta
          name="twitter:description"
          content="Generative AI Chatbot for your Documentation - powered by Cloudera"
        />
        <meta name="twitter:image" content="https://raw.githubusercontent.com/thammuio/doc-genius-ai/main/images/doc-genius-ai.png" />
      </head>
      <body className={`${inter.className} bg-slate-50`}>
        <ChatProvider>
          {children}
        </ChatProvider>
      </body>
    </html>
  );
}

RootLayout.propTypes = {
  children: PropTypes.node.isRequired,
};
