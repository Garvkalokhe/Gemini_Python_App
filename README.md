# Gemini Python Assistant

A Python-based AI assistant powered by **Google Gemini 3.1 Flash-Lite** with conversation history and real-time web search using the **Serper API**.

The application can handle normal conversations, remember previous interactions, and retrieve current information from Google Search when a question requires up-to-date data.

## Features

- AI-powered conversations using Gemini 3.1 Flash-Lite
- Conversation history using Gemini Interactions API
- Context-aware follow-up questions
- Real-time Google Search results using Serper API
- Current information retrieval for topics such as:
  - Bitcoin prices
  - Weather
  - News
  - Stock prices
  - Exchange rates
  - Other time-sensitive information
- Displays Google Search sources used for current-information queries
- Measures Google Search and Gemini response time
- Secure API key management using environment variables
- Command-line interface
- Error handling for API and network failures

## Project Architecture

```text
User
 |
 v
Python CLI
 |
 +------------------------------+
 |                              |
 | Normal Question              | Current Information
 |                              |
 v                              v
Gemini 3.1 Flash-Lite        Serper API
 |                              |
 |                              v
 |                         Google Search
 |                              |
 |                              v
 |                       Search Results
 |                              |
 +--------------+---------------+
                |
                v
        Gemini 3.1 Flash-Lite
                |
                v
          Final Response
```

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| Google Gemini 3.1 Flash-Lite | AI response generation |
| Gemini Interactions API | Conversation history |
| Serper API | Google Search results |
| Requests | HTTP/API requests |
| python-dotenv | Environment variable management |

## Project Structure

```text
Gemini_Python_App/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env
└── venv/
```

> `.env` and `venv/` are excluded from Git using `.gitignore`.

## How It Works

The application uses two different processing paths.

### 1. Normal Conversation

For general questions that do not require current information, the application sends the user's input directly to Gemini.

Example:

```text
You: My name is Garv and I am learning Python.

Gemini:
Hi Garv! ...
```

The application stores the Gemini interaction ID and uses it for subsequent requests.

Example:

```text
You: What is my name?

Gemini:
Your name is Garv.
```

This allows the assistant to maintain conversation context.

### 2. Current Information

When the user asks for information that may change over time, the application first performs a Google Search through the Serper API.

Example:

```text
You: What is the current Bitcoin price in USD?
```

The application:

1. Sends the question to Serper.
2. Retrieves Google Search results.
3. Extracts relevant search information.
4. Sends the search information to Gemini.
5. Gemini generates the final answer.
6. The application displays the sources used.

Example:

```text
Searching Google...
Google Search time: 1.70 seconds

Generating Gemini response...
Gemini response time: 4.51 seconds

Gemini:
[Current information based on search results]

Sources:
- Search result title
  https://example.com
```

## API Configuration

Create a `.env` file in the project root directory.

```env
GEMINI_API_KEY=your_gemini_api_key
SERPER_API_KEY=your_serper_api_key
```

Do not commit the `.env` file to GitHub.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Garvkalokhe/Gemini_Python_App.git
```

### 2. Open the project

```bash
cd Gemini_Python_App
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

Windows PowerShell:

```powershell
.\venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure API keys

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
SERPER_API_KEY=your_serper_api_key
```

### 7. Run the application

```bash
python main.py
```

## Example Queries

### General Conversation

```text
My name is Garv and I am learning Python.
```

```text
What is my name?
```

```text
Explain Python functions.
```

### Real-Time Information

```text
What is the current Bitcoin price in USD?
```

```text
What is the current weather in Mumbai?
```

```text
What are the latest news headlines?
```

```text
What is the current USD to INR exchange rate?
```

## Security

API credentials are loaded using environment variables through `python-dotenv`.

The following files are excluded from Git:

```text
.env
venv/
__pycache__/
*.pyc
```

Never upload API keys directly into source code or a public GitHub repository.

## API Architecture Note

This project uses **Gemini 3.1 Flash-Lite for AI generation** and the **Serper API as an external Google Search provider** for real-time web information.

The project does not claim to use Gemini's native Google Search grounding feature.

Serper was selected as the external search provider so that the application could provide Google Search-based current information while keeping the project within the available API configuration.

## Performance Monitoring

The application measures the processing time for both major external operations:

```text
Google Search time: X.XX seconds
Gemini response time: X.XX seconds
```

This provides basic visibility into API response latency during execution.

## Error Handling

The application handles:

- Missing API keys
- Google Search request failures
- Network errors
- Gemini API errors
- Empty user input
- Application exit commands

## Future Improvements

Potential future improvements include:

- Better intent detection for deciding when web search is required
- More structured search-result processing
- Improved source extraction
- Streaming Gemini responses
- Web-based user interface
- Conversation history persistence
- Additional external tools and APIs

## Author

**Garv Kalokhe**

B.Tech Computer Science Engineering

GitHub: https://github.com/Garvkalokhe