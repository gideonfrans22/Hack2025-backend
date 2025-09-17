# 🚀 ReadAble Platform - Ubuntu Server Deployment Guide

## Prerequisites

### **Server Requirements**
- Ubuntu 20.04 LTS or newer
- Minimum 2GB RAM (4GB recommended)
- 20GB disk space
- Root or sudo access
- Domain name (optional, for SSL)

### **Local Requirements**
- SSH access to your Ubuntu server
- Your project files ready for transfer

## 🔧 Step-by-Step Deployment

### **1. Server Setup & Updates**

```bash
# Connect to your Ubuntu server
ssh username@your-server-ip

# Update system packages
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install -y curl wget git vim ufw software-properties-common
```

### **2. Install Python 3.8+ and Dependencies**

```bash
# Install Python and pip
sudo apt install -y python3 python3-pip python3-venv python3-dev

# Verify Python version (should be 3.8+)
python3 --version

# Install system dependencies for Python packages
sudo apt install -y build-essential libssl-dev libffi-dev python3-setuptools
```

### **3. Create Application Directory**

```bash
# Create app directory
sudo mkdir -p /var/www/readable
sudo chown $USER:$USER /var/www/readable
cd /var/www/readable

# Clone or upload your project
# Option A: If using Git
git clone https://github.com/yourusername/hack2025-backend.git .

# Option B: Upload files manually (from your local machine)
# scp -r . username@your-server-ip:/var/www/readable/
```

### **4. Setup Python Virtual Environment**

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt

# Install additional production dependencies
pip install gunicorn uvicorn[standard]
```

### **5. Configure Environment Variables**

```bash
# Create production environment file
cp .env.example .env

# Edit environment variables
nano .env
```

**Update your `.env` file:**
```bash
# Firebase Configuration
GOOGLE_APPLICATION_CREDENTIALS=/var/www/readable/firebase-service-account.json
FIREBASE_PROJECT_ID=hack2025-backend

# JWT Configuration
JWT_SECRET_KEY=your-secure-jwt-secret-key-here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_HOURS=24

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here

# Production settings
DEBUG=False
ENVIRONMENT=production
```

### **6. Setup Firebase Service Account**

```bash
# Upload your Firebase service account JSON file
# From local machine:
# scp firebase-service-account.json username@your-server-ip:/var/www/readable/

# Set proper permissions
chmod 600 /var/www/readable/firebase-service-account.json
```

### **7. Test the Application**

```bash
# Activate virtual environment
source venv/bin/activate

# Test the application locally
python3 -c "import main; print('✅ Application imports successfully')"

# Run test server
uvicorn main:app --host 0.0.0.0 --port 8000

# Test in another terminal or browser
curl http://your-server-ip:8000/
```

### **8. Install and Configure Nginx**

```bash
# Install Nginx
sudo apt install -y nginx

# Create Nginx configuration
sudo nano /etc/nginx/sites-available/readable
```

**Nginx Configuration (`/etc/nginx/sites-available/readable`):**
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;  # Replace with your domain
    
    client_max_body_size 100M;
    
    # API routes
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }
    
    # Health check
    location /health {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Static files (if any)
    location /static/ {
        alias /var/www/readable/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

```bash
# Enable the site
sudo ln -s /etc/nginx/sites-available/readable /etc/nginx/sites-enabled/

# Remove default site
sudo rm /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
sudo systemctl enable nginx
```

### **9. Setup Systemd Service for FastAPI**

```bash
# Create systemd service file
sudo nano /etc/systemd/system/readable.service
```

**Service Configuration (`/etc/systemd/system/readable.service`):**
```ini
[Unit]
Description=ReadAble FastAPI Application
After=network.target

[Service]
Type=exec
User=www-data
Group=www-data
WorkingDirectory=/var/www/readable
Environment=PATH=/var/www/readable/venv/bin
ExecStart=/var/www/readable/venv/bin/gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 127.0.0.1:8000
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

```bash
# Set proper ownership
sudo chown -R www-data:www-data /var/www/readable

# Reload systemd and start service
sudo systemctl daemon-reload
sudo systemctl start readable
sudo systemctl enable readable

# Check service status
sudo systemctl status readable
```

