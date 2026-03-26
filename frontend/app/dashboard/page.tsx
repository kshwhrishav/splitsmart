import { auth0 } from "@/lib/auth0";
import { redirect } from "next/navigation";
import MeCard from "./UserCard";

export default async function DashboardPage() {
  const session = await auth0.getSession();

  if (!session) {
    redirect("/auth/login");
  }

  return (
    <main className="p-8">
      <h1 className="text-2xl font-bold">Dashboard</h1>
      <p className="mt-2">Welcome {session.user.name ?? session.user.email}</p>
      <MeCard />
      <a href="/auth/logout" className="underline">
        Logout
      </a>
    </main>
  );
}