# Deployment Guide for Hugging Face Spaces

This guide will help you deploy the Stock Data Insights App to Hugging Face Spaces.

## Prerequisites

1. A Hugging Face account ([sign up here](https://huggingface.co/join))
2. A Google Gemini API key ([get one here](https://makersuite.google.com/app/apikey))

## Step-by-Step Deployment

### 1. Create a New Space

1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Fill in the details:
   - **Space name**: `stock-data-insights` (or your preferred name)
   - **SDK**: Select **Streamlit**
   - **Visibility**: Choose Public or Private
4. Click "Create Space"

### 2. Configure Secrets

1. In your Space, go to **Settings** → **Variables and secrets**
2. Click **New secret**
3. Add the following secrets:
   - **Name**: `GEMINI_API_KEY`
   - **Value**: Your Google Gemini API key
   - Click **Add secret**

   (Optional) For support ticket functionality, add:
   - `TRELLO_API_KEY`
   - `TRELLO_TOKEN`
   - `TRELLO_BOARD_ID`

### 3. Upload Your Code

#### Option A: Using Git (Recommended)

1. Initialize git in your project directory (if not already):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. Add the Hugging Face Space as a remote:
   ```bash
   git remote add space https://huggingface.co/spaces/<your-username>/<space-name>
   ```

3. Push your code:
   ```bash
   git push space main
   ```

#### Option B: Using the Web Interface

1. In your Space, click **Files and versions**
2. Click **Add file** → **Upload files**
3. Upload all project files:
   - `app.py`
   - `agent.py`
   - `support_ticket.py`
   - `stock_database_setup.py`
   - `requirements.txt`
   - `README.md`
   - `LICENSE`
   - Any other necessary files

### 4. Wait for Build

1. After pushing/uploading, Hugging Face will automatically build your Space
2. You can monitor the build progress in the **Logs** tab
3. The first build may take 5-10 minutes as it:
   - Installs dependencies
   - Initializes the database (on first run)

### 5. Access Your App

Once the build completes:
1. Your app will be available at: `https://huggingface.co/spaces/<your-username>/<space-name>`
2. The database will auto-initialize on the first run
3. You can share this URL with others!

## Important Notes

- **Database Initialization**: The database is created automatically on first run. This may take a few minutes.
- **API Keys**: Never commit API keys to your repository. Always use Hugging Face Secrets.
- **Database Persistence**: The database file (`stock_data.db`) is stored in the Space's storage and persists between restarts.
- **Resource Limits**: Free Spaces have resource limits. If you encounter issues, consider upgrading to a paid plan.

## Troubleshooting

### Build Fails
- Check the **Logs** tab for error messages
- Verify `requirements.txt` has all dependencies
- Ensure `app.py` is the correct entry point

### Database Not Initializing
- Check logs for errors
- Verify `stock_database_setup.py` is included in the repository
- The initialization runs automatically on first app load

### API Key Issues
- Verify the secret name is exactly `GEMINI_API_KEY` (case-sensitive)
- Check that the API key is valid and has credits
- Review logs for authentication errors

### App Not Loading
- Check that all required files are uploaded
- Verify the SDK is set to "Streamlit"
- Check the **Logs** tab for runtime errors

## Updating Your Space

To update your Space with new code:

```bash
git add .
git commit -m "Update description"
git push space main
```

Hugging Face will automatically rebuild your Space.

## Support

For issues specific to:
- **Hugging Face Spaces**: Check the [Spaces documentation](https://huggingface.co/docs/hub/spaces)
- **This App**: Open an issue in the repository or check the main README.md

