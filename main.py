from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import uvicorn

# Initialize FastAPI app
app = FastAPI()

# OpenAI API key
openai.api_key = ''


class UserRequest(BaseModel):
    user_id: str
    session_data: str


user_profiles = {}


@app.post("/generate_summary/")
def generate_summary(request: UserRequest):
    # Storing user context for accurate advice generation on next session
    try:
        prompt = f"Summarize the user's progress in this session: {request.session_data}. Provide a summary that can be used to start the next session."
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        summary = response.choices[0].text.strip()
        user_profiles[request.user_id] = summary
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Retrieve user summary
@app.get("/get_summary/{user_id}")
def get_summary(user_id: str):
    if user_id in user_profiles:
        return {"summary": user_profiles[user_id]}
    else:
        raise HTTPException(status_code=404, detail="User not found")


# Run the app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

