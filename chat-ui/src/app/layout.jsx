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
        <title>Chat with Cloudera Documentation</title>
        <link rel="shortcut icon" href="https://raw.githubusercontent.com/thammuio/chat-cloudera-docs/main/chat-ui/src/images/favicon.ico" />
        <meta
          name="description"
          content="Chat with Cloudera Documentation"
        />
        <meta property="og:title" content="Chat with Cloudera Documentation" />
        <meta
          property="og:description"
          content="Chat with Cloudera Documentation"
        />
        <meta property="og:image" content="/images/cldr_genai_docs.png" />
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content="Chat with Cloudera Documentation" />
        <meta
          name="twitter:description"
          content="Chat with Cloudera Documentation"
        />
        <meta name="twitter:image" content="/images/cldr_genai_docs.png" />
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