### **10. Configure Firewall**

```bash
# Configure UFW firewall
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw --force enable

# Check firewall status
sudo ufw status
```

### **11. Setup SSL with Let's Encrypt (Optional but Recommended)**

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Test auto-renewal
sudo certbot renew --dry-run
```

## 🔍 Testing Deployment

### **Check Service Status**
```bash
# Check if FastAPI is running
sudo systemctl status readable

# Check Nginx status
sudo systemctl status nginx

# Check application logs
sudo journalctl -u readable -f
```

### **Test API Endpoints**
```bash
# Test health endpoint
curl http://your-domain.com/health

# Test API endpoints
curl -X POST http://your-domain.com/api/v1/users/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123", "full_name": "Test User"}'
```

## 📊 Monitoring & Maintenance

### **View Logs**
```bash
# FastAPI application logs
sudo journalctl -u readable -f

# Nginx access logs
sudo tail -f /var/log/nginx/access.log

# Nginx error logs
sudo tail -f /var/log/nginx/error.log
```

### **Restart Services**
```bash
# Restart FastAPI application
sudo systemctl restart readable

# Restart Nginx
sudo systemctl restart nginx

# Restart both
sudo systemctl restart readable nginx
```

### **Update Application**
```bash
# Navigate to app directory
cd /var/www/readable

# Pull latest changes (if using Git)
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Update dependencies
pip install -r requirements.txt

# Restart application
sudo systemctl restart readable
```

## 🛡️ Security Considerations

### **1. Environment Variables**
- Never commit `.env` files to version control
- Use strong, unique JWT secret keys
- Rotate API keys regularly

### **2. File Permissions**
```bash
# Set secure permissions
sudo chmod 600 /var/www/readable/.env
sudo chmod 600 /var/www/readable/firebase-service-account.json
sudo chown -R www-data:www-data /var/www/readable
```

### **3. Firewall Rules**
```bash
# Only allow necessary ports
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw deny 8000  # Block direct access to FastAPI
```

### **4. Regular Updates**
```bash
# Update system packages monthly
sudo apt update && sudo apt upgrade -y

# Update Python packages
pip list --outdated
pip install --upgrade package-name
```

## 🚨 Troubleshooting

### **Common Issues**

#### **Service Won't Start**
```bash
# Check detailed error logs
sudo journalctl -u readable -n 50

# Check if port is in use
sudo netstat -tulpn | grep :8000

# Verify virtual environment
source /var/www/readable/venv/bin/activate
python3 -c "import main"
```

#### **Database Connection Issues**
```bash
# Verify Firebase credentials
cat /var/www/readable/.env | grep FIREBASE
ls -la /var/www/readable/firebase-service-account.json
```

#### **OpenAI API Issues**
```bash
# Test OpenAI connection
python3 -c "
import os
from openai import OpenAI
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
print('OpenAI client initialized successfully')
"
```

#### **Permission Errors**
```bash
# Fix ownership
sudo chown -R www-data:www-data /var/www/readable

# Fix permissions
sudo chmod -R 755 /var/www/readable
sudo chmod 600 /var/www/readable/.env
sudo chmod 600 /var/www/readable/firebase-service-account.json
```

## 🎉 Deployment Complete!

Your ReadAble platform is now deployed and running on Ubuntu server!

**Access your application:**
- **API Base URL**: `https://your-domain.com/api/v1/`
- **Health Check**: `https://your-domain.com/health`
- **Documentation**: `https://your-domain.com/docs`

**Key URLs:**
- User Authentication: `/api/v1/users/`
- Vocabulary Library: `/api/v1/vocab/`
- AI Quiz Generation: `/api/v1/quiz/`

The platform is now ready for production use with:
✅ **Secure HTTPS** (if SSL configured)  
✅ **Auto-restart** on server reboot  
✅ **Process management** with systemd  
✅ **Reverse proxy** with Nginx  
✅ **Firewall protection**  
✅ **Production-ready** configuration  

**Next Steps**: Configure monitoring, set up backups, and connect your frontend application!