import gradio as gr
from llms.agents import QAAgent, SummarizationAgent, ReasoningAgent

# Initialize agents
qa_agent = QAAgent()
summ_agent = SummarizationAgent()
reason_agent = ReasoningAgent()


def handle_qa(context, question):
    return qa_agent.answer(context=context, question=question)


def handle_summarization(text):
    return summ_agent.summarize(text=text)


def handle_reasoning(question):
    return reason_agent.reason(question=question)


with gr.Blocks() as demo:
    gr.Markdown("#  Multi-Agent PDF Assistant")

    with gr.Tabs():
        # Q&A tab
        with gr.TabItem("Q&A"):
            context_input = gr.Textbox(label="Context / PDF Chunks", lines=10, placeholder="Paste extracted text here...")
            question_input = gr.Textbox(label="Question", placeholder="Ask something based on the context")
            qa_output = gr.Textbox(label="Answer", lines=5)
            gr.Button("Get Answer").click(
                fn=handle_qa,
                inputs=[context_input, question_input],
                outputs=[qa_output]
            )

        # Summarization tab
        with gr.TabItem("Summarization"):
            text_input = gr.Textbox(label="Text / PDF Content", lines=15, placeholder="Paste the text to summarize")
            summary_output = gr.Textbox(label="Summary", lines=10)
            gr.Button("Summarize").click(
                fn=handle_summarization,
                inputs=[text_input],
                outputs=[summary_output]
            )

        # Reasoning tab
        with gr.TabItem("Reasoning"):
            reasoning_input = gr.Textbox(label="Question", placeholder="Enter complex question")
            reasoning_output = gr.Textbox(label="Stepwise Answer", lines=10)
            gr.Button("Reason").click(
                fn=handle_reasoning,
                inputs=[reasoning_input],
                outputs=[reasoning_output]
            )

if __name__ == "__main__":
    demo.launch()
