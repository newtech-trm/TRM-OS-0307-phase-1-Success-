# 🚀 TRM-OS Railway Deployment Guide

## 📋 Prerequisites

1. **Railway Account**: Đăng ký tại [Railway.app](https://railway.app)
2. **Railway CLI**: Đã cài đặt và login
3. **Neo4j Database**: Cần add Neo4j service trên Railway
4. **Project Ready**: TRM-OS v1.0 đã chuẩn bị sẵn sàng

## 🔧 Railway Project Setup

### 1. Login và Link Project
```bash
# Login Railway (mở browser để authenticate)
railway login

# Link với project ID
railway link -p 6c79655c-bde0-4772-b630-a63581e750ca

# Kiểm tra connection
railway status
```

### 2. Add Neo4j Service
```bash
# Add Neo4j service
railway add neo4j

# Hoặc qua Railway Dashboard:
# 1. Vào project dashboard
# 2. Click "Add Service" 
# 3. Chọn "Neo4j"
# 4. Deploy service
```

### 3. Set Environment Variables
```bash
# Set các biến môi trường production
railway variables set PROJECT_NAME="TRM-OS API v1.0"
railway variables set ENVIRONMENT=production
railway variables set DEBUG=false
railway variables set LOG_LEVEL=info
railway variables set API_V1_STR="/api/v1"
railway variables set PYTHONPATH="/app"
railway variables set PYTHONUNBUFFERED=1

# Neo4j variables sẽ được Railway tự động set
# NEO4J_URL, NEO4J_USERNAME, NEO4J_PASSWORD
```

## 🚀 Deployment Process

### 1. Deploy Application
```bash
# Deploy từ current directory
railway up

# Hoặc deploy với specific service
railway up --service web
```

### 2. Monitor Deployment
```bash
# Xem logs real-time
railway logs

# Xem status
railway status

# Xem domain
railway domain
```

### 3. Seed Database (Post-deployment)
```bash
# Chạy seed script sau khi deploy xong
railway run python scripts/unified_seed_production.py --production

# Hoặc qua Railway dashboard -> Service -> Variables -> Add worker process
```

## 🔍 Verification Steps

### 1. Health Check
```bash
# Kiểm tra health endpoint
curl https://your-railway-domain.up.railway.app/health

# Expected response:
# {"status": "ok"}
```

### 2. API Documentation
```bash
# Truy cập Swagger UI
https://your-railway-domain.up.railway.app/docs

# Truy cập ReDoc
https://your-railway-domain.up.railway.app/redoc
```

### 3. Test Core Endpoints
```bash
# Test root endpoint
curl https://your-railway-domain.up.railway.app/

# Test API v1
curl https://your-railway-domain.up.railway.app/api/v1/agents

# Test specific functionality
curl https://your-railway-domain.up.railway.app/api/v1/projects
```

## 🛠 Configuration Files

### railway.json
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "pip install -r requirements.txt"
  },
  "deploy": {
    "startCommand": "uvicorn trm_api.main:app --host 0.0.0.0 --port $PORT --workers 4",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 100
  }
}
```

### nixpacks.toml
```toml
[phases.setup]
nixPkgs = ["python311", "pip"]

[phases.install]
cmds = ["pip install -r requirements.txt"]

[start]
cmd = "uvicorn trm_api.main:app --host 0.0.0.0 --port $PORT --workers 4"
```

### Procfile
```
web: uvicorn trm_api.main:app --host 0.0.0.0 --port $PORT --workers 4
worker: python scripts/unified_seed_production.py --production
```

## 🔐 Security Checklist

- [ ] **Secret Key**: Thay đổi SECRET_KEY trong production
- [ ] **Neo4j Credentials**: Kiểm tra Neo4j connection string
- [ ] **CORS Settings**: Cấu hình ALLOWED_ORIGINS cho production
- [ ] **Environment Variables**: Đảm bảo tất cả variables đã được set
- [ ] **Health Check**: Verify health endpoint hoạt động
- [ ] **Database Seed**: Chạy seed script sau deployment

## 🐛 Troubleshooting

### Common Issues

1. **Build Failed**
   ```bash
   # Kiểm tra logs
   railway logs --build
   
   # Kiểm tra requirements.txt
   railway run pip list
   ```

2. **Database Connection Failed**
   ```bash
   # Kiểm tra Neo4j service
   railway variables | grep NEO4J
   
   # Test connection
   railway run python -c "from trm_api.db.session import connect_to_db; connect_to_db()"
   ```

3. **Health Check Failed**
   ```bash
   # Test local health endpoint
   railway run python -c "import requests; print(requests.get('http://localhost:8000/health').json())"
   ```

### Debug Commands
```bash
# Xem tất cả services
railway services

# Xem environment variables
railway variables

# Restart service
railway restart

# Redeploy
railway up --detach
```

## 📊 Monitoring & Maintenance

### Performance Monitoring
- Railway Dashboard: CPU, Memory, Network usage
- Application Logs: `railway logs`
- Health Check: `/health` endpoint
- API Metrics: `/metrics` endpoint (if implemented)

### Regular Maintenance
- Database backups (Neo4j)
- Log rotation
- Security updates
- Performance optimization

## 🎯 Success Criteria

- [ ] ✅ Application deployed successfully
- [ ] ✅ Health check returns 200 OK
- [ ] ✅ API documentation accessible
- [ ] ✅ Neo4j database connected
- [ ] ✅ All 220 tests passing in production
- [ ] ✅ Seed data populated correctly
- [ ] ✅ Performance metrics within acceptable range

## 📞 Support

- **Railway Documentation**: https://docs.railway.app
- **TRM-OS Documentation**: `docs/API_V1_COMPREHENSIVE_GUIDE.md`
- **Issues**: GitHub repository issues
- **Railway Discord**: https://discord.gg/railway

---

**🎉 TRM-OS v1.0 is now ready for Railway deployment!**

For questions or issues, refer to the comprehensive documentation in the `docs/` folder or contact the development team. 