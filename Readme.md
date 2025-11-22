# Kubernetes AI Agent

Talk to your Kubernetes cluster using simple questions!

## What Does This Do?

Ask questions about your Kubernetes cluster in plain English and get answers.

**Examples:**
- "List all my pods"
- "Which pods are running?"
- "Show me my services"

## How It Works

```
     YOU
      ↓
  AI Agent (Python)
      ↓
  Amazon Bedrock ←→ MCP Server
  (AI Brain)        (Kubernetes Expert)
                         ↓
                    Kubernetes Cluster
```

**Simple Flow:**
1. You ask a question
2. AI Agent sends it to Amazon Bedrock (the smart AI)
3. MCP Server gets information from Kubernetes
4. You get your answer!

## What is MCP Server?

**MCP = Model Context Protocol**

It's a bridge that lets AI talk to Kubernetes. Without MCP, the AI doesn't know how to get information from your cluster.

**Think of it like:** A translator that helps AI and Kubernetes understand each other.

## What is Strands?

A Python tool that connects:
- AI models (Amazon Bedrock)
- Tools (MCP Server)

It makes building AI agents easy!

## What We Built

### 1. Created Kubernetes Cluster
Used Terraform to create a cluster on AWS.

### 2. Installed MCP Server
- Deployed MCP Server as a pod in Kubernetes
- Gave it permission to read cluster information
- Exposed it through a LoadBalancer (so we can access it from outside)

### 3. Built Python AI Agent
- Connects to MCP Server
- Connects to Amazon Bedrock AI
- Takes your questions and gives answers

## Setup

### Install Python Packages
```bash
pip install strands-agents mcp boto3
```

### Configure AWS
```bash
aws configure
# Enter your AWS credentials
```

### Deploy MCP Server
```bash
kubectl apply -f k8s-mcp-server/
kubectl get svc -n mcp-system
```

### Update Agent with LoadBalancer URL
Copy the EXTERNAL-IP from above and paste it in `k8s-ai-agent.py`:
```python
LOADBALANCER_URL = "http://YOUR-URL-HERE:8080/sse"
```

### Run the Agent
```bash
python k8s-ai-agent.py
```

## Example Chat

```
You: List all pods

Agent: Here are your pods:
- mcp-server-5f8f798d8d-94bjd (Running)
- nginx-deployment-7d... (Running)

You: exit
Goodbye!
```

## Files

```
k8s-ai-project/
├── terraform-aws/        # Creates Kubernetes cluster
├── mcp-server/          # MCP Server deployment files
└── ai-agent/            # Python AI agent
    └── k8s-ai-agent.py
```

## Troubleshooting

**Connection failed?**
- Check MCP Server is running: `kubectl get pods -n mcp-system`
- Verify LoadBalancer URL is correct

**AWS credentials error?**
- Run `aws configure` again

## What You Learned

- How to connect AI to Kubernetes
- What MCP Server does
- How to build an AI agent with Strands

---

**Made with ❤️ - Ask your Kubernetes cluster anything!**