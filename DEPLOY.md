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
