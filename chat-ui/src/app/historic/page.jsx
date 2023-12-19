import React from 'react';
import {
  Card, CardContent, CardHeader, CardTitle,
} from '@components/ui/card';
import { Header, HistoricTable } from '@/components';

export default function Home() {
  return (
    <main className="flex flex-col max-w-5xl m-auto min-h-screen">
      <div className="flex mb-20 justify-end">
        <Header />
      </div>
      <div>
        <Card className="">
          <CardHeader>
            <CardTitle>Historic</CardTitle>
          </CardHeader>
          <CardContent>
            <HistoricTable />
          </CardContent>
        </Card>
      </div>
    </main>
  );
}
