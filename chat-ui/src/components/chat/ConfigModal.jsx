import { ChatContext } from "@/provider";
import { Button } from "@components/ui/button";
import { Input } from "@components/ui/input";
import { Label } from "@components/ui/label";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@components/ui/select";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@components/ui/card";
import { Badge } from "@components/ui/badge";
import { Send, MessageSquarePlus, MoveUpRight, Settings } from "lucide-react";
import {
  Sheet,
  SheetClose,
  SheetContent,
  SheetDescription,
  SheetFooter,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@components/ui/sheet";
import { useContext, useState } from "react";

export function ConfigModal({ open, setOpen }) {
  const {
    models,
    model,
    setModel,
    temperature,
    setTemperature,
    maxTokens,
    setMaxTokens,
    vectorDatabases,
    vectorDatabase,
    setVectorDatabase,
    userID,
    setUserID,
  } = useContext(ChatContext);

  const handleSetModel = (modelName) => {
    console.log(modelName, "======");
    for (const item of models) {
      if (item.name === modelName) {
        setModel(item);
        break;
      }
    }
  };

  const handleSetVectorDatabase = (databaseName) => {
    console.log(databaseName, "======");
    for (const item of vectorDatabases) {
      if (item.name === databaseName) {
        setVectorDatabase(item);
        break;
      }
    }
  };

  
  return (
    <Sheet open={open} onOpenChange={setOpen}>
      <SheetTrigger asChild></SheetTrigger>
      <SheetContent>
        <SheetHeader>
          <SheetTitle>Chatbot Configuration</SheetTitle>
          <SheetDescription>Configure your chatbot settings</SheetDescription>
        </SheetHeader>
        <div className="grid gap-4 py-4">

          <div className="flex justify-end items-center gap-4">
            <Label htmlFor="name" className="text-right whitespace-nowrap">
              Model
            </Label>
            <Select
              className="col-span-1"
              value={model?.name}
              onValueChange={(value) => handleSetModel(value)}
            >
              <SelectTrigger className="w-auto">
                <SelectValue placeholder="Select a model" />
              </SelectTrigger>
              <SelectContent>
                <SelectGroup>
                  {models.map((item) => (
                    <SelectItem key={item.name} value={item.name}>
                      {item.name}
                    </SelectItem>
                  ))}
                </SelectGroup>
              </SelectContent>
            </Select>
          </div>
          <div className="flex justify-end items-center gap-4">
            <Label htmlFor="temperature" className="text-right whitespace-nowrap">
              Temperature
              <br />
              <small>(Randomness of Response)</small>
            </Label>
            <Input
              id="temperature"
              type="number"
              value={temperature}
              onChange={(e) => setTemperature(e.target.value)}
            />
          </div>
          <div className="flex justify-end items-center gap-4">
            <Label htmlFor="maxTokens" className="text-right whitespace-nowrap">
              Number of Tokens <br /> <small>(Length of Response)</small>
            </Label>
            <Input
              id="maxTokens"
              type="number"
              value={maxTokens}
              onChange={(e) => setMaxTokens(e.target.value)}
            />
          </div>
          <div className="flex justify-end items-center gap-4">
            <Label htmlFor="name" className="text-right whitespace-nowrap">
              Vector dB
            </Label>
            <Select
              className="col-span-1"
              value={vectorDatabase?.name}
              onValueChange={(value) => handleSetVectorDatabase(value)}
            >
              <SelectTrigger className="w-auto">
                <SelectValue placeholder="Select a Vector DB" />
              </SelectTrigger>
              <SelectContent>
                <SelectGroup>
                { (vectorDatabases || []).map((item) => (
                    <SelectItem key={item.name} value={item.name}>
                      {item.name}
                    </SelectItem>
                  ))}
                </SelectGroup>
              </SelectContent>
            </Select>
          </div>
        <div className="flex justify-end items-center gap-4">
            <Label htmlFor="userID" className="text-right whitespace-nowrap">
              User ID
            </Label>
            <Input
              id="userID"
              type="text"
              value={userID}
              onChange={(e) => setUserID(e.target.value)}
            />
          </div>



        </div>
        <SheetFooter>
          <SheetClose asChild>
            <Button type="submit">Save</Button>
          </SheetClose>
        </SheetFooter>
      </SheetContent>
    </Sheet>
  );
}
