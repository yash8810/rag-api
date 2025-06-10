import groq
from retriever import retrieve_similar
import os

# Initialize xAI Grok API client
client = groq.Groq(api_key="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")

def generate_response(user_query, user_data=None):
    # """Generate a short and accurate LLM response for regression-related queries using retrieved data."""
    # retrieved_context = retrieve_similar(user_query, top_k=3)
    # print("🔍 Retrieved Context for Query:", user_query)
    # print("Context:", retrieved_context)
    # if not retrieved_context.strip():
    #     print("⚠️ Warning: Retrieved context is empty!")
    
    # user_info = "" if not user_data else "\n".join([f"{key}: {value}" for key, value in user_data.items() if value])

    prompt = f"""
    You are a professional assistant with expertise in regression algorithms like Linear Regression.
Use regression outputs and user data (age, weight, goals, activity level, dietary preferences) to provide a personalized, detailed response **based on the user's query**.

Respond according to the type of request:
- If the user asks for a **meal or diet plan**, provide a full-day plan with calorie and macronutrient breakdowns.
- If the user asks for a **workout routine**, provide a structured plan with exercises, sets, reps, and rest periods tailored to their goal.
- If the user asks for a **recipe**, provide a healthy, goal-aligned recipe with ingredients, cooking steps, and nutrition facts.
- If the user requests **any combination** (e.g., recipe + diet plan), include all relevant parts together in a clear and structured format.

Keep the response helpful, realistic, and tailored to user goals such as fat loss, muscle gain, or maintenance. Avoid repetition, speculation, or unnecessary detail.
    ---
    Context:
    {user_data}

    User Query:
    {user_query}


    Response:
    """

    response = client.chat.completions.create(
        model="llama3-8b-8192",  # Use grok-beta or grok-2-1212 if available
        messages=[
            {"role": "system", "content": "You are a concise regression expert."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=120,
        top_p=0.8
    )

    return response.choices[0].message.content.strip()

# if __name__ == "__main__":
#     query = "What is internet marketing success?"
#     user_data = {"business_type": "e-commerce", "experience_level": "beginner"}
#     response = generate_response(query, user_data)
#     print(f"\nResponse: {response}")
