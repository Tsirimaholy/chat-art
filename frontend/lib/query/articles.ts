import { PrismaClient } from "@/app/generated/prisma";

const prisma = new PrismaClient();

export async function getArticles(
  query: string = "",
  sort: "asc" | "desc" = "desc",
) {
  // simulate delay for API call
  await new Promise((resolve) => setTimeout(resolve, 1000));

  let articles = await prisma.article.findMany({
    orderBy: {
      date: sort,
    },
  });

  // Filter by search query if provided
  if (query) {
    const queryLower = query.toLowerCase();
    articles = articles.filter(
      (article) =>
        article.title.toLowerCase().includes(queryLower) ||
        article.summary.toLowerCase().includes(queryLower),
    );
  }

  return articles;
}
