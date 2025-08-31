import gradio as gr
from llm.agents import QAAgent, SummarizationAgent, ReasoningAgent
from retrieval.retriever import Retriever

# Initialize agents
qa_agent = QAAgent()
summ_agent = SummarizationAgent()
reason_agent = ReasoningAgent()
retriever = Retriever()  # Fetch context from Qdrant

# Handlers
def handle_qa(question):
    if not question.strip():
        return "❌ Please enter a question."
    context, results = retriever.retrieve(question, top_k=5)
    return qa_agent.answer(context=context, question=question)

def handle_summarization(text):
    if not text.strip():
        return "❌ Please paste some text to summarize."
    return summ_agent.summarize(text=text)

def handle_reasoning(question):
    if not question.strip():
        return "❌ Please enter a question."
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
            gr.Button("Get Answer", variant="primary").click(
                fn=handle_qa,
                inputs=[question_input],
                outputs=[qa_output],
                show_progress=True
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
            gr.Button("Summarize", variant="primary").click(
                fn=handle_summarization,
                inputs=[text_input],
                outputs=[summary_output],
                show_progress=True
            )

        # Reasoning tab
        with gr.TabItem("Reasoning"):
            gr.Markdown("Ask a complex question requiring reasoning.")
            reasoning_input = gr.Textbox(
                label="Question", 
                placeholder="Enter a complex question"
            )
            reasoning_output = gr.Textbox(label="Stepwise Answer", lines=12)
            gr.Button("Reason", variant="primary").click(
                fn=handle_reasoning,
                inputs=[reasoning_input],
                outputs=[reasoning_output],
                show_progress=True
            )

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        show_error=True
    )
