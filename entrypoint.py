

if __name__ == "__main__":
    try:
        # Import the Gradio app object
        from ui.gradio_app import demo

        # Launch Gradio server
        demo.launch(
            server_name="0.0.0.0",  # accessible from host machine
            server_port=7860,        # default Gradio port
            share=False,             # set True if you want a public link via Gradio
            debug=True               # optional, useful for development
        )

    except Exception as e:
        print("❌ Failed to launch Gradio app:", e)
