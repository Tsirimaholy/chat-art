import { type NextRequest, NextResponse } from "next/server";
import { z } from "zod";
import { getArticles } from "@/lib/query/articles";

const querySchema = z.object({
  query: z.string().optional().default(""),
  sort: z.enum(["asc", "desc"]).optional().default("desc"),
});

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;
    const params = querySchema.parse({
      query: searchParams.get("query") || "",
      sort: searchParams.get("sort") || "desc",
    });
    const articles = await getArticles(params.query, params.sort);
    return NextResponse.json(articles);
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: "Invalid parameters", details: error.message },
        { status: 400 },
      );
    }

    console.error("Error fetching articles:", error);
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 },
    );
  }
}
