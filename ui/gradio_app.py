import gradio as gr
from llms.agents import QAAgent, SummarizationAgent, ReasoningAgent
from ingestion.retriever import Retriever

# Initialize agents
qa_agent = QAAgent()
summ_agent = SummarizationAgent()
reason_agent = ReasoningAgent()
retriever = Retriever()  # For fetching context from Qdrant


# Handlers
def handle_qa(question):
    context, results = retriever.retrieve(question, top_k=5)
    return qa_agent.answer(context=context, question=question)


def handle_summarization(text):
    return summ_agent.summarize(text=text)


def handle_reasoning(question):
    return reason_agent.reason(question=question)


# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# 📚 Multi-Agent PDF Assistant")

    with gr.Tabs():
        # Q&A tab
        with gr.TabItem("Q&A"):
            gr.Markdown("Ask a question based on ingested PDFs.")
            question_input = gr.Textbox(
                label="Question", 
                placeholder="Ask something from your PDFs"
            )
            qa_output = gr.Textbox(label="Answer", lines=8)
            gr.Button("Get Answer").click(
                fn=handle_qa,
                inputs=[question_input],
                outputs=[qa_output]
            )

        # Summarization tab
        with gr.TabItem("Summarization"):
            gr.Markdown("Paste any text to get a clear summary.")
            text_input = gr.Textbox(
                label="Text / PDF Content", 
                lines=15, 
                placeholder="Paste the text to summarize"
            )
            summary_output = gr.Textbox(label="Summary", lines=10)
            gr.Button("Summarize").click(
                fn=handle_summarization,
                inputs=[text_input],
                outputs=[summary_output]
            )

        # Reasoning tab
        with gr.TabItem("Reasoning"):
            gr.Markdown("Ask a complex question requiring reasoning.")
            reasoning_input = gr.Textbox(
                label="Question", 
                placeholder="Enter a complex question"
            )
            reasoning_output = gr.Textbox(label="Stepwise Answer", lines=12)
            gr.Button("Reason").click(
                fn=handle_reasoning,
                inputs=[reasoning_input],
                outputs=[reasoning_output]
            )

if __name__ == "__main__":
    demo.launch()
