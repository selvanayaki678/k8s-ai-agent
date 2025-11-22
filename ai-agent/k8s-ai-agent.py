from mcp.client.sse import sse_client
from strands import Agent
from strands.models import BedrockModel
from strands.tools.mcp import MCPClient

LOADBALANCER_URL = "http://ae97ab368919d441a8df22c0e84d99af-1269055025.us-east-1.elb.amazonaws.com:8080/sse"

client = None
agent = None

def reconnect():
    """Reconnect on error"""
    global client, agent
    
    if client:
        try:
            client.stop()
        except:
            pass
     
    client = MCPClient(lambda: sse_client(LOADBALANCER_URL))
    client.start()
    
    tools = client.list_tools_sync()
    
    bedrock_model = BedrockModel(
        model_id="us.anthropic.claude-sonnet-4-5-20250929-v1:0"        
    )
    
    agent = Agent(
        name="Strands Bedrock Agent",
        system_prompt=(
            "You are a helpful assistant with deep knowledge in Kubernetes "
            "and AWS Bedrock."
        ),
        model=bedrock_model,
        tools=tools
    )
    
    print("[Connected]")

# Initial connection
reconnect()

print("\nChat started! Type 'exit' to quit.\n")

while True:
    try:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['exit', 'quit', 'bye']:
            break
        
        if not user_input:
            continue
        
        response = agent(user_input)
        print(f"\nAgent: {response}\n")
        
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"\n[Connection error, reconnecting...]")
        reconnect()

print("Goodbye!")
if client:
    client.stop()