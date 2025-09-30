export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex flex-col min-h-screen">
      <header className="text-white p-4">
        <h1 className="text-2xl font-bold">Articles</h1>
      </header>
      <main className="flex-1 p-4">{children}</main>
      <footer className=" text-white p-4">
        <p className="text-center">Articles</p>
      </footer>
    </div>
  );
}
