import { auth0 } from "@/lib/auth0";

export default async function HomePage() {
  const session = await auth0.getSession();
  const user = session?.user;

  return (
    <main className="p-8">
      <h1 className="text-2xl font-bold">SplitSmart</h1>

      {user ? (
        <div className="mt-4 space-y-3">
          <p>Welcome, {user.name ?? user.email}</p>
          <a href="/dashboard" className="underline">
            Go to dashboard
          </a>
          <br />
          <a href="/auth/logout" className="underline">
            Logout
          </a>
        </div>
      ) : (
        <div className="mt-4">
          <a href="/auth/login" className="underline">
            Login
          </a>
        </div>
      )}
    </main>
  );
}