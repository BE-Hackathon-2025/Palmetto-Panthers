from Backend.services.firebase_service import get_user_data, update_user_summary
from Backend.services.llm_service import chat_with_claude, update_summary_with_llm

USER_ID = "xenfzFaXTmWWwpbxQFw6hyUji8I2"

if __name__ == "__main__":
    user_data = get_user_data(USER_ID)
    print(f"✅ Loaded user '{USER_ID}' data.\n")
    print("💬 Chat started (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in {"exit", "quit"}:
            print("👋 Ending chat.")
            break

        llm_response = chat_with_claude(user_data, user_input)
        print(f"\nAssistant:\n{llm_response}\n")

        new_summary = update_summary_with_llm(user_data, user_input, llm_response)
        update_user_summary(USER_ID, new_summary)
        user_data["summary"] = new_summary