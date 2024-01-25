from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
# global model and tokenizer variables set to None then assigned a value in LoadModel()
model = None
tokenizer = None

# add here any model you want
ModelLocation = "../models/meta-llama_Llama-2-7b-chat-hf"
def LoadModel():
    global model
    global tokenizer
    # Load model
    BNBConfig = BitsAndBytesConfig(load_in_8bit=True,
                                    load_in_8bit_fp32_cpu_offload = True
                                   )
    model = AutoModelForCausalLM.from_pretrained(ModelLocation, device_map="auto", quantization_config=BNBConfig, max_memory={0: '8000Mib', "cpu": '30Gib'})
    tokenizer = AutoTokenizer.from_pretrained(ModelLocation, padding_side="left")

def GenerateText(word):
    global model
    global tokenizer

    ModelInput = tokenizer(["Generate an undertale-styled determination quote"], return_tensors="pt").to("cuda")
    GeneratedIds = model.generate(**ModelInput, max_new_tokens=50)
    output = tokenizer.batch_decode(GeneratedIds, skip_special_tokens=True)[0]
    print(output)



