from transformers import (
    AutoModelForCausalLM,
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    pipeline,
    BitsAndBytesConfig,
)
import torch


class HuggingFaceModel:
    def __init__(self, model_name: str, device: str = None, quantize: bool = False):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"

        # Detect model type (seq2seq vs causal)
        if any(x in model_name.lower() for x in ["t5", "bart", "pegasus", "mbart"]):
            model_class = AutoModelForSeq2SeqLM
            pipeline_task = "text2text-generation"
        else:
            model_class = AutoModelForCausalLM
            pipeline_task = "text-generation"

        # Decide quantization safely
        quantization_config = None
        if quantize and device == "cuda":
            print(f"🔹 Loading {model_name} in 4-bit quantized mode (GPU detected)")
            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=True,
                bnb_4bit_compute_dtype=torch.float16,
            )
        elif quantize:
            print(f"⚠️ Quantization requested but no GPU found. Loading {model_name} normally.")

        # Load model
        self.model = model_class.from_pretrained(
            model_name,
            device_map="auto",
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            quantization_config=quantization_config,
        )

        # Create pipeline
        self.pipe = pipeline(
            pipeline_task,
            model=self.model,
            tokenizer=self.tokenizer,
            device=0 if device == "cuda" else -1,
            max_new_tokens=512,
        )

    def generate(self, prompt: str, temperature: float = 0.3, top_p: float = 0.9) -> str:
        output = self.pipe(prompt, do_sample=True, temperature=temperature, top_p=top_p)
        return output[0]["generated_text"]
