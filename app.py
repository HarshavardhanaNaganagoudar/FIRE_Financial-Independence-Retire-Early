import gradio as gr

from calculator import calculate_fire
from advisor import get_fire_advice


def fire_calculator(
    age,
    retirement_age,
    current_corpus,
    monthly_investment,
    annual_expenses,
    thinking,
):
    try:
        # ----------------------------
        # Input Validation
        # ----------------------------
        age = int(age)
        retirement_age = int(retirement_age)
        current_corpus = float(current_corpus)
        monthly_investment = float(monthly_investment)
        annual_expenses = float(annual_expenses)

        if retirement_age <= age:
            raise gr.Error(
                "Target retirement age must be greater than current age."
            )

        if current_corpus < 0:
            raise gr.Error(
                "Current corpus cannot be negative."
            )

        if monthly_investment < 0:
            raise gr.Error(
                "Monthly investment cannot be negative."
            )

        if annual_expenses <= 0:
            raise gr.Error(
                "Annual expenses must be greater than zero."
            )

        # ----------------------------
        # FIRE Calculation
        # ----------------------------
        result = calculate_fire(
            age=age,
            retirement_age=retirement_age,
            current_corpus=current_corpus,
            monthly_investment=monthly_investment,
            annual_expenses=annual_expenses,
        )

        # ----------------------------
        # AI Advice
        # ----------------------------
        data = {
            "age": age,
            "retirement_age": retirement_age,
            "current_corpus": current_corpus,
            "monthly_investment": monthly_investment,
            "annual_expenses": annual_expenses,
            "fire_number": result.fire_number,
            "projected_corpus": result.projected_corpus,
            "gap": result.gap,
            "progress_percent": result.progress_percent,
            "required_monthly_investment": result.required_monthly_investment,
            "years_left": result.years_left,
            "on_track": result.on_track,
        }

        try:
            advice = get_fire_advice(
                data,
                thinking=thinking,
            )
        except Exception as e:
            advice = (
                "⚠️ Unable to generate AI advice.\n\n"
                f"Reason:\n{str(e)}"
            )

        return (
            f"$ {result.fire_number:,.0f}",
            f"$ {result.projected_corpus:,.0f}",
            f"$ {result.gap:,.0f}",
            result.years_left,
            "✅ Yes" if result.on_track else "❌ No",
            f"{result.progress_percent:.1f}%",
            f"$ {result.required_monthly_investment:,.0f}",
            advice,
        )

    except Exception as e:
        raise gr.Error(str(e))


# =========================================================
# THEME — soft pastel, minimal fintech aesthetic
# =========================================================
theme = gr.themes.Base(
    primary_hue=gr.themes.colors.slate,
    neutral_hue=gr.themes.colors.stone,
    font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif"],
    font_mono=[gr.themes.GoogleFont("Space Grotesk"), "ui-monospace", "monospace"],
).set(
    body_background_fill="#F6F3EE",
    background_fill_primary="#FFFFFF",
    background_fill_secondary="#F1ECE4",
    border_color_primary="#E7E1D6",
    block_background_fill="#FFFFFF",
    block_border_width="0px",
    block_radius="24px",
    block_shadow="0 8px 30px rgba(60, 50, 40, 0.05)",
    block_label_background_fill="transparent",
    block_label_text_color="#8B8378",
    block_label_text_size="*text_sm",
    block_title_text_color="#2E2B27",
    input_background_fill="#FAF8F4",
    input_border_color="#E9E3D8",
    input_border_width="1px",
    input_radius="16px",
    button_primary_background_fill="#A9BFCF",
    button_primary_background_fill_hover="#93ABBD",
    button_primary_text_color="#242320",
    button_primary_border_color="#A9BFCF",
    button_large_radius="999px",
    button_large_padding="16px 28px",
    body_text_color="#2E2B27",
    body_text_color_subdued="#8B8378",
)

