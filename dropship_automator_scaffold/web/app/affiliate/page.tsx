'use client';
import { useState } from 'react';

export default function AffiliatePage() {
  const [aliId, setAliId] = useState('12345');
  const [res, setRes] = useState<any>(null);

  async function gen() {
    const r = await fetch(process.env.NEXT_PUBLIC_API_BASE + '/affiliate/link?ali_id=' + aliId);
    setRes(await r.json());
  }
  return (
    <section>
      <h1>Affiliate Links</h1>
      <p>Generate an AliExpress deep link (simulation).</p>
      <input value={aliId} onChange={(e)=>setAliId(e.target.value)} placeholder="AliExpress ID" />
      <button onClick={gen} style={{ marginLeft: 8 }}>Generate</button>
      <pre>{res ? JSON.stringify(res, null, 2) : '...'}</pre>
    </section>
  );
}
