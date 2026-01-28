## 🐛 Troubleshooting

### Error: "Connection refused" when connecting to database
- Check if containers are running: `docker compose ps`
- Wait a few seconds for database initialization (healthcheck)
- Verify credentials in `.env`

### Error: "Users service unreachable" when displaying news
- Confirm `users-service` is running: `docker compose ps`
- Check logs: `docker compose logs users-service`
- Internal APIs only work within Docker network

### Redis timeout or Session errors
- Restart Redis container: `docker compose restart redis-sessions`
- Check available memory: `docker stats`

### Port 8000 already in use
```bash
# Find process using the port
lsof -i :8000

# Or change port in docker-compose.yml:
# ports:
#   - "8001:80"  # Use 8001 instead of 8000
```

### `.env` file not loaded
- Confirm it's in project root: `ls -la | grep .env`
- Restart containers: `docker compose restart`

---