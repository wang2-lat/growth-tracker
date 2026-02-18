from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional

@dataclass
class Experiment:
    """增长实验数据模型"""
    id: str
    channel: str  # 渠道名称
    cost: float  # 投入成本
    users: int  # 获客数
    conversions: int  # 转化数
    date: str
    notes: Optional[str] = None
    
    @property
    def cac(self) -> float:
        """计算获客成本 (Customer Acquisition Cost)"""
        return self.cost / self.users if self.users > 0 else 0
    
    @property
    def conversion_rate(self) -> float:
        """计算转化率"""
        return (self.conversions / self.users * 100) if self.users > 0 else 0
    
    @property
    def roi(self) -> float:
        """计算 ROI (假设每个转化用户价值 100 元)"""
        revenue = self.conversions * 100
        return ((revenue - self.cost) / self.cost * 100) if self.cost > 0 else 0
    
    def to_dict(self):
        return asdict(self)