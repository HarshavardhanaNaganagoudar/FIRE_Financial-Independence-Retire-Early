import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_NAME = "Qwen/Qwen3-0.6B"

model = None
tokenizer = None


def load_model():
    """
    Load the model only once.
    """

    global model
    global tokenizer

    if model is not None:
        return

    print("=" * 60)
    print("Loading Qwen3-0.6B...")
    print("=" * 60)

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype="auto",
        device_map="auto",
    )

    print("Model loaded successfully!")
    print("=" * 60)


def build_prompt(data):

    status = (
        "ON TRACK"
        if data["on_track"]
        else "NOT ON TRACK"
    )

    return f"""
You are FIRE Mentor, a friendly financial coach specializing in Financial Independence and Early Retirement (FIRE).

Your ONLY job is to explain the calculator's results. The calculator has already completed every financial calculation correctly.

========================
CRITICAL RULES
========================

- Never perform calculations.
- Never verify calculations.
- Never change or correct any number.
- Never estimate missing information.
- Never invent assumptions.
- Never contradict the calculator.
- Never say the user is "on track" if the calculator says "NOT ON TRACK".
- Never say the user is "not on track" if the calculator says "ON TRACK".
- Do not mention formulas, percentages, or financial calculations.
- Keep the response between 100 and 200 words.
- Do not simply repeat every number shown by the calculator.
- Instead, explain what the numbers mean.
- Mention at most two numeric values in your response.
- Focus on insights rather than repeating the results.
- Write in simple conversational English.
- Be encouraging but realistic.
- Do not use markdown.
- Do not use bullet points.
- Do not use headings.


========================
AUTHORITATIVE RESULT
========================

The calculator has already determined the user's retirement status.

Retirement Status:

{status}

Treat this as a FACT.

Repeat this status consistently throughout your response.

Do not reinterpret or contradict it.

========================
HOW TO RESPOND
========================

Write one short paragraph that includes:

1. A clear overall assessment using the retirement status above.
2. One positive observation.
3. One realistic concern.
4. Exactly one practical suggestion.
5. End with one short encouraging sentence.
6. All numbers must be in dollar format.

If the retirement expenses entered appear unusually low or unusually high, politely suggest reviewing that input instead of assuming it is wrong.

========================
USER PROFILE
========================

Current Age:
{data['age']}

Target Retirement Age:
{data['retirement_age']}

Years Remaining:
{data['years_left']}

Current Investment Corpus:
${data['current_corpus']:,.0f}

Current Monthly Investment:
${data['monthly_investment']:,.0f}

Expected Annual Retirement Expenses:
${data['annual_expenses']:,.0f}

========================
CALCULATOR RESULTS
========================

Required FIRE Corpus:
${data['fire_number']:,.0f}

Projected Corpus:
${data['projected_corpus']:,.0f}

Remaining Corpus Gap:
${data['gap']:,.0f}

Progress:
{data['progress_percent']}%

Required Monthly Investment:
${data['required_monthly_investment']:,.0f}

Retirement Status:
{status}
"""


def get_fire_advice(data, thinking=False):
    """
    Generate AI advice based on precomputed FIRE metrics.
    """

    load_model()

    prompt = build_prompt(data)

    messages = [
        {
            "role": "system",
            "content": "You are a concise personal finance coach.",
        },
        {
            "role": "user",
            "content": prompt,
        },
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=thinking,
    )

    model_inputs = tokenizer(
        text,
        return_tensors="pt",
    ).to(model.device)

    with torch.no_grad():
        output_ids = model.generate(
            **model_inputs,
            max_new_tokens=150,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )

    generated_ids = output_ids[:, model_inputs.input_ids.shape[1]:]

    response = tokenizer.batch_decode(
        generated_ids,
        skip_special_tokens=True,
    )[0]

    return response.strip()