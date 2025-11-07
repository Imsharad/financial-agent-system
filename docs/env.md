### Project Environment

This project is designed to run in the  **Udacity Vocareum workspace** , which provides:

* Pre-configured Python environment with required packages
* OpenAI API access through Vocareum's custom endpoint
* All necessary data files (10-K PDFs, database files)
* Jupyter notebook environment for development and testing

We would be using local dev env however mimicing vocarium API keys


**Important Vocareum Configuration:** LlamaIndex requires special configuration to work with Vocareum's OpenAI endpoint. You'll need to use the `api_base` parameter when initializing OpenAI models:

<pre class="css-0"><div data-defines-codeblock="true" tabindex="0" class="css-ift61f"><div class="css-1wj0762"></div><div><code class="language-python"><span class="token">import</span><span> os
</span><span></span><span class="token">from</span><span> llama_index</span><span class="token">.</span><span>llms</span><span class="token">.</span><span>openai </span><span class="token">import</span><span> OpenAI
</span><span></span><span class="token">from</span><span> llama_index</span><span class="token">.</span><span>embeddings</span><span class="token">.</span><span>openai </span><span class="token">import</span><span> OpenAIEmbedding
</span>
<span>base_url </span><span class="token">=</span><span> os</span><span class="token">.</span><span>getenv</span><span class="token">(</span><span class="token">"OPENAI_API_BASE"</span><span class="token">,</span><span></span><span class="token">"https://openai.vocareum.com/v1"</span><span class="token">)</span><span>
</span><span>llm </span><span class="token">=</span><span> OpenAI</span><span class="token">(</span><span>model</span><span class="token">=</span><span class="token">"gpt-3.5-turbo"</span><span class="token">,</span><span> temperature</span><span class="token">=</span><span class="token">0</span><span class="token">,</span><span> api_base</span><span class="token">=</span><span>base_url</span><span class="token">)</span><span>
</span><span>embed_model </span><span class="token">=</span><span> OpenAIEmbedding</span><span class="token">(</span><span>model</span><span class="token">=</span><span class="token">"text-embedding-ada-002"</span><span class="token">,</span><span> api_base</span><span class="token">=</span><span>base_url</span><span class="token">)</span></code></div></div></pre>

 **Verification** : Before starting development, run the verification test:

<pre class="css-0"><div data-defines-codeblock="true" tabindex="0" class="css-ift61f"><div class="css-1wj0762"></div><div><code class="language-bash"><span>python tests/test_vocareum_setup_for_llama_index.py</span></code></div></div></pre>
