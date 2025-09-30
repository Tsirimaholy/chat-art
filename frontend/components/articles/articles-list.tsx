import type { Article } from "@/app/generated/prisma";

interface ArticlesWithSuspenseProps {
  query: string;
  sort: "asc" | "desc";
}

export async function ArticleList({ query, sort }: ArticlesWithSuspenseProps) {
  const res = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:3000"}/api/articles?query=${query}&sort=${sort}`,
  );

  const articles = await res.json() as Article[];

  return (
    <ul className="space-y-2">
      {articles.length > 0 ? (
        articles.map((article) => (
          <li key={article.id} className="p-3 rounded-lg border">
            <h2 className="font-semibold">{article.title}</h2>
            {article.summary && (
              <p className="text-gray-600 text-sm mt-1">{article.summary}</p>
            )}
            {article.date && (
              <p className="text-gray-600 text-sm mt-1">
                {new Date(article.date).toLocaleDateString()}
              </p>
            )}
          </li>
        ))
      ) : (
        <li className="p-3 rounded-lg">
          <p className="text-gray-600 text-sm mt-1">No articles found.</p>
        </li>
      )}
    </ul>
  );
}
