'use client';

import React, { useContext } from 'react';

import {
  Table, TableBody, TableCaption, TableCell, TableHead, TableHeader, TableRow,
} from '@components/ui/table';
import { ChatContext } from '@/provider';
import { Button } from '@components/ui/button';

const columns = [
  {
    acessoryKey: 'id',
    header: 'ID',
  },
  {
    acessoryKey: 'title',
    header: 'Title',
  },
];

const createCSVContent = ({ messages }) => {
  const csvData = messages.map((message) => ({
    ID: message.id,
    Role: message.role,
    Content: message.content,
  }));

  return [
    ['ID', 'Role', 'Content'],
    ...csvData.map((row) => [row.ID, row.Role, row.Content]),
  ]
    .map((row) => row.join(','))
    .join('\n');
};

const downloadCSV = (csvContent) => {
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);

  const link = document.createElement('a');
  link.href = url;
  link.download = 'chat_history.csv';
  link.style.display = 'none';
  document.body.appendChild(link);

  link.click();

  document.body.removeChild(link);
  URL.revokeObjectURL(url);
};

export default function HistoricTable() {
  const { historicMessages } = useContext(ChatContext);

  const handleDownloadCSV = (historic) => {
    const csvContent = createCSVContent(historic);
    downloadCSV(csvContent);
  };

  return (
    <Table>
      <TableCaption>Historic conversations</TableCaption>
      <TableHeader>
        <TableRow>
          {columns.map((
            { acessoryKey, header },
          ) => <TableHead key={acessoryKey}>{header}</TableHead>)}
        </TableRow>
      </TableHeader>
      <TableBody>
        {
          historicMessages.length > 0 ? historicMessages.map((historic) => (
            <TableRow key={historic.id}>
              <TableCell>{historic.id}</TableCell>
              <TableCell>{historic.title}</TableCell>
              <TableCell>
                <Button onClick={() => handleDownloadCSV(historic)}>Download</Button>
              </TableCell>

            </TableRow>
          )) : (
            <TableRow>
              <TableCell colSpan={columns.length} className="h-24 text-center">No results.</TableCell>
            </TableRow>
          )
        }
      </TableBody>
    </Table>
  );
}
