import Link from "next/link";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex flex-col min-h-screen">
      <header className="p-4">
        <Link href="/" className="inline text-2xl font-bold">Home</Link>
      </header>
      <h1 className="text-xl font-bold inline ml-4">Articles</h1>
      <main className="flex-1 p-4">{children}</main>
      <footer className=" text-white p-4">
        <p className="text-center">Articles</p>
      </footer>
    </div>
  );
}
