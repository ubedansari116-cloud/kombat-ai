from src.llm_coach import LLMCoach

coach = LLMCoach()

response = coach.generate_response("""
Say hello in one sentence.
""")

print(response)