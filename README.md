# Konserter i Stockholm
Keep track on concerts in Stockholm

# Run locally

1. Get docker
2. Run `docker compose up -d`
3. Wait for a while (check the logs `docker compose logs -f` if you like)
4. Visit http://localhost in your browser to see all concerts
5. Run `docker compose restart scraper` to scrape concerts again.