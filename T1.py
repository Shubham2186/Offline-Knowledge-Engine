def main():
    print("Offline Knowledge Engine")
    print("------------------------")

    while True:
        question = input("\nAsk a question (or type 'exit'): ")

        if question.lower() == "exit":
            print("Goodbye!")
            break

        # Temporary knowledge base
        knowledge = {
            "python": "Python is a high-level programming language.",
            "git": "Git is a version control system.",
            "github": "GitHub is a platform for hosting Git repositories.",
            "ai": "AI stands for Artificial Intelligence."
        }

        answer = knowledge.get(
            question.lower(),
            "Sorry, I don't have information about that yet."
        )

        print("Answer:", answer)


if __name__ == "__main__":
    main()
