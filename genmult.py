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

def generate_email(prompt, start_sentence, desired_length):
    cohere_api_key = 'dIGghIO8bwdavY8T44nItm4gJsifM4VYO6oTDrUL'
    co = cohere.Client(cohere_api_key)

    # Generate email using Cohere's co.generate
    response = co.generate(
        model="command-nightly",
        prompt=f"{prompt}\n\n{start_sentence}",
        max_tokens=desired_length,
        temperature=0.750)
    output = response.generations[0].text

    return output

# Read prompts and start sentences from file
combined_data = read_data("prompts.txt")

# To ensure we stay within cohere's free limits of 5 API calls/minute
desired_length = 250
calls_per_minute_limit = 5
call_interval_seconds = 60 / calls_per_minute_limit

with open("generated_emails.txt", "w") as output_file:
    for prompt, start in combined_data:
        email_text = generate_email(prompt, start, desired_length)

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

print("\nAll emails generated and written to 'generated_emails.txt'")