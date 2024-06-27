import cohere
import time

def read_data(filename):
    data = []
    with open(filename, 'r') as f:
        lines = f.read().split("===")  # Split using the consistent delimiter
        for entry in lines:
            entry = entry.strip()
            if entry:
                prompt_start = entry.split('\nStart:')
                if len(prompt_start) == 2:
                    prompt = prompt_start[0].replace('Prompt:', '').strip()
                    start = prompt_start[1].strip()
                    data.append((prompt, start))
    return data

def generate_email(prompt, start_sentence, desired_length, few_shot_examples):
    cohere_api_key = 'dIGghIO8bwdavY8T44nItm4gJsifM4VYO6oTDrUL'
    co = cohere.Client(cohere_api_key)

    # Prepare few-shot examples for conditioning
    conditioning_prompt = ''
    if few_shot_examples:
        for example_prompt, example_email in few_shot_examples:
            conditioning_prompt += f'\n**Prompt:** {example_prompt}\n{example_email}\n\n'

    # Generate email using Cohere's co.generate with conditioning
    response = co.generate(
        model="command-nightly",
        prompt=f"{conditioning_prompt}\n{prompt}\n\n{start_sentence}",
        max_tokens=desired_length,
        temperature=0.750)
    output = response.generations[0].text

    return output

# Read prompts and start sentences from file
combined_data = read_data("prompts.txt")

# Define few-shot examples for each prompt (all professional emails)
few_shot_examples = {
    "Write me a professional email to my client.": [
        ("Subject: Follow-Up on Recent Order", "Dear [Client Name],\n\nI trust this email finds you well. I wanted to follow up on your recent order and ensure that everything is meeting your expectations. If you have any questions or concerns, please don't hesitate to reach out. We value your business and look forward to serving you again."),
        ("Subject: Thank You for Your Business", "Dear [Client Name],\n\nI wanted to express my sincere gratitude for choosing our services. Your recent order is greatly appreciated, and we are committed to providing you with the best possible experience. If there's anything more we can do for you, please let us know."),
    ],
    "Write me a professional email to my colleague.": [
        ("Subject: Collaborative Project Update", "Hi [Colleague],\n\nI hope this email finds you well. I wanted to provide you with an update on our collaborative project [Project Name]. We've made significant progress, and I believe your input on [specific task] will be valuable. Let's schedule a brief meeting to discuss further details."),
        ("Subject: Request for Input on Upcoming Meeting", "Hello [Colleague],\n\nI hope your day is going well. As we prepare for the upcoming meeting on [Topic], I would appreciate your input on [specific aspect]. Your expertise in this area will contribute to the success of our discussion."),
    ],
    "Write me a professional email to myself.": [
        ("Subject: Reflection and Goal Setting", "Dear Self,\n\nAs you reflect on your recent accomplishments, take a moment to appreciate the progress you've made. Looking ahead, consider setting specific goals for the upcoming weeks. Your dedication and hard work will undoubtedly lead to continued success."),
        ("Subject: Acknowledgment of Achievements", "Hello [Your Name],\n\nI wanted to acknowledge the recent achievements you've accomplished. Your dedication and commitment to your goals are commendable. Keep up the excellent work, and remember that each step forward is a step closer to your long-term objectives."),
    ],
}

# To ensure we stay within Cohere's free limits of 5 API calls/minute
desired_length = 250
calls_per_minute_limit = 5
call_interval_seconds = 60 / calls_per_minute_limit

with open("generated_fewshot_emails.txt", "w") as output_file:
    for prompt, start in combined_data:
        email_text = generate_email(prompt, start, desired_length, few_shot_examples.get(prompt))

        # Display the generated email
        print(f"\n**Prompt:** {prompt}")
        print(f"**Start Sentence:** {start}")
        print(f"**Desired Length:** {desired_length}")
        print(f"**Generated Email:**\n{email_text}")

        # Write the generated email and prompt to file
        output_file.write(f"**Prompt:** {prompt}\n")
        output_file.write(f"**Start Sentence:** {start}\n")
        output_file.write(f"**Desired Length:** {desired_length}\n")
        output_file.write(f"**Generated Email:**\n{email_text}\n\n")

        # Pause for the specified interval before the next API call
        time.sleep(call_interval_seconds)

print("\nAll emails generated and written to 'generated_fewshot_emails.txt'")
