import { type NextRequest, NextResponse } from "next/server";
import { z } from "zod";

const chatRequestSchema = z.object({
  message: z.string().min(1, "Message cannot be empty"),
});

const PYTHON_SERVICE_URL = process.env.PYTHON_SERVICE_URL || "http://localhost:8001";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { message } = chatRequestSchema.parse(body);

    // Log the request
    console.log(`[${new Date().toISOString()}] Chat request: ${message}`);

    const response = await fetch(`${PYTHON_SERVICE_URL}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      throw new Error(`Python service responded with status: ${response.status}`);
    }

    const data = await response.json();

    // Log the response
    console.log(`[${new Date().toISOString()}] Chat response:`, data);

    return NextResponse.json(data);
  } catch (error) {
    console.error("Chat API error:", error);

    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: "Invalid request", details: error.message },
        { status: 400 }
      );
    }

    // If Python service is not available, return a mock response
    if (error instanceof TypeError && error.message.includes("fetch")) {
      console.log("Python service unavailable, returning mock response");
      return NextResponse.json({
        answer: "I'm sorry, the chat service is currently unavailable. Please try again later.",
        sources: ["system#unavailable"]
      });
    }

    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    );
  }
}