"use client";

import React, { useState, useMemo, useEffect } from "react";
import PropTypes from "prop-types";
import {
  CONVERSATION_END,
  HELP_START_OPTIONS,
  createNewAssistantMessage,
  createNewUserMessage,
  firstMessage,
  resetMessageIdCounter,
} from "@/utils";
import ChatContext from "./ChatContext";

export default function ChatProvider({ children }) {
  const [historicMessages, setHistoricMessages] = useState([]);
  const [messages, setMessages] = useState([]);
  const [user, setUser] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [isWaiting, setIsWaiting] = useState(false);
  const [model, setModel] = useState({});
  const [models, setModels] = useState([]);
  const [temperature, setTemperature] = useState(0.7);
  const [maxTokens, setMaxTokens] = useState(100);
  const [isFinishedConversation, setIsFinishedConversation] = useState(false);
  const domain = process.env.NEXT_PUBLIC_CHATBOT_API_DOMAIN;
  const api = `https://docgenius-api.${domain}`;
  const origin = `https://docgenius-ui.${domain}`;


  useEffect(() => {
    fetch(`${api}/settings`).then((response) => {
      if (response.ok) {
        response.json().then((data) => {
          if (data?.models) {
            setModels(data.models);
            setModel(data.models[0]);
          }
        });
      }
    });
  }, []);

  const createNewChat = () => {
    setMessages([]);
    setIsTyping(false);
    setIsWaiting(false);
    setIsFinishedConversation(false);
    setUser("");
  };

  const handleAssistantResponse = (response) => {
    setMessages((prevMessages) => [
      ...prevMessages,
      createNewAssistantMessage(
        response.content,
        response.options,
        response.reference
      ),
    ]);
  };

  const getBotResponse = async (message) => {
    setIsTyping(true);
    setIsWaiting(true);

    try {
      const body = JSON.stringify({
        prompt: message,
        parameters: {
          temperature,
          max_tokens: maxTokens,
        },
        "selected_model": model.name,
        "selected_vector_db": "MILVUS",
        "user": "genius"
      });

      console.log("Sending request with body:", body);

      const response = await fetch(`${api}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json",
          "Access-Control-Allow-Origin": origin,
          "Origin": origin,
        },
        body,
      });

      console.log("Received response with status:", response.status);
      
      if (response.ok) { // Check if response status is 200
        const data = await response.json();
        handleAssistantResponse({ content: data.response });
      } else {
        handleAssistantResponse({ content: 'Something went wrong, please try again later' });
      }

    } catch (error) {
      console.error("Error:", error);
    }

    setIsWaiting(false);
    // setTimeout(() => {
    //   const response = `This is the response of "${message}"`;
    //   handleAssistantResponse({ content: response });

    //   setIsWaiting(false);
    // }, 1000);
  };

  const finishConversation = () => {
    setIsFinishedConversation(true);
    setMessages((prevMessages) => [
      ...prevMessages,
      createNewAssistantMessage("Bye! 👋"),
    ]);
    setHistoricMessages((prevMessages) => [
      ...prevMessages,
      {
        id: prevMessages.length + 1,
        title: `Conversation ${user || "user"} #${
          prevMessages.length + 1
        } - ${new Date().toLocaleString()}`,
        messages,
      },
    ]);
    setUser("");
    setTimeout(() => {
      resetMessageIdCounter();
      setMessages([firstMessage]);
      setIsFinishedConversation(false);
    }, 2000);
  };

  const sendMessage = (message) => {
    setMessages((prevMessages) => [
      ...prevMessages,
      createNewUserMessage(message),
    ]);

    if (message === CONVERSATION_END) {
      finishConversation();
    } else {
      getBotResponse(message);
    }
  };

  const contextType = useMemo(
    () => ({
      createNewChat,
      messages,
      sendMessage,
      historicMessages,
      models,
      model,
      setModel,
      temperature,
      setTemperature,
      maxTokens,
      setMaxTokens,
      isWaiting,
      setIsWaiting,
      isTyping,
      setIsTyping,
      isFinishedConversation,
    }),
    [
      createNewChat,
      messages,
      sendMessage,
      historicMessages,
      models,
      model,
      setModel,
      temperature,
      setTemperature,
      maxTokens,
      setMaxTokens,
      isWaiting,
      setIsWaiting,
      isTyping,
      setIsTyping,
      isFinishedConversation,
    ]
  );

  return (
    <ChatContext.Provider value={contextType}>{children}</ChatContext.Provider>
  );
}

ChatProvider.propTypes = {
  children: PropTypes.node.isRequired,
};
