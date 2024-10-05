"use client";

import React from "react";
import Link from "next/link";
import Image from "next/image";
import {
  NavigationMenu,
  NavigationMenuList,
  NavigationMenuItem,
  NavigationMenuLink,
  navigationMenuTriggerStyle,
} from "./ui/navigation-menu";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@components/ui/popover";
import { Menu } from "lucide-react";
import logo from '../images/cloudera-newco-logo.svg';
// import cnowlogo from '../images/cnow-logo.png';

const menuItems = [
  {
    name: "Try Cloudera",
    href: "https://trycloudera.com",
  },
  {
    name: "Products",
    href: "https://www.cloudera.com/products.html",
  },
  {
    name: "Solutions",
    href: "https://www.cloudera.com/solutions.html",
  },
  {
    name: "Resources",
    href: "https://www.cloudera.com/resources.html",
  },
  {
    name: "Support",
    href: "https://www.cloudera.com/services-and-support.html",
  },
];

const navigation = [
  { name: "Products", href: "/" },
  { name: "Cloudera", href: "/playground" },
];

export default function Header() {
  return (
    <header className="flex py-2 justify-between px-8 bg-white">
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
        <Image
          src={logo}
          alt="Cloudera Logo"
          style={{ height: '70%', width: 'auto', objectFit: 'contain' }}
        />
      </div>
      <Popover>
        <PopoverTrigger>
          <button className="md:hidden">
            <Menu color="white" size={24} />
          </button>
        </PopoverTrigger>
        <PopoverContent className="bg-[#132329] border-white/30 mr-4 ml-4">
          <NavigationMenu className="self-end">
            <NavigationMenuList>
              <NavigationMenuItem className="flex flex-col gap-4">
                {menuItems.map((item) => (
                  <Link href={item.href} legacyBehavior passHref>
                    <NavigationMenuLink
                      className="bg-transparent text-white py-2 border-[#132329] border-solid border-b-[1px] hover:border-white"
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      {item.name}
                    </NavigationMenuLink>
                  </Link>
                ))}
              </NavigationMenuItem>
            </NavigationMenuList>
          </NavigationMenu>
        </PopoverContent>
      </Popover>
      <NavigationMenu className="self-end hidden md:flex">
        <NavigationMenuList>
          <NavigationMenuItem className="flex space-x-10">
            {menuItems.map((item) => (
              <Link href={item.href} legacyBehavior passHref>
                <NavigationMenuLink
                  className="bg-transparent text-black py-2 border-white border-solid border-b-[1px] hover:border-[#132329]"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {item.name}
                </NavigationMenuLink>
              </Link>
            ))}
          </NavigationMenuItem>
        </NavigationMenuList>
      </NavigationMenu>
    </header>
  );
}
