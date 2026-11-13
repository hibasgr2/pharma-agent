import os
from dotenv import load_dotenv

load_dotenv()

model = os.getenv("OPENAI_MODEL")
embedding = os.getenv("OPENAI_EMBEDDING_MODEL")

print("OPENAI_MODEL:", model)
print("OPENAI_EMBEDDING_MODEL:", embedding)

if model and embedding:
    print("✅ .env loaded successfully!")
else:
    print("❌ Some environment variables are missing!")