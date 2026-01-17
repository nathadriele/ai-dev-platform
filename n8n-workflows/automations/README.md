# n8n Automation Workflows

This directory contains n8n workflow configurations for automating various tasks in the AI-Assisted Developer Productivity Platform.

## Available Workflows

### 1. LinkedIn Technical Post Generator

**File**: `linkedin-post-generator.json`

**Purpose**: Automatically generates LinkedIn technical posts based on a topic and key points using AI.

**Webhook Endpoint**: `POST /webhook/linkedin-post`

**Input Format**:
```json
{
  "topic": "AI-Assisted Development",
  "keyPoints": [
    "AI tools can increase developer productivity by 40%",
    "Code agents help with boilerplate and reviews",
    "Human oversight is essential for quality"
  ],
  "tone": "professional",
  "targetAudience": "developers",
  "includeHashtags": true
}
```

**Output Format**:
```json
{
  "success": true,
  "post": "Generated LinkedIn post content...",
  "characterCount": 1250,
  "generatedAt": "2024-01-15T10:30:00Z"
}
```

**Usage Example**:
```bash
curl -X POST http://localhost:5678/webhook/linkedin-post \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Best Practices for FastAPI",
    "keyPoints": [
      "Use async/await for database operations",
      "Implement proper error handling",
      "Write comprehensive OpenAPI specs"
    ]
  }'
```

### 2. Resume Customizer for Job Applications

**Purpose**: Customizes a resume for a specific job description using AI.

**Features**:
- Extracts key requirements from job description
- Matches relevant experience and skills
- Generates tailored summary
- Suggests additional keywords

**Workflow Steps**:
1. Receive job description and base resume via webhook
2. Use AI to analyze job requirements
3. Match and prioritize relevant experience
4. Generate customized resume content
5. Return optimized resume

**Input Format**:
```json
{
  "jobDescription": "Job description text...",
  "baseResume": {
    "summary": "Professional summary...",
    "experience": [...],
    "skills": [...],
    "education": [...]
  }
}
```

### 3. Weekly Activity Report Generator

**Purpose**: Generates weekly reports of AI-assisted development activities.

**Features**:
- Fetches activities from platform API
- Summarizes key achievements
- Calculates productivity metrics
- Generates formatted report

**Workflow Steps**:
1. Triggered weekly via cron
2. Fetch data from platform API
3. Use AI to analyze and summarize
4. Generate Markdown report
5. Send via email or Slack

**Schedule**: Every Friday at 5:00 PM

### 4. Code Review PR Summary

**Purpose**: Creates AI-generated summaries for Pull Requests.

**Features**:
- Analyzes PR changes
- Identifies key modifications
- Generates review checklist
- Highlights potential issues

**Workflow Steps**:
1. Webhook triggered on PR creation/update
2. Fetch PR diff via GitHub API
3. Use AI to analyze changes
4. Generate summary and review points
5. Post comment on PR

## Setting Up n8n Workflows

### Prerequisites

1. **Install n8n**:
   ```bash
   docker run -it --rm \
     --name n8n \
     -p 5678:5678 \
     -v ~/.n8n:/home/node/.n8n \
     n8nio/n8n
   ```

   Or use the docker-compose service:
   ```bash
   docker-compose up -d n8n
   ```

2. **Access n8n UI**:
   - Open http://localhost:5678
   - Create admin account
   - Configure authentication

### Importing Workflows

1. **Import Workflow JSON**:
   - Click "Import from File"
   - Select workflow JSON file
   - Configure credentials
   - Save and activate

2. **Configure Credentials**:
   - **Anthropic API**: For Claude AI models
   - **OpenAI API**: For GPT models
   - **Platform API**: For internal API access
   - **GitHub**: For PR workflows

3. **Set Up Webhooks**:
   - Each workflow with a webhook node gets a unique URL
   - Copy webhook URL from workflow
   - Use in external applications

### Environment Variables

Configure these in n8n or in docker-compose:

