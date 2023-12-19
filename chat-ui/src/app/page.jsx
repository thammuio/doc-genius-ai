import React from "react";
import { Chat, Header } from "@/components";

export default function Home() {
  return (
    <main className="flex flex-col m-auto h-screen">
      <Header />
      <Chat />
    </main>
  );
}
