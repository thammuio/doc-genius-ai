"use client";

import { ChatContext } from "@/provider";
import { Button } from "@components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@components/ui/card";
import { Input } from "@components/ui/input";
import { Label } from "@components/ui/label";
import { ScrollArea } from "@components/ui/scroll-area";
import { Badge } from "@components/ui/badge";
import { useContext, useEffect, useRef, useState } from "react";
import BotCardContent from "./BotCardContent";
import BotMessageWithOptions from "./BotMessageWithOptions";
import BotMessageWithReference from "./BotMessageWithReference";
import { ConfigModal } from "./ConfigModal";
import LoadingDots from "./LoadingDots";
import UserMessage from "./UserMessage";
import { Send, MessageSquarePlus, MoveUpRight, Settings, ShieldCheck, ShieldX } from "lucide-react";
import Link from "next/link";
import Image from 'next/image';
import cmlicon from '../../images/cmlicon.svg';
import cmltext from '../../images/cmltext-black.svg';


export default function Chat() {
  const {
    createNewChat,
    messages,
    sendMessage,
    model,
    isTyping,
    isWaiting,
    isFinishedConversation,
    isChatAvailable,
    sampleQuestions,
  } = useContext(ChatContext);
  const [chatInput, setChatInput] = useState("");
  const [openConfigModal, setOpenConfigModal] = useState(false);
  const lastMessageRef = useRef(null);
  const sectionRef = useRef(null);
  const headerRef = useRef(null);
  const footerRef = useRef(null);
  const sendButtonRef = useRef(null);

  const [bodyHeight, setBodyHeight] = useState(300);

  useEffect(() => {
    if (lastMessageRef.current) {
      lastMessageRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  useEffect(() => {
    if (sectionRef.current && headerRef.current && footerRef.current) {
      setBodyHeight(
        sectionRef.current.clientHeight -
          headerRef.current.clientHeight -
          footerRef.current.clientHeight -
          10
      );
    }
  }, [sectionRef, headerRef, footerRef]);

  const handleSubmit = async (message) => {
    if (message.trim() === "") {
      return;
    }

    sendMessage(message);
    setChatInput("");
  };

  const renderBotMessage = (message) => {
    if (message.options) {
      return (
        <BotMessageWithOptions
          key={message.id}
          message={message.content}
          options={message.options}
        />
      );
    }
    if (message.reference) {
      return (
        <BotMessageWithReference
          key={message.id}
          message={message.content}
          reference={message.reference}
        />
      );
    }

    return <BotCardContent key={message.id}>{message.content}</BotCardContent>;
  };

  return (
    <section className="w-full h-[90%] my-auto px-4 pb-0" ref={sectionRef}>
      <Card className="max-w-5xl mx-auto h-full relative pb-0">
        <CardHeader ref={headerRef} className="pb-1 md:pb-1 lg:pb-2">
          <CardTitle className="text-xl lg:text-2xl">
          {`DocGenius AI`}
            {isChatAvailable ? (
              <Button className="border-green-500 text-green-500 text-xs lg:text-sm px-1 lg:px-2 py-0 ml-2" variant="outline" size="xs">
                <ShieldCheck className="mr-1" />Available
              </Button>
            ) : (
              <Button className="border-red-500 text-red-500 text-xs lg:text-sm px-1 lg:px-2 py-0 ml-2" variant="outline" size="xs">
                <ShieldX className="mr-1" /> Not Available
              </Button>
            )}
          </CardTitle>
          <CardDescription className="hidden md:block">
            Generative AI Chatbot for your Documents!
          </CardDescription>
          <hr className="w-full md:w-3/5" />
          <div className="flex flex-row items-center gap-2">
            <small className="text-gray-500">Powered by</small>
            <div className="flex items-center">
              <Image
                src={cmlicon}
                alt="CML Icon"
                width={40} // adjust as needed for mobile
                height={40} // adjust as needed for mobile
                className="w-10 h-10 md:w-12 md:h-12"
              />
              <Image
                src={cmltext}
                alt="CML Text"
                width={120} // adjust as needed for mobile
                height={40} // adjust as needed for mobile
                className="w-30 h-10 md:w-40 md:h-12"
              />
            </div>
          </div>
          <hr className="w-full md:w-3/5" />

          <div className="flex flex-row md:flex-row md:absolute right-4 top-4 gap-4">
            <Button
              disabled={isFinishedConversation}
              onClick={createNewChat}
              className="w-full md:w-auto"
            >
              <div className="flex items-center gap-2">
                <MessageSquarePlus className="h-4 w-4" />{" "}
                <div className="hidden md:block">New Chat</div>
              </div>
            </Button>
            <Button
              variant="outline"
              className="block md:hidden rounded-full p-2 flex justify-center items-center w-10"
              onClick={(e) => setOpenConfigModal(true)}
            >
              <Settings className="h-4 w-4" />
            </Button>
            <ConfigModal open={openConfigModal} setOpen={setOpenConfigModal} />
            <Card className="hidden md:block w-full md:w-[350px]">
              <CardContent className="my-4 mb-0 py-0 flex flex-col gap-2 relative">
                <Button
                  variant="outline"
                  className="absolute top-0 right-2 rounded-full p-2 flex justify-center items-center w-10"
                  onClick={(e) => setOpenConfigModal(true)}
                >
                  <Settings className="h-4 w-4" />
                </Button>
                <Label>Current Model</Label>
                <Badge variant="outline" className="w-fit mt-2">
                  {model?.name || "No Model selected"}
                </Badge>
                <Button variant="link" className="w-fit p-0">
                  <Link
                    href={model?.link || ""}
                    target="_blank"
                    className="flex gap-2"
                  >
                    <MoveUpRight className="h-4 w-4" />
                    <small>Model page</small>
                  </Link>
                </Button>
              </CardContent>
            </Card>
          </div>
        </CardHeader>
        <CardContent
          className="max-w-full md:max-w-5xl mx-auto relative py-1 md:py-1 lg:py-2 overflow-y-auto"
          style={{ height: `${bodyHeight}px` }}
        >
          {messages.length > 0 ? (
            <ScrollArea className="w-full h-full pr-4">
              {messages.map((message, index) =>
                message.role === "assistant" ? (
                  <div
                    ref={index === messages.length - 1 ? lastMessageRef : null}
                    key={message.id}
                  >
                    {renderBotMessage(message)}
                  </div>
                ) : (
                  <UserMessage key={message.id} message={message} />
                )
              )}
              {isWaiting && <LoadingDots />}
            </ScrollArea>
          ) : (
            <div className="w-full h-full flex flex-col justify-center gap-2">
              <Label>Examples</Label>
              <div className="w-full flex flex-col md:flex-row justify-between gap-4 mx-auto">
                {sampleQuestions.map((question) => (
                  <Button
                    key={question}
                    variant="secondary"
                    onClick={(e) => {
                      handleSubmit(question);
                    }}
                    className="w-full px-4 py-1 md:py-1 lg:py-2 text-blue-500 text-xs"
                  >
                    {question}
                  </Button>
                ))}
              </div>
            </div>
          )}
        </CardContent>
        <CardFooter
          className="w-full mt-auto mb-0 max-w-5xl mx-auto px-4 md:px-0 pb-0"
          ref={footerRef}
        >
          <form
            className="w-full"
            onSubmit={(e) => {
              e.preventDefault();
              handleSubmit(chatInput);
            }}
          >
            <div className="w-full flex flex-row gap-2 items-end px-2 md:px-4">
              <Input
                placeholder="How can I help you?"
                value={chatInput}
                disabled={isFinishedConversation}
                onChange={(e) => setChatInput(e.target.value)}
                className="w-full flex-1"
              />
              <Button
                disabled={isFinishedConversation || isWaiting || isTyping}
                ref={sendButtonRef}
                onClick={() => handleSubmit(chatInput)}
                className="w-auto"
              >
                <Send className="h-4 w-4" />
              </Button>
            </div>
            <small className="ml-2 md:ml-2 pt-1 md:pt-2 text-xxs md:text-xxs text-gray-500 leading-none">
              Current Model: <b>{model?.name || "No Model selected"}</b> | Check important info.
            </small>
          </form>
        </CardFooter>
      </Card>
    </section>
  );
}