CUSTOM_CSS = """
.gradio-container {
    max-width: 880px !important;
    margin: auto !important;
}

/* Hero heading */
#hero h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 500;
    letter-spacing: -0.02em;
    color: #2E2B27;
}
#hero p {
    color: #8B8378;
    font-size: 0.95rem;
}

/* Section eyebrow label */
#results-heading h2 {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 500;
    font-size: 0.85rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #A9927B;
    margin-top: 8px;
    margin-bottom: 4px;
}

/* Card-like grouping */
.card-panel {
    background: #FFFFFF;
    border-radius: 24px !important;
    padding: 22px !important;
    box-shadow: 0 8px 30px rgba(60, 50, 40, 0.05);
    border: 1px solid #EFE9DE;
}

/* Big, calm number display for key metrics */
.metric-value textarea,
.metric-value input {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.6rem !important;
    font-weight: 500 !important;
    color: #2E2B27 !important;
    text-align: left;
    background: transparent !important;
    border: none !important;
}

/* Accent pill for the "on track" status */
#status-box textarea,
#status-box input {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.1rem !important;
    font-weight: 500 !important;
}

/* Advisor panel reads like a soft note card */
#advisor-box textarea {
    background: #F1ECE4 !important;
    border-radius: 18px !important;
    border: none !important;
    font-family: 'Inter', sans-serif !important;
    line-height: 1.55;
    color: #3A362F !important;
}

/* Checkbox row spacing */
#thinking-row {
    padding: 4px 2px 10px 2px;
}

/* Soften the info accordion */
#info-accordion {
    border-radius: 18px !important;
    background: #F1ECE4 !important;
    border: none !important;
}

/* Primary button full-width, pill-shaped */
#calc-btn {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 500;
    letter-spacing: 0.01em;
}
"""

with gr.Blocks(title="🔥 FIRE AI", theme=theme, css=CUSTOM_CSS) as demo:

    with gr.Column(elem_id="hero"):
        gr.Markdown(
            """
# 🔥 FIRE AI

What if work became a choice, not a necessity? 🔥 FIRE (Financial Independence, Retire Early) helps you estimate how much you need to invest today to achieve financial freedom sooner.
"""
        )

    with gr.Column(elem_classes="card-panel"):
        with gr.Row():
            age = gr.Number(label="Current Age", value=28)
            retirement_age = gr.Number(label="Target Retirement Age", value=40)

        current_corpus = gr.Number(
            label="Current Invested Corpus ($)",
            value=10000,
        )

        monthly_investment = gr.Number(
            label="Monthly Investment ($)",
            value=500,
        )

        annual_expenses = gr.Number(
            label="Expected Annual Expenses After Retirement ($)",
            value=6000,
        )

        with gr.Row(elem_id="thinking-row"):
            thinking = gr.Checkbox(
                label="🧠 Enable Thinking Mode (Slower, Better Reasoning)",
                value=False,
            )

        btn = gr.Button("🔥 Calculate & Get AI Advice", variant="primary", elem_id="calc-btn", size="lg")

    with gr.Column(elem_id="results-heading"):
        gr.Markdown("## Results")

    with gr.Column(elem_classes="card-panel"):
        with gr.Row():
            fire_number = gr.Textbox(label="🎯 FIRE Corpus", elem_classes="metric-value")
            projected = gr.Textbox(label="📈 Projected Corpus", elem_classes="metric-value")

        with gr.Row():
            gap = gr.Textbox(label="💰 Corpus Gap", elem_classes="metric-value")
            years = gr.Number(label="📅 Years Left", elem_classes="metric-value")

        with gr.Row():
            progress = gr.Textbox(label="📊 Progress", elem_classes="metric-value")
            status = gr.Textbox(label="✅ On Track?", elem_id="status-box")

        required_sip = gr.Textbox(
            label="💵 Required Monthly SIP",
            elem_classes="metric-value",
        )

    with gr.Column(elem_classes="card-panel"):
        advisor = gr.Textbox(
            label="🤖 AI FIRE Coach",
            lines=8,
            elem_id="advisor-box",
        )

    with gr.Accordion("ℹ️ What do these results mean?", open=False, elem_id="info-accordion"):

        gr.Markdown("""
    **🎯 FIRE Corpus:** The total investment corpus needed to retire based on your expected annual expenses.

    **📈 Projected Corpus:** The estimated value of your investments at your target retirement age.

    **💰 Corpus Gap:** The additional amount needed to reach your FIRE corpus ($0 means you've reached your goal).

    **📅 Years Left:** The number of years remaining until your target retirement age.

    **📊 Progress:** The percentage of your required FIRE corpus that you are projected to achieve.

    **✅ Retirement Status:** Indicates whether you are currently projected to meet your FIRE goal by your target retirement age.

    **💵 Required Monthly SIP:** The estimated monthly investment needed to achieve your FIRE corpus by your target retirement age.

    **🤖 AI FIRE Coach:** Personalized insights and suggestions based on your calculated FIRE results.

    ---
    **Calculator Assumptions**

    - Expected annual return: **12%**
    - Inflation: **6%**
    - Safe Withdrawal Rate (SWR): **4%**
    - All calculations are estimates and should not be considered financial advice.
    """)

    btn.click(
        fn=fire_calculator,
        inputs=[
            age,
            retirement_age,
            current_corpus,
            monthly_investment,
            annual_expenses,
            thinking,
        ],
        outputs=[
            fire_number,
            projected,
            gap,
            years,
            status,
            progress,
            required_sip,
            advisor,
        ],
    )

demo.launch()