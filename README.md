🍹 Drink Recipe Generator

A playful, responsive app for discovering drink recipes based on your available ingredients. Instantly generate **cocktails, mocktails, smoothies, and more** with a creative AI twist.

[**Live Demo**](xxxxx) 

## 🖼️ App Preview

<p align="center">
  <img src="https://github.com/user-attachments/assets/1427aa15-6b4d-4f60-bf58-1e794acc2905" width="200"/>
  <img src="https://github.com/user-attachments/assets/e7b614b0-9278-4020-9bd7-9634deb319ca" width="200"/>
  <img src="https://github.com/user-attachments/assets/50b874b4-b5a9-4b6f-88c4-bbe875786ab7" width="200"/>
  <img src="https://github.com/user-attachments/assets/e4046125-17a9-4b29-b3da-0f25857417d1" width="200"/>
</p>



## 🏗️ Architecture

**Architecture Overview:**

- **Frontend** (React app): User interacts with the UI, which sends requests to the backend.
- **Backend** (FastAPI): Handles recipe logic, AI-powered drink generation, and manages favorites. Communicates with the Pexels service for images.
- **Pexels Service** (FastAPI microservice): Fetches relevant drink images from the Pexels API.

## ✨ Features

- **AI Recipe Generator:** Enter your ingredients to create a unique drink recipe.
- **Browse Drinks:** Explore a curated collection of recipes.
- **Random Drink:** Get a surprise suggestion.
- **Favorites:** Mark and revisit your favorite drinks.
- **Image Integration:** Each recipe includes a relevant image from Pexels.
- **Modern UI:** Responsive, accessible, and easy to use.

## 🛠️ Tech Stack

- **Frontend:** Vite, React, TypeScript, MUI, styled-components, React Context API
- **Backend:** FastAPI (Python), Pydantic models
- **AI:** Groq LLM for creative recipe generation
- **Images:** Pexels API via dedicated microservice
- **Infrastructure:** Docker & Docker Compose for full-stack orchestration

## 🚀 Getting Started

### Prerequisites

- [Docker](https://www.docker.com/) and Docker Compose installed
- API keys for [Groq](https://console.groq.com/keys) and [Pexels](https://www.pexels.com/api/key/)

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/EASS-HIT-PART-A-2025-CLASS-VII/its_five_pm_somewhere.git
   cd its_five_pm_somewhere
   ```

2. **Prepare environment variables:**

   - `backend/.env`:
     ```
     GROQ_API_KEY=your_groq_api_key
     ```
   - `pexels_service/.env`:
     ```
     PEXELS_API_KEY=your_pexels_api_key
     ```

3. **Build and run the app:**
   ```bash
   docker-compose up --build
   ```

4. **Access the app:**

   - Frontend: **[http://localhost:5173](http://localhost:5173)**
   - Backend: **[http://localhost:8000/docs](http://localhost:8000/docs)**
   - Pexels Service: **[http://localhost:9000/docs](http://localhost:9000/docs)**

## 🧪 Testing

- **Automated integration tests** run automatically when the Docker stack is started.

## 📁 Code Structure

| Directory         | Description                                      |
|-------------------|--------------------------------------------------|
| `frontend/`       | React app, hooks, context, and styled components |
| `backend/`        | FastAPI backend, models, routes, AI integration  |
| `pexels_service/` | Microservice for fetching images from Pexels     |
| `docker-compose.yml` | Orchestrates the full stack                   |

Certainly! Below is a well-structured "Advanced Code" section for your README, highlighting the key architectural and engineering decisions reflected in your codebase. This section is tailored to your implementation and includes the points you requested, plus additional best practices observed in your code.

## Advanced Code

This project demonstrates several advanced engineering practices to ensure performance, maintainability, and scalability across both frontend and backend components.

**Key advanced techniques include:**

- **Frontend Image Caching:**  
  Images fetched from the Pexels API are cached on the frontend, reducing redundant network requests and improving load times for users. This is particularly beneficial for repeated ingredient or drink image lookups, leading to a smoother user experience.

- **Debounce for API Calls:**  
  Debouncing is implemented on the frontend to limit the frequency of API calls, especially for image search or ingredient suggestions. This prevents unnecessary load on the backend and external APIs, optimizing both performance and cost.

- **Global State Management with React Context:**  
  React Context is used to manage global state, such as selected ingredients and user preferences, across the application. This approach avoids prop drilling and keeps the codebase modular and easy to maintain.

- **Strict Data Validation with Pydantic Models:**  
  The backend leverages Pydantic models for robust data validation and serialization. This ensures that all API inputs and outputs adhere to well-defined schemas, reducing bugs and improving API reliability.

- **Modular and Typed Backend Structure:**  
  The backend is organized into clear modules (models, routes, services), with type annotations throughout. This improves code readability and maintainability, and enables better tooling support (e.g., autocompletion, static analysis).

- **Comprehensive Automated Testing:**  
  Automated tests cover critical API endpoints, including success and error cases. This ensures reliability and enables safe refactoring and scaling of the codebase.

- **Dockerized Multi-Service Architecture:**  
  The project uses Docker Compose to orchestrate separate services for the backend, frontend, and the Pexels image proxy. This separation of concerns makes the system easier to develop, test, and deploy.

- **Asynchronous API Operations:**  
  The backend uses asynchronous HTTP clients (httpx) and async FastAPI endpoints where appropriate. This allows the server to handle many concurrent requests efficiently, especially when interacting with external APIs.

- **Environment-Based Configuration:**  
  Sensitive credentials and configuration values are managed via environment variables and `.env` files, keeping secrets out of the codebase and supporting multiple deployment environments.


Enjoy mixing and discovering new drinks! 🍸