```bash
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=your-secure-password
WEBHOOK_URL=http://localhost:5678/

ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...

PLATFORM_API_URL=http://localhost:8000/api/v1
PLATFORM_API_TOKEN=your-api-token

SMTP_HOST=smtp.gmail.com
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

## Creating Custom Workflows

### Basic Workflow Structure

1. **Trigger Node**: Webhook, Schedule, or Event
2. **Data Processing**: Function nodes for transformations
3. **AI Integration**: OpenAI/Anthropic nodes for AI tasks
4. **External API Calls**: HTTP Request nodes
5. **Response**: Respond to webhook or send notification

### Best Practices

1. **Error Handling**:
   - Add error workflows
   - Implement retry logic
   - Log failures

2. **Rate Limiting**:
   - Add wait nodes between API calls
   - Use batch processing
   - Monitor API usage

3. **Security**:
   - Use credentials manager
   - Never hardcode API keys
   - Validate input data
   - Use HTTPS for webhooks

4. **Monitoring**:
   - Enable execution logs
   - Set up alerts for failures
   - Track workflow performance

### Example: Simple AI Text Processing

```javascript
const prompt = `Process this text: ${$json.text}`;

return [{ json: { prompt } }];
```

Then connect to an AI node (OpenAI or Anthropic) and process the response.

## Testing Workflows

### Manual Testing

1. Open workflow in n8n UI
2. Click "Execute Workflow"
3. Provide test data
4. Review results in execution log

### Webhook Testing

Use curl to test webhook workflows:

```bash
curl -X POST http://localhost:5678/webhook/your-webhook-path \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'
```

### Automated Testing

1. Create test workflow
2. Use n8n API to trigger workflows
3. Validate outputs
4. Check logs for errors

## Monitoring and Debugging

### Execution Logs

- View in n8n UI under "Executions"
- Shows detailed step-by-step execution
- Includes data at each step
- Useful for debugging

### Common Issues

1. **Webhook Not Triggering**:
   - Check webhook URL is correct
   - Verify workflow is active
   - Check n8n is accessible

2. **AI API Errors**:
   - Verify API credentials
   - Check API quota/rate limits
   - Review prompt length

3. **Data Transformation Errors**:
   - Check function node syntax
   - Validate input data structure
   - Use JSON.stringify for debugging

### Performance Optimization

1. **Batch Operations**: Process multiple items together
2. **Caching**: Cache API responses when appropriate
3. **Async Processing**: Use sub-workflows for long tasks
4. **Error Recovery**: Implement proper error handling

## Integration Examples

### With Platform API

```javascript
// HTTP Request node configuration
const response = await axios.get(
  'http://localhost:8000/api/v1/projects',
  {
    headers: {
      'Authorization': 'Bearer ' + $env.API_TOKEN
    }
  }
);

return [{ json: response.data }];
```

### With GitHub

```javascript
// Listen for GitHub webhooks
// Process PR events
// Generate AI summary
// Post comment back to PR
```

### With Slack

```javascript
// Send workflow results to Slack
const slackMessage = {
  text: "Weekly Report Generated",
  attachments: [
    {
      text: $json.report
    }
  ]
};

// Send to Slack webhook
```

## Advanced Features

### Sub-Workflows

Break complex workflows into smaller, reusable sub-workflows.

1. Create main workflow
2. Add "Execute Workflow" node
3. Select sub-workflow
4. Pass data between workflows

### Error Workflows

Define error handling workflows that trigger on failures.

1. Create error workflow
2. Add "Error Trigger" node
3. Handle error appropriately
4. Send notifications

### Custom Code Nodes

Use JavaScript/TypeScript for complex logic:

```javascript
// Advanced data processing
const items = $input.all();

const processed = items.map(item => {
  // Custom processing logic
  return {
    json: {
      original: item.json,
      processed: transform(item.json)
    }
  };
});

return processed;
```

## Security Considerations

1. **API Key Management**:
   - Use n8n credentials store
   - Rotate keys regularly
   - Use read-only keys when possible

2. **Input Validation**:
   - Validate all webhook inputs
   - Sanitize data before processing
   - Check for malicious content

3. **Access Control**:
   - Enable authentication
   - Use strong passwords
   - Restrict webhook URLs
   - Monitor execution logs

## Backup and Restore

### Export Workflows

```bash
# Export all workflows
n8n export:workflow --all --output=workflows-backup.json
```

### Import Workflows

```bash
n8n import:workflow --input=workflows-backup.json
```

### Database Backup

```bash
docker exec n8n-db pg_dump -U n8n n8n > n8n-backup.sql
```
