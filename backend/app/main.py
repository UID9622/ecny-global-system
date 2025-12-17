#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eCNY全球化系统 - FastAPI主服务
DNA追溯码：#CNSH-FASTAPI-MAIN-V1.0
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import sys
import os

# 添加services路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.yijing_engine import YiJingEngine
from services.growth_model import eCNY_GrowthModel

# 初始化FastAPI
app = FastAPI(
    title="eCNY全球化系统API",
    description="数字人民币全球化推演与预测系统",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化引擎
yijing_engine = YiJingEngine()
growth_model = eCNY_GrowthModel()

# 请求模型
class YearQuery(BaseModel):
    year: int

class DivinationQuery(BaseModel):
    question: str

class GrowthQuery(BaseModel):
    years: int = 10

# ==================== API路由 ====================

@app.get("/")
def read_root():
    """根路径"""
    return {
        "system": "eCNY全球化系统",
        "version": "1.0.0",
        "dna_code": "#CNSH-e-CNY-GLOBAL-API",
        "status": "running"
    }

@app.get("/health")
def health_check():
    """健康检查"""
    return {"status": "healthy"}

@app.post("/api/yijing/deployment")
def get_deployment_phase(query: YearQuery):
    """
    获取指定年份的部署阶段
    """
    try:
        result = yijing_engine.calculate_deployment_phase(query.year)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/yijing/strategy")
def get_bagua_strategy():
    """
    获取八卦战略布局
    """
    try:
        result = yijing_engine.get_eight_trigram_strategy()
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/yijing/divine")
def divine_strategy(query: DivinationQuery):
    """
    易经占卜决策
    """
    try:
        result = yijing_engine.divine_strategy(query.question)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/growth/predict")
def predict_growth(query: GrowthQuery):
    """
    预测未来N年的采用率
    """
    try:
        df = growth_model.predict_adoption(query.years)
        result = df.to_dict(orient='records')
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/growth/efficiency")
def get_efficiency_matrix():
    """
    获取五行闭环效率矩阵
    """
    try:
        matrix = growth_model.calculate_loop_efficiency()
        return {
            "success": True,
            "data": {
                "elements": ["木", "火", "土", "金", "水"],
                "matrix": matrix.tolist()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/growth/montecarlo")
def run_monte_carlo(iterations: int = 10000):
    """
    运行蒙特卡洛模拟
    """
    try:
        result = growth_model.monte_carlo_simulation(iterations)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 运行服务
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)