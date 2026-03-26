"use client";

import { useEffect, useState } from "react";

type MeResponse = {
  id: string;
  auth0_id: string;
  email: string | null;
  name: string | null;
};

export default function MeCard() {
  const [data, setData] = useState<MeResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function load() {
      try {
        const tokenRes = await fetch("/auth/access-token");
        const tokenJson = await tokenRes.json();

        const accessToken = tokenJson.token;
        if (!accessToken) {
          throw new Error("No access token returned");
        }

        const apiUrl = process.env.NEXT_PUBLIC_API_URL;
        const res = await fetch(`${apiUrl}/me`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });

        if (!res.ok) {
          throw new Error(`Backend returned ${res.status}`);
        }

        const json = await res.json();
        setData(json);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Unknown error");
      }
    }

    load();
  }, []);

  if (error) return <p className="mt-4 text-red-600">{error}</p>;
  if (!data) return <p className="mt-4">Loading backend user…</p>;

  return (
    <div className="mt-4 rounded border p-4">
      <p><strong>ID:</strong> {data.id}</p>
      <p><strong>Name:</strong> {data.name ?? "-"}</p>
      <p><strong>Email:</strong> {data.email ?? "-"}</p>
    </div>
  );
}