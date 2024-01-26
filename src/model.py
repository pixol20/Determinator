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

def GenerateText(purpose=""):
    NoPurposeTemplate = [
        {"role": "system",
         "content": "You are an undertale quote generator that responds only with quote and nothing else. Your resposes may be interesting and unexpected but always inspiring. Your output shouldn't contain double or single quotes. You finish your sentence with 'fills you with determination'"},
        {"role": "user", "content": "Generate an undertale-styled determination quote"},
        {"role": "assistant","content": "Knowing the mouse might one day leave its hole and get the cheese... It fills you with determination."},
        {"role": "user", "content": "Generate an undertale-styled determination quote"},
        {"role": "assistant", "content": "You feel a calming tranquility. You're filled with determination..."},
        {"role": "user", "content": "Generate an undertale-styled determination quote"},
        {"role": "assistant", "content": "You feel... something... It's determination"},
        {"role": "user", "content": "Generate an undertale-styled determination quote"},
        {"role": "assistant", "content": "Your heartbeat fills you with determination"},
        {"role": "user", "content": "Generate an undertale-styled determination quote"},
        {"role": "assistant", "content": "Through trials and tribulations, your unbreakable will fills you with determination."},
        {"role": "user", "content": "Generate an undertale-styled determination quote"},
        {"role": "assistant", "content": "In the quiet moments, the strength within you resonates and fills you with determination"},
        {"role": "user", "content": "Generate an undertale-styled determination quote"},
        {"role": "assistant", "content": "Each obstacle you overcome fills you with determination"},
        {"role": "user", "content": "Generate an undertale-styled determination quote"}
    ]

    Template = [
        {"role": "system",
         "content": "You are an undertale quote generator that responds only with quote and nothing else. Your resposes may be interesting and unexpected but always inspiring. You pay attention to why user needs determination. Your output shouldn't contain double or single quotes. You finish your sentence with 'fills you with determination'"},
        {"role": "user", "content": "Generate an undertale-styled determination quote i need it to think about cheese"},
        {"role": "assistant",
         "content": "Knowing the mouse might one day leave its hole and get the cheese. It fills you with determination."},
        {"role": "user", "content": "Generate an undertale-styled determination quote i need it to calm down"},
        {"role": "assistant", "content": "You feel a calming tranquility. You're filled with determination."},
        {"role": "user", "content": "Generate an undertale-styled determination quote i need it to change something in my life"},
        {"role": "assistant", "content": "You feel strong will to change something in your life. This will fills you with determination"},
        {"role": "user", "content": "Generate an undertale-styled determination quote i need it to continue my hard path"},
        {"role": "assistant",
         "content": "Through trials and tribulations, your unbreakable will fills you with determination."},
        {"role": "user", "content": "Generate an undertale-styled determination quote i need it to start programming"},
        {"role": "assistant",
         "content": "You suddenly feel that you like programming and computers. This feeling fills you with determination"},
        {"role": "user", "content": "Generate an undertale-styled determination quote i need it confess in love"},
        {"role": "assistant",
         "content": "Your heart gives you feeling of love. That feeling fills you with determination"},
        {"role": "user", "content": "Generate an undertale-styled determination quote i need it confess love"},
        {"role": "assistant",
         "content": "You feel love. It fills you with determination to confess your feelings"},
        {"role": "user", "content": "Generate an undertale-styled determination quote i need it " + purpose}
    ]
    global model
    global tokenizer
    if purpose == "":
        tokenized_chat = tokenizer.apply_chat_template(NoPurposeTemplate, tokenize=True, add_generation_prompt=True,
                                                       return_tensors="pt").to("cuda")
        GeneratedIds = model.generate(tokenized_chat, max_new_tokens=250)
        output = tokenizer.batch_decode(GeneratedIds, skip_special_tokens=True)[0]
        output = output[1296:]
        print(output)
        return output
    else:
        tokenized_chat = tokenizer.apply_chat_template(Template, tokenize=True, add_generation_prompt=True,
                                                       return_tensors="pt").to("cuda")
        GeneratedIds = model.generate(tokenized_chat, max_new_tokens=250)
        output = tokenizer.batch_decode(GeneratedIds, skip_special_tokens=True)[0]
        output = output[1679+len(purpose):]
        print(output)
        return output

