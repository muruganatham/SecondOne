---
description: how to deploy the backend to Render using the Blueprint
---

Follow these steps to deploy your AI Application Backend to Render:

### 1. Prepare your Code
Ensure your code is pushed to a GitHub or GitLab repository. The repository must contain:
- `app/` directory (the backend code)
- `requirements.txt` (including `gunicorn` and `uvicorn`)
- `render.yaml` (the blueprint file)

### 2. Connect to Render
1.  Log in to the [Render Dashboard](https://dashboard.render.com/).
2.  Click the **New +** button in the top right.
3.  Select **Blueprint**.

### 3. Deploy the Blueprint
1.  Connect your GitHub/GitLab account if you haven't already.
2.  Select the repository containing your backend code.
3.  Render will automatically parse the `render.yaml` file.
4.  Give the Blueprint a name (e.g., `ai-backend-production`).
5.  Click **Approve**.

### 4. Configure Environment Variables
Render will prompt you for the values of the variables defined in `render.yaml`. You will need to provide:
- `DB_HOST`: Your MySQL host (e.g., from Aiven, PlanetScale, or Render Managed MySQL).
- `DB_USER`: Your database username.
- `DB_PASSWORD`: Your database password.
- `DB_NAME`: Your database name.
- `GROQ_API_KEY`: Your Groq API key.
- `OPENAI_API_KEY`: Your OpenAI API key.
- `DEEPSEEK_API_KEY`: Your DeepSeek API key.
- `MASTER_API_KEY`: A secure random string for master admin access.

### 5. Finalize Deployment
1.  Once you click **Deploy**, Render will start building the service.
2.  You can monitor the logs in the **Logs** tab of the service.
3.  Once the build is complete, your API will be live at a URL like `https://ai-application-backend.onrender.com`.

### 6. Verify Connection
1.  Go to `https://[your-url]/docs` to verify the Swagger UI is active.
2.  Test the `/health` endpoint (if available) or the `/login` endpoint to ensure the database connection is working.

> [!NOTE]
> If your MySQL database is also on Render, ensure you provide the **Internal Database URL** for better performance and security.
