import json
import os
from pathlib import Path
from typing import List
from .models import Experiment

class Storage:
    """数据存储管理"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.file_path = self.data_dir / "experiments.json"
        
    def load(self) -> List[Experiment]:
        """加载所有实验数据"""
        if not self.file_path.exists():
            return []
        
        with open(self.file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [Experiment(**item) for item in data]
    
    def save(self, experiments: List[Experiment]):
        """保存实验数据"""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump([exp.to_dict() for exp in experiments], f, ensure_ascii=False, indent=2)
    
    def add(self, experiment: Experiment):
        """添加新实验"""
        experiments = self.load()
        experiments.append(experiment)
        self.save(experiments)
    
    def delete(self, exp_id: str) -> bool:
        """删除实验"""
        experiments = self.load()
        filtered = [exp for exp in experiments if exp.id != exp_id]
        if len(filtered) < len(experiments):
            self.save(filtered)
            return True
        return False