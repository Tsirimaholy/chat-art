import { Suspense } from "react";
import { ArticleList } from "@/components/articles/articles-list";
import Loading from "@/components/articles/loading-component";
import { ChatWidget } from "@/components/chat/chat-widget";
import { ChatErrorBoundary } from "@/components/chat/chat-error-boundary";

interface PageProps {
  searchParams: {
    query?: string;
    sort?: "asc" | "desc";
  };
}

export default async function ArticlesPage({ searchParams }: PageProps) {
  const { query = "", sort = "desc" } = (await searchParams) || {};

  return (
    <div className="mx-auto px-4 max-w-7xl">
      <div className="flex gap-6">
        {/* Main Content */}
        <div className="flex-1">
          <form className="mb-4 flex justify-center gap-4">
            <input
              type="text"
              name="query"
              defaultValue={query}
              placeholder="Search articles..."
              className="border border-gray-300 rounded-md px-3 py-2 w-full"
            />
            <div className="flex flex-col">
              <label htmlFor="sort">Sort date:</label>
              <select
                name="sort"
                defaultValue={sort}
                className="border border-gray-300 rounded-md px-3 py-2"
              >
                <option value="asc">Ascending</option>
                <option value="desc">Descending</option>
              </select>
            </div>
            <button
              type="submit"
              className="bg-blue-500 text-white px-4 py-2 rounded-md"
            >
              Search
            </button>
          </form>
          <Suspense fallback={<Loading />}>
            <ArticleList query={query} sort={sort} />
          </Suspense>
        </div>
        
        {/* Chat Widget Sidebar */}
        <div className="w-80 flex-shrink-0">
          <div className="sticky top-4">
            <ChatErrorBoundary>
              <ChatWidget />
            </ChatErrorBoundary>
          </div>
        </div>
      </div>
    </div>
  );
}
