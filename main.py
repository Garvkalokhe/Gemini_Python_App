import time
import os
import requests
from dotenv import load_dotenv
from google import genai


# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

if not SERPER_API_KEY:
    raise ValueError("SERPER_API_KEY not found in .env file")


# Create Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-3.1-flash-lite"


def google_search(query):
    """Search Google using Serper API."""

    url = "https://google.serper.dev/search"

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "q": query,
        "num": 5
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=15
    )

    response.raise_for_status()

    return response.json()


def format_search_results(search_data):
    """Convert Google Search results into compact text for Gemini."""

    results = search_data.get("organic", [])

    if not results:
        return "No search results were found."

    formatted_results = []

    for result in results[:3]:

        title = result.get("title", "No title")
        snippet = result.get("snippet", "")

        formatted_results.append(
            f"{title}\n{snippet}"
        )

    return "\n\n".join(formatted_results)


def needs_search(question):
    """Determine whether the question needs current web information."""

    search_keywords = [
        "current",
        "today",
        "latest",
        "recent",
        "news",
        "price",
        "weather",
        "temperature",
        "bitcoin",
        "stock",
        "exchange rate",
        "live",
        "now"
    ]

    question_lower = question.lower()

    return any(
        keyword in question_lower
        for keyword in search_keywords
    )


print("\n====================================")
print("       Gemini Python Assistant")
print("====================================")
print("Gemini 3.1 Flash-Lite + Google Search")
print("Conversation history enabled.")
print("Type 'exit' to stop.\n")


previous_interaction_id = None


while True:

    user_input = input("You: ").strip()

    if user_input.lower() == "exit":
        print("\nGemini: Goodbye!")
        break

    if not user_input:
        continue

    try:

        # ==========================================
        # NORMAL CONVERSATION
        # ==========================================

        if not needs_search(user_input):

            print("\nGenerating Gemini response...")

            gemini_start = time.time()

            if previous_interaction_id:

                response = client.interactions.create(
                    model=MODEL_NAME,
                    input=user_input,
                    previous_interaction_id=previous_interaction_id
                )

            else:

                response = client.interactions.create(
                    model=MODEL_NAME,
                    input=user_input
                )

            gemini_time = time.time() - gemini_start

            print(
                f"Gemini response time: "
                f"{gemini_time:.2f} seconds"
            )

            previous_interaction_id = response.id

            print("\nGemini:")
            print(response.output_text)
            print()

        # ==========================================
        # GOOGLE SEARCH + GEMINI
        # ==========================================

        else:

            print("\nSearching Google...")

            search_start = time.time()

            search_data = google_search(user_input)

            search_time = time.time() - search_start

            print(
                f"Google Search time: "
                f"{search_time:.2f} seconds"
            )

            search_results = format_search_results(
                search_data
            )

            # ======================================
            # PREPARE GEMINI PROMPT
            # ======================================

            prompt = f"""
Answer this question using the Google Search results.

Question:
{user_input}

Search results:
{search_results}

Give a concise and factual answer.
Use the latest information available in the results.
Do not invent information.
"""

            # ======================================
            # GEMINI REQUEST
            # ======================================

            print("Generating Gemini response...")

            gemini_start = time.time()

            if previous_interaction_id:

                response = client.interactions.create(
                    model=MODEL_NAME,
                    input=prompt,
                    previous_interaction_id=previous_interaction_id
                )

            else:

                response = client.interactions.create(
                    model=MODEL_NAME,
                    input=prompt
                )

            gemini_time = time.time() - gemini_start

            print(
                f"Gemini response time: "
                f"{gemini_time:.2f} seconds"
            )

            # ======================================
            # SAVE CONVERSATION HISTORY
            # ======================================

            previous_interaction_id = response.id

            # ======================================
            # DISPLAY ANSWER
            # ======================================

            print("\nGemini:")
            print(response.output_text)

            # ======================================
            # DISPLAY SOURCES
            # ======================================

            print("\nSources:")

            organic_results = search_data.get(
                "organic",
                []
            )

            for result in organic_results[:3]:

                title = result.get(
                    "title",
                    "Unknown"
                )

                link = result.get(
                    "link",
                    ""
                )

                print(f"- {title}")
                print(f"  {link}")

            print()

    except requests.exceptions.RequestException as error:

        print("\nGoogle Search request failed:")
        print(error)
        print()

    except Exception as error:

        print("\nRequest failed:")
        print(error)
        print()