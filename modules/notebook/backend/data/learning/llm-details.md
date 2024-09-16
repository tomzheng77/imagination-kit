### low level LLM details
- low level gemma
- how to find bugs in LLMs
- tokenization is extremely anno
- from a few days to 10 minutes (to understnad the code)ying
  - different types of tokenization issues
- SVD can spawn into many algorithms
- is Nemotron unique (??)
- LoRA does not work (??)
- showing triton code
- T4 is better than P4
- H100 be careful of marketing - sparse?
- lambdalabs aws colab rampart
- NVIDIA don't fire transistors on zeros (lol)
  - most companies don't train for sparsity
- 2x faster - where does it come from?
- from unsloth import `FastLanguageModel`
- tied weight ??? train for more data > scheduler size
  - number of epochs is more important
- 5T tokens x3 is different to 15T tokens
- "I just read the code and fixed the bugs"
- offload correctly from system GPU to RAM (?)
  - non-blocking - 2% slower
  - some implementations offload incorrectly
    - who would ??? offload to disk

# Topic 1: Low Level Technicals
- does anyone not know what the transformer is?
- is behind all language models

### What is a transformer?
- good for sequence modelling - SORA
- assume transformers are behind all LLMs
- GPT2 style mostly decoder style
  - improved with Transformer++
- how does architecture look like? is just math

### LLaMA in one slide
- eventually you get Logits (??)
- if you write this down in PyTorch you will get a working impl
- cosmic (???)
  - every layer fashion designer makes you change clothes
  - and they don't like the previous opinion
- in general everything with a capital letter is a matrix
  - you could do all vecs but M is faster

### sentences example
- number of ??? 5,6,8,7
- tokenization suggestions
- stem the word
- BERT is ??? there is a lowercase version
- "correct" way is ???
  - start with small individual characters and use statistics
- it should predict what you should type next
  - always read the methodology - did they put future data in
    - I am NOT loling - 98% accuracy
- normally in research one person does the coding
  - the coder may have misinterpreted the methodology
- you have to be very careful how you split TD
  - use stratification, use random shuffling
  - Kaggle - using test in the training data
- must tokenize each component into numbers (word2vec?)
  - why use more numbers - computers can learn
  - initially all numbers are randomly initialized
    - random large components will destroy training
    - model loss = zero, you may have infinity

### intuition of attention
- attention mask
- O(N^2) instead of O(N^3) training

### visualising Q K V math
- Q K transpose
- normalize to 1 because
- box folding diagram
- "layernorms just training a bit better"

### backprop much harder than fwdprop
- derivative of a rowsum

### rope embeddings
- can extend context window
- one million context len
- what if you don't have a long dataset ???
- you want to tell the model to learn what is the position of the words
- yarn extend automatically ...
- rope kernel in triton
- R is a rotation matrix
- finding the derivatives is hard

### cross entropy loss
- a sum is a dot product on all ones
- chunked cross entropy
  - larger logits - chunked - easier multithreading
- chunking is needed for larger than 65536

### training across multiple GPUs
- things splitting ...

### layernorm
- use layernorms everywhere
- "stabilizes" training

### probabilities of each token
- the lm head
- upcast to f32 to make training more stable
- shifting trick
- "its not that scary, you just need to see what components you can ignore"

### gemma bugfixes
- what is L2 layernorm
- is graphed in LOG
- tinyllama 80% trained found bug in tokenization
  - if you change the tokenization you have to retrain from scratch
- if you don't follow the original implementation
- open three ??? deepmind huggingface ??? guess what is correct
  - error checking cannot be automated
- why use gelu approx ???
- fused ??? adapters pls unfuse

### merging CSV columns into one prompt

### chat template ollama

### finetuning template
- ??? two columns
  - this is a fundamental ???
- can merge X columns to instruction

### lora adapters
- something 100mb

### float multiplication
- number of transistors - fraction is 7, exponent is 8
  - exponent + (fraction squared)

### quantization
- bfloat16 can be ~10x faster than float32
- you must have the sign bit
- 4 bit quantization
- 1.58 bit bitmap ???
- mixtral 8x7b 2bit ???

### minus the maximum ???
- reduce ??? not just predicting one token

# Topic 2: Unsloth: Fast finetuning

# Topic 3: Finding & fixing bugs
