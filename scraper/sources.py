"""
Data sources configuration for web scraping.
Defines URLs and parsing rules for each source.
"""

# Wikipedia pages with AI history - excellent sources
WIKIPEDIA_SOURCES = [
    {
        "name": "Timeline of AI",
        "url": "https://en.wikipedia.org/wiki/Timeline_of_artificial_intelligence",
        "type": "timeline_table"
    },
    {
        "name": "History of AI",
        "url": "https://en.wikipedia.org/wiki/History_of_artificial_intelligence",
        "type": "article"
    },
    {
        "name": "Timeline of ML",
        "url": "https://en.wikipedia.org/wiki/Timeline_of_machine_learning",
        "type": "timeline_table"
    }
]

# Key AI milestones to ensure we capture (manually curated backup)
# These are critical events that MUST be in the database
ESSENTIAL_EVENTS = [
    # Early History
    {
        "year": 1950,
        "title": "Turing Test Proposed",
        "description": "Alan Turing publishes 'Computing Machinery and Intelligence', proposing the Turing Test as a measure of machine intelligence.",
        "category": "research",
        "importance": 5
    },
    {
        "year": 1956,
        "title": "Dartmouth Conference - AI Field Founded",
        "description": "The Dartmouth Summer Research Project on Artificial Intelligence marks the official founding of AI as a field. John McCarthy coins the term 'Artificial Intelligence'.",
        "category": "milestone",
        "importance": 5
    },
    {
        "year": 1957,
        "title": "Perceptron Invented",
        "description": "Frank Rosenblatt invents the Perceptron, an early neural network that could learn from data.",
        "category": "research",
        "importance": 4
    },
    {
        "year": 1966,
        "title": "ELIZA Chatbot Created",
        "description": "Joseph Weizenbaum creates ELIZA, one of the first chatbots, simulating conversation with a psychotherapist.",
        "category": "model",
        "importance": 4
    },
    {
        "year": 1969,
        "title": "First AI Winter Begins",
        "description": "Minsky and Papert publish 'Perceptrons', highlighting limitations of neural networks, leading to reduced funding.",
        "category": "milestone",
        "importance": 4
    },
    {
        "year": 1979,
        "title": "Stanford Cart Navigates Autonomously",
        "description": "The Stanford Cart successfully navigates a room full of obstacles, an early autonomous vehicle milestone.",
        "category": "milestone",
        "importance": 3
    },
    {
        "year": 1986,
        "title": "Backpropagation Popularized",
        "description": "Rumelhart, Hinton, and Williams publish on backpropagation, enabling training of multi-layer neural networks.",
        "category": "research",
        "importance": 5
    },
    {
        "year": 1997,
        "title": "Deep Blue Defeats Kasparov",
        "description": "IBM's Deep Blue defeats world chess champion Garry Kasparov, a landmark moment for AI in games.",
        "category": "milestone",
        "importance": 5
    },
    {
        "year": 1997,
        "title": "LSTM Networks Introduced",
        "description": "Hochreiter and Schmidhuber introduce Long Short-Term Memory networks, crucial for sequence learning.",
        "category": "research",
        "importance": 5
    },
    {
        "year": 2006,
        "title": "Deep Learning Renaissance Begins",
        "description": "Geoffrey Hinton publishes breakthrough work on deep belief networks, reigniting interest in neural networks.",
        "category": "research",
        "importance": 5
    },
    {
        "year": 2009,
        "title": "ImageNet Dataset Released",
        "description": "The ImageNet large-scale visual recognition dataset is released, enabling major advances in computer vision.",
        "category": "research",
        "importance": 4
    },
    {
        "year": 2011,
        "title": "IBM Watson Wins Jeopardy!",
        "description": "IBM Watson defeats human champions on the quiz show Jeopardy!, demonstrating natural language understanding.",
        "category": "milestone",
        "importance": 4
    },
    {
        "year": 2011,
        "title": "Siri Launched by Apple",
        "description": "Apple launches Siri, bringing AI voice assistants to mainstream consumers.",
        "category": "product",
        "importance": 4
    },
    {
        "year": 2012,
        "title": "AlexNet Wins ImageNet Competition",
        "description": "Alex Krizhevsky's deep CNN dramatically outperforms traditional methods, sparking the deep learning revolution.",
        "category": "research",
        "importance": 5
    },
    {
        "year": 2013,
        "title": "Word2Vec Released",
        "description": "Google researchers release Word2Vec, enabling efficient word embeddings that capture semantic meaning in vector space.",
        "category": "research",
        "importance": 4
    },
    {
        "year": 2014,
        "title": "Sequence-to-Sequence Learning Introduced",
        "description": "Sutskever, Vinyals, and Le introduce Seq2Seq models with LSTMs for machine translation, enabling neural machine translation.",
        "category": "research",
        "importance": 4
    },
    {
        "year": 2014,
        "title": "GANs Introduced",
        "description": "Ian Goodfellow introduces Generative Adversarial Networks, revolutionizing generative AI.",
        "category": "research",
        "importance": 5
    },
    {
        "year": 2014,
        "title": "Amazon Alexa Launched",
        "description": "Amazon launches Alexa and the Echo smart speaker, expanding AI voice assistants in homes.",
        "category": "product",
        "importance": 4
    },
    {
        "year": 2015,
        "title": "Attention Mechanism for Neural MT",
        "description": "Bahdanau et al. introduce the attention mechanism for neural machine translation, a precursor to Transformers.",
        "category": "research",
        "importance": 5
    },
    {
        "year": 2015,
        "title": "OpenAI Founded",
        "description": "OpenAI is founded by Elon Musk, Sam Altman, and others as a non-profit AI research lab.",
        "category": "company",
        "importance": 5
    },
    {
        "year": 2015,
        "title": "TensorFlow Open Sourced",
        "description": "Google releases TensorFlow, making deep learning more accessible to developers worldwide.",
        "category": "product",
        "importance": 4
    },
    {
        "year": 2016,
        "month": 3,
        "title": "AlphaGo Defeats Lee Sedol",
        "description": "DeepMind's AlphaGo defeats world Go champion Lee Sedol, a major breakthrough in game-playing AI.",
        "category": "milestone",
        "importance": 5
    },
    {
        "year": 2017,
        "title": "Transformer Architecture Introduced",
        "description": "Google publishes 'Attention Is All You Need', introducing the Transformer architecture that powers modern LLMs.",
        "category": "research",
        "importance": 5
    },
    {
        "year": 2018,
        "month": 6,
        "title": "GPT-1 Released",
        "description": "OpenAI releases GPT-1, demonstrating the power of unsupervised pre-training for NLP.",
        "category": "model",
        "importance": 4
    },
    {
        "year": 2018,
        "month": 10,
        "title": "BERT Released by Google",
        "description": "Google releases BERT, revolutionizing NLP benchmarks with bidirectional transformers.",
        "category": "model",
        "importance": 5
    },
    {
        "year": 2019,
        "month": 2,
        "title": "GPT-2 Released",
        "description": "OpenAI releases GPT-2, initially withholding the full model due to concerns about misuse.",
        "category": "model",
        "importance": 4
    },
    {
        "year": 2020,
        "month": 6,
        "title": "GPT-3 Released",
        "description": "OpenAI releases GPT-3 with 175 billion parameters, showing impressive few-shot learning capabilities.",
        "category": "model",
        "importance": 5
    },
    {
        "year": 2021,
        "month": 1,
        "title": "DALL-E Announced",
        "description": "OpenAI announces DALL-E, capable of generating images from text descriptions.",
        "category": "model",
        "importance": 4
    },
    {
        "year": 2021,
        "title": "GitHub Copilot Launched",
        "description": "GitHub launches Copilot, an AI pair programmer powered by OpenAI Codex.",
        "category": "product",
        "importance": 4
    },
    {
        "year": 2022,
        "month": 4,
        "title": "DALL-E 2 Released",
        "description": "OpenAI releases DALL-E 2 with dramatically improved image generation quality.",
        "category": "model",
        "importance": 4
    },
    {
        "year": 2022,
        "month": 8,
        "title": "Stable Diffusion Released",
        "description": "Stability AI releases Stable Diffusion, making high-quality image generation open source.",
        "category": "model",
        "importance": 5
    },
    {
        "year": 2022,
        "month": 11,
        "day": 30,
        "title": "ChatGPT Launched",
        "description": "OpenAI launches ChatGPT, a conversational AI that becomes the fastest-growing consumer app in history.",
        "category": "product",
        "importance": 5
    },
    {
        "year": 2023,
        "month": 2,
        "title": "Bing Chat (Copilot) Launched",
        "description": "Microsoft integrates GPT-4 into Bing Search as Bing Chat, later renamed Copilot.",
        "category": "product",
        "importance": 4
    },
    {
        "year": 2023,
        "month": 3,
        "title": "GPT-4 Released",
        "description": "OpenAI releases GPT-4, a multimodal model with significantly improved reasoning capabilities.",
        "category": "model",
        "importance": 5
    },
    {
        "year": 2023,
        "month": 3,
        "title": "Claude Released by Anthropic",
        "description": "Anthropic releases Claude, an AI assistant focused on safety and helpfulness.",
        "category": "model",
        "importance": 4
    },
    {
        "year": 2023,
        "month": 3,
        "title": "ChatGPT Plugins Announced",
        "description": "OpenAI announces plugins for ChatGPT, allowing it to connect to external services and APIs.",
        "category": "product",
        "importance": 4
    },
    {
        "year": 2023,
        "month": 5,
        "title": "Google Bard Launched",
        "description": "Google launches Bard, its conversational AI chatbot powered by LaMDA and later Gemini.",
        "category": "product",
        "importance": 4
    },
    {
        "year": 2023,
        "month": 7,
        "title": "Meta Releases Llama 2",
        "description": "Meta releases Llama 2 as an open-source LLM, making powerful AI models freely available.",
        "category": "model",
        "importance": 5
    },
    {
        "year": 2023,
        "month": 10,
        "title": "AI Executive Order Signed (US)",
        "description": "President Biden signs executive order on AI safety, establishing new standards and reporting requirements.",
        "category": "regulation",
        "importance": 4
    },
    {
        "year": 2023,
        "month": 11,
        "title": "OpenAI Leadership Crisis",
        "description": "Sam Altman briefly fired as OpenAI CEO, then reinstated after employee backlash and Microsoft intervention.",
        "category": "company",
        "importance": 4
    },
    {
        "year": 2023,
        "month": 11,
        "title": "GPTs and Custom ChatGPT Launched",
        "description": "OpenAI launches GPTs, allowing users to create custom ChatGPT agents without coding.",
        "category": "product",
        "importance": 4
    },
    {
        "year": 2023,
        "month": 12,
        "title": "Google Gemini Released",
        "description": "Google releases Gemini (Ultra, Pro, Nano), its most capable multimodal AI model.",
        "category": "model",
        "importance": 5
    },
    {
        "year": 2024,
        "month": 2,
        "title": "Gemini 1.5 with 1M Token Context",
        "description": "Google releases Gemini 1.5 with 1 million token context window, a major advance in long-context understanding.",
        "category": "model",
        "importance": 4
    },
    {
        "year": 2024,
        "month": 2,
        "title": "Sora Video Generation Announced",
        "description": "OpenAI announces Sora, capable of generating realistic minute-long videos from text prompts.",
        "category": "model",
        "importance": 5
    },
    {
        "year": 2024,
        "month": 3,
        "title": "Claude 3 Released",
        "description": "Anthropic releases Claude 3 family (Opus, Sonnet, Haiku) with improved reasoning and capabilities.",
        "category": "model",
        "importance": 4
    },
    {
        "year": 2024,
        "month": 4,
        "title": "Meta Releases Llama 3",
        "description": "Meta releases Llama 3, continuing to advance open-source AI capabilities.",
        "category": "model",
        "importance": 4
    },
    {
        "year": 2024,
        "month": 5,
        "title": "GPT-4o Released",
        "description": "OpenAI releases GPT-4o with native multimodal capabilities including real-time voice conversation.",
        "category": "model",
        "importance": 5
    },
    {
        "year": 2024,
        "month": 6,
        "title": "Anthropic Claude 3.5 Sonnet",
        "description": "Anthropic releases Claude 3.5 Sonnet with significantly improved coding and reasoning abilities.",
        "category": "model",
        "importance": 4
    },
    {
        "year": 2024,
        "month": 8,
        "title": "EU AI Act Takes Effect",
        "description": "The European Union's AI Act, the world's first comprehensive AI law, begins enforcement.",
        "category": "regulation",
        "importance": 5
    },
    {
        "year": 2024,
        "month": 9,
        "title": "OpenAI o1 (Strawberry) Released",
        "description": "OpenAI releases o1, a model trained with reinforcement learning to reason before responding.",
        "category": "model",
        "importance": 5
    },
    {
        "year": 2024,
        "month": 10,
        "title": "ChatGPT Canvas Launched",
        "description": "OpenAI launches Canvas, a new interface for collaborative writing and coding with ChatGPT.",
        "category": "product",
        "importance": 3
    },
    {
        "year": 2024,
        "month": 12,
        "title": "Google Gemini 2.0 Released",
        "description": "Google releases Gemini 2.0 with enhanced agentic capabilities and improved multimodal understanding.",
        "category": "model",
        "importance": 4
    }
]

# Category mappings for parsing scraped text
CATEGORY_KEYWORDS = {
    "research": ["paper", "published", "introduced", "proposed", "study", "research", "algorithm", "method"],
    "model": ["model", "released", "launched model", "gpt", "bert", "llm", "neural network", "trained"],
    "company": ["founded", "acquired", "company", "startup", "incorporated", "merger"],
    "product": ["launched", "released", "app", "service", "platform", "integration", "product", "available"],
    "hardware": ["gpu", "chip", "tpu", "processor", "hardware", "nvidia", "compute"],
    "regulation": ["law", "regulation", "act", "policy", "ban", "rule", "government", "executive order"],
    "milestone": ["first", "record", "breakthrough", "defeated", "achieved", "won", "surpassed"]
}
