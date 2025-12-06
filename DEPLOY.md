# Deploying to Render

We have configured this project with a `render.yaml` Blueprint, making deployment extremely easy.

## Prerequisites
1. A GitHub account with this repository pushed to it.
2. A [Render](https://render.com) account.

## Steps to Deploy

1. **Push your code** to GitHub (if you haven't already).
   ```bash
   git add .
   git commit -m "Add Render configuration"
   git push
   ```

2. **Go to Render Dashboard**:
   - Log in to [dashboard.render.com](https://dashboard.render.com).

3. **Create New Blueprint**:
   - Click the **New +** button in the top right.
   - Select **Blueprint**.
   - Connect your GitHub repository (`snake-arena`).

4. **Review & Apply**:
   - Render will detect the `render.yaml` file.
   - It will show you the resources it will create:
     - `snake-arena-db` (Postgres)
     - `snake-arena` (Web Service)
   - Click **Apply**.

## Post-Deployment

- Render will build the Docker image and provision the database.
- Once finished, you will see a URL for your web service (e.g., `https://snake-arena.onrender.com`).
- The database will be automatically seeded with initial data during the first start.

### Troubleshooting
- **Logs**: Click on the `snake-arena` service in Render to view the build and runtime logs.
- **Database**: The free tier database on Render expires after 90 days. For long-term usage, upgrade to a paid instance ($7/month).

## CI/CD Pipeline

We have included a GitHub Actions workflow (`.github/workflows/ci.yml`) that runs tests on every push.

### Automating Deployment

To enable the pipeline to automatically deploy to Render after tests pass:

1.  **Get Deploy Hook URL**:
    - Go to your Render Dashboard.
    - Click on your **Web Service** (`snake-arena`).
    - Go to **Settings** > **Deploy Hook**.
    - Copy the `https://api.render.com/deploy/...` URL.

2.  **Add Secret to GitHub**:
    - Go to your GitHub Repository.
    - **Settings** > **Secrets and variables** > **Actions**.
    - Click **New repository secret**.
    - Name: `RENDER_DEPLOY_HOOK_URL`.
    - Value: (Paste the URL you copied).
    - Click **Add secret**.

3.  **Disable Auto-Deploy (Optional)**:
    - In Render Settings, set "Auto-Deploy" to **No**.
    - This ensures Render *only* deploys when GitHub Actions triggers it (after tests pass).
