#!/bin/bash
# 🚀 eCNY全球化系统启动脚本
# DNA追溯码：#CNSH-START-SCRIPT-V1.0

echo "🌐 启动数字人民币全球化系统..."
echo "=================================================="

# 检查Python版本
echo "🔍 检查Python环境..."
if command -v python3.11 &> /dev/null; then
    echo "✅ Python 3.11 已安装"
else
    echo "❌ Python 3.11 未安装，请先安装Python 3.11"
    exit 1
fi

# 检查Docker
echo "🔍 检查Docker环境..."
if command -v docker &> /dev/null; then
    echo "✅ Docker 已安装"
else
    echo "❌ Docker 未安装，请先安装Docker"
    exit 1
fi

# 检查Docker Compose
echo "🔍 检查Docker Compose..."
if command -v docker-compose &> /dev/null; then
    echo "✅ Docker Compose 已安装"
else
    echo "❌ Docker Compose 未安装，请先安装Docker Compose"
    exit 1
fi

echo ""
echo "📦 准备启动系统组件..."

# 创建Python虚拟环境
echo "🐍 创建Python虚拟环境..."
if [ ! -d "venv" ]; then
    python3.11 -m venv venv
    echo "✅ 虚拟环境创建成功"
else
    echo "✅ 虚拟环境已存在"
fi

# 激活虚拟环境并安装依赖
echo "📚 安装Python依赖..."
source venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Python依赖安装成功"
else
    echo "❌ Python依赖安装失败"
    exit 1
fi

# 启动Docker服务
echo "🐳 启动Docker服务..."
docker-compose up -d
if [ $? -eq 0 ]; then
    echo "✅ Docker服务启动成功"
else
    echo "❌ Docker服务启动失败"
    exit 1
fi

echo ""
echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
echo "🔍 检查服务状态..."

# 检查PostgreSQL
echo "📊 检查PostgreSQL..."
if docker ps | grep -q "ecny-postgres"; then
    echo "✅ PostgreSQL 运行正常"
else
    echo "❌ PostgreSQL 启动失败"
fi

# 检查Redis
echo "🔴 检查Redis..."
if docker ps | grep -q "ecny-redis"; then
    echo "✅ Redis 运行正常"
else
    echo "❌ Redis 启动失败"
fi

# 检查FastAPI后端
echo "🐍 检查FastAPI后端..."
if docker ps | grep -q "ecny-backend"; then
    echo "✅ FastAPI后端 运行正常"
else
    echo "❌ FastAPI后端 启动失败"
fi

echo ""
echo "🧪 运行系统测试..."

# 运行API测试
python backend/test_api.py

echo ""
echo "=================================================="
echo "🎉 eCNY全球化系统启动完成！"
echo ""
echo "🌐 访问地址："
echo "   API文档：http://localhost:8000/docs"
echo "   健康检查：http://localhost:8000/health"
echo "   系统状态：http://localhost:8000/"
echo ""
echo "📋 可用API端点："
echo "   POST /api/yijing/deployment - 获取部署阶段"
echo "   GET  /api/yijing/strategy  - 获取八卦战略"
echo "   POST /api/yijing/divine    - 易经占卜决策"
echo "   POST /api/growth/predict   - 预测增长趋势"
echo "   GET  /api/growth/montecarlo - 蒙特卡洛模拟"
echo ""
echo "🔧 管理命令："
echo "   查看日志：docker-compose logs -f"
echo "   停止服务：docker-compose down"
echo "   重启服务：docker-compose restart"
echo ""
echo "📚 详细文档："
echo "   安装指南：cat INSTALL.md"
echo "   测试报告：python backend/test_api.py"
echo ""
echo "DNA确认码：#CNSH-SYSTEM-STARTUP-COMPLETE"
echo "=================================================="