#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数字人民币出海增长模型
基于五行相生相克的量化预测
DNA追溯码：#CNSH-GROWTH-MODEL-V1.0
"""

import numpy as np
import pandas as pd
from typing import List, Dict
from datetime import datetime, timedelta


class eCNY_GrowthModel:
    """数字人民币增长预测模型"""
    
    def __init__(self):
        # 五行权重配置
        self.wuxing_weights = {
            "木": 0.20,  # 用户增长（数据采集）
            "火": 0.25,  # 场景覆盖（技术扩张）
            "土": 0.15,  # 基建稳定（钱包部署）
            "金": 0.25,  # 资金流动（交易收敛）
            "水": 0.15   # 系统优化（反馈循环）
        }
        
        # 初始采用率
        self.base_rate = 0.05  # 5%
        
        # 相生相克矩阵
        self.shengke_matrix = np.array([
            [1.0, 0.9, 0.0, 0.0, 0.8],   # 木生火、水生木
            [0.9, 1.0, 0.85, 0.0, 0.0],  # 火生土
            [0.0, 0.85, 1.0, 0.9, 0.0],  # 土生金
            [0.0, 0.0, 0.9, 1.0, 0.88],  # 金生水
            [0.8, 0.0, 0.0, 0.88, 1.0]   # 水生木（循环）
        ])
    
    def predict_adoption(self, years: int = 10) -> pd.DataFrame:
        """
        预测未来N年的采用率
        
        Args:
            years: 预测年数
        
        Returns:
            包含年份、采用率、卦象的DataFrame
        """
        results = []
        base_year = 2025
        
        for t in range(years):
            year = base_year + t
            
            # 五行相生增长
            mu_growth = self.wuxing_weights["木"] * np.exp(t * 0.1)
            huo_growth = self.wuxing_weights["火"] * (1 + t * 0.15)
            tu_growth = self.wuxing_weights["土"] * np.log(t + 2)
            jin_growth = self.wuxing_weights["金"] * np.sqrt(t + 1)
            shui_growth = self.wuxing_weights["水"] * (t * 0.05)
            
            growth_factor = mu_growth + huo_growth + tu_growth + jin_growth + shui_growth
            
            # Sigmoid约束（避免过热）
            constraint = 1 / (1 + np.exp(-(t - 5)))
            
            # 最终采用率
            adoption = self.base_rate * growth_factor * constraint
            adoption = min(adoption, 0.60)  # 上限60%
            
            # 对应卦象
            gua = self._year_to_gua(year)
            
            results.append({
                "year": year,
                "adoption_rate": round(adoption, 4),
                "percentage": f"{round(adoption * 100, 2)}%",
                "hexagram": gua,
                "phase": self._get_phase(t)
            })
        
        return pd.DataFrame(results)
    
    def _year_to_gua(self, year: int) -> str:
        """年份转卦象"""
        gua_sequence = [
            "泰䷊", "渐䷴", "晋䷢", "丰䷶", "既济䷾",
            "同人䷌", "大有䷍", "革䷰", "鼎䷱", "恒䷟"
        ]
        index = (year - 2025) % len(gua_sequence)
        return gua_sequence[index]
    
    def _get_phase(self, t: int) -> str:
        """获取发展阶段"""
        if t <= 2:
            return "试点期"
        elif t <= 5:
            return "扩张期"
        elif t <= 8:
            return "突破期"
        else:
            return "守成期"
    
    def calculate_loop_efficiency(self) -> np.ndarray:
        """
        计算闭环效率矩阵
        
        Returns:
            5x5的相生相克效率矩阵
        """
        return self.shengke_matrix
    
    def monte_carlo_simulation(self, iterations: int = 10000) -> Dict:
        """
        蒙特卡洛模拟 - 评估不同场景的概率分布
        
        Args:
            iterations: 模拟次数
        
        Returns:
            各场景的概率分布
        """
        scenarios = {
            "国家间合作": 0,
            "技术突破": 0,
            "政策阻力": 0,
            "市场接受": 0,
            "竞争压力": 0
        }
        
        for _ in range(iterations):
            # 随机生成场景权重
            weights = np.random.dirichlet(np.ones(5))
            max_idx = np.argmax(weights)
            scenario_keys = list(scenarios.keys())
            scenarios[scenario_keys[max_idx]] += 1
        
        # 转换为百分比
        total = sum(scenarios.values())
        return {
            k: f"{round(v / total * 100, 2)}%"
            for k, v in scenarios.items()
        }


# 使用示例
if __name__ == "__main__":
    model = eCNY_GrowthModel()
    
    # 预测10年采用率
    df = model.predict_adoption(10)
    print("\n=== 数字人民币全球采用率预测 ===")
    print(df.to_string(index=False))
    
    # 闭环效率矩阵
    efficiency = model.calculate_loop_efficiency()
    print("\n=== 五行相生相克效率矩阵 ===")
    print("行列顺序：木 火 土 金 水")
    print(efficiency)
    
    # 蒙特卡洛模拟
    mc_result = model.monte_carlo_simulation(10000)
    print("\n=== 蒙特卡洛场景模拟（10000次）===")
    for scenario, prob in mc_result.items():
        print(f"{scenario}: {prob}")