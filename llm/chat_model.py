from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

class HuggingFaceModel:
    def __init__(self, model_name: str, device: str = "cuda"):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        # load model with auto device placement
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
            torch_dtype="auto"
        )

        # text generation pipeline
        self.pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device=0 if device == "cuda" else -1,
            max_new_tokens=512
        )

    def generate(self, prompt: str, temperature: float = 0.3, top_p: float = 0.9) -> str:
        output = self.pipe(prompt, do_sample=True, temperature=temperature, top_p=top_p)
        return output[0]["generated_text"]
