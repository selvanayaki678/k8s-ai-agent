from strands import Agent
from strands.models import BedrockModel
from strands.tools.mcp import MCPClient
from mcp.client.sse import sse_client
from bedrock_agentcore.runtime import BedrockAgentCoreApp

# Configuration
LOADBALANCER_URL = "http://a659d143872114059acd467e16330d4e-440917701.us-east-1.elb.amazonaws.com:8080/sse"

# Initialize App
app = BedrockAgentCoreApp()

# System Prompt
system_prompt = """
You are a helpful assistant with deep knowledge in Kubernetes 
and AWS Bedrock. You can also answer general internet-related 
questions about AWS services.
"""

# Initialize MCP Client and Tools
print("[Connecting to MCP server...]")
client = MCPClient(lambda: sse_client(LOADBALANCER_URL))
client.start()
tools = client.list_tools_sync()
print(f"[Connected - Loaded {len(tools)} tools]")

# Create Agent
agent = Agent(
    name="Strands Bedrock Agent",
    system_prompt=system_prompt,
    model=BedrockModel(
        model_id="us.anthropic.claude-3-5-sonnet-20241022-v2:0"
    ),
    tools=tools
)

@app.entrypoint
def invoke(payload):
    """Main entrypoint for Agent Core"""
    user_input = payload.get("prompt")
    response = agent(user_input)
    return response

if __name__ == "__main__":
    print("Starting the app")
    app.run(port=8080)