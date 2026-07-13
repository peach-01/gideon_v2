MODEL_REGISTRY = {

    # add vision to strengths
    
    # -------- OPENAI --------
    #"gpt-4.1": {
        #"provider":     "gpt",
        #"cost":         0.03,
        #"latency":      0.7,
        #"quality":      0.95,
        #"strengths":    ["coding", "tool_use"],
    #},

    #"o3": {
        #"provider":     "gpt",
        #"cost":         0.05,
        #"latency":      1.2,
        #"quality":      0.98,
        #"strengths":    ["reasoning", "planning", "critic"],
    #},
    
    # -------- GEMINI --------
    #"gemini-2.5-flash": {
        #"provider":     "gemini",
        #"cost":         0.01,
        #"latency":      0.6,
        #"quality":      0.90,
        #"strengths":    ["coding", "tool_use", "reasoning"],
    #},
    
    #"gemini-2.5-flash-lite": {
        #"provider":     "gemini",
        #"cost":         0.005,
        #"latency":      0.4,
        #"quality":      0.85,
        #"strengths":    ["summarization", "extraction", "memory"],
    #},
    
    # -------- LOCAL --------
    "qwen3:8b": {
        "provider":     "local",
        "cost":         0.0,
        "latency":      0.2,
        "quality":      0.70,
        "strengths":    ["memory", "summarization", "extraction"],
    },

    #"qwen3:4b": {},
    
    #"qwen3:14b": {},
    #"qwen3-coder:30b": {},
}