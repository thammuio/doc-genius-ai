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
    <section className="w-full h-[90%] my-auto px-4" ref={sectionRef}>
      <Card className="max-w-5xl mx-auto h-full relative pb-10">
        <CardHeader ref={headerRef} className="pb-10">
          <CardTitle>{`DocGenius AI`} 
          {isChatAvailable ? 
          <Button className="border-green-500 text-green-500 text-xs px-1 py-0 ml-2" variant="outline" size="xs"><ShieldCheck className="mr-1" />Available</Button> 
          : 
          <Button className="border-red-500 text-red-500 text-xs px-1 py-0 ml-2" variant="outline" size="xs"><ShieldX className="mr-1" /> Not Available</Button>
          }
          </CardTitle>
          <CardDescription>
          Generative AI Chatbot for your Documents!
          </CardDescription>
          <hr style={{ width: '62%' }} />
          <div className="flex items-center gap-2">
          <small style={{ color: '#6c757d' }}>Powered by</small>
          <div className="flex items-center">
            <Image
              src={cmlicon}
              alt="CML Icon"
              width={50} // adjust as needed
              height={50} // adjust as needed
            />
            <Image
              src={cmltext}
              alt="CML Text"
              width={160} // adjust as needed
              height={50} // adjust as needed
            />
          </div>
          </div>
          <hr />

          <div className="md:absolute right-4 top-4 flex gap-4 pb-10">
            <Button disabled={isFinishedConversation} onClick={createNewChat}>
              <div className="flex items-center gap-2">
                <MessageSquarePlus className="h-4 w-4" />{" "}
                <div className="hidden md:block">New Chat</div>
              </div>
            </Button>
            <ConfigModal open={openConfigModal} setOpen={setOpenConfigModal} />
            <Card className="w-[350px]">
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
          className="max-w-5xl mx-auto relative py-10"
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
                    className="w-full"
                  >
                    {question}
                  </Button>
                ))}
              </div>
            </div>
          )}
        </CardContent>
        <CardFooter
          className="w-full mt-auto mb-0 max-w-5xl mx-auto"
          ref={footerRef}
        >
          <form
            className="w-full"
            onSubmit={(e) => {
              e.preventDefault();
              handleSubmit(chatInput);
            }}
          >
            <div className="w-full flex gap-2 items-end">
              <Input
                placeholder="How can I help you?"
                value={chatInput}
                disabled={isFinishedConversation}
                onChange={(e) => setChatInput(e.target.value)}
              />
              <Button
                disabled={isFinishedConversation || isWaiting || isTyping}
                ref={sendButtonRef}
                onClick={() => handleSubmit(chatInput)}
              >
                <Send className="h-4 w-4" />
              </Button>
            </div>
            <small className="ml-2 text-gray-500 text-xs">
              Current Model: <b>{model?.name || "No Model selected"}</b> | Generated content may be inaccurate. Check important info.
            </small>
          </form>
        </CardFooter>
      </Card>
    </section>
  );
}
