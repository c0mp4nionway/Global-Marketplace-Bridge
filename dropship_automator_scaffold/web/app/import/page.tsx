'use client';
import { useState } from 'react';

export default function ImportPage() {
  const [aliId, setAliId] = useState('12345');
  const [res, setRes] = useState<any>(null);

  async function onImport() {
    const body = { ali_id: aliId };
    const r = await fetch(process.env.NEXT_PUBLIC_API_BASE + '/import', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    });
    setRes(await r.json());
  }

  return (
    <section>
      <h1>Import</h1>
      <input value={aliId} onChange={(e)=>setAliId(e.target.value)} placeholder="AliExpress ID" />
      <button onClick={onImport} style={{ marginLeft: 8 }}>Import</button>
      <pre>{res ? JSON.stringify(res, null, 2) : '...'}</pre>
    </section>
  );
}
